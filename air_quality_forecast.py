import pandas as pd
import mysql.connector
import os
import sys

# Manually specify the correct paths for TCL and TK
os.environ['TCL_LIBRARY'] = r"C:\Users\Sai\AppData\Local\Programs\Python\Python310\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\Sai\AppData\Local\Programs\Python\Python310\tcl\tk8.6"


from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from prophet import Prophet

# Database credentials
DB_USER = "root"
DB_PASSWORD = "1029%40AZby"  # '@' replaced with '%40' (URL encoding)
DB_HOST = "127.0.0.1"
DB_NAME = "air_quality"
TABLE_NAME = "air_quality_data"

# Connect to MySQL database
try:
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    conn = engine.connect()
    print("✅ Database Connection Successful!")
except Exception as e:
    print(f"❌ Error Connecting to Database: {e}")
    exit()

# Fetch AQI data
try:
    query = f"SELECT timestamp, aqi FROM {TABLE_NAME} ORDER BY timestamp"
    df = pd.read_sql(query, conn)
    print("✅ Data Fetch Successful!")
    print(df.head())  # Display first few rows
except Exception as e:
    print(f"❌ Error Fetching Data: {e}")
    conn.close()
    exit()

# Close database connection
conn.close()

# Preprocess Data
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.rename(columns={"timestamp": "ds", "aqi": "y"})  # Prophet requires 'ds' and 'y' column names

# Train Prophet Model
model = Prophet()
model.fit(df)

# Forecast Next 7 Days
future = model.make_future_dataframe(periods=7, freq="D")
forecast = model.predict(future)

# Plot Results
plt.figure(figsize=(10, 5))
plt.plot(df['ds'], df['y'], label="Historical AQI", color='blue')
plt.plot(forecast['ds'], forecast['yhat'], label="Forecasted AQI", color='red', linestyle='dashed')
plt.xlabel("Date")
plt.ylabel("AQI")
plt.title("Air Quality Forecast (Next 7 Days)")
plt.legend()
plt.grid()
plt.savefig("forecast_plot.png")  # Save as an image instead of showing a GUI window

