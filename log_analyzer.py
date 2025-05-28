import streamlit as st
import argparse
from datetime import datetime
from collections import Counter
import io

def parse_arguments():
    parser = argparse.ArgumentParser(description="Advanced Log File Analyzer")
    parser.add_argument('--file', type=str, default='app.log', help='Path to the log file')
    parser.add_argument('--start-date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--end-date', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('--levels', nargs='+', choices=['INFO', 'WARNING', 'ERROR'], default=['INFO', 'WARNING', 'ERROR'], help='Log levels to include')
    return parser.parse_args()

def parse_log_line(line):
    try:
        timestamp_str, level, message = line.strip().split(' - ', 2)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return timestamp, level, message
    except ValueError:
        return None, None, None  # Malformed line

def analyze_log_file(file_lines, start_date, end_date, levels):
    log_counts = Counter()
    error_messages = []

    for line in file_lines:
        timestamp, level, message = parse_log_line(line)
        if not timestamp or level not in levels:
            continue

        if (start_date and timestamp < start_date) or (end_date and timestamp > end_date):
            continue

        log_counts[level] += 1
        if level == "ERROR":
            error_messages.append(message)

    most_common_error = Counter(error_messages).most_common(1)[0][0] if error_messages else None

    return log_counts, most_common_error


# Streamlit UI
st.title("Log File Analyzer")

uploaded_file = st.file_uploader("Upload your `.log` file", type="log")

with st.sidebar:
    st.header("Filter Options")
    start_date = st.date_input("Start Date", value=None)
    end_date = st.date_input("End Date", value=None)
    levels = st.multiselect("Log Levels", ["INFO", "WARNING", "ERROR"], default=["INFO", "WARNING", "ERROR"])

if uploaded_file:
    file_contents = uploaded_file.getvalue().decode("utf-8").splitlines()

    start_dt = datetime.combine(start_date, datetime.min.time()) if start_date else None
    end_dt = datetime.combine(end_date, datetime.max.time()) if end_date else None

    log_counts, most_common_error = analyze_log_file(file_contents, start_dt, end_dt, levels)

    st.subheader("Log Summary")
    for level in levels:
        st.write(f"{level}: {log_counts[level]}")

    if "ERROR" in levels and most_common_error:
        st.write(f"Most common ERROR: \"{most_common_error}\"")