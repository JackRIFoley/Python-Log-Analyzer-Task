import argparse
from datetime import datetime
from collections import Counter

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

def analyze_log_file(file_path, start_date, end_date, levels):
    log_counts = Counter()
    error_messages = []

    with open(file_path, 'r') as f:
        for line in f:
            timestamp, level, message = parse_log_line(line)
            if not timestamp or level not in levels:
                continue

            if (start_date and timestamp < start_date) or (end_date and timestamp > end_date):
                continue

            log_counts[level] += 1
            if level == "ERROR":
                error_messages.append(message)

    most_common_error = Counter(error_messages).most_common(1)[0][0] if error_messages else None

    print("Log Summary:")
    for level in levels:
        print(f"{level}: {log_counts[level]}")
    if "ERROR" in levels and most_common_error:
        print(f"Most common ERROR: \"{most_common_error}\"")

def main():
    args = parse_arguments()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else None

    analyze_log_file(args.file, start_date, end_date, args.levels)

if __name__ == "__main__":
    main()
