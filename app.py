from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
import sys
import traceback

from MyGratMain import Ui_MainWindow  # Importing your UI class

# Import your logic functions here
from mainWeekly import (
    process_orders_for_week,
    process_time_entries_for_week,
    distribute_tips_among_employees_for_week,
    write_excel_data,
    read_csv_data,
    role_pool_points
)


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)

        # Connecting buttons to methods
        self.pushButton.clicked.connect(self.upload_time_entries)
        self.pushButton_2.clicked.connect(self.upload_orders)
        self.pushButton_3.clicked.connect(self.distribute_tips_weekly)
        self.pushButton_5.clicked.connect(self.save_results)

        # Variables to store file paths
        self.orders_file_path = ""
        self.time_entries_file_path = ""

    def upload_time_entries(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Time Entries CSV File", "",
                                                  "CSV files (*.csv);;All files (*)")
        if filepath:
            self.time_entries_file_path = filepath  # Fixed here
            self.statusbar.showMessage("Time entries file uploaded successfully!")

    def upload_orders(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Orders CSV File", "",
                                                  "CSV files (*.csv);;All files (*)")
        if filepath:
            self.orders_file_path = filepath  # Fixed here
            self.statusbar.showMessage("Orders file uploaded successfully!")

    def distribute_tips_weekly(self):
        try:
            orders_df, error_msg = read_csv_data(self.orders_file_path)
            if error_msg:
                raise Exception(error_msg)
            weekly_tip_pools = process_orders_for_week(orders_df)
            lunch_hours_per_week, dinner_hours_per_week = process_time_entries_for_week(self.time_entries_file_path)
            time_entries_df, error_msg = read_csv_data(self.time_entries_file_path)
            print(type(time_entries_df))
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

    def save_results(self):
        try:
            output_data = [{"Employee": key, "Weekly Tips": value} for key, value in self.employee_weekly_cuts.items()]
            output_file = 'employee_weekly_results.xlsx'
            write_excel_data(output_file, output_data, 'EmployeeWeeklyCuts')
            self.statusbar.showMessage(f"Employee weekly cuts have been saved to {output_file}.")
        except Exception as e:
            error_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
            self.ErrorTracebackBox.setText(error_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
