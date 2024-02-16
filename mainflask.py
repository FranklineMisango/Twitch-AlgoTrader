from flask import Flask, render_template
import api

app = Flask(__name__)

@app.route('/')
def index():
    data = api.convertWatchlist()
    cleaned_data = [symbol.split(':')[1] for symbol in data]
    print(cleaned_data)
    return render_template('index.html', data=cleaned_data)

if __name__ == '__main__':
    app.run(debug=True)
