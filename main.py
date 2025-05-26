import os
import sys
import subprocess
import json
import winshell
from win32com.client import Dispatch
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QCheckBox, 
                             QPushButton, QWidget, QLabel, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import Qt, QTimer

class AppLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Startup App Launcher")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # App paths from the app_config file
        config_path = os.path.join(os.path.dirname(__file__), 'app-config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        self.apps = config['apps']
        
        self.init_ui()
        self.init_timer()
        
    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select apps to launch:")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(title)
        
        # Create checkboxes for each app
        self.checkboxes = []
        for app in self.apps:
            cb = QCheckBox(app["name"])
            cb.setChecked(app["enabled"])
            cb.stateChanged.connect(self.reset_timer)
            self.checkboxes.append(cb)
            main_layout.addWidget(cb)
        
        # Selection buttons
        selection_btn_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all)
        selection_btn_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all)
        selection_btn_layout.addWidget(deselect_all_btn)
        
        main_layout.addLayout(selection_btn_layout)
        
        # Timer display
        self.timer_label = QLabel("Launching in 20 seconds...")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 12px;")
        main_layout.addWidget(self.timer_label)
        
        # Action buttons
        buttons_layout = QGridLayout()
        
        # Cancel Timer button
        self.cancel_timer_btn = QPushButton("Cancel Timer")
        self.cancel_timer_btn.clicked.connect(self.cancel_timer)
        buttons_layout.addWidget(self.cancel_timer_btn, 0, 0)
        
        # Launch Now button
        launch_btn = QPushButton("Launch Now")
        launch_btn.clicked.connect(self.launch_apps)
        buttons_layout.addWidget(launch_btn, 0, 1)
        
        # Cancel button
        cancel_btn = QPushButton("Close")
        cancel_btn.clicked.connect(self.close)
        buttons_layout.addWidget(cancel_btn, 0, 2)
        
        main_layout.addLayout(buttons_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Set window size and center it
        self.resize(350, 300)
        self.center_window()
        
    def center_window(self):
        frame_geo = self.frameGeometry()
        screen_center = QApplication.desktop().screen().rect().center()
        frame_geo.moveCenter(screen_center)
        self.move(frame_geo.topLeft())
        
    def init_timer(self):
        self.countdown = 20  # 20 seconds
        self.timer_active = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second
        
    def reset_timer(self):
        if self.timer_active:
            self.countdown = 20
            self.timer_label.setText(f"Launching in {self.countdown} seconds...")
        
    def update_timer(self):
        if not self.timer_active:
            return
            
        self.countdown -= 1
        self.timer_label.setText(f"Launching in {self.countdown} seconds...")
        
        if self.countdown <= 0:
            self.timer.stop()
            self.launch_apps()
            
    def cancel_timer(self):
        self.timer_active = False
        self.timer.stop()
        self.timer_label.setText("Timer canceled")
        self.cancel_timer_btn.setEnabled(False)
        
    def select_all(self):
        self.cancel_timer()
        for cb in self.checkboxes:
            cb.setChecked(True)
        self.reset_timer()
        
    def deselect_all(self):
        self.cancel_timer()
        for cb in self.checkboxes:
            cb.setChecked(False)
        self.reset_timer()
            
    def launch_apps(self):
        self.timer.stop()
        for i, app in enumerate(self.apps):
            if self.checkboxes[i].isChecked():
                try:
                    if app["args"]:
                        subprocess.Popen([app["path"]] + app["args"])
                    else:
                        subprocess.Popen(app["path"])
                except Exception as e:
                    print(f"Error launching {app['name']}: {e}")
        
        self.close()

def add_to_startup_bat():
    # Get the path to the current script
    script_path = os.path.abspath(__file__)
    
    # Create a batch file to run the script
    batch_content = f'@echo off\npython "{script_path}"'
    batch_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'startup_apps_launcher.bat')
    
    with open(batch_path, 'w') as f:
        f.write(batch_content)

def add_to_startup():
    script_path = os.path.abspath(__file__)
    startup_folder = winshell.startup()
    shortcut_path = os.path.join(startup_folder, "AppLauncher.lnk")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = sys.executable  # Path to pythonw.exe
    shortcut.Arguments = f'"{script_path}"'
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.WindowStyle = 7  # 1 = Minimized, 7 = Minimized (no window)
    shortcut.save()


if __name__ == "__main__":
    # Check if we should add to startup (run with --setup parameter)
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        add_to_startup()
        print("Added to Windows startup successfully!")
    else:
        app = QApplication(sys.argv)
        launcher = AppLauncher()
        launcher.show()
        sys.exit(app.exec_())