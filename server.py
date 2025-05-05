from flask import Flask, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

DUMP1090_URL = "http://127.0.0.1:8080/data/aircraft.json"

@app.route("/")
def home():
    return send_from_directory(os.path.dirname(__file__), "map.html")

@app.route("/aircraft")
def get_aircraft():
    try:
        response = requests.get(DUMP1090_URL, timeout=5)
        if response.status_code != 200:
            return jsonify({"error": "Dump1090 nu este accesibil"}), 500

        data = response.json()
        aircraft_list = []

        for aircraft in data.get("aircraft", []):
            lat = aircraft.get("lat")
            lon = aircraft.get("lon")
            callsign = aircraft.get("flight", "Unknown").strip()
            altitude = aircraft.get("altitude", "N/A")
            speed = aircraft.get("speed", "N/A")
            track = aircraft.get("track", "N/A")
            icao = aircraft.get("hex", "N/A").upper()

            if lat and lon:
                aircraft_list.append({
                    "lat": lat,
                    "lon": lon,
                    "callsign": callsign,
                    "icao": icao,
                    "altitude": altitude,
                    "speed": speed,
                    "track": track
                })

        return jsonify(aircraft_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/icons/<path:filename>")
def get_icon(filename):
    return send_from_directory("icons", filename)

if __name__ == "__main__":
    context = ('certificat.pem', 'cheie_privata.pem')
    app.run(debug=True, host="0.0.0.0", port=5000, ssl_context=context)

