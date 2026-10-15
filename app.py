
import os
import pickle
from flask import Flask, request, render_template_string

app = Flask(__name__)
MODEL_VERSION = "1.0"

with open("model/student_model.pkl", "rb") as f:
    model = pickle.load(f)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Result Predictor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2ff;
            margin: 0;
            padding: 30px 15px;
        }
        .card {
            max-width: 430px;
            margin: 30px auto;
            padding: 28px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 25px #0001;
        }
        h1 { color: #3730a3; }
        label { display: block; margin-top: 16px; }
        input, button {
            box-sizing: border-box;
            width: 100%;
            padding: 12px;
            margin-top: 7px;
            border-radius: 8px;
            border: 1px solid #ccc;
        }
        button {
            background: #4f46e5;
            color: white;
            border: none;
            margin-top: 22px;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            padding: 12px;
            background: #eef2ff;
            border-radius: 8px;
            font-weight: bold;
        }
        .version { color: #666; font-size: 13px; }
    </style>
</head>
<body>
<div class="card">
    <h1>Student Result Predictor</h1>
    <p>Enter the student's details to predict the result.</p>
    <p class="version">Model Version: {{ version }}</p>

    <form method="POST">
        <label>Study Hours (0–10)</label>
        <input type="number" name="hours" min="0" max="10"
               step="0.1" required>

        <label>Attendance (%)</label>
        <input type="number" name="attendance" min="0" max="100"
               step="0.1" required>

        <label>Internal Marks (0–100)</label>
        <input type="number" name="marks" min="0" max="100"
               step="0.1" required>

        <button type="submit">Predict Result</button>
    </form>

    {% if prediction %}
    <div class="result">Predicted Result: {{ prediction }}</div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None

    if request.method == "POST":
        try:
            hours = float(request.form["hours"])
            attendance = float(request.form["attendance"])
            marks = float(request.form["marks"])

            if not (0 <= hours <= 10 and
                    0 <= attendance <= 100 and
                    0 <= marks <= 100):
                raise ValueError("Input out of range")

            result = model.predict([[hours, attendance, marks]])[0]
            prediction = "Pass" if result == 1 else "Fail"

        except (ValueError, TypeError):
            prediction = "Invalid input. Please check the values."

    return render_template_string(
        HTML, prediction=prediction, version=MODEL_VERSION
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
