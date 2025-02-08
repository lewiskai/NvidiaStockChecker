import requests
import time
import json
from bs4 import BeautifulSoup

# 读取配置文件
with open("config.json", "r") as file:
    config = json.load(file)

NVIDIA_URLS = {
    "UK": "https://www.nvidia.com/en-gb/geforce/"
}

DISCORD_WEBHOOK = config["discord_webhook"]
CHECK_INTERVAL = config["check_interval"]
FE_KEYWORDS = ["Founders Edition", "FE"]
ADD_TO_CART_TEXT = "Add to Cart"

# 检测库存
def check_nvidia_stock():
    for region, url in NVIDIA_URLS.items():
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 查找是否有 FE 版
            found_fe = any(keyword in response.text for keyword in FE_KEYWORDS)
            
            # 查找是否有 "Add to Cart" 按钮
            add_to_cart = ADD_TO_CART_TEXT in response.text
            
            if found_fe and add_to_cart:
                send_discord_notification(f"🚀 **NVIDIA 5080/5090 FE In Stock in {region}!** 🛒 [Buy Now]({url})")
            elif found_fe:
                send_discord_notification(f"⚠️ **NVIDIA 5080/5090 FE Found in {region}, but not available yet!** ⏳ [Check]({url})")
            else:
                print(f"❌ No stock available in {region}.")
        except Exception as e:
            print(f"Error checking {region} stock: {e}")

# 发送 Discord 通知
def send_discord_notification(message):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=payload)

if __name__ == "__main__":
    while True:
        check_nvidia_stock()
        time.sleep(CHECK_INTERVAL)

