from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/chat', methods=['GET'])
def chat():
    # Get the user's message from the query parameters
    user_input = request.args.get('message')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    # Set up the external API details
    url = "https://aibr.elway-mobile.com/chatCompletion"
    headers = {
        'User-Agent': "Ktor client",
        'Accept': "application/json",
        'Accept-Encoding': "gzip",
        'aibsg': "WCwmuYES90tTPV6fiTG+u2IJaUD87zsjKQStUhR9FTXoX0fyzRdyPmNKsRcHRi42qNuyfUckrReJuoq8vp9EY6rsvOyS8luAFk9QatNCT9mIukLCNcK2Ee29um0X1mIqdaGNtGv4dOF5lYHhHh4TuXLOZgbPFAcPtqUu/K7A25zWwG8KKe6FQpU8OP1qCpt/kYq5ohAbdW7/BxcaOYs8NV7/N8Hs0B2Kykm/Z+l1A7pC27EwVysgM9sTmVTF5Oh5L+GvTEqyMekG7M9SzFAZ4Dl4c4veqdCNIXRa47IN8aER8/M7TmvVJFOq8tBzyyGxyzb3IY77y29IWjJxciNrNA==",
        'aibpf': "android",
        'aibmd': "default",
        'appmv': "14",
        'appvr': "1440",
        'Accept-Charset': "UTF-8"
    }
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    # Send the request to the external API
    response = requests.get(url, json=payload, headers=headers)
    
    # Parse and format the response data
    if response.status_code == 200:
        response_data = response.json()
        return jsonify(response_data)
    else:
        return jsonify({"error": "Failed to get response from the external API"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
