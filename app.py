from flask import Flask, render_template
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging

logger = logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Configure the logger for the Flask app
app.logger.setLevel(logging.INFO)  # Set the desired level

scheduler = BackgroundScheduler()

with app.app_context() as g:

    # Initialize a global variable to store data
    g.data = "Initial Data"

    def fetch_data():
        # Replace with your data-fetching logic
        # time.sleep(20) # simulate time to get data
        g.data = f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}"

    def schedule_fetch_data():
        scheduler.add_job(fetch_data, 'interval', seconds=30)
        scheduler.start()

    # Start fetching data immediately upon starting the app
    fetch_data()

    # Start the scheduler
    schedule_fetch_data()


@app.route("/")
def home():
    return render_template('index.html', data=g.data)


if __name__ == "__main__":
    try:
        app.run()
    except:
        scheduler.shutdown()  # Properly shutdown the scheduler
