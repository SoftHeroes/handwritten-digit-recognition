from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('paint.html')

# API endpoint


@app.route("/predict", methods=['POST'])
def get_data():
    # Prepare the data you want to return
    data = {
        "predicted": 2,
    }

    # Return the data as JSON
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
