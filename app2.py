from flask import Flask, render_template
from datetime import datetime
from flask_apscheduler import APScheduler
import time
import logging

logger = logging.basicConfig(level=logging.INFO, format='%(asctime)s||%(levelname)s||%(funcName)s||%(message)s')
logger = logging.getLogger(__name__)

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
# Configure the logger for the Flask app
app.logger.setLevel(logging.INFO)  # Set the desired level
app.config.from_object(Config())

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


with app.app_context() as g:

    # Initialize a global variable to store data
    g.data = "Initial Data"

    def fetch_data():
        # Replace with your data-fetching logic
        # time.sleep(20) # simulate time to get data
        g.data = f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}"


    # interval example
    @scheduler.task('interval', id='do_job_1', seconds=30, misfire_grace_time=900)
    def job1():
        fetch_data()
        logger.info('Job 1 executed')

    # Start fetching data immediately upon starting the app
    fetch_data()



@app.route("/")
def home():
    return render_template('index.html', data=g.data)


if __name__ == "__main__":
    try:
        app.run()
        
    except:
        scheduler.shutdown()  # Properly shutdown the scheduler
