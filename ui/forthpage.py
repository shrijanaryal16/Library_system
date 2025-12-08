
def forth(role_type): # Accepts role
    from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
    from PySide6.QtGui import (QCursor)
    from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                   QLabel, QPushButton, QLineEdit, QSpacerItem, 
                                   QSizePolicy, QScrollArea, QFrame, QMessageBox)
    import database
    import re

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            self.MainWindow = MainWindow
            self.current_role = role_type # Store role to save in DB

            if not self.MainWindow.objectName():
                self.MainWindow.setObjectName(u"MainWindow")
            
            self.MainWindow.resize(600, 800)
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
            self.titleLabel.setText(f"Create {self.current_role.capitalize()} Account")
            self.titleLabel.setStyleSheet(u"color: #2c3e50; font-family: 'Segoe UI'; font-size: 28px; font-weight: bold;")
            self.scrollLayout.addWidget(self.titleLabel)

            input_style = u"""
            QLineEdit { border: 2px solid #e0e0e0; border-radius: 10px; padding: 10px; font-size: 14px; background-color: white; }
            QLineEdit:focus { border: 2px solid #3498db; }
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
            self.eidText.setPlaceholderText("user@example.com")
            self.eidText.setStyleSheet(input_style)
            self.scrollLayout.addWidget(self.eidText)

            # Added Phone Field
            self.phone = QLabel("Phone Number", self.scrollContent)
            self.phone.setStyleSheet(label_style)
            self.scrollLayout.addWidget(self.phone)
            self.phoneText = QLineEdit(self.scrollContent)
            self.phoneText.setPlaceholderText("(123)456-7890")
            self.phoneText.setStyleSheet(input_style)
            self.scrollLayout.addWidget(self.phoneText)

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
            QPushButton { background-color: #27ae60; border: none; border-radius: 10px; color: white; font-size: 16px; font-weight: bold; padding: 15px; }
            QPushButton:hover { background-color: #2ecc71; }
            """)
            self.scrollLayout.addWidget(self.caccountButton)

            # Back Button
            self.btnBack = QPushButton("Go Back", self.scrollContent)
            self.btnBack.setCursor(QCursor(Qt.PointingHandCursor))
            self.btnBack.setStyleSheet("background-color: transparent; color: #7f8c8d; border: none; margin-top: 10px;")
            self.scrollLayout.addWidget(self.btnBack)

            self.scrollArea.setWidget(self.scrollContent)
            self.mainLayout.addWidget(self.scrollArea)
            self.MainWindow.setCentralWidget(self.centralwidget)
            self.MainWindow.setWindowTitle(u"Registration")
            QMetaObject.connectSlotsByName(self.MainWindow)

            self.caccountButton.clicked.connect(self.register)
            self.btnBack.clicked.connect(self.goBack)
            self.new_window = None

        def register(self):
            fname = self.fnameText.text()
            lname = self.lnameText.text()
            email = self.eidText.text()
            phone = self.phoneText.text()
            zip_c = self.zidText.text()
            pass1 = self.cpasswordtext.text()
            pass2 = self.rpasswordText.text()

            # Regex 
            # We are using a very simple logical way of doing regex
            # Although there are few libraries out there which can do better and more efficiently
            name_regex = r"^[a-zA-Z ]{2,}$"
            email_regex = r"^[a-zA-Z0-9-_.]+@[a-zA-Z-]+\.[a-zA-Z]{2,}$"
            # Adjusted phone regex for Python re compatibility
            phone_regex = r"^[(]{1}[0-9]{3}[)]{1}[0-9]{3}[-]{1}[0-9]{4}$"

            if not all([fname, lname, email, phone, zip_c, pass1]):
                QMessageBox.warning(self.MainWindow, "Error", "Please fill in all fields.")
                return

            # Validate
            if not re.match(name_regex, fname) or not re.match(name_regex, lname):
                QMessageBox.warning(self.MainWindow, "Format Error", "Names must be at least 2 letters.")
                return
            if not re.match(email_regex, email):
                QMessageBox.warning(self.MainWindow, "Format Error", "Invalid Email Format.")
                return
            if not re.match(phone_regex, phone):
                QMessageBox.warning(self.MainWindow, "Format Error", "Phone must be (xxx)xxx-xxxx")
                return

            if pass1 != pass2:
                QMessageBox.warning(self.MainWindow, "Error", "Passwords do not match!")
                return

            # Insert with ROLE and PHONE
            result = database.insert_student(fname, lname, email, zip_c, pass1, phone, self.current_role)

            if result == "Success":
                QMessageBox.information(self.MainWindow, "Success", "Account created successfully!")
                self.goToLogin()
            else:
                QMessageBox.critical(self.MainWindow, "Database Error", result)

        def goToLogin(self):
            from ui.thirdpage import third
            self.new_window = third(self.current_role)
            self.new_window.show()
            self.MainWindow.close()

        def goBack(self):
            from ui.secondpage import second
            self.new_window = second(self.current_role)
            self.new_window.show()
            self.MainWindow.close()

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.ui = ui 
    return window

