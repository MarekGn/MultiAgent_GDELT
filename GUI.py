import sys
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel
from PyQt5 import QtGui
from Process import agent_start

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "Agent system GDELT"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 300

        self.start_year = None
        self.stop_year = None
        self.most_common_countries = None
        self.country_code = None
        self.root_codes = None

        self.create_ui_components()
        self.init_window()

    def init_window(self):
        self.setWindowIcon(QtGui.QIcon("res\\assets\\agh.jpg"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

    def create_ui_components(self):
        vbox = QVBoxLayout()

        self.create_start_year_hboxlayout()
        self.create_stop_year_hboxlayout()
        self.create_most_common_countries_hboxlayout()
        self.create_country_code_hboxlayout()
        self.create_root_codes_hboxlayout()

        self.create_buttons_start_stop_hboxlayout()

        vbox.addLayout(self.start_year_hboxlayout)
        vbox.addLayout(self.stop_year_hboxlayout)
        vbox.addLayout(self.most_common_countries_hboxlayout)
        vbox.addLayout(self.country_code_hboxlayout)
        vbox.addLayout(self.root_codes_hboxlayout)

        vbox.addLayout(self.start_stop_hboxlayout)


        self.setLayout(vbox)

    def create_buttons_start_stop_hboxlayout(self):
        self.start_stop_hboxlayout = QHBoxLayout()
        start_button = QPushButton("Start filtration", self)
        start_button.clicked.connect(self.on_press_start_button)
        start_button.setMinimumHeight(50)

        stop_button = QPushButton("Exit", self)
        stop_button.clicked.connect(self.on_press_stop_button)
        stop_button.setMinimumHeight(50)

        self.start_stop_hboxlayout.addWidget(start_button)
        self.start_stop_hboxlayout.addWidget(stop_button)


    def on_press_start_button(self):
        self.start_year = self.start_year_lineedit.text()
        self.stop_year = self.stop_year_lineedit.text()
        self.most_common_countries = self.most_common_countries_lineedit.text()
        self.country_code = self.country_code_lineedit.text()
        self.root_codes = self.root_codes_lineedit.text()

        self.check_quality_of_input()

        agent_start(self.start_year, self.stop_year, self.most_common_countries, self.country_code, self.root_codes)

    def on_press_stop_button(self):
        sys.exit()

    def create_start_year_hboxlayout(self):
        self.start_year_hboxlayout = QHBoxLayout()
        self.start_year_lineedit = QLineEdit(self)
        self.start_year_lineedit.setToolTip("<h2>This is the beginning year from which filtering will begin<h2>")
        self.start_year_label = QLabel("The beginning year (e.g. 1980)")
        self.start_year_label.setMinimumWidth(300)
        self.start_year_hboxlayout.addWidget(self.start_year_lineedit)
        self.start_year_hboxlayout.addWidget(self.start_year_label)

    def create_stop_year_hboxlayout(self):
        self.stop_year_hboxlayout = QHBoxLayout()
        self.stop_year_lineedit = QLineEdit(self)
        self.stop_year_lineedit.setToolTip("<h2>This is the final year in which filtering ends<h2>")
        self.stop_year_label = QLabel("The end year (e.g. 1981)")
        self.stop_year_label.setMinimumWidth(300)
        self.stop_year_hboxlayout.addWidget(self.stop_year_lineedit)
        self.stop_year_hboxlayout.addWidget(self.stop_year_label)

    def create_most_common_countries_hboxlayout(self):
        self.most_common_countries_hboxlayout = QHBoxLayout()
        self.most_common_countries_lineedit = QLineEdit(self)
        self.most_common_countries_lineedit.setToolTip("<h2>This is the number of countries considered in the displayed final results<h2>")
        self.most_common_countries_label = QLabel("The amount of countries in final results (e.g. 20)")
        self.most_common_countries_label.setMinimumWidth(300)
        self.most_common_countries_hboxlayout.addWidget(self.most_common_countries_lineedit)
        self.most_common_countries_hboxlayout.addWidget(self.most_common_countries_label)

    def create_country_code_hboxlayout(self):
        self.country_code_hboxlayout = QHBoxLayout()
        self.country_code_lineedit = QLineEdit(self)
        self.country_code_lineedit.setToolTip("<h2>This is the country against which the events are considered<h2>")
        self.country_code_label = QLabel("Considered country (e.g. POL)")
        self.country_code_label.setMinimumWidth(300)
        self.country_code_hboxlayout.addWidget(self.country_code_lineedit)
        self.country_code_hboxlayout.addWidget(self.country_code_label)

    def create_root_codes_hboxlayout(self):
        self.root_codes_hboxlayout = QHBoxLayout()
        self.root_codes_lineedit = QLineEdit(self)
        self.root_codes_lineedit.setToolTip("<h2>These are codes of events for which filtration will take place<h2>")
        self.root_codes_label = QLabel("Considered CAMEO codes for which filtration will take place (e.g. 04, 05, 19)")
        self.root_codes_label.setMinimumWidth(300)
        self.root_codes_hboxlayout.addWidget(self.root_codes_lineedit)
        self.root_codes_hboxlayout.addWidget(self.root_codes_label)

    def check_quality_of_input(self):
        self.start_year = int(self.start_year)
        self.stop_year = int(self.stop_year)
        self.most_common_countries = int(self.most_common_countries)
        self.country_code = str(self.country_code)
        self.country_code = self.country_code.upper()
        self.root_codes = str(self.root_codes)
        self.root_codes = self.root_codes.replace('.', ' ')
        self.root_codes = self.root_codes.replace(',', ' ')
        self.root_codes = self.root_codes.split()
