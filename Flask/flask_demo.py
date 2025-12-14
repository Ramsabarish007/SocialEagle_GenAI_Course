from flask import Flask, request, jsonify

app = Flask(__name__)

def validate_numbers(data):
    try:
        a = float(data.get("a"))
        b = float(data.get("b"))
        return a, b, None
    except (TypeError, ValueError):
        return None, None, "Inputs must be valid numbers"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Math API is running 🚀",
        "endpoints": {
            "/add": "POST",
            "/subtract": "POST",
            "/multiply": "POST",
            "/divide": "POST"
        },
        "example_body": {"a": 10, "b": 5}
    })


@app.route("/add", methods=["POST"])
def add():
    data = request.json
    a, b, error = validate_numbers(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"result": a + b})


@app.route("/subtract", methods=["POST"])
def subtract():
    data = request.json
    a, b, error = validate_numbers(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"result": a - b})


@app.route("/multiply", methods=["POST"])
def multiply():
    data = request.json
    a, b, error = validate_numbers(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"result": a * b})


@app.route("/divide", methods=["POST"])
def divide():
    data = request.json
    a, b, error = validate_numbers(data)
    if error:
        return jsonify({"error": error}), 400
    if b == 0:
        return jsonify({"error": "Division by zero is not allowed"}), 400
    return jsonify({"result": a / b})


if __name__ == "__main__":
    app.run(debug=True)
