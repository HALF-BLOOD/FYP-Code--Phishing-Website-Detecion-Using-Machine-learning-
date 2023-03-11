from flask import Flask, request

app = Flask(__name__)

@app.route('/check-phishing', methods=['POST', 'OPTIONS'])
def check_phishing():
    if request.method == 'OPTIONS':
        # Set CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    url = request.json['url']
    print(f'Received URL: {url}')
    return ''


if __name__ == '__main__':
  app.run(debug=True)
