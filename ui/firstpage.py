
def first():
    from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt)
    from PySide6.QtGui import (QCursor)
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                   QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy)

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            self.MainWindow = MainWindow
            if not self.MainWindow.objectName():
                self.MainWindow.setObjectName(u"MainWindow")
            
            self.MainWindow.resize(900, 600)
            self.MainWindow.setStyleSheet(u"QMainWindow { background-color: #f4f6f9; }")

            self.centralwidget = QWidget(self.MainWindow)
            self.verticalLayout = QVBoxLayout(self.centralwidget)
            self.verticalLayout.setSpacing(20)
            self.verticalLayout.setContentsMargins(50, 50, 50, 50)

            self.titleLabel = QLabel(self.centralwidget)
            self.titleLabel.setAlignment(Qt.AlignCenter)
            self.titleLabel.setText(u"Library Management System")
            self.titleLabel.setStyleSheet(u"color: #2c3e50; font-family: 'Segoe UI'; font-size: 32px; font-weight: bold;")
            self.verticalLayout.addWidget(self.titleLabel)

            self.subtitleLabel = QLabel(self.centralwidget)
            self.subtitleLabel.setAlignment(Qt.AlignCenter)
            self.subtitleLabel.setText(u"Welcome! Let's get started.")
            self.subtitleLabel.setStyleSheet(u"color: #7f8c8d; font-family: 'Segoe UI'; font-size: 18px; margin-bottom: 20px;")
            self.verticalLayout.addWidget(self.subtitleLabel)

            self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
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
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #3498db;
                color: white;
                border: 2px solid #3498db;
            }
            """

            self.startLibrarian = QPushButton("Start as Librarian", self.centralwidget)
            self.startLibrarian.setCursor(QCursor(Qt.PointingHandCursor))
            self.startLibrarian.setStyleSheet(button_style)
            self.horizontalLayout.addWidget(self.startLibrarian)

            self.startUser = QPushButton("Start as User", self.centralwidget)
            self.startUser.setCursor(QCursor(Qt.PointingHandCursor))
            self.startUser.setStyleSheet(button_style)
            self.horizontalLayout.addWidget(self.startUser)

            self.verticalLayout.addLayout(self.horizontalLayout)
            self.verticalSpacer2 = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.verticalLayout.addItem(self.verticalSpacer2)

            self.MainWindow.setCentralWidget(self.centralwidget)
            self.MainWindow.setWindowTitle(u"Library System")
            QMetaObject.connectSlotsByName(self.MainWindow)

            # --- NAVIGATION ---
            self.startLibrarian.clicked.connect(self.openLibrarianPage)
            self.startUser.clicked.connect(self.openUserPage)

        def openLibrarianPage(self):
            from ui.secondpage import second
            # We pass "librarian" to the next page
            self.window = second("librarian")
            self.window.show()
            self.MainWindow.hide()

        def openUserPage(self):
            from ui.secondpage import second
            # We pass "user" to the next page
            self.window = second("user")
            self.window.show()
            self.MainWindow.hide()

    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # We must start the loop here since this is the entry point
    MainWindow.show()
    app.exec()

