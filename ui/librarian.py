

def librarian_dashboard():
    from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
    from PySide6.QtGui import (QCursor)
    from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                   QHBoxLayout, QLabel, QPushButton, QStackedWidget, 
                                   QFrame, QSpacerItem, QSizePolicy, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView)
    import database

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            self.MainWindow = MainWindow
            if not self.MainWindow.objectName():
                self.MainWindow.setObjectName(u"MainWindow")
            
            self.MainWindow.resize(1100, 750)
            self.MainWindow.setStyleSheet(u"QMainWindow { background-color: #f4f6f9; }")

            self.centralwidget = QWidget(self.MainWindow)
            self.mainLayout = QHBoxLayout(self.centralwidget)
            self.mainLayout.setSpacing(0)
            self.mainLayout.setContentsMargins(0, 0, 0, 0)

            # Sidebar
            self.sidebarFrame = QFrame(self.centralwidget)
            self.sidebarFrame.setMinimumWidth(260)
            self.sidebarFrame.setMaximumWidth(260)
            self.sidebarFrame.setStyleSheet(u"background-color: #2c3e50; color: white; border-right: 1px solid #34495e;")
            
            self.sidebarLayout = QVBoxLayout(self.sidebarFrame)
            self.sidebarLayout.setSpacing(15)
            self.sidebarLayout.setContentsMargins(20, 40, 20, 40)

            self.appTitle = QLabel("Librarian Admin", self.sidebarFrame)
            self.appTitle.setAlignment(Qt.AlignCenter)
            self.appTitle.setStyleSheet(u"color: #ecf0f1; font-family: 'Segoe UI'; font-size: 24px; font-weight: bold; margin-bottom: 30px;")
            self.sidebarLayout.addWidget(self.appTitle)

            sidebar_btn_style = u"""
            QPushButton {
                background-color: transparent;
                color: #ecf0f1;
                text-align: left;
                padding-left: 20px;
                font-family: 'Segoe UI';
                font-size: 16px;
                border: none;
                border-radius: 10px;
                height: 50px;
            }
            QPushButton:hover {
                background-color: #34495e;
                color: #ffffff;
                font-weight: bold;
                border-left: 5px solid #e74c3c;
            }
            """

            self.lmanage_books = QPushButton("  Manage Books", self.sidebarFrame)
            self.lmanage_books.setCursor(QCursor(Qt.PointingHandCursor))
            self.lmanage_books.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.lmanage_books)

            self.lmanage_members = QPushButton("  Manage Members", self.sidebarFrame)
            self.lmanage_members.setCursor(QCursor(Qt.PointingHandCursor))
            self.lmanage_members.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.lmanage_members)

            self.lborrow_history = QPushButton("  Borrow History", self.sidebarFrame)
            self.lborrow_history.setCursor(QCursor(Qt.PointingHandCursor))
            self.lborrow_history.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.lborrow_history)

            self.ltransactions = QPushButton("  Transactions & Fines", self.sidebarFrame)
            self.ltransactions.setCursor(QCursor(Qt.PointingHandCursor))
            self.ltransactions.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.ltransactions)

            self.lbook_catalog = QPushButton("  Book Catalog", self.sidebarFrame)
            self.lbook_catalog.setCursor(QCursor(Qt.PointingHandCursor))
            self.lbook_catalog.setStyleSheet(sidebar_btn_style)
            self.sidebarLayout.addWidget(self.lbook_catalog)

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

            # Manage books
            self.page_manage_books = QWidget()
            self.layout_m_books = QVBoxLayout(self.page_manage_books)
            self.layout_m_books.setContentsMargins(40,40,40,40)
            
            lbl = QLabel("Manage Books", self.page_manage_books)
            lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
            self.layout_m_books.addWidget(lbl)

            # Book Inputs
            inputLayout = QHBoxLayout()
            self.bookNameInput = QLineEdit()
            self.bookNameInput.setPlaceholderText("Book Name")
            self.isbnInput = QLineEdit()
            self.isbnInput.setPlaceholderText("ISBN")
            self.authorInput = QLineEdit()
            self.authorInput.setPlaceholderText("Author Name")
            
            inputLayout.addWidget(self.bookNameInput)
            inputLayout.addWidget(self.isbnInput)
            inputLayout.addWidget(self.authorInput)
            self.layout_m_books.addLayout(inputLayout)

            btnLayout = QHBoxLayout()
            self.btnAddBook = QPushButton("Add Book", self.page_manage_books)
            self.btnAddBook.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
            self.btnAddBook.setCursor(QCursor(Qt.PointingHandCursor))
            
            self.btnRemoveBook = QPushButton("Remove Book (by Name)", self.page_manage_books)
            self.btnRemoveBook.setStyleSheet("background-color: #c0392b; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
            self.btnRemoveBook.setCursor(QCursor(Qt.PointingHandCursor))

            btnLayout.addWidget(self.btnAddBook)
            btnLayout.addWidget(self.btnRemoveBook)
            self.layout_m_books.addLayout(btnLayout)

            # Mini Catalog Table
            self.tableBooksMini = QTableWidget()
            self.tableBooksMini.setColumnCount(4)
            self.tableBooksMini.setHorizontalHeaderLabels(["Book Name", "Status", "ISBN", "Author"])
            self.tableBooksMini.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout_m_books.addWidget(self.tableBooksMini)

            self.stackedWidget.addWidget(self.page_manage_books)

            # Manage members
            self.page_manage_members = QWidget()
            self.layout_m_members = QVBoxLayout(self.page_manage_members)
            self.layout_m_members.setContentsMargins(40,40,40,40)
            
            lbl2 = QLabel("Registered Members", self.page_manage_members)
            lbl2.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
            self.layout_m_members.addWidget(lbl2)

            
            removeLayout = QHBoxLayout()
            self.inputMemberEmail = QLineEdit()
            self.inputMemberEmail.setPlaceholderText("Enter Member Email to Remove")
            self.btnRemoveMember = QPushButton("Remove Member")
            self.btnRemoveMember.setStyleSheet("background-color: #c0392b; color: white; padding: 5px; border-radius: 5px;")
            removeLayout.addWidget(self.inputMemberEmail)
            removeLayout.addWidget(self.btnRemoveMember)
            self.layout_m_members.addLayout(removeLayout)

            self.tableMembers = QTableWidget()
            self.tableMembers.setColumnCount(5)
            self.tableMembers.setHorizontalHeaderLabels(["First Name", "Last Name", "Email", "Phone", "Role"])
            self.tableMembers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout_m_members.addWidget(self.tableMembers)
            self.stackedWidget.addWidget(self.page_manage_members)

            # Borrow History
            self.page_history = QWidget()
            self.layout_history = QVBoxLayout(self.page_history)
            self.layout_history.setContentsMargins(40,40,40,40)

            lbl3 = QLabel("Borrowing Log (Append Only)", self.page_history)
            lbl3.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
            self.layout_history.addWidget(lbl3)

            self.tableHistory = QTableWidget()
            self.tableHistory.setColumnCount(4)
            self.tableHistory.setHorizontalHeaderLabels(["Book", "User", "Borrow Date", "Return Date"])
            self.tableHistory.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout_history.addWidget(self.tableHistory)
            self.stackedWidget.addWidget(self.page_history)

            # TRANSACTIONS (Fines)
            self.page_transactions = QWidget()
            self.layout_trans = QVBoxLayout(self.page_transactions)
            self.layout_trans.setContentsMargins(40,40,40,40)

            lbl4 = QLabel("Active Fines", self.page_transactions)
            lbl4.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
            self.layout_trans.addWidget(lbl4)

            self.btnRefreshFines = QPushButton("Refresh Fines")
            self.btnRefreshFines.setCursor(QCursor(Qt.PointingHandCursor))
            self.btnRefreshFines.setStyleSheet("background-color: #f39c12; color: white; padding: 10px; border-radius: 5px;")
            self.layout_trans.addWidget(self.btnRefreshFines)

            self.tableFines = QTableWidget()
            self.tableFines.setColumnCount(5)
            self.tableFines.setHorizontalHeaderLabels(["Book", "User", "Borrow Date", "Due Date", "Fine ($)"])
            self.tableFines.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout_trans.addWidget(self.tableFines)
            self.stackedWidget.addWidget(self.page_transactions)

           
            self.page_catalog = QWidget()
            self.layout_catalog = QVBoxLayout(self.page_catalog)
            self.layout_catalog.setContentsMargins(40,40,40,40)

            lbl5 = QLabel("Full Book Catalog", self.page_catalog)
            lbl5.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
            self.layout_catalog.addWidget(lbl5)

            self.tableCatalog = QTableWidget()
            self.tableCatalog.setColumnCount(4)
            self.tableCatalog.setHorizontalHeaderLabels(["Book Name", "Status", "ISBN", "Author"])
            self.tableCatalog.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.layout_catalog.addWidget(self.tableCatalog)
            self.stackedWidget.addWidget(self.page_catalog)

            self.mainLayout.addWidget(self.stackedWidget)
            self.MainWindow.setCentralWidget(self.centralwidget)
            self.retranslateUi(self.MainWindow)
            QMetaObject.connectSlotsByName(self.MainWindow)

            
            self.lmanage_books.clicked.connect(lambda: self.switch_page(0))
            self.lmanage_members.clicked.connect(lambda: self.switch_page(1))
            self.lborrow_history.clicked.connect(lambda: self.switch_page(2))
            self.ltransactions.clicked.connect(lambda: self.switch_page(3))
            self.lbook_catalog.clicked.connect(lambda: self.switch_page(4))
            self.btnLogout.clicked.connect(self.logout)

            self.btnAddBook.clicked.connect(self.add_book_logic)
            self.btnRemoveBook.clicked.connect(self.remove_book_logic)
            self.btnRemoveMember.clicked.connect(self.remove_member_logic)
            self.btnRefreshFines.clicked.connect(self.refresh_fines_logic)

            # Initial Load
            self.load_catalog_mini()

        def retranslateUi(self, MainWindow):
            MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Librarian Dashboard", None))

        def logout(self):
            import sys, subprocess
            self.MainWindow.close()
            subprocess.Popen([sys.executable, 'main.py'])

        def switch_page(self, index):
            self.stackedWidget.setCurrentIndex(index)
            if index == 0: self.load_catalog_mini()
            if index == 1: self.load_members()
            if index == 2: self.load_history()
            if index == 3: self.load_fines()
            if index == 4: self.load_catalog()

        # 
        def add_book_logic(self):
            name = self.bookNameInput.text()
            isbn = self.isbnInput.text()
            auth = self.authorInput.text()
            if name:
                res = database.add_book(name, isbn, auth)
                QMessageBox.information(self.MainWindow, "Info", res)
                self.bookNameInput.clear()
                self.isbnInput.clear()
                self.authorInput.clear()
                self.load_catalog_mini()

        def remove_book_logic(self):
            name = self.bookNameInput.text()
            if name:
                res = database.remove_book(name)
                QMessageBox.information(self.MainWindow, "Info", res)
                self.bookNameInput.clear()
                self.load_catalog_mini()

        def remove_member_logic(self):
            email = self.inputMemberEmail.text()
            if email:
                res = database.remove_student(email)
                QMessageBox.information(self.MainWindow, "Info", res)
                self.inputMemberEmail.clear()
                self.load_members()

        def load_members(self):
            data = database.get_all_students()
            self.tableMembers.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tableMembers.insertRow(row_num)
                for col_num, data in enumerate(row_data):
                    self.tableMembers.setItem(row_num, col_num, QTableWidgetItem(str(data)))

        def load_history(self):
            data = database.get_all_active_borrows()
            self.tableHistory.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tableHistory.insertRow(row_num)
                self.tableHistory.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))
                self.tableHistory.setItem(row_num, 1, QTableWidgetItem(str(row_data[1])))
                self.tableHistory.setItem(row_num, 2, QTableWidgetItem(str(row_data[2])))
                self.tableHistory.setItem(row_num, 3, QTableWidgetItem(str(row_data[3])))

        def load_fines(self):
            data = database.get_all_fines()
            self.tableFines.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tableFines.insertRow(row_num)
                for col_num, cell_data in enumerate(row_data):
                    self.tableFines.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        def refresh_fines_logic(self):
            database.refresh_fines()
            self.load_fines()
            QMessageBox.information(self.MainWindow, "Info", "Fines Refreshed!")

        def load_catalog(self):
            data = database.get_all_books()
            self.tableCatalog.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tableCatalog.insertRow(row_num)
                for col_num, cell_data in enumerate(row_data):
                    self.tableCatalog.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

        def load_catalog_mini(self):
            data = database.get_all_books()
            self.tableBooksMini.setRowCount(0)
            for row_num, row_data in enumerate(data):
                self.tableBooksMini.insertRow(row_num)
                for col_num, cell_data in enumerate(row_data):
                    self.tableBooksMini.setItem(row_num, col_num, QTableWidgetItem(str(cell_data)))

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    window.ui = ui
    return window

