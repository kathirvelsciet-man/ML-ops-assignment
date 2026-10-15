
import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

os.makedirs("model", exist_ok=True)

# Sample student data
rng = np.random.default_rng(42)
students = 500

study_hours = rng.uniform(0, 10, students)
attendance = rng.uniform(30, 100, students)
internal_marks = rng.uniform(0, 100, students)

# Simple sample rule for Pass/Fail labels
score = (
    study_hours * 5
    + attendance * 0.25
    + internal_marks * 0.45
)

results = (score >= 55).astype(int)

X = np.column_stack(
    [study_hours, attendance, internal_marks]
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X, results)

with open("model/student_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved successfully!")
