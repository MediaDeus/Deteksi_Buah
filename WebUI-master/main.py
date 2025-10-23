from flask import Flask, render_template, request
from flask import jsonify
from werkzeug.utils import secure_filename

from flask import Response

from os import listdir

import detect_image
# import miscellaneous modules
import os

# set tf backend to allow memory to grow, instead of claiming everything
#import tensorflow as tf

app = Flask(__name__, template_folder='template')
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    models = [f for f in listdir('./static/models')]

    return render_template('index.html', models=models)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global filename
    if request.method == 'POST':
        f = request.files['file']
        save_dir = os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        filename = f.filename
        f.save(save_dir)
        print(save_dir)
        return jsonify({"result": save_dir})

model = ""
filename = ""
#buah = ""

# @app.route('/get_buah', methods=['GET', 'POST'])
# def get_buah():
#     global buah
#     buah_name = request.args.get("buah_name")
#     buah_path = './static/models/'+buah_name
#     buah = detect_image.get_buah(buah_path)
#     return jsonify({"result": buah_name})

@app.route('/get_model', methods=['GET', 'POST'])
def get_model():
    global model
    model_name = request.args.get("model_name")
    model_path = './static/models/'+model_name
    model = detect_image.get_model(model_path)
    return jsonify({"result": model_name})
    # buah_name = get_buah()
    # global model
    # model_name = request.args.get("model_name")
    # if buah_name == "Jeruk":
    #     model_path = './static/models/Jeruk/'+model_name
    #     model = detect_image.get_model(model_path)
    #     return jsonify({"result": model_name})
    # elif buah_name == "Mangga":
    #     model_path = './static/models/Mangga/'+model_name
    #     model = detect_image.get_model(model_path)
    #     return jsonify({"result": model_name})
    # else:
    #     model_path = './static/models/Pepaya/'+model_name
    #     model = detect_image.get_model(model_path)
    #     return jsonify({"result": model_name})

@app.route('/detect')
def detect_object():
    image_path = request.args.get('image_path')
    BuahMatang_conf = float(request.args.get('BuahMatang_conf'))
    BuahTidakMatang_conf = float(request.args.get('BuahTidakMatang_conf'))
    confidence_cutoff = {'BuahMatang': BuahMatang_conf, 'BuahTidakMatang': BuahTidakMatang_conf}
    print(image_path, BuahMatang_conf, BuahTidakMatang_conf)
    result = detect_image.detect(
        image_path, model, filename, confidence_cutoff)

    return jsonify(result)


if __name__ == '__main__':
    detect_image.init_tf()

    app.run(host='0.0.0.0', port='80')
