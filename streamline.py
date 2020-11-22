import numpy as np
import pandas as pd
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

QT_CREATOR_FILE = "streamline.ui" # import ui file for window
UI_MAIN_WINDOW, QT_BASE_CLASS = uic.loadUiType(QT_CREATOR_FILE)

class MainWindow(QtWidgets.QMainWindow, UI_MAIN_WINDOW):
	"""Gui MainWindow, presentation layer"""
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		UI_MAIN_WINDOW.__init__(self)
		
		# set up presentation layer
		self.setupUi(self)
		# self.setFixedSize(self.size())

		# action buttons
		self.read_button.pressed.connect(self.read)
		self.save_button.pressed.connect(self.save)
		self.config_view.setFocusPolicy(Qt.NoFocus)
		self.directory_edit.setPlaceholderText("directory name you want to save")


	def read(self):
		self.df_train = pd.read_csv('train.csv', index_col=0)
		totalHousePrice = self.df_train['Total Price($)'].iloc[0]
		downPayment =  self.df_train['Down payment($)'].iloc[0]
		self.loanInterest = self.df_train['Loan Interest(%)'].iloc[0]
		self.terms = self.df_train['Terms(Year)'].iloc[0]
		propertyTax = self.df_train['Property tax(%)'].iloc[0]
		hoa = self.df_train['HOA(%)'].iloc[0]
		insurance = self.df_train['Insurance(%)'].iloc[0]
		rentalRateOfReturn = self.df_train['Rental rate of return(%)'].iloc[0]
		returnOfAsset = self.df_train['Return of asset(%)'].iloc[0]

		self.render()

	def render(self):
		header = ['Total Price($)', 'Down payment($)', 'Loan Interest(%)', 'Terms(Year)', 'Property tax(%)', 'HOA(%)', 'Insurance(%)', 'Rental rate of return(%)', 'Return of asset(%)']
		num_columns = len(header)
		num_rows = len(self.df_train)

		self.config_view.setRowCount(num_rows)
		self.config_view.setColumnCount(num_columns)
		self.config_view.setHorizontalHeaderLabels(header)

		for row in range(num_rows):
			for col in range(num_columns):
				text = str(self.df_train.iloc[row, col+1])
				item = QTableWidgetItem(text)

				self.config_view.setItem(row, col, item)

		

	def Costs(self, totalHousePrice, downPayment, propertyTax, hoa, insurance):
		totalLoans = totalHousePrice - downPayment
		investmentLoanInterest = self.loanInterest + 0.005
		paymentPerTerm = totalLoans * investmentLoanInterest +  totalLoans * investmentLoanInterest / ((1 + investmentLoanInterest)**(self.terms) - 1) 
		annualPropertyTax = propertyTax *  totalHousePrice
		annualHoa = hoa * totalHousePrice
		annualInsurance = insurance * totalHousePrice
	    
		return paymentPerTerm + annualPropertyTax + annualHoa + annualInsurance


	def RentalReturn(self, totalHousePrice, rentalRateOfReturn):
		return totalHousePrice * rentalRateOfReturn

	def ROA(self, totalHousePrice, returnOfAsset):
		return totalHousePrice * returnOfAsset


	def save(self):
		self.df_train['Costs'] = self.df_train.apply(lambda x: self.Costs(x['Total Price($)'], x['Down payment($)'],  x['Property tax(%)'], x['HOA(%)'], x['Insurance(%)']), axis=1)
		self.df_train['RentalReturn'] = self.df_train.apply(lambda x: self.RentalReturn(x['Total Price($)'], x['Rental rate of return(%)']), axis=1)
		self.df_train['ROA'] = self.df_train.apply(lambda x: self.ROA(x['Total Price($)'], x['Return of asset(%)']), axis=1)
		self.df_train['ProfitMargin'] = self.df_train['RentalReturn'] - self.df_train['Costs']
		self.df_train.to_csv('train.csv') 

		self.autocomplete()

	def autocomplete(self):
		header = ['Costs', 'RentalReturn', 'ROA', 'ProfitMargin']
		num_columns = len(header)
		num_rows = len(self.df_train)
		self.autocomplete_view.setRowCount(num_rows)
		self.autocomplete_view.setColumnCount(num_columns)
		self.autocomplete_view.setHorizontalHeaderLabels(header)


		for row in range(num_rows):
			for col in range(num_columns):
				text = str(self.df_train.iloc[row, col+10])
				item = QTableWidgetItem(text)

				self.autocomplete_view.setItem(row, col, item)

 
def main():
	"""main function, main window"""
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()
	sys.exit()


if __name__ == "__main__":
	main()