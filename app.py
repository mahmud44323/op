from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/chat', methods=['GET'])
def chat():
    # Set up the request URL and headers
    url = 'https://www.blackbox.ai/api/chat'
    headers = {
        'authority': 'www.blackbox.ai',
        'accept': '*/*',
        'accept-language': 'en-SG,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'cookie': 'sessionId=21b9cdf9-df30-486f-b114-0d34c05b5c42; __Host-authjs.csrf-token=4ad540eaacdf8603762296d14b2ce880a5af772d821dfe7fec6f814999bb8e4d%7C8ee5274a727bc70dc30214a7a2d8bb05ea4cfb2f00dda5f2451566ee38751058; __Secure-authjs.callback-url=https%3A%2F%2Fwww.blackbox.ai; intercom-id-jlmqxicb=fce17476-95ad-423f-8ba5-6ad568a0cc33; intercom-session-jlmqxicb=; intercom-device-id-jlmqxicb=10662a8f-63f9-4918-8356-45a78bbbecff',
        'origin': 'https://www.blackbox.ai',
        'referer': 'https://www.blackbox.ai/agent/ImageGenerationLV45LJp',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
    }

    # Collect user input for the message content from query parameters
    user_content = request.args.get("user_content")

    if not user_content:
        return jsonify({"error": "No user content provided"}), 400

    # Set up the data payload with dynamic content input
    data = {
        "messages": [
            {"id": "user-message", "content": user_content, "role": "user"}
        ],
        "id": "unique-id",
        "previewToken": None,
        "userId": None,
        "codeModelMode": True,
        "agentMode": {"mode": True, "id": "ImageGenerationLV45LJp", "name": "Image Generation"},
        "trendingAgentMode": {},
        "isMicMode": False,
        "maxTokens": 1024,
        "playgroundTopP": None,
        "playgroundTemperature": None,
        "isChromeExt": False,
        "githubToken": None,
        "clickedAnswer2": False,
        "clickedAnswer3": False,
        "clickedForceWebSearch": False,
        "visitFromDelta": False,
        "mobileClient": False,
        "userSelectedModel": None
    }

    # Send the request to the external API
    response = requests.post(url, headers=headers, json=data)

    # Return the response back to the client
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
