import asyncio
import requests
import sys

# Test HTTP endpoints first
url_api = "https://theisle.gachacity.vn/api/overlay/hello"
headers = {
    "User-Agent": "Mozilla/5.0",
}
try:
    res = requests.get(url_api, headers=headers, timeout=5)
    print("HTTP GET /api/overlay/hello Status:", res.status_code)
    print("Response:", res.text[:200])
except Exception as e:
    print("HTTP GET failed:", e)

# Test WS connection
import websockets

async def test_ws():
    ws_url = "wss://theisle.gachacity.vn/ows"
    print("Connecting to WebSocket:", ws_url)
    try:
        async with websockets.connect(ws_url, extra_headers={"User-Agent": "Mozilla/5.0"}, open_timeout=5) as ws:
            print("WS Connection successful!")
    except Exception as e:
        print("WS Connection failed:", e)

asyncio.run(test_ws())
