# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# File to store workout data
workout_file = 'workouts.json'

# Check if workout file exists, if not, create an empty one
if not os.path.isfile(workout_file):
    with open(workout_file, 'w') as f:
        json.dump([], f)

def get_workouts():
    """
    Get the workouts from the workout file.

    Returns:
    - list: List of workout entries.
    """
    with open(workout_file, 'r') as f:
        workouts = json.load(f)
    return workouts

def save_workouts(workouts):
    """
    Save the workouts to the workout file.

    Args:
    - workouts (list): List of workout entries.
    """
    with open(workout_file, 'w') as f:
        json.dump(workouts, f)

@app.route('/')
def index():
    workouts = get_workouts()
    return render_template('index.html', workouts=workouts)

@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'GET':
        return render_template('log_workout.html')
    elif request.method == 'POST':
        workouts = get_workouts()
        date = request.form['date']
        exercise = request.form['exercise']
        duration = request.form['duration']
        calories_burned = request.form['calories_burned']
        workouts.append({
            'date': date,
            'exercise': exercise,
            'duration': duration,
            'calories_burned': calories_burned
        })
        save_workouts(workouts)
        flash('Workout logged successfully!', 'success')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)






<!-- templates/index.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fitness Tracker</title>
</head>
<body>

    <h1>Fitness Tracker</h1>

    <ul>
        {% for workout in workouts %}
            <li>
                <strong>Date:</strong> {{ workout.date }} |
                <strong>Exercise:</strong> {{ workout.exercise }} |
                <strong>Duration:</strong> {{ workout.duration }} |
                <strong>Calories Burned:</strong> {{ workout.calories_burned }}
            </li>
        {% endfor %}
    </ul>

    <a href="/log_workout">Log Workout</a>

</body>
</html>






<!-- templates/log_workout.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log Workout</title>
</head>
<body>

    <h1>Log Workout</h1>

    <form action="/log_workout" method="post">
        <label for="date">Date:</label>
        <input type="date" id="date" name="date" required>
        <br>
        <label for="exercise">Exercise:</label>
        <input type="text" id="exercise" name="exercise" required>
        <br>
        <label for="duration">Duration (minutes):</label>
        <input type="number" id="duration" name="duration" required>
        <br>
        <label for="calories_burned">Calories Burned:</label>
        <input type="number" id="calories_burned" name="calories_burned" required>
        <br>
        <button type="submit">Log Workout</button>
    </form>

    <a href="/">Back to Home</a>

</body>
</html>
