from src.check_availability import check_availability
from datetime import datetime

location = "New York"
restuarant = "Sawa"
date = datetime.today().strftime("%Y-%m-%d")
time = "7:00 pm"
party_size = 2

check_availability(location, restuarant, date, time, party_size)