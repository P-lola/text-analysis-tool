from flask import Flask, render_template

app = Flask(__name__)

# Debug setting set to true
app.debug = True

@app.route('/health')
def index():
    return "Flask server is up and running"

if __name__ == '__main__':
    app.run()