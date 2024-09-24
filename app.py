from flask import Flask, render_template, request, redirect, url_for
import json
from model import probe_model_5l_profit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'dataFile' not in request.files:
        return redirect(url_for('index'))

    file = request.files['dataFile']

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        # Read and load JSON data
        data = json.load(file)
        result = probe_model_5l_profit(data['data'])

        # Render result page with the financial analysis data
        return render_template('result.html', company=data['data']['company'], flags=result['flags'], description=data['data']['description'])

if __name__ == '__main__':
    app.run(debug=True)
