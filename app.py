from flask import Flask, render_template, request
from easyOCR import easyOCR
import os
import json


app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/easyOCR', methods=['POST'])
def process_image_route():
    # Получение загруженного изображения
    image = request.files['file']
    # Сохранение изображения на диск
    image.save('uploaded_image.jpg')
    # Обработка изображения и распознавание текста
    text = easyOCR('uploaded_image.jpg')
    # Удаление сохраненного изображения
    os.remove('uploaded_image.jpg')

    json_data = json.dumps(text, ensure_ascii=False)

    response = app.response_class(
        response=json_data,
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == '__main__':
    app.run()
