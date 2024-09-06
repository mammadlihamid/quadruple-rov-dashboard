# 🌊 QuadRuple - Teknofest Unmanned Underwater System Competition 🌊

## 🛠️ Overview

This project is developed for the **Teknofest Unmanned Underwater System Competition** by Team **QuadRuple**. The application assists in controlling and monitoring our unmanned underwater system (UUS) through a graphical user interface (GUI). It integrates various functionalities, including real-time video feeds, serial communication with external hardware, and user interaction automation to enhance the control of our underwater vehicle.

Visit our website: [quadruple.netlify.app](https://quadruple.netlify.app)

## 🚀 Features

- 📷 **Real-time camera feed** using OpenCV for underwater monitoring.
- 🖥️ **PyQt5-based GUI** for controlling and interacting with the UUS system.
- 🔌 **Serial communication** with the UUS for sending and receiving commands.
- 🤖 **Automated user input** using PyAutoGUI for streamlined control.
- ⏰ **Timing and scheduling** using Python’s `datetime` and `QTimer` for precise task execution.

## 💻 Installation

### ⚙️ Prerequisites

Make sure you have **Python 3.7+** installed. You can download the latest version from the [official Python website](https://www.python.org/downloads/).

### 📥 Step-by-Step Installation

1. **Clone the repository** (or download the project):
   ```bash
   git clone https://github.com/mammadlihamid/quadruple-rov-dashboard.git
   cd quadruple-rov-dashboard
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install the required libraries**:
   
   To install all necessary Python libraries in one go, use the `requirements.txt` file by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, you can install each library individually:

   ```bash
   pip install PyQt5==5.15.4
   pip install pyserial==3.5
   pip install numpy==1.21.2
   pip install pyautogui==0.9.53
   pip install opencv-python==4.5.5.62
   pip install pygame==2.6.0
   ```

### 📦 Required Libraries:

- **PyQt5**: For building the graphical user interface. Install via:
  ```bash
  pip install PyQt5==5.15.4
  ```
  [PyQt5 Documentation](https://pypi.org/project/PyQt5/)

- **pyserial**: For communication with serial devices. Install via:
  ```bash
  pip install pyserial==3.5
  ```
  [PySerial Documentation](https://pypi.org/project/pyserial/)

- **numpy**: For numerical operations and array processing. Install via:
  ```bash
  pip install numpy==1.21.2
  ```
  [NumPy Documentation](https://numpy.org/)

- **pyautogui**: For automating GUI tasks. Install via:
  ```bash
  pip install pyautogui==0.9.53
  ```
  [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)

- **opencv-python**: For video capture and image processing. Install via:
  ```bash
  pip install opencv-python==4.5.5.62
  ```
  [OpenCV Documentation](https://opencv.org/)

- **pygame**: For multimedia and audio tasks. Install via:
  ```bash
  pip install pygame==2.6.0
  ```
  [Pygame Documentation](https://www.pygame.org/)

## ▶️ Running the Application

Once the dependencies are installed, you can start the application using the following command in your terminal:

```bash
python run.py
```

Make sure all necessary hardware components, such as the camera and serial devices, are connected before starting the application.

## 🛠️ Troubleshooting

- **Library Errors**: If you encounter issues related to missing or incorrect versions of libraries, verify that the correct versions are installed using the `requirements.txt` file.

- **Serial Communication**: Make sure the underwater system is properly connected and recognized by your operating system if you encounter issues with serial communication.

## 🏆 Competition Information

- **Category**: Unmanned Underwater System Competition
- **Race**: Teknofest
- **Team Name**: QuadRuple

## 🤝 Contributing

We welcome contributions from team members! To contribute:

1. Fork this repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request for review.

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## 👥 Team QuadRuple

- **Captain**: Hamid Mammadli
- **Team Members**: Togrul Abbas 
