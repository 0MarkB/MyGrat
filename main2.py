import pandas as pd
from datetime import datetime, timedelta



# Define the role_pool_points dictionary.
role_pool_points = {
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
}

def try_parsing_date(text):
    """Try parsing a date string using multiple formats."""
    for fmt in ('%m/%d/%Y %H:%M', '%m/%d/%y %I:%M %p'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError(f'time data {text} does not match any of the expected formats')



def read_csv_data(filename):
    """Reads data from a CSV file."""
    try:
        df = pd.read_csv(filename)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None


def write_excel_data(filename, data, sheet_name):
    """Writes data to an Excel file."""
    try:
        df = pd.DataFrame(data)
        df.to_excel(filename, sheet_name=sheet_name, engine='openpyxl', index=False)
    except Exception as e:
        print(f"Error writing to Excel file: {e}")


def determine_pool(timestamp_str):
    """Determines which pool (Lunch or Dinner) an order belongs to."""
    timestamp = try_parsing_date(timestamp_str)
    if 6 <= timestamp.hour < 17:
        return "Lunch"
    else:
        return "Dinner"



from datetime import timedelta

def calculate_hours_in_pool(in_date_str, out_date_str):
    """Calculates hours worked in each pool for a given time entry."""
    in_date = try_parsing_date(in_date_str)
    out_date = try_parsing_date(out_date_str)

    # Handle cases where out_date is on the next day (e.g., shift crossing midnight)
    if out_date < in_date:
        out_date += timedelta(days=1)

    lunch_start = in_date.replace(hour=6, minute=0)
    lunch_end = in_date.replace(hour=16, minute=59)
    dinner_start = in_date.replace(hour=17, minute=0)
    dinner_end = in_date.replace(hour=5, minute=59) + timedelta(days=1)

    lunch_hours = max(min(out_date, lunch_end) - max(in_date, lunch_start), timedelta(0)).total_seconds() / 3600
    dinner_hours = max(min(out_date, dinner_end) - max(in_date, dinner_start), timedelta(0)).total_seconds() / 3600

    return lunch_hours, dinner_hours



def distribute_tips_among_employees(tip_pool, hours_per_employee, role_pool_points, time_entries_df):
    """Distributes the tip pool among employees based on hours worked and role points."""
    # Deducting 3.5% for credit card processing fees
    total_tip_pool = tip_pool * 0.965

    # Calculating the total weighted contribution
    total_weighted_contribution = sum([hours * role_pool_points.get(
        time_entries_df[time_entries_df['Employee'] == employee]['Job Title'].values[0], 0)
                                       for employee, hours in hours_per_employee.items()])

    # Calculating value per point
    value_per_point = total_tip_pool / total_weighted_contribution if total_weighted_contribution != 0 else 0

    # Calculating each employee's cut
    employee_cuts = {}
    for employee, hours in hours_per_employee.items():
        job_title = time_entries_df[time_entries_df['Employee'] == employee]['Job Title'].values[0]
        employee_cuts[employee] = hours * role_pool_points.get(job_title, 0) * value_per_point

    return employee_cuts


def process_orders_csv(filename):
    """Processes the Orders.csv file and returns aggregated tips for Lunch and Dinner."""
    df = pd.read_csv(filename)
    df['Pool'] = df['Opened'].apply(determine_pool)

    lunch_tips = df[df['Pool'] == 'Lunch']['Tip'].sum() + df[df['Pool'] == 'Lunch']['Gratuity'].sum()
    dinner_tips = df[df['Pool'] == 'Dinner']['Tip'].sum() + df[df['Pool'] == 'Dinner']['Gratuity'].sum()

    return lunch_tips, dinner_tips


def process_time_entries_csv(filename):
    """Processes the TimeEntries.csv file and returns total hours worked by each employee in Lunch and Dinner shifts."""
    df = pd.read_csv(filename)
    df['Lunch Hours'], df['Dinner Hours'] = zip(
        *df.apply(lambda row: calculate_hours_in_pool(row['In Date'], row['Out Date']), axis=1))

    lunch_hours_per_employee = df.groupby('Employee')['Lunch Hours'].sum().to_dict()
    dinner_hours_per_employee = df.groupby('Employee')['Dinner Hours'].sum().to_dict()

    return lunch_hours_per_employee, dinner_hours_per_employee


def main_interactive():
    try:
        # Prompt the user for the Orders.csv file path
        orders_file_path = input("Enter the path to your Orders.csv file: ")
        # Read and process data from Orders.csv
        lunch_tip_pool, dinner_tip_pool = process_orders_csv(orders_file_path)

        # Prompt the user for the TimeEntries.csv file path
        time_entries_file_path = input("Enter the path to your TimeEntries.csv file: ")
        # Read and process data from TimeEntries.csv
        lunch_hours_per_employee, dinner_hours_per_employee = process_time_entries_csv(time_entries_file_path)

        # Read the TimeEntries.csv into a DataFrame
        time_entries_df = read_csv_data(time_entries_file_path)

        # Distribute tips for Lunch and Dinner shifts
        lunch_employee_cuts = distribute_tips_among_employees(lunch_tip_pool, lunch_hours_per_employee,
                                                              role_pool_points, time_entries_df)
        dinner_employee_cuts = distribute_tips_among_employees(dinner_tip_pool, dinner_hours_per_employee,
                                                               role_pool_points, time_entries_df)

        # Generate output data with additional columns for both Lunch and Dinner
        output_data = [{"Employee": key, "Lunch Tips": value, "Dinner Tips": dinner_employee_cuts.get(key, 0)}
                       for key, value in lunch_employee_cuts.items()]

        # Write results back to an Excel file
        output_file = 'employee_results.xlsx'
        write_excel_data(output_file, output_data, 'EmployeeCuts')

        print(f"Employee cuts with additional details have been saved to {output_file}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main_interactive()