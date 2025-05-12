import sys
import time
import os
import winreg
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont

from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
                             QFormLayout, QComboBox, QCheckBox, QPushButton, QSpinBox,QLineEdit, QColorDialog,
                             QGroupBox, QFontComboBox, QHBoxLayout)


from PyQt5.QtCore import QTimer, Qt, QPoint, QSettings, QStandardPaths, QSize
import webbrowser



APP_NAME = "WidgetHora"
APP_VERSION = "1.0"
APP_AUTHOR = "Nkounga Exauce"


def is_dark_theme():
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return value == 0
    except:
        return False


def add_to_startup(enable):
    startup_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.ApplicationsLocation),
                                "Startup", f"{APP_NAME}.lnk")
    app_path = os.path.abspath(sys.argv[0])
    try:
        if enable:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(startup_path)
            shortcut.Targetpath = app_path
            shortcut.WorkingDirectory = os.path.dirname(app_path)
            shortcut.save()
        else:
            if os.path.exists(startup_path):
                os.remove(startup_path)
        return True
    except Exception as e:
        print(f"Erreur démarrage : {e}")
        return False


class SettingsPanel(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = QSettings(APP_AUTHOR, APP_NAME)
        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        format_group = QGroupBox("Format d'affichage")
        format_layout = QFormLayout()

        self.time_format = QComboBox()
        self.time_format.addItems(["HH:MM:SS", "HH:MM", "hh:mm:ss AM/PM", "hh:mm AM/PM"])
        format_layout.addRow("Format de l'heure:", self.time_format)

        self.date_format = QComboBox()
        self.date_format.addItems(["Jour DD Mois AAAA", "DD/MM/AAAA", "MM/DD/AAAA", "AAAA-MM-DD"])
        format_layout.addRow("Format de la date:", self.date_format)

        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        appear_group = QGroupBox("Apparence")
        appear_layout = QFormLayout()

        self.font_combo_time = QFontComboBox()
        appear_layout.addRow("Police (heure):", self.font_combo_time)

        self.font_combo_date = QFontComboBox()
        appear_layout.addRow("Police (date):", self.font_combo_date)

        self.font_size_time = QSpinBox()
        self.font_size_time.setRange(12, 72)
        appear_layout.addRow("Taille police (heure):", self.font_size_time)

        self.font_size_date = QSpinBox()
        self.font_size_date.setRange(8, 36)
        appear_layout.addRow("Taille police (date):", self.font_size_date)

        self.spacing = QSpinBox()
        self.spacing.setRange(0, 100)
        appear_layout.addRow("Espacement (px):", self.spacing)

        self.show_time = QCheckBox("Afficher l'heure")
        self.show_date = QCheckBox("Afficher la date")
        appear_layout.addRow(self.show_time)
        appear_layout.addRow(self.show_date)

        appear_group.setLayout(appear_layout)
        layout.addWidget(appear_group)

        option_group = QGroupBox("Options")
        option_layout = QVBoxLayout()

        self.start_with_windows = QCheckBox("Lancer au démarrage")
        self.enable_drag = QCheckBox("Autoriser le déplacement")
        option_layout.addWidget(self.start_with_windows)
        option_layout.addWidget(self.enable_drag)
        self.enable_drag.stateChanged.connect(self.toggle_drag)

        option_group.setLayout(option_layout)
        layout.addWidget(option_group)

        self.apply_button = QPushButton("Appliquer")
        self.apply_button.clicked.connect(self.apply_settings)

        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_settings)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

        self.color_time = QLineEdit()
        self.color_time.setPlaceholderText("Cliquez pour choisir")
        self.color_time.setReadOnly(True)
        self.color_time.mousePressEvent = self.choose_color_time
        appear_layout.addRow("Couleur (heure):", self.color_time)

        self.color_date = QLineEdit()
        self.color_date.setPlaceholderText("Cliquez pour choisir")
        self.color_date.setReadOnly(True)
        self.color_date.mousePressEvent = self.choose_color_date
        appear_layout.addRow("Couleur (date):", self.color_date)

    def choose_color_time(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_time.setText(color.name())

    def choose_color_date(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_date.setText(color.name())

    def load_settings(self):
        self.time_format.setCurrentText(self.settings.value("timeFormat", "HH:MM:SS"))
        self.date_format.setCurrentText(self.settings.value("dateFormat", "Jour DD Mois AAAA"))

        self.font_combo_time.setCurrentFont(QFont(self.settings.value("fontFamilyTime", "Arial")))
        self.font_combo_date.setCurrentFont(QFont(self.settings.value("fontFamilyDate", "Arial")))

        self.font_size_time.setValue(int(self.settings.value("fontSizeTime", 53)))
        self.font_size_date.setValue(int(self.settings.value("fontSizeDate", 18)))
        self.spacing.setValue(int(self.settings.value("spacing", 0)))
        self.show_time.setChecked(self.settings.value("showTime", True, type=bool))
        self.show_date.setChecked(self.settings.value("showDate", True, type=bool))
        self.start_with_windows.setChecked(self.settings.value("startWithWindows", False, type=bool))
        self.enable_drag.setChecked(self.settings.value("enableDrag", False, type=bool))

        self.color_time.setText(self.settings.value("colorTime", "#FFFFFF"))
        self.color_date.setText(self.settings.value("colorDate", "#FFFFFF"))

    def apply_settings(self):
        self.parent.apply_settings(
            time_format=self.time_format.currentText(),
            date_format=self.date_format.currentText(),
            font_family_time=self.font_combo_time.currentFont().family(),
            font_family_date=self.font_combo_date.currentFont().family(),
            font_size_time=self.font_size_time.value(),
            font_size_date=self.font_size_date.value(),
            spacing=self.spacing.value(),
            show_time=self.show_time.isChecked(),
            show_date=self.show_date.isChecked(),
            enable_drag=self.enable_drag.isChecked(),
            color_time=self.color_time.text(),
            color_date=self.color_date.text()
        )
        self.enable_drag.setChecked(False)  # Décocher après l'application

    def toggle_drag(self, state):
        is_enabled = bool(state)
        self.parent.settings.setValue("enableDrag", is_enabled)
        self.parent.update_drag_visual(is_enabled)

    def save_settings(self):
        self.settings.setValue("timeFormat", self.time_format.currentText())
        self.settings.setValue("dateFormat", self.date_format.currentText())

        self.settings.setValue("fontFamilyTime", self.font_combo_time.currentFont().family())
        self.settings.setValue("fontFamilyDate", self.font_combo_date.currentFont().family())

        self.settings.setValue("fontSizeTime", self.font_size_time.value())
        self.settings.setValue("fontSizeDate", self.font_size_date.value())
        self.settings.setValue("spacing", self.spacing.value())
        self.settings.setValue("showTime", self.show_time.isChecked())
        self.settings.setValue("showDate", self.show_date.isChecked())
        self.settings.setValue("startWithWindows", self.start_with_windows.isChecked())
        self.settings.setValue("enableDrag", self.enable_drag.isChecked())

        add_to_startup(self.start_with_windows.isChecked())

        self.apply_settings()
        #QMessageBox.information(self, "Paramètres", "Paramètres enregistrés.")
        self.parent.settings_window.hide()
        self.enable_drag.setChecked(False)

        self.settings.setValue("colorTime", self.color_time.text())
        self.settings.setValue("colorDate", self.color_date.text())


class SettingsWindow(QMainWindow):
    def __init__(self, parent_clock):
        super().__init__()

        self.setWindowTitle("Paramètres")
        self.setWindowIcon(QIcon("assets/images/widgetHora x64.png"))
        self.setGeometry(100, 100, 400, 400)

        self.panel = SettingsPanel(parent_clock)
        self.setCentralWidget(self.panel)

    def closeEvent(self, event):
        self.panel.enable_drag.setChecked(False)
        event.ignore()
        self.hide()


class ClockWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings(APP_AUTHOR, APP_NAME)

        self.setWindowTitle("Widget Horloge")


        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        central = QWidget()
        self.setCentralWidget(central)

        self.main_layout = QVBoxLayout(central)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)

        self.date_label = QLabel()
        self.date_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.date_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.apply_settings_from_saved()

        self.resize(300, 150)

        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        center_x = (screen_rect.width() - self.width()) // 2
        saved_y = self.settings.value("posY", 20, type=int)

        self.move(center_x, saved_y)

        self.dragging = False
        self.offset = QPoint()

        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.update_theme)
        self.theme_timer.start(5000)
        self.update_theme()

        self.settings_window = SettingsWindow(self)


    def update_drag_visual(self, is_enabled):
        target = self.centralWidget()
        if is_enabled:
            target.setStyleSheet("""
                border: 2px solid rgba(0, 170, 255, 0.5);
                border-radius: 15px;
                background-color: rgba(0, 170, 255, 0.05);
            """)
        else:
            target.setStyleSheet("")

    def update_time(self):
        time_format_map = {
            "HH:MM:SS": "%H:%M:%S",
            "HH:MM": "%H:%M",
            "hh:mm:ss AM/PM": "%I:%M:%S %p",
            "hh:mm AM/PM": "%I:%M %p"
        }
        date_format_map = {
            "Jour DD Mois AAAA": "%A %d %B %Y",
            "DD/MM/AAAA": "%d/%m/%Y",
            "MM/DD/AAAA": "%m/%d/%Y",
            "AAAA-MM-DD": "%Y-%m-%d"
        }

        time_format_key = self.settings.value("timeFormat", "HH:MM:SS")
        date_format_key = self.settings.value("dateFormat", "Jour DD Mois AAAA")

        current_time = time.strftime(time_format_map.get(time_format_key, "%H:%M:%S"))
        current_date = time.strftime(date_format_map.get(date_format_key, "%A %d %B %Y"))

        if self.settings.value("showTime", True, type=bool):
            self.time_label.setText(current_time)
            self.time_label.show()
        else:
            self.time_label.hide()

        if self.settings.value("showDate", True, type=bool):
            self.date_label.setText(current_date)
            self.date_label.show()
        else:
            self.date_label.hide()

    def update_theme(self):
        # Utiliser les couleurs sauvegardées dans les paramètres, peu importe le thème
        color_time = self.settings.value("colorTime", "#FFFFFF")
        color_date = self.settings.value("colorDate", "#FFFFFF")

        self.time_label.setStyleSheet(f"color: {color_time};")
        self.date_label.setStyleSheet(f"color: {color_date};")

    def apply_settings_from_saved(self):
        self.apply_settings(
            time_format=self.settings.value("timeFormat", "HH:MM:SS"),
            date_format=self.settings.value("dateFormat", "Jour DD Mois AAAA"),
            font_family_time=self.settings.value("fontFamilyTime", "Arial"),
            font_family_date=self.settings.value("fontFamilyDate", "Arial"),
            font_size_time=int(self.settings.value("fontSizeTime", 36)),
            font_size_date=int(self.settings.value("fontSizeDate", 18)),
            spacing=int(self.settings.value("spacing", 10)),
            show_time=self.settings.value("showTime", True, type=bool),
            show_date=self.settings.value("showDate", True, type=bool),
            enable_drag=self.settings.value("enableDrag", True, type=bool),
            color_time = self.settings.value("colorTime", "#FFFFFF"),
            color_date = self.settings.value("colorDate", "#FFFFFF")

        )

    def apply_settings(self, time_format, date_format, font_family_time, font_family_date,
                       font_size_time, font_size_date, spacing, show_time, show_date, enable_drag,
                       color_time="#FFFFFF", color_date="#FFFFFF"):
        self.settings.setValue("timeFormat", time_format)
        self.settings.setValue("dateFormat", date_format)
        self.settings.setValue("fontFamilyTime", font_family_time)
        self.settings.setValue("fontFamilyDate", font_family_date)
        self.settings.setValue("fontSizeTime", font_size_time)
        self.settings.setValue("fontSizeDate", font_size_date)
        self.settings.setValue("spacing", spacing)
        self.settings.setValue("showTime", show_time)
        self.settings.setValue("showDate", show_date)
        self.settings.setValue("colorTime", color_time)
        self.settings.setValue("colorDate", color_date)

        self.time_label.setFont(QFont(font_family_time, font_size_time, QFont.Bold))
        self.date_label.setFont(QFont(font_family_date, font_size_date))

        self.time_label.setStyleSheet(f"color: {color_time};")
        self.date_label.setStyleSheet(f"color: {color_date};")


        self.main_layout.setSpacing(spacing)

        self.update_time()
        self.update_drag_visual(enable_drag)

    def show_about_window(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.settings.value("enableDrag", True, type=bool):
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            self.move(self.mapToGlobal(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.settings.setValue("posX", self.pos().x())
            self.settings.setValue("posY", self.pos().y())

    def contextMenuEvent(self, event):
        from PyQt5.QtWidgets import QMenu, QAction
        menu = QMenu(self)

        options_action = QAction("Options", self)
        options_action.triggered.connect(self.toggle_settings_panel)
        menu.addAction(options_action)

        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about_window)
        menu.addAction(about_action)

        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)
        menu.addAction(exit_action)


        menu.exec_(event.globalPos())

    def toggle_settings_panel(self):
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def closeEvent(self, event):
        self.settings.setValue("posX", self.pos().x())
        self.settings.setValue("posY", self.pos().y())
        event.accept()




class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("À propos")
        self.setWindowIcon(QIcon("assets/images/widgetHora x64.png"))

        self.setFixedSize(300, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Logo de l'app
        logo_label = QLabel()
        pixmap = QPixmap("assets/images/widgetHora x64.png")
        pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Titre de l'app
        label_title = QLabel(f"{APP_NAME} v{APP_VERSION}")
        label_title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        label_title.setFont(font)

        # Auteur
        label_author = QLabel(f"Développé par {APP_AUTHOR}")
        label_author.setAlignment(Qt.AlignCenter)

        # Bouton GitHub
        btn_github = QPushButton("Voir sur GitHub")
        btn_github.clicked.connect(self.open_github)
        icon = QIcon("assets/svg/github_logo.svg")

        btn_github.setIcon(icon)
        btn_github.setIconSize(QSize(20, 20))

        btn_github.setStyleSheet("""
            QPushButton {
                background-color: #24292e;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 16px; 
            }
            QPushButton:hover {
                background-color: #333;
            }
            QPushButton:pressed {
                background-color: #000;
            }
        """)
        # Ajout des widgets au layout
        layout.addStretch()
        layout.addWidget(logo_label)
        layout.addWidget(label_title)
        layout.addWidget(label_author)
        layout.addStretch()
        layout.addWidget(btn_github)

        self.setLayout(layout)

    def open_github(self):
        webbrowser.open("https://github.com/Nkounga42")  # Mets ton vrai lien ici


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(APP_AUTHOR)

    widget = ClockWidget()
    widget.show()
    sys.exit(app.exec_())
