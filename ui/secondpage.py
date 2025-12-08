

def second(role_type):
    from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
    from PySide6.QtGui import (QCursor)
    from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                                   QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy)

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            self.MainWindow = MainWindow
            self.current_role = role_type

            if not self.MainWindow.objectName():
                self.MainWindow.setObjectName(u"MainWindow")
            
            self.MainWindow.resize(600, 400)
            self.MainWindow.setStyleSheet(u"QMainWindow { background-color: #f4f6f9; }")

            self.centralwidget = QWidget(self.MainWindow)
            self.verticalLayout = QVBoxLayout(self.centralwidget)
            self.verticalLayout.setSpacing(20)
            self.verticalLayout.setContentsMargins(50, 50, 50, 50)

            self.titleLabel = QLabel(self.centralwidget)
            self.titleLabel.setAlignment(Qt.AlignCenter)
            
            if self.current_role == "librarian":
                self.titleLabel.setText(u"Librarian Access")
            else:
                self.titleLabel.setText(u"User Access")
                
            self.titleLabel.setStyleSheet(u"color: #2c3e50; font-family: 'Segoe UI'; font-size: 28px; font-weight: bold;")
            self.verticalLayout.addWidget(self.titleLabel)

            self.subtitleLabel = QLabel(self.centralwidget)
            self.subtitleLabel.setAlignment(Qt.AlignCenter)
            self.subtitleLabel.setText(u"Please log in or create a new account.")
            self.subtitleLabel.setStyleSheet(u"color: #7f8c8d; font-family: 'Segoe UI'; font-size: 16px;")
            self.verticalLayout.addWidget(self.subtitleLabel)

            self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.verticalLayout.addItem(self.verticalSpacer)

            self.horizontalLayout = QHBoxLayout()
            self.horizontalLayout.setSpacing(40)

            button_style = u"""
            QPushButton {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 15px;
                color: #34495e;
                font-family: 'Segoe UI';
                font-size: 16px;
                font-weight: 600;
                padding: 15px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #3498db;
                color: white;
                border: 2px solid #3498db;
            }
            """

            self.login = QPushButton("Log In", self.centralwidget)
            self.login.setCursor(QCursor(Qt.PointingHandCursor))
            self.login.setStyleSheet(button_style)
            self.horizontalLayout.addWidget(self.login)

            self.createaccount = QPushButton("Create Account", self.centralwidget)
            self.createaccount.setCursor(QCursor(Qt.PointingHandCursor))
            self.createaccount.setStyleSheet(button_style)
            self.horizontalLayout.addWidget(self.createaccount)

            self.verticalLayout.addLayout(self.horizontalLayout)
            
            # --- GO BACK BUTTON ---
            self.btnBack = QPushButton("Go Back", self.centralwidget)
            self.btnBack.setCursor(QCursor(Qt.PointingHandCursor))
            self.btnBack.setStyleSheet("background-color: transparent; color: #7f8c8d; border: none; margin-top: 20px;")
            self.verticalLayout.addWidget(self.btnBack, alignment=Qt.AlignCenter)

            self.verticalSpacer2 = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.verticalLayout.addItem(self.verticalSpacer2)

            self.MainWindow.setCentralWidget(self.centralwidget)
            self.MainWindow.setWindowTitle(u"Access")
            QMetaObject.connectSlotsByName(self.MainWindow)

            self.login.clicked.connect(self.loginPage)
            self.createaccount.clicked.connect(self.createaccountPage)
            self.btnBack.clicked.connect(self.goBack)
            self.new_window = None

        def loginPage(self):
            from ui.thirdpage import third
            self.new_window = third(self.current_role)
            self.new_window.show()
            self.MainWindow.close()

        def createaccountPage(self):
            from ui.forthpage import forth
            # Pass role to registration so we create the correct account type
            self.new_window = forth(self.current_role) 
            self.new_window.show()
            self.MainWindow.close()

        def goBack(self):
            from ui.firstpage import first
            self.MainWindow.close()
            import sys, subprocess
            subprocess.Popen([sys.executable, 'main.py'])

    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.ui = ui
    return window

