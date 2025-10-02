# Libaries
from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# Functions
from src.run_resy_bot import run_resy_bot

# Load environment variables
load_dotenv()

# Store Flask app
app = Flask(__name__)

# Homepage
@app.route("/")
def home():
	return "Resy Bot is running!"

# GET Commands
@app.route("/run-bot")
def run_bot():
# Placeholder for your bot logic
	try:
		result = run_resy_bot()
		return jsonify({"status": "success", "details": result})
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
  app.run(debug=True)