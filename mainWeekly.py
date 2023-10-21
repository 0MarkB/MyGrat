import pandas as pd
from datetime import datetime, timedelta

# New: Define the different point systems
POINT_SYSTEMS = {
    "Mocha Red": {
        'Head Bartender': 1.25,
        'Bartender': 1,
        'Captain': 1,
        'Expeditor': 1,
        'Server': 1,
        'Head Barback': 0.7,
        'Runner': 0.7,
        'Barback': 0.5,
        'Busser': 0.5,
        'Maitre\'D': 0.2,
        'General Manager': 0,
        'Manager': 0,
        'Training': 0
    },
    "Mocha Lux": {
        'Captain': 8,
        'Lead Bartender': 8,
        'Bartender': 6,
        'Server': 6,
        'Expeditor': 5,
        'Runner': 4,
        'Barback': 3.5,
        'Busser': 3.5,
        'Polisher': 2,
        'Beverage Manager': 0,
        'General Manager': 0,
        'GeneralManager': 0,
        'Host': 0,
        'OLO_GS': 0,
        'Shift Manager / Assistant Manager': 0,
        'Training': 0
    }
}

# Reference the default system for backward compatibility
role_pool_points = POINT_SYSTEMS["Mocha Red"]

def try_parsing_date(text):
    for fmt in ('%m/%d/%Y %H:%M', '%m/%d/%y %I:%M %p'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError(f'time data {text} does not match any of the expected formats')


def read_csv_data(filename):
    try:
        df = pd.read_csv(filename)
        return df, None  # Returning None as the second value to indicate no error
    except Exception as e:
        return None, str(e)  # Returning the error message as the second value


def write_excel_data(filename, data, sheet_name):
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, sheet_name=sheet_name, engine='openpyxl', index=False)
        return None  # Returning None to indicate no error
    except Exception as e:
        return str(e)  # Returning the error message


def determine_pool(timestamp_str):
    timestamp = try_parsing_date(timestamp_str)
    if 6 <= timestamp.hour < 17:
        return "Lunch"
    else:
        return "Dinner"


def calculate_hours_in_pool(in_date_str, out_date_str):
    in_date = try_parsing_date(in_date_str)
    out_date = try_parsing_date(out_date_str)
    if out_date < in_date:
        out_date += timedelta(days=1)
    lunch_start = in_date.replace(hour=6, minute=0)
    lunch_end = in_date.replace(hour=16, minute=59)
    dinner_start = in_date.replace(hour=17, minute=0)
    dinner_end = in_date.replace(hour=5, minute=59) + timedelta(days=1)
    lunch_hours = max(min(out_date, lunch_end) - max(in_date, lunch_start), timedelta(0)).total_seconds() / 3600
    dinner_hours = max(min(out_date, dinner_end) - max(in_date, dinner_start), timedelta(0)).total_seconds() / 3600
    return lunch_hours, dinner_hours


def process_orders_for_week(df):
    """Processes the Orders.csv file and returns aggregated tips for Lunch and Dinner for each day."""

    # Check if 'Opened' column exists in the dataframe
    if 'Opened' not in df.columns:
        raise ValueError("The 'Opened' column is missing in the Orders.csv file. Please check the file.")

    df['Date'] = df['Opened'].apply(lambda x: try_parsing_date(x).date())
    df['Pool'] = df['Opened'].apply(determine_pool)

    grouped_tips = df.groupby(['Date', 'Pool']).apply(lambda group: group['Tip'].sum() + group['Gratuity'].sum())

    return grouped_tips.to_dict()


def process_time_entries_for_week(filename):
    df = pd.read_csv(filename)
    df['Date'] = df['In Date'].apply(lambda x: try_parsing_date(x).date())
    df['Lunch Hours'], df['Dinner Hours'] = zip(
        *df.apply(lambda row: calculate_hours_in_pool(row['In Date'], row['Out Date']), axis=1))

    lunch_hours_per_day = df.groupby(['Date', 'Employee'])['Lunch Hours'].sum().to_dict()
    dinner_hours_per_day = df.groupby(['Date', 'Employee'])['Dinner Hours'].sum().to_dict()

    return lunch_hours_per_day, dinner_hours_per_day


def distribute_tips_for_day(date, pool, tip_pool, hours_per_employee, point_system, time_entries_df):
    total_tip_pool = tip_pool * 0.965

    # Filtering only employees who worked on that day and shift
    working_employees = [employee for (day, employee), hours in hours_per_employee.items() if day == date and hours > 0]

    # Calculating the total weighted contribution for the filtered employees
    total_weighted_contribution = sum(
        [hours_per_employee.get((date, employee), 0) * role_pool_points.get(
            time_entries_df.loc[time_entries_df['Employee'] == employee, 'Job Title'].values[0], 0)
         for employee in working_employees])

    # Calculating value per point
    value_per_point = total_tip_pool / total_weighted_contribution if total_weighted_contribution != 0 else 0

    # Calculating each employee's cut for the day and shift
    daily_cuts = {}
    for employee in working_employees:
        job_title = time_entries_df.loc[time_entries_df['Employee'] == employee, 'Job Title'].values[0]
        daily_cuts[employee] = hours_per_employee.get((date, employee), 0) * point_system.get(job_title,
                                                                                              0) * value_per_point
    return daily_cuts


def distribute_tips_among_employees_for_week(tip_pools, lunch_hours_per_employee, dinner_hours_per_employee, point_system, time_entries_df):
    employee_weekly_cuts = {}

    for (date, pool), tip_pool in tip_pools.items():
        daily_cuts = distribute_tips_for_day(date, pool, tip_pool,
                                             lunch_hours_per_employee if pool == 'Lunch' else dinner_hours_per_employee,
                                             point_system, time_entries_df)
        for employee, cut in daily_cuts.items():
            employee_weekly_cuts[employee] = employee_weekly_cuts.get(employee, 0) + cut

    return employee_weekly_cuts

# The main function is not needed since the logic will now be driven by GUI interactions.
