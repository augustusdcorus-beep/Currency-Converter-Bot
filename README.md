# 🇺🇦 Telegram Currency Converter Bot

A smart Telegram bot for real-time currency tracking and conversion. 
Built with **Python**, integrating **NBU API** for live exchange rates and **SQLite** for user data management.

## 🚀 Features
* **Live Exchange Rates:** Fetches real-time data from the National Bank of Ukraine (NBU) API.
* **Smart Memory:** Remembers user's preferred currency (USD/EUR) using a SQLite database.
* **Currency Calculator:** Interactive tool to convert UAH to USD/EUR instantly.
* **Robust Error Handling:** Handles API failures and invalid user inputs gracefully.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Libraries:** `pyTelegramBotAPI`, `requests`, `sqlite3`
* **Database:** SQLite
* **Deployment:** PythonAnywhere (Cloud)

## ⚙️ How to Run
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install pyTelegramBotAPI requests
