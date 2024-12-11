from flask import Flask, jsonify, render_template, send_file, request
import os

AI_FIRST_IMAGE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'images', 'ai_first_image.jpg')
CONTRAST_FILE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'files', 'contrast_value.txt')
STEERING_ANGLE_FILE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'files', 'steering_angle.txt')
BATTERY_FILE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'files', 'battery_level.txt')
VOLTAGE_FILE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'files', 'voltage.txt')
AI_SECOND_IMAGE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'images', 'ai_second_image.jpg')
AI_THIRD_IMAGE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'images', 'ai_third_image.jpg')
AI_FOURTH_IMAGE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'images', 'ai_fourth_image.jpg')
KP_FILE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'files', 'KP.txt')

app = Flask(__name__)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return float(file.read().strip())

def write_file(file_path, value):
    with open(file_path, 'w') as file:
        file.write(str(value))

def get_battery_level():
    try:
        with open(BATTERY_FILE_PATH, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return -1
    except ValueError:
        return -1

def get_voltage():
    try:
        with open(VOLTAGE_FILE_PATH, 'r') as file:
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
    try:
        last_modified = os.path.getmtime(AI_FIRST_IMAGE_PATH)
        return jsonify({"last_modified": last_modified})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/image_first')
def get_image_first():
    try:
        return send_file(AI_FIRST_IMAGE_PATH)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


@app.route('/image/last_modified_second/')
def image_last_modified_second():
    try:
        last_modified = os.path.getmtime(AI_SECOND_IMAGE_PATH)
        return jsonify({"last_modified": last_modified})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/image_second')
def get_image_second():
    try:
        return send_file(AI_SECOND_IMAGE_PATH)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/image/last_modified_third/')
def image_last_modified_third():
    try:
        last_modified = os.path.getmtime(AI_THIRD_IMAGE_PATH)
        return jsonify({"last_modified": last_modified})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/image_third')
def get_image_third():
    try:
        return send_file(AI_THIRD_IMAGE_PATH)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/image/last_modified_fourth/')
def image_last_modified_fourth():
    try:
        last_modified = os.path.getmtime(AI_FOURTH_IMAGE_PATH)
        return jsonify({"last_modified": last_modified})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/image_fourth')
def get_image_fourth():
    try:
        return send_file(AI_FOURTH_IMAGE_PATH)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/values/contrast_value')
def get_contrast_value():
    try:
        contrast_value = read_file(CONTRAST_FILE_PATH)
        return jsonify({"contrast_value": contrast_value})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except ValueError:
        return jsonify({"error": "Invalid contrast value"}), 400
    
@app.route('/values/steering_angle')
def get_steering_angle():
    try:
        steering_angle = read_file(STEERING_ANGLE_FILE_PATH)
        return jsonify({"contrast_value": steering_angle})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except ValueError:
        return jsonify({"error": "Invalid contrast value"}), 400

@app.route('/control_car')
def control_car():
    return render_template('control_car.html', KP_value = read_file(KP_FILE_PATH))

@app.route('/save_KP_value', methods=['POST'])
def save_contrast_value():
    if request.method == 'POST':
        KP = request.get_json()["KP"]
        write_file(KP_FILE_PATH, KP)
        return "OK", 200
    return "Method not allowed", 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)