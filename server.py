from flask import Flask, render_template, abort

app = Flask(__name__)

# Debug setting set to true
app.debug = True

@app.route('/health')
def healthCheck():
    return "Flask server is up and running"


@app.route('/analyze-stock/<ticker>')
def analyzeStock(ticker):
    if len(ticker) > 5 or not ticker.isidentifier():
        abort(400, "Invalid ticker symbol")
    return {"data" : "Analysis for " + ticker + " Coming Soon"}


if __name__ == '__main__':
    app.run()