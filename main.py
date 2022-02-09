import sys
from qtpy import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from qtpy import QtTest
import monitoringFunc
import csv

from frontend.mainwindow import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QMainWindow()

ui_window = Ui_MainWindow()
ui_window.setupUi(window)

window.show()

listAccDynamic = []
newEntries = []

def initReporting():
    with open('settings/settings.csv', 'r', newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=';', quotechar='"')

        tableRow = 0
        rowCount = 1

        for row in file:
            ui_window.tableWidget.setRowCount(rowCount)

            acc = monitoringFunc.account(row[0], row[1], row[2], int(row[3]))
            acc.login()

            ui_window.tableWidget.setItem(tableRow, 0, QTableWidgetItem(row[1]))
            ui_window.tableWidget.setItem(tableRow, 1, QTableWidgetItem(str(int(acc.numMessages) - int(row[3]))))

            acc.quit()

            rowCount = rowCount + 1
            tableRow = tableRow + 1

def onButtonReportingClick():
    ui_window.label_3.setText(" ++++ REPORTING IS BEING UPDATED ++++ ")
    ui_window.pushButton.setEnabled(False)
    ui_window.pushButton_2.setEnabled(False)
    QtTest.QTest.qWait(1000)

    monitoringFunc.openSettings()
    monitoringFunc.writeSettings()
    monitoringFunc.writeReporting()

    ui_window.pushButton.setEnabled(True)
    ui_window.label_3.setText(" ++++ REPORTING IS FINISHED ++++ ")

def onButtonResearchClick():
    ui_window.label_2.setText(" ++++ RESEARCH IS RUNNING ++++ ")
    ui_window.pushButton.setEnabled(False)
    ui_window.pushButton_2.setEnabled(False)
    QtTest.QTest.qWait(1000)

    searchItem = ui_window.lineEdit.displayText()
    searchCount = ui_window.horizontalSlider.value()
    monitoringFunc.massSearch(searchItem, searchCount)

    ui_window.pushButton.setEnabled(True)
    ui_window.pushButton_2.setEnabled(True)
    ui_window.label_2.setText(" ++++ RESEARCH FINISHED ++++ ")

def onSliderChange():
    searchCount = ui_window.horizontalSlider.value()
    ui_window.label.setText(str(searchCount) + " Mails werden durchsucht.")


initReporting()
ui_window.pushButton.clicked.connect(onButtonResearchClick)
ui_window.pushButton_2.clicked.connect(onButtonReportingClick)
ui_window.horizontalSlider.valueChanged.connect(onSliderChange)

sys.exit(app.exec_())