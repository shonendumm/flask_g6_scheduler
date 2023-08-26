from flask import Flask, render_template, Response
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging

logger = logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(levelname)s|%(funcName)s|%(message)s')
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
        g.data = f"date is {time.strftime('%Y-%m-%d %H:%M:%S')}"

    def schedule_fetch_data():
        scheduler.add_job(fetch_data, 'interval', seconds=5)
        scheduler.start()

    # Start fetching data immediately upon starting the app
    fetch_data()

    # Start the scheduler
    schedule_fetch_data()

    def generate_data():
        while True:
            # need the "data:" keyword because frontend is calling .data as the key
            # also need \n\n or else it won't display the text. The double newline characters are used to delimit individual messages in the SSE stream. Each SSE message must be followed by two newline characters to indicate the end of the message. 
            yield f"data: {g.data}\n\n"
            time.sleep(10)  # Adjust the interval as needed


@app.route("/")
def home():
    return render_template('index.html', data=g.data)

@app.route('/data-stream')
def data_stream():
    return Response(generate_data(), content_type='text/event-stream')


if __name__ == "__main__":
    try:
        app.run()
    except:
        scheduler.shutdown()  # Properly shutdown the scheduler
