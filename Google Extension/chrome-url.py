from flask import Flask, request

app = Flask(__name__)

@app.route('/url', methods=['POST'])
def process_url():
    url = request.form['url']
    # process the URL here
    print(url)
    return 'URL processed successfully'

if __name__ == '__main__':
    app.run(debug=True)
