# ✈️ **FCT** (Flight Comms and Tracker)

Is a real-time aircraft tracking project using **RTL-SDR**, **Dump1090**, and **Flask**. The application allows users to monitor aircraft via an interactive web interface, displaying details such as altitude, speed, and heading.

---

## 🚀 Features
✔️ Real-time aircraft tracking  
✔️ Displaying aircraft positions on **map.html**  
✔️ Flight details (callsign, altitude, speed, heading)    
✔️ Automatic position updates  

---

## 📦 Technologies Used
- **Python** *(Flask, Requests)*
- **JavaScript** *(Leaflet.js)*
- **HTML/CSS**
- **Dump1090**
- **RTL-SDR**
- **ttkbootstrap**
  
---

## 🛠️ Installation and Setup

- Under development
  
### 1️⃣ Prerequisites
- RTL-SDR (e.g., RTL2832U)
- Dump1090 (https://github.com/gvanem/Dump1090)
- Python 3.8+ installed (and all the libraries needed)
- Git installed

  
### 2️⃣ How the program Works
- Connect your **RTL-SDR** into your computer. You will see on the down right corner the status
- Start the **Flask Server** to connect an IP adress to **map.html** and collecting data from **aircraft.json**
- Start **Dump1090** to capture in real-time **ADS-B** signals
- Once you got the **lat.** and **log.** of a plane, you can open **map.html** to see the planes you captured
- You can check via **Flight Radar** to discover more information about the planes you captured

### 3️⃣ Installing the Project
Clone the repository:
```sh
git clone https://github.com/username/FlightComms_and_Tracker.git
cd FlightComms_and_Tracker
