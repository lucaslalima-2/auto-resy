# Libaries
from flask import Flask, request, jsonify
from datetime import datetime
import threading, time

# Function
from src.run_resy_bot import run_resy_bot
from src.check_availability import check_availability

# Store Flask app
app = Flask(__name__)

# Homepage
@app.route("/", methods=["POST"])
def start_watching():
	data = request.get_json()
	reservation_config.update({ # allows for dynamic entry
    "restaurant": data.get("restaurant", "Sawa"),
    "date": data.get("date", datetime.today().strftime("%Y-%m-%d")),
    "time": data.get("time", "7:00 pm"),
    "party_size": data.get("party_size", 2)
	})
  threading.Thread(target=watch_reservations, daemon=True).start()
	return jsonify({"status": "watching", "details": reservation_config})

# Background watcher
def watch_reservations():
	while True:
		page, available_res = check_availability(**reservation_config)
		if available_res:
			make_reservation(page, available_res)
			break
		time.sleep(60) # Checks every minute

if __name__ == "__main__":
	app.run(debug=True, use_reloader=False)
	return