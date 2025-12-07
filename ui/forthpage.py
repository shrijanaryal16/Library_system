
def forth():
    from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
    from PySide6.QtGui import (QCursor)
    from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                   QLabel, QPushButton, QLineEdit, QSpacerItem, 
                                   QSizePolicy, QScrollArea, QFrame, QMessageBox)
    import database

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            self.MainWindow = MainWindow
            if not self.MainWindow.objectName():
                self.MainWindow.setObjectName(u"MainWindow")
            
            self.MainWindow.resize(600, 750)
            self.MainWindow.setStyleSheet(u"QMainWindow { background-color: #f4f6f9; }")

            self.centralwidget = QWidget(self.MainWindow)
            self.mainLayout = QVBoxLayout(self.centralwidget)
            self.mainLayout.setContentsMargins(0, 0, 0, 0)
            
            self.scrollArea = QScrollArea(self.centralwidget)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setFrameShape(QFrame.NoFrame)
            self.scrollArea.setStyleSheet(u"background-color: transparent;")
            
            self.scrollContent = QWidget()
            self.scrollLayout = QVBoxLayout(self.scrollContent)
            self.scrollLayout.setSpacing(15)
            self.scrollLayout.setContentsMargins(80, 40, 80, 40)

            self.titleLabel = QLabel(self.scrollContent)
            self.titleLabel.setAlignment(Qt.AlignCenter)
            self.titleLabel.setText(u"Create Account")
            self.titleLabel.setStyleSheet(u"color: #2c3e50; font-family: 'Segoe UI'; font-size: 28px; font-weight: bold;")
            self.scrollLayout.addWidget(self.titleLabel)

            self.subtitleLabel = QLabel(self.scrollContent)
            self.subtitleLabel.setAlignment(Qt.AlignCenter)
            self.subtitleLabel.setText(u"Fill in your details to register.")
            self.subtitleLabel.setStyleSheet(u"color: #7f8c8d; font-family: 'Segoe UI'; font-size: 14px; margin-bottom: 20px;")
            self.scrollLayout.addWidget(self.subtitleLabel)

            input_style = u"""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Segoe UI';
                font-size: 14px;
                background-color: #ffffff;
                color: #34495e;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            """
            label_style = u"color: #34495e; font-family: 'Segoe UI'; font-size: 14px; font-weight: 600; margin-top: 5px;"

            self.fname = QLabel("First Name", self.scrollContent)
            self.fname.setStyleSheet(label_style)
            self.scrollLayout.addWidget(self.fname)
            self.fnameText = QLineEdit(self.scrollContent)
            self.fnameText.setStyleSheet(input_style)
            self.scrollLayout.addWidget(self.fnameText)

            self.lname = QLabel("Last Name", self.scrollContent)
            self.lname.setStyleSheet(label_style)
            self.scrollLayout.addWidget(self.lname)
            self.lnameText = QLineEdit(self.scrollContent)
            self.lnameText.setStyleSheet(input_style)
            self.scrollLayout.addWidget(self.lnameText)

            self.eid = QLabel("Email Address", self.scrollContent)
            self.eid.setStyleSheet(label_style)
            self.scrollLayout.addWidget(self.eid)
            self.eidText = QLineEdit(self.scrollContent)
            self.eidText.setStyleSheet(input_style)
            self.scrollLayout.addWidget(self.eidText)

            self.zid = QLabel("Zip Code", self.scrollContent)
            self.zid.setStyleSheet(label_style)
            self.scrollLayout.addWidget(self.zid)
            self.zidText = QLineEdit(self.scrollContent)
            self.zidText.setStyleSheet(input_style)
            self.scrollLayout.addWidget(self.zidText)

            self.cpassword = QLabel("Create Password", self.scrollContent)
            self.cpassword.setStyleSheet(label_style)
            self.scrollLayout.addWidget(self.cpassword)
            self.cpasswordtext = QLineEdit(self.scrollContent)
            self.cpasswordtext.setEchoMode(QLineEdit.Password)
            self.cpasswordtext.setStyleSheet(input_style)
            self.scrollLayout.addWidget(self.cpasswordtext)

            self.rpassword = QLabel("Confirm Password", self.scrollContent)
            self.rpassword.setStyleSheet(label_style)
            self.scrollLayout.addWidget(self.rpassword)
            self.rpasswordText = QLineEdit(self.scrollContent)
            self.rpasswordText.setEchoMode(QLineEdit.Password)
            self.rpasswordText.setStyleSheet(input_style)
            self.scrollLayout.addWidget(self.rpasswordText)

            self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.scrollLayout.addItem(self.verticalSpacer)

            self.caccountButton = QPushButton("Create Account", self.scrollContent)
            self.caccountButton.setCursor(QCursor(Qt.PointingHandCursor))
            self.caccountButton.setStyleSheet(u"""
            QPushButton {
                background-color: #27ae60;
                border: none;
                border-radius: 10px;
                color: white;
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            """)
            self.scrollLayout.addWidget(self.caccountButton)

            self.scrollArea.setWidget(self.scrollContent)
            self.mainLayout.addWidget(self.scrollArea)
            self.MainWindow.setCentralWidget(self.centralwidget)
            self.MainWindow.setWindowTitle(u"Registration")
            QMetaObject.connectSlotsByName(self.MainWindow)

            self.caccountButton.clicked.connect(self.register)
            self.new_window = None

        def register(self):
            fname = self.fnameText.text()
            lname = self.lnameText.text()
            email = self.eidText.text()
            zip_c = self.zidText.text()
            pass1 = self.cpasswordtext.text()
            pass2 = self.rpasswordText.text()

            if not fname or not lname or not email or not zip_c or not pass1:
                QMessageBox.warning(self.MainWindow, "Error", "Please fill in all fields.")
                return

            if pass1 != pass2:
                QMessageBox.warning(self.MainWindow, "Error", "Passwords do not match!")
                return

            result = database.insert_student(fname, lname, email, zip_c, pass1)

            if result == "Success":
                QMessageBox.information(self.MainWindow, "Success", "Account created successfully!")
                self.goToLogin()
            else:
                QMessageBox.critical(self.MainWindow, "Database Error", result)

        def goToLogin(self):
            from ui.thirdpage import third
            # New account = User role by default
            self.new_window = third("user") 
            self.new_window.show()
            self.MainWindow.close()

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.ui = ui 
    return window

