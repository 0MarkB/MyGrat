# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Morde\Downloads\My Grat .UI file\MyGratMain.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(808, 576)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(330, 0, 131, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 80, 81, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 200, 81, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 310, 41, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(70, 410, 51, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(70, 340, 341, 31))
        self.label_6.setObjectName("label_6")
        self.ErrorTracebackBox = QtWidgets.QTextEdit(self.centralwidget)
        self.ErrorTracebackBox.setGeometry(QtCore.QRect(420, 500, 321, 31))
        self.ErrorTracebackBox.setObjectName("ErrorTracebackBox")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(540, 480, 91, 16))
        self.label_7.setObjectName("label_7")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(70, 110, 220, 52))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.progressBar_2 = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName("progressBar_2")
        self.verticalLayout_2.addWidget(self.progressBar_2)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.progressBar_3 = QtWidgets.QProgressBar(self.layoutWidget1)
        self.progressBar_3.setProperty("value", 24)
        self.progressBar_3.setObjectName("progressBar_3")
        self.verticalLayout.addWidget(self.progressBar_3)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(70, 230, 110, 52))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget2)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(70, 440, 158, 25))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(420, 60, 121, 16))
        self.label_8.setObjectName("label_8")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(420, 80, 221, 381))
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pointSystemDropdown = QtWidgets.QComboBox(self.widget)
        self.pointSystemDropdown.setObjectName("pointSystemDropdown")
        self.pointSystemDropdown.addItem("")
        self.pointSystemDropdown.addItem("")
        self.verticalLayout_4.addWidget(self.pointSystemDropdown)
        self.pointsTable = QtWidgets.QTableWidget(self.widget)
        self.pointsTable.setRowCount(10)
        self.pointsTable.setColumnCount(2)
        self.pointsTable.setObjectName("pointsTable")
        item = QtWidgets.QTableWidgetItem()
        self.pointsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.pointsTable.setHorizontalHeaderItem(1, item)
        self.verticalLayout_4.addWidget(self.pointsTable)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 808, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">My Grat</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Upload Files</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Process Tips</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Status</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Results</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" text-decoration: underline;\">Error Traceback</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Orders"))
        self.pushButton.setText(_translate("MainWindow", "Time Entries"))
        self.pushButton_3.setText(_translate("MainWindow", "Distribute Tips"))
        self.pushButton_4.setText(_translate("MainWindow", "View Results"))
        self.pushButton_5.setText(_translate("MainWindow", "Save Results"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; text-decoration: underline;\">Select Point System</span></p></body></html>"))
        self.pointSystemDropdown.setItemText(0, _translate("MainWindow", "Mocha Red"))
        self.pointSystemDropdown.setItemText(1, _translate("MainWindow", "Mocha Lux"))
        item = self.pointsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Role"))
        item = self.pointsTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Points"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
