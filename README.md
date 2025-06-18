# 🧾 Log File Analyzer (Streamlit)

This is a simple web app built using **Streamlit** that allows users to upload a `.log` file and analyze its contents. It supports:

- Filtering by date range
- Filtering by log level (`INFO`, `WARNING`, `ERROR`)
- Identifying the most common error message

---

## 📦 Features

- 📁 Upload `.log` files (in the format: `YYYY-MM-DD HH:MM:SS - LEVEL - Message`)
- 📅 Filter logs by a start and end date
- ⚠️ Filter by log level (e.g., only `ERROR`)
- 🔍 See a summary count of each log level
- ❗ Get the most frequent error message

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/streamlit-log-analyzer.git
cd streamlit-log-analyzer
python -m streamlit run log_analyzer.py
