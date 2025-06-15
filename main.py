
from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    coin = data.get("ticker", "N/A")
    price = data.get("price", "N/A")
    tf = data.get("timeframe", "N/A")
    tp = data.get("tp", "N/A")
    capital = float(data.get("capital", 0))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        entry_price = float(price)
        tp_price = float(tp)
        profit = (tp_price - entry_price) * capital
    except:
        profit = "N/A"

    setup_flags = data.get("setup", [])
    setup = "\n   - " + "\n   - ".join(setup_flags).replace("_", " ").title()

    message = f"""
🚨 *SNIPER ALERT DETECTED*

🕒 *Time*: {now}
💎 *Coin*: {coin} ({tf})
🎯 *Entry Price*: {price}
📌 *Setup Details*:{setup}
📊 *BTC Trend*: ✅ Bullish

🎯 *TP Price*: {tp}
🔥 *Win Probability*: 84%
💰 *Capital Suggested*: ${capital:,.2f}
📈 *Est. Profit (TP Hit)*: *${profit:,.2f}*

🔒 *Mode*: Project Israfil – Phase 1 (Sniper Eye)
"""
    send_telegram_message(message)
    return {'status': 'sent'}
