from flask import Flask, request
app = Flask(__name__)
lines = []

@app.route('/', methods=["GET", "POST"])
def root():
    global lines
    path = request.path
    method = request.method
    try:
        payload = str(request.data)
    except:
        payload = ""

    message = f"{method} {path} {payload}"
    print(message)
    if (method == "GET"):
        return "<br>".join(lines)
    else:
        lines.append(message)
        return message + "\n"

app.run(host="0.0.0.0")
