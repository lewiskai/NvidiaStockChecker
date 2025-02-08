import requests
import time
import json

# 读取配置文件
with open("config.json", "r") as file:
    config = json.load(file)

NVIDIA_URL = config["nvidia_url"]
DISCORD_WEBHOOK = config["discord_webhook"]
CHECK_INTERVAL = config["check_interval"]

def check_nvidia_stock():
    try:
        response = requests.get(NVIDIA_URL, timeout=10)
        if "Add to Cart" in response.text:
            send_discord_notification("🚀 **NVIDIA 5080/5090** **In Stock!** 🛒")
        else:
            print("❌ No stock available.")
    except Exception as e:
        print(f"Error checking stock: {e}")

def send_discord_notification(message):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=payload)

if __name__ == "__main__":
    while True:
        check_nvidia_stock()
        time.sleep(CHECK_INTERVAL)
