# Attendance Summary Web App

This is a Streamlit web app that processes biometric attendance logs and generates a summary report.

## Features

- Upload an Excel attendance log
- Automatically extract employee attendance
- Calculate total tardiness in hours
- Exclude employees with zero attendance
- Download the summary as an Excel file

## How to Run (macOS)

1. Open Terminal
2. Create and activate a virtual environment (optional but recommended):

   python3 -m venv attendance_env
   source attendance_env/bin/activate

3. Install dependencies:

   pip install -r requirements.txt

4. Run the app:

   streamlit run attendance_app.py
