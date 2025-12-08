

def user_dashboard(current_email):
    from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt, QDate)
    from PySide6.QtGui import (QCursor)
    from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                   QHBoxLayout, QLabel, QPushButton, QStackedWidget, 
                                   QFrame, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QHeaderView, QDateEdit)
    import database

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            self.MainWindow = MainWindow
            self.user_email = current_email

            if not self.MainWindow.objectName():
                self.MainWindow.setObjectName(u"MainWindow")
            
            self.MainWindow.resize(1000, 700)
            self.MainWindow.setStyleSheet(u"QMainWindow { background-color: #f4f6f9; }")

            self.centralwidget = QWidget(self.MainWindow)
            self.mainLayout = QHBoxLayout(self.centralwidget)
            self.mainLayout.setSpacing(0)
            self.mainLayout.setContentsMargins(0, 0, 0, 0)

            # Side bar
            self.sidebarFrame = QFrame(self.centralwidget)
            self.sidebarFrame.setMinimumWidth(250)
            self.sidebarFrame.setMaximumWidth(250)
            self.sidebarFrame.setStyleSheet(u"background-color: #ffffff; border-right: 1px solid #e0e0e0;")
            
            self.sidebarLayout = QVBoxLayout(self.sidebarFrame)
            self.sidebarLayout.setSpacing(10)
            self.sidebarLayout.setContentsMargins(20, 30, 20, 30)

            self.appTitle = QLabel("Library User", self.sidebarFrame)
            self.appTitle.setAlignment(Qt.AlignCenter)
            self.appTitle.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
            self.sidebarLayout.addWidget(self.appTitle)
            
            self.userLabel = QLabel(f"Logged in as:\n{self.user_email}", self.sidebarFrame)
            self.userLabel.setStyleSheet("color: #7f8c8d; font-size: 12px; margin-bottom: 20px;")
            self.userLabel.setAlignment(Qt.AlignCenter)
            self.sidebarLayout.addWidget(self.userLabel)

            sidebar_btn_style = u"""
            QPushButton { background-color: transparent; color: #34495e; text-align: left; padding-left: 20px; font-size: 16px; border: none; height: 50px; }
            QPushButton:hover { background-color: #f0f2f5; font-weight: bold; }
            """

            self.ubrowse_books = QPushButton("  Browse Books", self.sidebarFrame)
            self.ubrowse_books.setCursor(QCursor(Qt.PointingHandCursor))
            self.ubrowse_books.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.ubrowse_books)

            self.uborrow_history = QPushButton("  Borrow History", self.sidebarFrame)
            self.uborrow_history.setCursor(QCursor(Qt.PointingHandCursor))
            self.uborrow_history.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.uborrow_history)

            self.umy_profile = QPushButton("  My Profile", self.sidebarFrame)
            self.umy_profile.setCursor(QCursor(Qt.PointingHandCursor))
            self.umy_profile.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.umy_profile)

            self.ufines = QPushButton("  Fines & Transactions", self.sidebarFrame)
            self.ufines.setCursor(QCursor(Qt.PointingHandCursor))
            self.ufines.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.ufines)

            self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.sidebarLayout.addItem(self.verticalSpacer)

            # Logout
            self.btnLogout = QPushButton("  Logout", self.sidebarFrame)
            self.btnLogout.setCursor(QCursor(Qt.PointingHandCursor))
            self.btnLogout.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.btnLogout)

            self.mainLayout.addWidget(self.sidebarFrame)

            
            self.stackedWidget = QStackedWidget(self.centralwidget)
            self.stackedWidget.setStyleSheet(u"background-color: #f4f6f9;")

            # Browse books
            self.page_browse = QWidget()
            self.layout_browse = QVBoxLayout(self.page_browse)
            self.layout_browse.setContentsMargins(40,40,40,40)
            self.layout_browse.addWidget(QLabel("Browse Books", styleSheet="font-size: 24px; font-weight: bold;"))
            
            inputLayout = QHBoxLayout()
            self.inputBookName = QLineEdit(placeholderText="Enter Book Name")
            self.dateLabel = QLabel("Return Date:")
            self.dateInput = QDateEdit()
            self.dateInput.setCalendarPopup(True)
            self.dateInput.setDate(QDate.currentDate().addDays(7))
            inputLayout.addWidget(self.inputBookName)
            inputLayout.addWidget(self.dateLabel)
            inputLayout.addWidget(self.dateInput)
            self.layout_browse.addLayout(inputLayout)

            btnLayout = QHBoxLayout()
            self.btnBorrow = QPushButton("Borrow Book", styleSheet="background-color: #27ae60; color: white; padding: 10px;")
            self.btnBorrow.setCursor(QCursor(Qt.PointingHandCursor))
            self.btnReturn = QPushButton("Return Book", styleSheet="background-color: #e67e22; color: white; padding: 10px;")
            self.btnReturn.setCursor(QCursor(Qt.PointingHandCursor))
            btnLayout.addWidget(self.btnBorrow)
            btnLayout.addWidget(self.btnReturn)
            self.layout_browse.addLayout(btnLayout)

            self.tableBrowse = QTableWidget()
            self.tableBrowse.setColumnCount(4)
            self.tableBrowse.setHorizontalHeaderLabels(["Book Name", "Status", "ISBN", "Author"])
            self.tableBrowse.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout_browse.addWidget(self.tableBrowse)
            self.stackedWidget.addWidget(self.page_browse)

           
            self.page_history = QWidget()
            self.layout_history = QVBoxLayout(self.page_history)
            self.layout_history.setContentsMargins(40,40,40,40)
            self.layout_history.addWidget(QLabel("My Borrow History", styleSheet="font-size: 24px; font-weight: bold;"))
            
            self.tableHistory = QTableWidget()
            self.tableHistory.setColumnCount(4)
            self.tableHistory.setHorizontalHeaderLabels(["Book", "Email", "Borrow Date", "Due Date"])
            self.tableHistory.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout_history.addWidget(self.tableHistory)
            self.stackedWidget.addWidget(self.page_history)

           # Profile
            self.page_profile = QWidget()
            self.layout_profile = QVBoxLayout(self.page_profile)
            self.layout_profile.setContentsMargins(40,40,40,40)
            self.layout_profile.addWidget(QLabel("My Profile", styleSheet="font-size: 24px; font-weight: bold;"))
            
            self.profileDetails = QLabel("Loading...")
            self.profileDetails.setStyleSheet("font-size: 18px; color: #2c3e50; background: white; padding: 20px; border-radius: 10px;")
            self.layout_profile.addWidget(self.profileDetails)
            self.layout_profile.addStretch()
            self.stackedWidget.addWidget(self.page_profile)

            # Fines
            self.page_fines = QWidget()
            self.layout_fines = QVBoxLayout(self.page_fines)
            self.layout_fines.setContentsMargins(40,40,40,40)
            self.layout_fines.addWidget(QLabel("My Fines", styleSheet="font-size: 24px; font-weight: bold;"))
            
            self.tableFines = QTableWidget()
            self.tableFines.setColumnCount(5)
            self.tableFines.setHorizontalHeaderLabels(["Book", "Email", "Date", "Due", "Fine"])
            self.tableFines.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout_fines.addWidget(self.tableFines)
            self.stackedWidget.addWidget(self.page_fines)

            self.mainLayout.addWidget(self.stackedWidget)
            self.MainWindow.setCentralWidget(self.centralwidget)
            self.retranslateUi(self.MainWindow)
            QMetaObject.connectSlotsByName(self.MainWindow)

            # Connections
            self.ubrowse_books.clicked.connect(lambda: self.switch_page(0))
            self.uborrow_history.clicked.connect(lambda: self.switch_page(1))
            self.umy_profile.clicked.connect(lambda: self.switch_page(2))
            self.ufines.clicked.connect(lambda: self.switch_page(3))
            self.btnLogout.clicked.connect(self.logout)
            self.btnBorrow.clicked.connect(self.borrow_logic)
            self.btnReturn.clicked.connect(self.return_logic)

            # Initial Load
            self.load_books()

        def retranslateUi(self, MainWindow):
            MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Library User Dashboard", None))

        def logout(self):
            import sys, subprocess
            self.MainWindow.close()
            subprocess.Popen([sys.executable, 'main.py'])

        def switch_page(self, index):
            self.stackedWidget.setCurrentIndex(index)
            if index == 0: self.load_books()
            if index == 1: self.load_history()
            if index == 2: self.load_profile()
            if index == 3: self.load_fines()

        def load_books(self):
            data = database.get_all_books()
            self.tableBrowse.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tableBrowse.insertRow(row_num)
                for col_num, cell in enumerate(row_data):
                    self.tableBrowse.setItem(row_num, col_num, QTableWidgetItem(str(cell)))

        def borrow_logic(self):
            book = self.inputBookName.text()
            email = self.user_email
            qdate = self.dateInput.date()
            date_str = qdate.toString("yyyy-MM-dd")
            if book:
                res = database.borrow_book(book, email, date_str)
                QMessageBox.information(self.MainWindow, "Info", res)
                self.load_books()

        def return_logic(self):
            book = self.inputBookName.text()
            email = self.user_email
            if book:
                res = database.return_book(book, email)
                QMessageBox.information(self.MainWindow, "Info", res)
                self.load_books()

        def load_history(self):
            email = self.user_email
            data = database.get_user_history(email)
            self.tableHistory.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tableHistory.insertRow(row_num)
                for col_num, cell in enumerate(row_data):
                    self.tableHistory.setItem(row_num, col_num, QTableWidgetItem(str(cell)))

        def load_profile(self):
            email = self.user_email
            data = database.get_student_details(email)
            if data:
                txt = f"Name: {data[0]} {data[1]}\nEmail: {data[2]}\nZip Code: {data[3]}\nPhone: {data[5]}\nRole: {data[6]}"
                self.profileDetails.setText(txt)
            else:
                self.profileDetails.setText("User not found.")

        def load_fines(self):
            email = self.user_email
            data = database.get_user_active_fines(email)
            self.tableFines.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tableFines.insertRow(row_num)
                for col_num, cell in enumerate(row_data):
                    self.tableFines.setItem(row_num, col_num, QTableWidgetItem(str(cell)))

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.ui = ui 
    return window
