from flask import Flask, render_template
import csv

schedule_data = []

with open('schedule/Monday.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        schedule_data.append(row)
    
    print(schedule_data)

app = Flask(__name__)

@app.route("/")
def hello_world(schedule=schedule_data):
    return render_template('index.html', schedule=schedule)