from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QTableWidgetItem
import sys
import traceback
import os
from datetime import datetime

from MyGratMain import Ui_MainWindow  # Importing your UI class
from ResultWindow import Ui_ResultWindow  # Importing your Result Window

# Import your logic functions here
from mainWeekly import (
    process_orders_for_week,
    process_time_entries_for_week,
    distribute_tips_among_employees_for_week,
    write_excel_data,
    read_csv_data,
    role_pool_points
)

def try_parsing_date(text):
    for fmt in ('%m/%d/%Y', '%m/%d/%y'):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f'time data {text} does not match any of the expected formats')


class ResultsDialog(QMainWindow, Ui_ResultWindow):
    def __init__(self, data, parent=None):
        super(ResultsDialog, self).__init__(parent)
        self.setupUi(self)
        self.populate_table(data)

    def populate_table(self, data):
        self.resultsTable.setRowCount(len(data))
        self.resultsTable.setColumnCount(2)
        self.resultsTable.setHorizontalHeaderLabels(["Employee", "Weekly Tips"])
        for row, (employee, tip) in enumerate(data.items()):
            self.resultsTable.setItem(row, 0, QTableWidgetItem(employee))
            self.resultsTable.setItem(row, 1, QTableWidgetItem(str(tip)))


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)

        # Connecting buttons to methods
        self.pushButton.clicked.connect(self.upload_time_entries)
        self.pushButton_2.clicked.connect(self.upload_orders)
        self.pushButton_3.clicked.connect(self.distribute_tips_weekly)
        self.pushButton_4.clicked.connect(self.show_results)  # Connect the "Show Results" button
        self.pushButton_5.clicked.connect(self.save_results)

        # Variables to store file paths
        self.orders_file_path = ""
        self.time_entries_file_path = ""

    def upload_time_entries(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Time Entries CSV File", "",
                                                  "CSV files (*.csv);;All files (*)")
        if filepath:
            self.time_entries_file_path = filepath
            # Read the CSV and store it as an attribute
            self.time_entries_df, error_msg = read_csv_data(filepath)
            if error_msg:
                self.ErrorTracebackBox.setText(error_msg)
                return
            self.statusbar.showMessage("Time entries file uploaded successfully!")

    def upload_orders(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Orders CSV File", "",
                                                  "CSV files (*.csv);;All files (*)")
        if filepath:
            self.orders_file_path = filepath
            self.statusbar.showMessage("Orders file uploaded successfully!")

    def distribute_tips_weekly(self):
        try:
            orders_df, error_msg = read_csv_data(self.orders_file_path)
            if error_msg:
                raise Exception(error_msg)
            weekly_tip_pools = process_orders_for_week(orders_df)
            lunch_hours_per_week, dinner_hours_per_week = process_time_entries_for_week(self.time_entries_file_path)
            time_entries_df, error_msg = read_csv_data(self.time_entries_file_path)
            if error_msg:
                raise Exception(error_msg)

            self.employee_weekly_cuts = distribute_tips_among_employees_for_week(
                weekly_tip_pools,
                lunch_hours_per_week,
                dinner_hours_per_week,
                role_pool_points,
                time_entries_df
            )
            self.statusbar.showMessage("Tips distributed successfully!")
        except Exception as e:
            error_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
            self.ErrorTracebackBox.setText(error_message)

    def show_results(self):
        if hasattr(self, 'employee_weekly_cuts'):
            self.results_dialog = ResultsDialog(self.employee_weekly_cuts, self)
            self.results_dialog.show()
        else:
            QMessageBox.warning(self, "No Results", "Please distribute the tips first.")

    def save_results(self):
        try:
            # Extract in-dates from the time entries dataframe
            in_dates = self.time_entries_df['In Date'].apply(
                lambda x: try_parsing_date(x.split()[0]))

            # Extract the start and end dates
            start_date = min(in_dates)
            end_date = max(in_dates)

            # Create the filename with the desired format
            file_name = f"PayrollResults_{start_date.strftime('%m-%d-%Y')}_to_{end_date.strftime('%m-%d-%Y')}_Created{datetime.now().strftime('%m-%d-%Y_%Hh.%Mm.%Ss')}.xlsx"
            output_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)

            # Save the data to the Excel file
            output_data = [{"Employee": key, "Weekly Tips": value} for key, value in self.employee_weekly_cuts.items()]
            write_excel_data(output_path, output_data, 'EmployeeWeeklyCuts')

            # Automatically open the file using the default application
            os.startfile(output_path)

            self.statusbar.showMessage(f"Employee weekly cuts have been saved to {output_path}.")

        except Exception as e:
            error_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
            self.ErrorTracebackBox.setText(error_message)
6

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
