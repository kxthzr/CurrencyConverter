import sys
import requests
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QLabel
from Currency_ui import Ui_MainWindow
import tkinter

class CurrencyConverterApp(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        """
        Set up the application, including the UI and error labels.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Error labels
        self.amount_empty_error_label = QLabel(self)
        self.amount_empty_error_label.setStyleSheet("color: red; font-size: 18px;")
        self.amount_empty_error_label.setGeometry(150, 160, 300, 20)
        self.amount_empty_error_label.hide()

        self.conversion_successful = QLabel(self)
        self.conversion_successful.setStyleSheet("color: green; font-size: 18px;")
        self.conversion_successful.setGeometry(150, 410, 400, 20)
        self.conversion_successful.hide()

        self.amount_invalid_error_label = QLabel(self)
        self.amount_invalid_error_label.setStyleSheet("color: red; font-size: 16px;")
        self.amount_invalid_error_label.setGeometry(130, 160, 300, 20)
        self.amount_invalid_error_label.hide()

        self.currency_error_label = QLabel(self)
        self.currency_error_label.setStyleSheet("color: red; font-size: 18px;")
        self.currency_error_label.setGeometry(150, 410, 400, 20)
        self.currency_error_label.hide()

        # Initialize currency options
        self.initialize_currencies()

        # Connect the Convert button to the conversion function
        self.ui.ConvertButton.clicked.connect(self.convert_currency)

    def initialize_currencies(self) -> None:
        """
        Fetch currency data from the API and populate the combo boxes.
        """
        try:
            url = "https://v6.exchangerate-api.com/v6/4b5011b8eaf105df7e245aad/latest/USD"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("result") != "success":
                raise RuntimeError("API error: Unable to fetch currency list.")

            currencies = data.get("conversion_rates", {}).keys()

            for currency in sorted(currencies):
                self.ui.FromBox.addItem(currency)
                self.ui.ToBox.addItem(currency)

        except requests.RequestException as e:
            self.ui.ResultsDisplay.setText(f"Error fetching currencies: {str(e)}")
        except Exception as e:
            self.ui.ResultsDisplay.setText(f"Unexpected error: {str(e)}")

    def convert_currency(self) -> None:
        """
        Convert the entered amount from one currency to another.
        """
        # Clear error labels
        self.amount_empty_error_label.hide()
        self.amount_invalid_error_label.hide()
        self.currency_error_label.hide()
        self.conversion_successful.hide()

        # Validate if the amount is empty
        if not self.ui.lineEdit.text():
            self.amount_empty_error_label.setText("Please enter an amount.")
            self.amount_empty_error_label.show()
            return

        try:
            amount = float(self.ui.lineEdit.text())

            from_currency = self.ui.FromBox.currentText()
            to_currency = self.ui.ToBox.currentText()

            if from_currency == "Choose" or to_currency == "Choose":
                self.currency_error_label.setText("Please select a currency.")
                self.currency_error_label.show()
                return

            # Get exchange rate
            rate = self.get_exchange_rate(from_currency, to_currency)

            # Perform conversion
            converted_amount = amount * rate
            self.ui.ResultsDisplay.setText(f"<p style='text-align: center;'> {converted_amount:.2f} {to_currency}")
            #self.ui.ResultsDisplay.setAlignment('text: center;')

            #{amount:.2f} {from_currency}

            # Clear fields after conversion
            self.ui.lineEdit.clear()
            self.ui.FromBox.setCurrentIndex(0)
            self.ui.ToBox.setCurrentIndex(0)
            self.conversion_successful.setText("Conversion Successful!")
            self.conversion_successful.show()

        except ValueError:
            self.amount_invalid_error_label.setText("Invalid! Please enter a valid number.")
            self.amount_invalid_error_label.show()
        except RuntimeError as e:
            self.ui.ResultsDisplay.setText(str(e))
        except Exception as e:
            self.ui.ResultsDisplay.setText(f"Unexpected error: {str(e)}")

    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str) -> float:
        """
        Fetch the exchange rate for the specified currency pair.
        """
        try:
            url = f"https://v6.exchangerate-api.com/v6/4b5011b8eaf105df7e245aad/latest/{from_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("result") != "success":
                raise RuntimeError("Currency not available")

            rates = data.get("conversion_rates", {})
            if to_currency not in rates:
                raise ValueError(f"Currency {to_currency} not supported.")

            return rates[to_currency]

        except requests.RequestException as e:
            raise RuntimeError(f"HTTP error: {str(e)}")
        except ValueError as e:
            raise RuntimeError(f"Data error: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CurrencyConverterApp()
    window.show()
    sys.exit(app.exec())
