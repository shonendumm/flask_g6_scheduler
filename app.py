from flask import Flask, render_template
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging

logger = logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
scheduler = BackgroundScheduler()


# Configure the logger for the Flask app
app.logger.setLevel(logging.INFO)  # Set the desired level

# Initialize a global variable to store data
data = "Initial Data"

def fetch_data():
    # Replace with your data-fetching logic
    # time.sleep(20) # simulate time to get data
    global data 
    data = f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    app.logger.info(f'data = {data}')

def schedule_fetch_data():
    scheduler.add_job(fetch_data, 'interval', seconds=30)
    scheduler.start()

# Start fetching data immediately upon starting the app
fetch_data()

# Start the scheduler
schedule_fetch_data()


@app.route("/")
def home():
    return render_template('index.html', data=data)


if __name__ == "__main__":
    try:
        app.run()
    except KeyboardInterrupt:
        scheduler.shutdown()  # Properly shutdown the scheduler
