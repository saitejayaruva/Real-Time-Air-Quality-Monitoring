import requests
import mysql.connector
from datetime import datetime

# WAQI API Configuration
API_KEY = "17f646e1a5816b5e08c194aae2d7cf1cdefa63cc"  #WAQI API key
CITY_LIST = ["New Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru",
             "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow"]

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="air_quality",
    port="3306"
)
cursor = conn.cursor()

# Fetch air quality data for each city and store it in MySQL
for city in CITY_LIST:
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
    response = requests.get(url).json()

    if response.get("status") == "ok":
        data = response["data"]
        aqi = data["aqi"]
        iaqi = data["iaqi"]

        # Extract pollutant values safely
        pm10 = iaqi.get("pm10", {}).get("v", None)
        pm2_5 = iaqi.get("pm25", {}).get("v", None)
        o3 = iaqi.get("o3", {}).get("v", None)
        no2 = iaqi.get("no2", {}).get("v", None)
        so2 = iaqi.get("so2", {}).get("v", None)
        co = iaqi.get("co", {}).get("v", None)
        timestamp = datetime.strptime(data["time"]["s"], "%Y-%m-%d %H:%M:%S")

        # Insert data into MySQL
        insert_query = """
        INSERT INTO air_quality_data (city_name, aqi, pm10, pm2_5, o3, no2, so2, co, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (city, aqi, pm10, pm2_5, o3, no2, so2, co, timestamp)
        cursor.execute(insert_query, values)
        conn.commit()
        print(f"✅ Data for {city} inserted successfully!")

# Close the connection
cursor.close()
conn.close()
