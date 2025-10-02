from src.check_availability import check_availability
from datetime import datetime

location = "New York"
restuarant = "Sawa"
date = "October 30, 2025"
time_window = ["7:00 PM", "9:00 PM"]
party_size = 3

check_availability(location, restuarant, date, time_window, party_size)