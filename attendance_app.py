import streamlit as st
import pandas as pd
import io
from datetime import datetime

def parse_attendance_sheet(df):
    summary = []
    i = 0
    while i < len(df):
        row = df.iloc[i]
        if str(row[0]).strip() == "ID:":
            emp_id = row[2]
            name = df.iloc[i][10]
            dept = df.iloc[i][20]
            time_row = df.iloc[i + 1]
            attendance_days = 0
            tardy_minutes = 0
            for cell in time_row[2:]:
                if pd.isna(cell):
                    continue
                times = [cell[j:j+5] for j in range(0, len(cell), 5) if len(cell[j:j+5]) == 5]
                if times:
                    attendance_days += 1
                    try:
                        time_in = min(datetime.strptime(t, "%H:%M") for t in times)
                        if time_in > datetime.strptime("10:00", "%H:%M"):
                            tardy_minutes += (time_in - datetime.strptime("10:00", "%H:%M")).seconds / 60
                    except:
                        pass
            if attendance_days > 0:
                summary.append({
                    "Employee ID": emp_id,
                    "Name": name,
                    "Department": dept,
                    "Days Present": attendance_days,
                    "Tardiness Hours": round(tardy_minutes / 60, 2)
                })
            i += 2
        else:
            i += 1
    return pd.DataFrame(summary)

st.title("Attendance Summary Generator")

uploaded_file = st.file_uploader("Upload Attendance Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name=0, header=None, engine='openpyxl')
    summary_df = parse_attendance_sheet(df)

    st.subheader("Summary")
    st.dataframe(summary_df)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        summary_df.to_excel(writer, index=False, sheet_name="Summary")
    st.download_button("Download Summary Excel", data=output.getvalue(), file_name="attendance_summary.xlsx")
