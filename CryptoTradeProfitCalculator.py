from ast import If
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pyqtgraph as pg
from pyqtgraph import DateAxisItem
from datetime import datetime

class MainWindow(QWidget):

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.initUI()

    def initUI(self):
        # main grid to hold the input & display layout panels
        grid = QGridLayout()
        grid.setSpacing(50)
        
        # Input widgets
        self.stockName = QLabel('Crypto Currency Purchased :')
        self.stockNameOption = QComboBox()
        self.stockNameOption.addItems(list(self.data.keys()))
        self.stockNameOption.activated.connect(self.onClick)

        self.qtyPurchase = QLabel('Quantity Purchased :')
        self.qtyPurchaseEdit = QSpinBox(minimum=1)
        self.qtyPurchaseEdit.valueChanged.connect(self.onClick)

        self.purchaseDate = QLabel('Choose a Purchase Date :')
        self.purchaseDateEdit = QCalendarWidget()
        self.purchaseDateEdit.SelectionMode(1)

        self.sellDate = QLabel('Choose a Sell Date :')
        self.sellDateEdit = QCalendarWidget()
        self.sellDateEdit.SelectionMode(1)

        # Layout panel that holds input widgets
        self.inputGrid = QGridLayout() 
        self.inputGrid.setSpacing(10)

        self.inputGrid.addWidget(self.stockName, 1, 0)
        self.inputGrid.addWidget(self.stockNameOption, 1, 1)
        self.inputGrid.addWidget(self.qtyPurchase, 2, 0)
        self.inputGrid.addWidget(self.qtyPurchaseEdit, 2, 1)
        self.inputGrid.addWidget(self.purchaseDate, 3, 0,)
        self.inputGrid.addWidget(self.purchaseDateEdit, 3, 1,)
        self.inputGrid.addWidget(self.sellDate, 5, 0, 1, 1)
        self.inputGrid.addWidget(self.sellDateEdit, 5, 1)

        # Details widgets
        self.detailGrid = QGridLayout() # Layout panel that holds details widgets
        self.detailGrid.setColumnMinimumWidth(0,250)
        self.detailGrid.setVerticalSpacing(30)
        self.borderBox = QGroupBox('Results')
        self.borderBox.setStyleSheet("font-size:16px;")
        self.purchaseDayDetails = QFormLayout()
        self.sellDayDetails = QFormLayout()
        self.purchaseDetails = QFormLayout()

        self.purchaseDayDetailHeader = QLabel('Purchase Prices')
        self.purchaseDayDetailHeader.setStyleSheet("text-decoration:underline")

        self.purchaseOpenEdit = QLabel('Awaiting input...')
        self.purchaseCloseEdit = QLabel('Awaiting input...')
        self.purchaseHighEdit = QLabel('Awaiting input...')
        self.purchaseLowEdit = QLabel('Awaiting input...')
        self.selectedPurchaseDateEdit = QLabel('Awaiting input...')
        self.purchaseDateEdit.setSelectedDate(QDate(2020, 10, 6))
        self.purchaseDateEdit.clicked.connect(self.onClick)
        
        self.purchaseDayDetails.addRow(self.purchaseDayDetailHeader)
        self.purchaseDayDetails.addRow('Selected Date :', self.selectedPurchaseDateEdit)
        self.purchaseDayDetails.addRow('Open :', self.purchaseOpenEdit)
        self.purchaseDayDetails.addRow('Close :', self.purchaseCloseEdit)
        self.purchaseDayDetails.addRow('Highest :', self.purchaseHighEdit)
        self.purchaseDayDetails.addRow('Lowest :', self.purchaseLowEdit)

        self.sellDetailHeader = QLabel('Sell Prices')
        self.sellDetailHeader.setStyleSheet("text-decoration:underline")

        self.selectedSellDateEdit = QLabel('Awaiting input...')
        self.sellDateEdit.setSelectedDate(QDate(2020, 10, 8))
        self.sellDateEdit.clicked.connect(self.onClick)

        self.sellOpenEdit = QLabel('Awaiting input...')
        self.sellCloseEdit = QLabel('Awaiting input...')
        self.sellHighEdit = QLabel('Awaiting input...')
        self.sellLowEdit = QLabel('Awaiting input...')

        self.sellDayDetails.addRow(self.sellDetailHeader)
        self.sellDayDetails.addRow('Selected Date :', self.selectedSellDateEdit)
        self.sellDayDetails.addRow('Open :', self.sellOpenEdit)
        self.sellDayDetails.addRow('Close :', self.sellCloseEdit)
        self.sellDayDetails.addRow('Highest :', self.sellHighEdit)
        self.sellDayDetails.addRow('Lowest :', self.sellLowEdit)

        self.purchaseDetailHeader = QLabel('Transaction')
        self.purchaseDetailHeader.setStyleSheet("text-decoration:underline")
        self.purchaseTotalEdit = QLabel('Awaiting input...')
        self.sellTotalEdit = QLabel('Awaiting input...')
        self.profitTotalEdit = QLabel('Awaiting input...')

        self.purchaseDetails.addRow(self.purchaseDetailHeader)
        self.purchaseDetails.addRow('Purchase Total :',self.purchaseTotalEdit)
        self.purchaseDetails.addRow('Sell Total :',self.sellTotalEdit)
        self.purchaseDetails.addRow('Profit Total :',self.profitTotalEdit)

        # construct the display detail panel
        self.detailGrid.addLayout(self.purchaseDayDetails,0,0)
        self.detailGrid.addLayout(self.sellDayDetails,1,0)
        self.detailGrid.addLayout(self.purchaseDetails,2,0)
        self.borderBox.setLayout(self.detailGrid)

        # Additional Feature, Graph of the month
        # graph colors
        self.graphWidget = pg.PlotWidget(axisItems={'bottom': DateAxisItem(orientation='bottom')})
        self.graphWidget.setBackground('k')
        self.setMinimumHeight(900)
        self.graphWidget.setTitle('Awaiting input...', color="b", size="14pt")
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "14px"}
        self.graphWidget.setLabel("left", "Price", **styles)
        self.graphWidget.setLabel("bottom", "Date", **styles)
        #Add legend
        self.graphWidget.addLegend()
        #Add grid
        self.graphWidget.showGrid(x=True, y=True)
        #Set Range
        self.graphWidget.setXRange(0, 8)
        self.graphWidget.setYRange(10, 80)

        # adding the input and display details panel into the main grid
        grid.addLayout(self.inputGrid, 0, 0)
        grid.addWidget(self.borderBox, 0, 1, alignment=Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.graphWidget,1,0,1,2)
        self.setLayout(grid)

        #sets the window title of the UI 
        self.setWindowTitle('CryptoCurrency Profit/Loss Calculator')
        self.show()

    def plot(self, x, y, plotname, color):
        pen = pg.mkPen(color=color)
        self.graphWidget.plot(x, y, name=plotname, pen=pen, symbol='+', symbolSize=8, symbolBrush=(color))
        
    def onClick(self):
        """ Function that handles any changes on input
        """        
        
        selectedCryptoCurrency = None
        try:
            # selectedCryptoCurrency = self.data[self.stockNameOption.currentText()]
            from collections import OrderedDict
            selectedCryptoCurrency = OrderedDict(sorted(self.data[self.stockNameOption.currentText()].items()))
            
            date_format = '%Y-%m-%d'
        
            # Get first and last available day from data 
            firstDate = datetime.strptime([*selectedCryptoCurrency.keys()][0], date_format)
            lastDate = datetime.strptime([*selectedCryptoCurrency.keys()][-1], date_format)

            # Set min max date for purchase edit calendar
            self.purchaseDateEdit.setMinimumDate(QDate(firstDate.year, firstDate.month, firstDate.day))
            self.purchaseDateEdit.setMaximumDate(QDate(lastDate.year, lastDate.month, lastDate.day))
            
            # Get the user selected date 
            selectedPurchaseDate = self.purchaseDateEdit.selectedDate()
            # Set min max date for sell edit calendar where the minimum date is from the purchase date onwards
            self.sellDateEdit.setMinimumDate(selectedPurchaseDate)
            self.sellDateEdit.setMaximumDate(QDate(lastDate.year, lastDate.month, lastDate.day))

            #set the title of the graph
            self.graphWidget.setTitle('Price graph of {:} 7 days from {:}'.format(self.stockNameOption.currentText(),self.purchaseDateEdit.selectedDate().toString('yyyy-MM-dd')), color="r", size="16pt")

        except KeyError:
            print("Selection not available")
        except: # Default 
            print("Something else went wrong")
            
        if(selectedCryptoCurrency is not None):
            
            cryptoPurchaseData = None
            try:
                cryptoPurchaseData = selectedCryptoCurrency[self.purchaseDateEdit.selectedDate().toString('yyyy-MM-dd')] # Retreive purchase day detail from data
                self.selectedPurchaseDateEdit.setText(self.purchaseDateEdit.selectedDate().toString('yyyy-MM-dd')) # Set label text
                
            except KeyError as e:
                print("Purchase Date not available")
                self.selectedPurchaseDateEdit.setText('Selected Purchase Date not available') # Set label text for unavailable purchase date
                
            except: # Default 
                print("Something else went wrong")
            
            cryptoSellData = None    
            try:
                cryptoSellData = selectedCryptoCurrency[self.sellDateEdit.selectedDate().toString('yyyy-MM-dd')] # Retreive sell day detail from data
                self.selectedSellDateEdit.setText(self.sellDateEdit.selectedDate().toString('yyyy-MM-dd')) # Set label text
                
            except KeyError as e:
                print(selectedCryptoCurrency)
                self.selectedSellDateEdit.setText('Selected Sell Date not available') # Set label text for unavailable sell date
                
            except: # Default 
                print("Something else went wrong")
            
            # Only run when both cryptoSellData and cryptoPurchaseData are retreived from data 
            if cryptoSellData is not None and cryptoPurchaseData is not None: 
                self.setPurchaseDayDetails(cryptoPurchaseData)
                self.setSellDayDetails(cryptoSellData)
                self.calculateEarning(self.qtyPurchaseEdit.value(), cryptoPurchaseData['open'], cryptoSellData['close'])
                
                # plot xy labels that is 7 days from the selected purchase date
                self.days = []
                self.sellPriceSevenDayHistory = []
                self.purchasePriceSevenDayHistory = []
                
                # gets the frst date to plot 
                firstDayIndex = list(selectedCryptoCurrency).index(self.purchaseDateEdit.selectedDate().toPyDate().strftime('%Y-%m-%d'))
                sevenDayIndexList = list(selectedCryptoCurrency.keys())[firstDayIndex:firstDayIndex+7]
                
                for index, dateKey in enumerate(sevenDayIndexList):
                    date = self.purchaseDateEdit.selectedDate().addDays(index)
                    self.days.append(datetime.strptime(sevenDayIndexList[index], '%Y-%m-%d').timestamp())
                    self.sellPriceSevenDayHistory.append(int(float(selectedCryptoCurrency[dateKey]['open'])))
                    self.purchasePriceSevenDayHistory.append(int(float(selectedCryptoCurrency[dateKey]['close'])))
                    
                self.graphWidget.clear() # Clear previous plot
                self.graphWidget.setXRange(self.days[0], self.days[6], padding=0.1)
                self.graphWidget.setYRange(0, max(self.sellPriceSevenDayHistory)+20 , padding=0)
                
                self.plot(self.days, self.sellPriceSevenDayHistory, "Buy Price", 'r')
                self.plot(self.days, self.purchasePriceSevenDayHistory, "Sell Price", 'b')
        
    def setPurchaseDayDetails(self, purchaseDayData):
        """Set Text for purchase day detail labels

        Args:
            purchaseDayData (dict): purchase day date
        """        
        self.purchaseOpenEdit.setText("{:.4f}".format(float(purchaseDayData['open'])))
        self.purchaseCloseEdit.setText("{:.4f}".format(float(purchaseDayData['close'])))
        self.purchaseHighEdit.setText("{:.4f}".format(float(purchaseDayData['high'])))
        self.purchaseLowEdit.setText("{:.4f}".format(float(purchaseDayData['low'])))
        
    def setSellDayDetails(self, cryptoSellData):
        """Set Text for sell day detail labels

        Args:
            cryptoSellData (_type_): sell day date
        """        
        self.sellOpenEdit.setText("{:.4f}".format(float(cryptoSellData['open'])))
        self.sellCloseEdit.setText("{:.4f}".format(float(cryptoSellData['close'])))
        self.sellHighEdit.setText("{:.4f}".format(float(cryptoSellData['high'])))
        self.sellLowEdit.setText("{:.4f}".format(float(cryptoSellData['low'])))
        
    def calculateEarning(self, purchaseQuantity, purchasePrice, sellPrice):
        """Compute the earning of the Crypto Currency and graph

        Args:
            purchaseQuantity (string): _description_
            purchasePrice (string): _description_
            sellPrice (string): _description_
        """        
        # calculate the profit/loss from the selected stock & dates
        purchaseTotalPrice = float(purchaseQuantity) * float(purchasePrice)
        sellTotalPrice = float(purchaseQuantity) * float(sellPrice)
        totalProfit = (sellTotalPrice - purchaseTotalPrice) * purchaseQuantity

        # display the calculated value, in 4 decimal points format
        self.purchaseTotalEdit.setText(str(round(purchaseTotalPrice, 4)))
        self.sellTotalEdit.setText(str(round(sellTotalPrice, 4)))
        self.profitTotalEdit.setText(str(round(totalProfit, 4)))
        
        # Additional Feature, Set bg and text color based on profit, red if there's a loss, blue if there's profit
        # color selected to ensure colour-blind friendliness
        if totalProfit > 0:
            self.profitTotalEdit.setStyleSheet("background-color:blue;color:white")
        elif totalProfit < 0:
            self.profitTotalEdit.setStyleSheet("background-color:red;color:white")
        elif totalProfit == 0:
            self.profitTotalEdit.setStyleSheet("background-color:transparent;color:black")
        

def readDataFromCsv():
    """Read data from csv and parse into a dict 
    Example dict
    {
        'AAVE': {
            '2020-10-05': {
                'open': '52.67503496',
                'high': '55.11235847',
                'low': '49.78789992',
                'close': '53.21924296',
                'volume': '0',
                'Marketcap': '89128128.86'
            },
            '2020-10-06': {
                'open': '53.29196931',
                'high': '53.40227002',
                'low': '40.73457791',
                'close': '42.40159861',
                'volume': '583091.4598',
                'Marketcap': '71011441.25'},
            }
        },
    }
    
    Returns:
        dict: dict that contains all data parse from CSV
    """
    import csv
    
    data = {}

    with open("PuiKwan_CHIEW_3132438_Ass1/combined.csv", 'r') as file:
        csvreader = csv.reader(file) 
        for index, row in enumerate(csvreader):
            if index == 0: 
                # If index = 0 = First row = Header of CSV
                # Skip header because it's a header 
                continue
            
            name = row[6] # Get the Crypto Currency Name
            if name not in data:
                # Check if the Crypto Currency Name exists
                # if no exists add it into the dict
                data[name] = {}
            
            # Each day = daily record of a Crypto Currency 
            # Uses date as unique key
            data[name][row[0]] = {
                'open': row[1].format(),
                'high': row[2],
                'low': row[3],
                'close': row[4],
                'volume': row[5],
                'Marketcap': row[7],
            }
    return data 

def main():

    app = QApplication(sys.argv)
    ex = MainWindow(readDataFromCsv())
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()
    
