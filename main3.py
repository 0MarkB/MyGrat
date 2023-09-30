import pandas as pd
from datetime import datetime, timedelta


def parse_datetime(timestamp_str):
    """Attempt to parse datetime with multiple formats."""
    formats = ["%m/%d/%Y %H:%M", "%m/%d/%y %I:%M %p"]

    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Time data '{timestamp_str}' does not match any known format.")


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
    timestamp = parse_datetime(timestamp_str)
    if 6 <= timestamp.hour < 17:
        return "Lunch"
    else:
        return "Dinner"


def calculate_hours_in_pool(start_str, end_str):
    """Calculates hours worked in Lunch and Dinner shifts based on start and end times."""
    start_time = parse_datetime(start_str)
    end_time = parse_datetime(end_str)
    if end_time < start_time:  # Handle shifts that cross midnight
        end_time += timedelta(days=1)

    lunch_start = start_time.replace(hour=6, minute=0, second=0)
    dinner_start = start_time.replace(hour=17, minute=0, second=0)

    lunch_hours = max((min(end_time, dinner_start) - start_time).total_seconds() / 3600, 0)
    dinner_hours = max((end_time - max(start_time, dinner_start)).total_seconds() / 3600, 0)

    return lunch_hours, dinner_hours


def process_orders_csv(filename):
    """Processes the Orders.csv file and calculates the total tip pool for Lunch and Dinner shifts."""
    df = pd.read_csv(filename)
    df['Pool'] = df['Date'].apply(determine_pool)

    lunch_tips = df[df['Pool'] == 'Lunch']['Tip'].sum()
    lunch_gratuity = df[df['Pool'] == 'Lunch']['Gratuity'].sum()
    dinner_tips = df[df['Pool'] == 'Dinner']['Tip'].sum()
    dinner_gratuity = df[df['Pool'] == 'Dinner']['Gratuity'].sum()

    total_lunch_pool = (lunch_tips + lunch_gratuity) * 0.965
    total_dinner_pool = (dinner_tips + dinner_gratuity) * 0.965

    return total_lunch_pool, total_dinner_pool


def process_time_entries_csv(filename):
    """Processes the TimeEntries.csv file and returns total hours worked by each employee in Lunch and Dinner shifts."""
    df = pd.read_csv(filename)
    df['Lunch Hours'], df['Dinner Hours'] = zip(
        *df.apply(lambda row: calculate_hours_in_pool(row['In Date'], row['Out Date']), axis=1))

    lunch_hours_per_employee = df.groupby('Employee')['Lunch Hours'].sum().to_dict()
    dinner_hours_per_employee = df.groupby('Employee')['Dinner Hours'].sum().to_dict()

    return lunch_hours_per_employee, dinner_hours_per_employee


def distribute_tips_among_employees(tip_pool, hours_per_employee, role_pool_points, time_entries_df):
    """Distributes the tip pool among employees based on hours worked and role points."""
    total_weighted_contribution = sum([hours * role_pool_points.get(role, 0)
                                       for employee, hours in hours_per_employee.items()
                                       for role in time_entries_df[time_entries_df['Employee'] == employee]['Role']])

    value_per_point = tip_pool / total_weighted_contribution if total_weighted_contribution != 0 else 0

    employee_cuts = {}
    for employee, hours in hours_per_employee.items():
        role = time_entries_df[time_entries_df['Employee'] == employee]['Role'].iloc[0]
        employee_cuts[employee] = hours * role_pool_points.get(role, 0) * value_per_point

    return employee_cuts


def generate_output_data_with_totals(lunch_hours_per_employee, dinner_hours_per_employee, lunch_employee_cuts,
                                     dinner_employee_cuts):
    """Generates the output data with totals to be written to Excel."""
    output_data = []
    total_lunch_tips = 0
    total_dinner_tips = 0

    for employee in lunch_hours_per_employee.keys():
        lunch_hours_formatted = "{:02d}:{:02d}".format(*divmod(int(lunch_hours_per_employee.get(employee, 0) * 60), 60))
        dinner_hours_formatted = "{:02d}:{:02d}".format(
            *divmod(int(dinner_hours_per_employee.get(employee, 0) * 60), 60))

        lunch_tip = lunch_employee_cuts.get(employee, 0)
        dinner_tip = dinner_employee_cuts.get(employee, 0)

        total_lunch_tips += lunch_tip
        total_dinner_tips += dinner_tip

        output_data.append({
            "Employee": employee,
            "Lunch Tips": lunch_tip,
            "Lunch Hours": lunch_hours_formatted,
            "Dinner Tips": dinner_tip,
            "Dinner Hours": dinner_hours_formatted,
            "Total Tips": lunch_tip + dinner_tip
        })

    output_data.append({
        "Employee": "TOTAL",
        "Lunch Tips": total_lunch_tips,
        "Lunch Hours": "",
        "Dinner Tips": total_dinner_tips,
        "Dinner Hours": "",
        "Total Tips": total_lunch_tips + total_dinner_tips
    })

    return output_data


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


def main_interactive():
    try:
        orders_file_path = input("Enter the path to your Orders.csv file: ")
        lunch_tip_pool, dinner_tip_pool = process_orders_csv(orders_file_path)

        time_entries_file_path = input("Enter the path to your TimeEntries.csv file: ")
        lunch_hours_per_employee, dinner_hours_per_employee = process_time_entries_csv(time_entries_file_path)

        time_entries_df = read_csv_data(time_entries_file_path)

        lunch_employee_cuts = distribute_tips_among_employees(lunch_tip_pool, lunch_hours_per_employee,
                                                              role_pool_points, time_entries_df)
        dinner_employee_cuts = distribute_tips_among_employees(dinner_tip_pool, dinner_hours_per_employee,
                                                               role_pool_points, time_entries_df)

        output_data = generate_output_data_with_totals(lunch_hours_per_employee, dinner_hours_per_employee,
                                                       lunch_employee_cuts, dinner_employee_cuts)

        output_file = 'employee_results.xlsx'
        write_excel_data(output_file, output_data, 'EmployeeCuts')

        print(f"Employee cuts with additional details have been saved to {output_file}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main_interactive()
