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
            # Extract date range from the time entries data
            in_dates = self.time_entries_df['In Date'].apply(lambda x: datetime.strptime(x.split()[0], "%m/%d/%Y").date())
            start_date = min(in_dates)
            end_date = max(in_dates)

            # Format the filename
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"PayrollResults_{start_date}to{end_date}_{current_time}.xlsx"
            output_file_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)

            # Write data to Excel
            output_data = [{"Employee": key, "Weekly Tips": value} for key, value in self.employee_weekly_cuts.items()]
            write_excel_data(output_file_path, output_data, 'EmployeeWeeklyCuts')

            # Open the file with default application
            os.startfile(output_file_path)

            self.statusbar.showMessage(
                f"Employee weekly cuts have been saved to {filename} in the Downloads directory.")
        except PermissionError:
            error_message = "Permission denied: Unable to save file to Downloads directory."
            self.ErrorTracebackBox.setText(error_message)
        except FileNotFoundError:
            error_message = "Excel application not found. The file has been saved, but couldn't be opened automatically."
            self.ErrorTracebackBox.setText(error_message)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
            self.ErrorTracebackBox.setText(error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
