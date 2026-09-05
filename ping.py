import requests

# Replace with your actual Bot Token from BotFather
BOT_TOKEN = "8192185738:AAEZSJo-r-erLu0lPlWserqoyt3LhV6uzVw"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def call_endpoint(method_name, payload=None):
  """Helper function to test any Telegram Bot API endpoint easily."""
  url = f"{BASE_URL}/{method_name}"

  try:
    # Use POST if sending data (payload), otherwise use GET
    if payload:
      response = requests.post(url, json=payload)
    else:
      response = requests.get(url)

    print(f"\n--- Testing Endpoint: /{method_name} ---")
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())
    return response.json()

  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  # 1. Test 'getMe' (Checks if your token is valid and shows bot info)
  call_endpoint("getMe")

  # 2. Test 'getUpdates' (Checks your message queue)
  call_endpoint("getUpdates")

  # 3. Test 'sendMessage' (Uncomment and fill in your chat_id to test sending)
  # payload = {
  #     "chat_id": "YOUR_CHAT_ID_HERE",
  #     "text": "Hello! Testing the Telegram API from Python."
  # }
  # call_endpoint("sendMessage", payload)

