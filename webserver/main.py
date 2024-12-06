from flask import Flask, jsonify, render_template, send_file
import os

IMAGE_PATH = os.path.join(os.getcwd(), 'static', 'images', 'ai_first_image.jpg')

print(IMAGE_PATH)
app = Flask(__name__)

def get_battery_level():
    try:
        with open('battery_level.txt', 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return -1
    except ValueError:
        return -1

def get_voltage():
    try:
        with open('voltage.txt', 'r') as file:
            return float(file.read().strip())
    except FileNotFoundError:
        return -1
    except ValueError:
        return -1

@app.route('/')
def index():
    return render_template('index.html', battery_level = get_battery_level())

@app.route('/battery')
def battery():
    return render_template('battery.html', battery_level = get_battery_level(), voltage = get_voltage())

@app.route("/ai_prediction")
def ai_prediction():
    return render_template('ai_prediction.html')

@app.route('/image/last_modified_first/')
def image_last_modified_first():
    print(IMAGE_PATH)
    print(os.path.exists(IMAGE_PATH))
    try:
        last_modified = os.path.getmtime(IMAGE_PATH)
        return jsonify({"last_modified": last_modified})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/image_first')
def get_image():
    try:
        return send_file(IMAGE_PATH)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)