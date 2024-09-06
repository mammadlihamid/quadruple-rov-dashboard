from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QPainter
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtMultimedia import QCamera, QCameraInfo
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from datetime import datetime
import pygame
import time
import serial 
import numpy as np
import pyautogui
import cv2
import serial.tools.list_ports
from settingsScreen import settings

startedTimer = False
lightRelayCondition = False
longLightRelayCondition = False

arduinoPort = 'COM8'
cameraIndex = 1


class main(QtWidgets.QMainWindow):
    def __init__(self):
        super(main, self).__init__()

        uic.loadUi('interfaceDesign.ui', self)
        self.serialPort = None  
        self.isRecording = False
        self.out = None
        self.screenSize = pyautogui.size()

        # self.settingsWindow = settings()

        # Background Image
        self.backgroundImage = QPixmap('assets\\images\\interface images\\QuadRuple.png')

        # Log setup
        self.outputLabel = self.findChild(QtWidgets.QLabel, 'outputLabel')
        self.outputLabel.setStyleSheet(" color: white; font-size: 11pt; ")
        self.outputLabel.setWordWrap(True)

        # self.serialPortInput = self.findChild(QtWidgets.QLineEdit, 'serialPort')
        # self.serialPortOkButton = self.findChild(QtWidgets.QPushButton, 'serialPortButton')
        
        # if self.serialPortOkButton.isChecked():
        #     arduinoPort = self.getSerialPort

        # QTimer setup
        self.timer = QTimer(self)
        self.joystickTimer = QTimer(self)


        try:
            self.serialPort = serial.Serial(arduinoPort, 9600, timeout=1)
            if self.serialPort.is_open:
                self.UpdateOutput(f"Connected to {self.serialPort.port}")
                print(f"Connected to {self.serialPort.port}")
            else:
                self.UpdateOutput("Failed to open COM20")
                print("Failed to open COM20")
                self.serialPort = None  # Explicitly set to None if the port isn't open
        except serial.SerialException as e:
            self.UpdateOutput(f"SerialException: {e}")
            print(f"SerialException: {e}")
            self.serialPort = None  # Ensure self.serialPort is None on failure
        except Exception as e:
            self.UpdateOutput(f"Exception: {e}")
            print(f"Exception: {e}")
            self.serialPort = None  # Ensure self.serialPort is None on failure

        # Main part setup
        self.timerLabel = self.findChild(QtWidgets.QLabel, 'timerLabel')
        self.StartTorpedoButton = self.findChild(QtWidgets.QPushButton, 'start_torpedo')
        self.StopTorpedoButton = self.findChild(QtWidgets.QPushButton, 'stop_torpedo')
        self.StartGearButton = self.findChild(QtWidgets.QPushButton, 'start_gear')
        self.StopGearButton = self.findChild(QtWidgets.QPushButton, 'stop_gear')
        self.quadrupleText = self.findChild(QtWidgets.QLabel, 'quadruple_text')
        self.cameraPlaceholder = self.findChild(QtWidgets.QWidget, 'cameraPlaceholder')
        self.turboGearButton = self.findChild(QtWidgets.QPushButton, 'turbo_gear')
        self.turboTorpedoButton = self.findChild(QtWidgets.QPushButton, 'turbo_torpedo')
        self.lightRelayButton = self.findChild(QtWidgets.QPushButton, 'light_relay')
        self.longLightRelayButton = self.findChild(QtWidgets.QPushButton, 'long_light_relay')

        # Change Settings Screen setup
        # self.changeScreenButton = self.findChild(QtWidgets.QPushButton, 'changeScreen')
        # self.changeScreenButton.clicked.connect(self.SettingsScreenChange)

        #Joystick settings
        pygame.init()
        pygame.joystick.init()

        # Ensure joystick is connected
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Controller: {self.joystick.get_name()} connected")
        else:
            print("No joystick connected")
            self.joystick = None

        # self.checkJoystick()
        self.joystickTimer.timeout.connect(self.checkJoystick)
        self.joystickTimer.start(100) 


        # Font setup
        fontId = QFontDatabase.addApplicationFont("assets\\fonts\\tt-supermolot-neue-bold.ttf")
        if fontId == -1:
            print("Failed to load font")
            self.UpdateOutput("Fontu yükləmək alınmadı")
        else:
            fontFamilies = QFontDatabase.applicationFontFamilies(fontId)
            if fontFamilies:
                font = QFont(fontFamilies[0], 30)
            else:
                print("Font tapılmadı")
                font = QFont("Arial", 60)

        # Camera setup
        self.viewfinder = QCameraViewfinder(self.cameraPlaceholder)
        self.viewfinder.setGeometry(self.cameraPlaceholder.geometry())  # Adjust size and position to fill the widget
        self.viewfinder.show()


        # selected_camera_index = self.settingsWindow.GetSelectedCamera()

        # Correcting part: attaching QCamera to the viewfinder
        available_cameras = QCameraInfo.availableCameras()
        if available_cameras:
            try:
                self.camera = QCamera(available_cameras[cameraIndex])
                self.camera.setViewfinder(self.viewfinder)
                self.camera.start()
            except IndexError:
                self.UpdateOutput("Invalid camera index selected")
        else:
            self.UpdateOutput("No camera available")

        # Timer setup
        self.timerLabel = self.findChild(QtWidgets.QLabel, 'timerLabel')
        self.timerLabel.setStyleSheet("font-size: 22pt; font-weight: bold; color: white;")
        self.timerLabel.setText("00:00:00")
        self.timerLabel.setWordWrap(True)

        self.timer.timeout.connect(self.UpdateTimer)
        self.startTime = time.time()

        # quadrupleText setup
        self.quadrupleText.setFont(font)

        # Torpedo control
        self.turboTorpedoButton.clicked.connect(self.TurboTorpedo)
        self.StartTorpedoButton.clicked.connect(self.StartTorpedo)
        self.StopTorpedoButton.clicked.connect(self.StopTorpedo)
        self.StartGearButton.clicked.connect(self.StartGear)
        self.StopGearButton.clicked.connect(self.StopGear)
        self.turboGearButton.clicked.connect(self.TurboGear)
        self.lightRelayButton.clicked.connect(self.ToggleLightRelay)
        self.longLightRelayButton.clicked.connect(self.ToggleLongLightRelay)
        
        if(startedTimer == False):
            self.StopTimer()

    def checkJoystick(self):
        print("checkJoystick function called")
        if self.joystick is None:
            print("No joystick connected")
            return

        for event in pygame.event.get():
            print(f"Event detected: {event}")
            if event.type == pygame.JOYBUTTONDOWN:
                print("Button pressed event detected")
                # Check specifically for button 8 and 9
                if self.joystick.get_button(8):
                    self.StopGear()
                    self.StopTorpedo()
                if self.joystick.get_button(9):
                    self.StartTorpedo()
                    # time.sleep(1000)
                    self.StartGear()



        


    # def getSerialPort(self):
    #     arduinoPort = self.serialPortInput.text()
    #     return arduinoPort
    


    # def UseSelectedPorts(self):
    #     selected_port = self.settingsWindow.GetSelectedPorts()
    # #     return selected_port


    # # Settings Screen settings
    # def SettingsScreenChange(self):
    #     self.settingsWindow = settings()
    #     self.settingsWindow.show()
    
    # # Change camera settings
    # @pyqtSlot(QtGui.QImage)
    # def SetImage(self, image):
    #     pixmap = QtGui.QPixmap.fromImage(image)
    #     scaled_pixmap = pixmap.scaled(self.cameraPlaceholder.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
    #     self.imageLabel.setPixmap(pixmap)
    #     self.imageLabel.setScaledContents(True)

    # Recording settings
    def StartRecording(self):
        if not self.isRecording:
            self.isRecording = True
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            filename = self.GenerateFilename(extension='mp4')
            self.out = cv2.VideoWriter(filename, fourcc, 10.0, (self.screenSize.width, self.screenSize.height))
            if not self.out.isOpened():
                self.UpdateOutput("Failed to start recording")
                self.isRecording = False
                return
            self.timer.timeout.connect(self.RecordFrame)
            self.timer.start(100)
            self.UpdateOutput("Ekran qeydiyyatı və timer başladı")

    def StopRecording(self):
        if self.isRecording:
            self.timer.stop()
            self.isRecording = False
            if self.out is not None:
                self.out.release()
            self.UpdateOutput("Ekran qeydiyyatı və timer dayandı")

    def SaveRecording(self):
        self.StopRecording()
        self.UpdateOutput("Ekran qeydiyyatı yadda saxlanıldı")

    def RecordFrame(self):
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.out.write(frame)

    def TakeScreenshot(self):
        screenshot = pyautogui.screenshot()
        filename = self.GenerateFilename(extension='png')
        screenshot.save(filename)
        self.UpdateOutput("Ekran şəkli çəkildi")

    def GenerateFilename(self, extension):
        now = datetime.now()
        return f"C://Users//User//Desktop//{now.strftime('%Y-%m-%d_%H-%M-%S')}.{extension}"

    # Log settings
    def UpdateOutput(self, message):
        self.outputLabel.setText(message)
        QtWidgets.QApplication.processEvents()
        self.outputLabel.setStyleSheet("font-size: 12pt; font-weight: bold; color: white;")

    # Background settings
    def changeBackground(self, imagePath):
        self.backgroundImage = QPixmap(imagePath)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.backgroundImage.isNull():
            painter.drawPixmap(self.rect(), self.backgroundImage)
        else:
            self.UpdateOutput("Arxa fon şəkli yüklənmədi")

    # Timer settings
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_S:
            self.StartTimer()
            self.StartRecording()
        elif event.key() == QtCore.Qt.Key_F:
            self.RestartTimer()
            self.SaveRecording()
        elif event.key() == QtCore.Qt.Key_D:
            self.StopTimer()
            self.StopRecording()
        elif event.key() == QtCore.Qt.Key_P:
            self.TakeScreenshot()

    
    def StartTimer(self):
        self.startTime = time.time()
        self.timer.start(100)
        startedTimer = True

    def StopTimer(self):
        self.timer.stop()
        self.UpdateTimer() 

    def RestartTimer(self):
        self.StartTimer()
        self.StopTimer()
        self.UpdateOutput("Zamanlayıcı yeniləndi")
        
    def UpdateTimer(self):
        elapsed_time = int(time.time() - self.startTime)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.timerLabel.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    # Torpedo control
    def StopTorpedo(self):
        try:
            self.serialPort.write(b'0')
            self.UpdateOutput("Atəş dayandı")
        except Exception as e:
            self.UpdateOutput("Atəşi dayandırmaq mümkün olmadı")
        finally: 
            print("0")
        
    def StartTorpedo(self):
        if self.serialPort and self.serialPort.is_open:
            try:
                self.serialPort.write(b'1')
                self.UpdateOutput("Atəş başladı")
                print("Sent '1' to serial port")
            except Exception as e:
                self.UpdateOutput(f"Error writing to serial port: {str(e)}")
                print(f"Error writing to serial port: {str(e)}")
        else:
            self.UpdateOutput("Serial port is not open")
            print("Serial port is not open")


    def TurboTorpedo(self):
        try:
            self.serialPort.write(b'2')
            self.UpdateOutput("Motorun turbo modu qoşuldu")
        except Exception as e:
            self.update("Motorun turbo modunu qoşmaq mümkün olmadı")
        finally:
            print("2")

    def StopGear(self):
        try:
            self.serialPort.write(b'3')
            self.UpdateOutput("Çarx dayandı")
        except Exception as e:
            self.UpdateOutput("Çarxı dayandırmaq mümkün olmadı")
        finally:
            print("3")

    def StartGear(self):
        try:
            self.serialPort.write(b'4')
            self.UpdateOutput("Çarx fırlanır")
        except Exception as e:
            self.UpdateOutput("Çarxı fırlatmaq mümkün olmadı")
        finally:
            print("4")

    def TurboGear(self):
        try:
            self.serialPort.write(b'5')
            self.UpdateOutput("Çarxın turbo modu qoşuldu")
        except Exception as e:
            self.UpdateOutput("Çarxın turbo modunu qoşmaq mümkün olmadı")
        finally:
            print("5")

    def LightRelayOff(self):
        try:
            self.serialPort.write(b'6')
            self.UpdateOutput("İşıq söndü")
        except Exception as e:
            self.UpdateOutput("İşığı söndürmək mümkün olmadı")
        finally:
            print("6")
            self.lightRelayButton.setText("İşığı yandır")

    def LightRelayOn(self):
        try:
            self.serialPort.write(b'7')
            self.UpdateOutput("İşıq yandı")
        except Exception as e:
            self.UpdateOutput("İşığı yandırmaq mümkün olmadı")
        finally:
            print("7")
            self.lightRelayButton.setText("İşığı söndür")

    def LongLightRelayOn(self):
        try:
            self.serialPort.write(b'9')
            self.UpdateOutput("Uzun işıq yandı")
        except Exception as e:
            self.UpdateOutput("Uzun işığı yandırmaq mümkün olmadı")
        finally:
            print("9")
            self.longLightRelayButton.setText("Uzun işığı söndür")

    def LongLightRelayOff(self):
        try:
            self.serialPort.write(b'8')
            self.UpdateOutput("Uzun işıq söndü")
        except Exception as e:
            self.UpdateOutput("Uzun işığı söndürmək mümkün olmadı")
        finally:
            print("8")
            self.longLightRelayButton.setText("Uzun işığı yandır")

    def ToggleLightRelay(self):
        global lightRelayCondition
        if lightRelayCondition == False:
            self.LightRelayOn()
            lightRelayCondition = True
        else:
            self.LightRelayOff()
            lightRelayCondition = False

    def ToggleLongLightRelay(self):
        global longLightRelayCondition
        if longLightRelayCondition == False:
            self.LongLightRelayOn()
            longLightRelayCondition = True
        else:
            self.LongLightRelayOff()
            longLightRelayCondition = False 

    # Update text
    def CloseEvent(self, event):
        if hasattr(self, 'serialPort') and self.serialPort.is_open:
            self.serialPort.close()
        super(main, self).CloseEvent(event)
