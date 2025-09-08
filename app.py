from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
	return "Resy Bot is running!"

@app.route("/run-bot")
def run_bot():
# Placeholder for your bot logic
	try:
		result = run_resy_bot()
		return jsonify({"status": "success", "details": result})
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), 500

def run_resy_bot():
	# This is where your scraping or automation logic goes
	# For now, just return a dummy response
	return "Bot executed successfully."

if __name__ == "__main__":
  app.run(debug=True)