from PyQt5 import QtWidgets, QtCore, uic
import serial
from PyQt5.QtMultimedia import QCameraInfo
import serial.tools.list_ports

class settings(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('parametrs_design.ui', self)
        self.setFixedSize(800, 600)
        self.setWindowTitle("Parametrlər")
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('assets/images/interface images/changeScreen.png');
                background-repeat: no-repeat;
                background-position: center;
            }
        """)

        # ComboBox setup for Arduino Ports
        self.arduinoPort = self.findChild(QtWidgets.QComboBox, 'arduinoPort')
        
        # ComboBox setup for Camera Index
        self.cameraIndex = self.findChild(QtWidgets.QComboBox, 'cameraIndex')

        # QTimer setup
        self.timer = QtCore.QTimer(self)

        # Ports and Cameras refreshing setup
        self.timer.timeout.connect(self.PopulateSerialPorts)
        self.timer.timeout.connect(self.PopulateCameras)
        self.timer.start(1000)

        # Populate the lists immediately upon loading the settings window
        self.PopulateSerialPorts()
        self.PopulateCameras()

    def PopulateSerialPorts(self):
        try:
            # Save current selection
            current_selection = self.arduinoPort.currentText()

            # Get available serial ports
            ports = serial.tools.list_ports.comports()
            self.arduinoPort.clear()  # Clear the ComboBox

            # Populate the ComboBox with available ports
            for port in ports:
                item_text = f"{port.device} - {port.description}"
                self.arduinoPort.addItem(item_text)

            # Restore the previous selection if available
            if current_selection:
                index = self.arduinoPort.findText(current_selection)
                if index != -1:
                    self.arduinoPort.setCurrentIndex(index)
                else:
                    # If the current selection is not found, select the first item
                    self.arduinoPort.setCurrentIndex(0)
            else:
                # If there was no previous selection, select the first item by default
                self.arduinoPort.setCurrentIndex(0)

        except Exception as e:
            print(f"Error populating serial ports: {e}")

    def PopulateCameras(self):
        try:
            # Save current selection
            current_selection = self.cameraIndex.currentText()

            # Get available cameras
            cameras = QCameraInfo.availableCameras()
            self.cameraIndex.clear()  # Clear the ComboBox

            # Populate the ComboBox with available cameras
            for index, camera in enumerate(cameras):
                item_text = f"{index} - {camera.description()}"
                self.cameraIndex.addItem(item_text)

            # Restore the previous selection if available
            if current_selection:
                index = self.cameraIndex.findText(current_selection)
                if index != -1:
                    self.cameraIndex.setCurrentIndex(index)
                else:
                    # If the current selection is not found, select the first item
                    self.cameraIndex.setCurrentIndex(0)
            else:
                # If there was no previous selection, select the first item by default
                self.cameraIndex.setCurrentIndex(0)

        except Exception as e:
            print(f"Error populating cameras: {e}")

    def GetSelectedPorts(self):
        try:
            arduino_port = self.arduinoPort.currentText().split(' - ')[0]  # Split and take the first part
            if arduino_port:
                print(f"Selected port: {arduino_port}")
                return arduino_port
            else:
                print("No port selected or invalid format")
                return None
        except Exception as e:
            print(f"Error getting selected port: {e}")
            return None

    def GetSelectedCamera(self):
        try:
            camera_index = int(self.cameraIndex.currentText().split(' - ')[0])
            print(f"Selected camera index: {camera_index}")
            return camera_index
        except Exception as e:
            print(f"Error getting selected camera: {e}")
            return None
