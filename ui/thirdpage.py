
def third(role_type):
    from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
    from PySide6.QtGui import (QCursor)
    from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                                   QLabel, QPushButton, QLineEdit, QSpacerItem, 
                                   QSizePolicy, QMessageBox)
    import database

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            self.MainWindow = MainWindow
            self.current_role = role_type

            if not self.MainWindow.objectName():
                self.MainWindow.setObjectName(u"MainWindow")

            self.MainWindow.resize(600, 500)
            self.MainWindow.setStyleSheet(u"QMainWindow { background-color: #f4f6f9; }")

            self.centralwidget = QWidget(self.MainWindow)
            self.verticalLayout = QVBoxLayout(self.centralwidget)
            self.verticalLayout.setSpacing(15)
            self.verticalLayout.setContentsMargins(100, 50, 100, 50)

            self.titleLabel = QLabel(self.centralwidget)
            self.titleLabel.setAlignment(Qt.AlignCenter)
            self.titleLabel.setText(f"{self.current_role.capitalize()} Login")
            self.titleLabel.setStyleSheet(u"color: #2c3e50; font-family: 'Segoe UI'; font-size: 28px; font-weight: bold;")
            self.verticalLayout.addWidget(self.titleLabel)

            self.subtitleLabel = QLabel(self.centralwidget)
            self.subtitleLabel.setAlignment(Qt.AlignCenter)
            self.subtitleLabel.setText(u"Please enter your details to sign in.")
            self.subtitleLabel.setStyleSheet(u"color: #7f8c8d; font-family: 'Segoe UI'; font-size: 14px; margin-bottom: 20px;")
            self.verticalLayout.addWidget(self.subtitleLabel)

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
            label_style = u"color: #34495e; font-family: 'Segoe UI'; font-size: 14px; font-weight: 600;"

            self.emailLabel = QLabel("Email Address", self.centralwidget)
            self.emailLabel.setStyleSheet(label_style)
            self.verticalLayout.addWidget(self.emailLabel)

            self.emailText = QLineEdit(self.centralwidget)
            self.emailText.setPlaceholderText(u"name@example.com")
            self.emailText.setStyleSheet(input_style)
            self.verticalLayout.addWidget(self.emailText)

            self.verticalLayout.addSpacing(10)

            self.passwordLabel = QLabel("Password", self.centralwidget)
            self.passwordLabel.setStyleSheet(label_style)
            self.verticalLayout.addWidget(self.passwordLabel)

            self.passwordText = QLineEdit(self.centralwidget)
            self.passwordText.setPlaceholderText(u"Enter your password")
            self.passwordText.setEchoMode(QLineEdit.Password)
            self.passwordText.setStyleSheet(input_style)
            self.verticalLayout.addWidget(self.passwordText)

            self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.verticalLayout.addItem(self.verticalSpacer)

            self.loginButton = QPushButton("Log In", self.centralwidget)
            self.loginButton.setCursor(QCursor(Qt.PointingHandCursor))
            self.loginButton.setStyleSheet(u"""
            QPushButton {
                background-color: #3498db;
                border: none;
                border-radius: 10px;
                color: white;
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            """)
            self.verticalLayout.addWidget(self.loginButton)
            self.verticalSpacer2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.verticalLayout.addItem(self.verticalSpacer2)

            self.MainWindow.setCentralWidget(self.centralwidget)
            self.MainWindow.setWindowTitle(u"Login")
            QMetaObject.connectSlotsByName(self.MainWindow)

            self.loginButton.clicked.connect(self.validateLogin)
            self.new_window = None

        def validateLogin(self):
            email = self.emailText.text()
            password = self.passwordText.text()

            if not email or not password:
                QMessageBox.warning(self.MainWindow, "Error", "Please enter both email and password.")
                return

            if database.check_login(email, password):
                print(f"Login Successful as {self.current_role}")
                
                if self.current_role == "user":
                    from ui.user import user_dashboard
                    # Email is passed here
                    self.new_window = user_dashboard(email)
                
                elif self.current_role == "librarian":
                    from ui.librarian import librarian_dashboard
                    self.new_window = librarian_dashboard()
                
                self.new_window.show()
                self.MainWindow.close()
            else:
                QMessageBox.warning(self.MainWindow, "Login Failed", "Invalid email or password.")

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.ui = ui 
    return window
