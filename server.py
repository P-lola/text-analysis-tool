from flask import Flask, render_template

app = Flask(__name__)

# Debug setting set to true
app.debug = True

@app.route('/health')
def healthCheck():
    return "Flask server is up and running"


@app.route('/analyze-stock/<ticker>')
def analyzeStock(ticker):
    return {"data" : "Analysis for " + ticker + " Coming Soon"}


if __name__ == '__main__':
    app.run()