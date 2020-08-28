import flask
from flask import Flask, request, render_template
import numpy as np
from PIL import Image
import json
from tensorflow.keras.models import load_model
from tensorflow.config.experimental import set_visible_devices
app = Flask(__name__)

@app.route("/")
def index():
    return flask.render_template('index.html')


@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method == 'POST':

        # get uploaded image
        file = request.files['image']
        if not file:
            return render_template('index.html', label="No file uploaded")

        # read file as pil image
        # apply transforms and convert into tensor
        img = Image.open(file)
        img = img.resize((80, 60))
        img = img.transpose(Image.ROTATE_90)
        img = np.asarray(img)
        img = np.array([img])
        
        prediction_output = ['{:.2f}%'.format(x*100) for x in model.predict(img)[0]]
        
        return render_template('index.html', prediction_output=prediction_output)


if __name__ == '__main__':
    # Carregar o modelo
    set_visible_devices([], 'GPU') # garante que o modelo vai usar a CPU, para evitar erros de incompatibilidade CUDA/CUDNN
    model = load_model('static/modelo')
    # Roda o webapp
    app.run(debug=True)
