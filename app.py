from flask import Flask, render_template, request, jsonify
from image_ocr import easyOCR
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/image_ocr', methods=['POST']) # чтобы использовать алгоритм tesseract меняйте на '/tesseract_ocr'
def process_image_route():
    # Получение загруженного изображения
    image = request.files['file']
    # Сохранение изображения на диск
    image.save('uploaded_image.jpg')
    # Обработка изображения и распознавание текста
    text = easyOCR('uploaded_image.jpg')
    # Удаление сохраненного изображения
    os.remove('uploaded_image.jpg')
    print("iamge processing is over!!!")
    return text

if __name__ == '__main__':
    app.run(debug=True)

'''
 # Возвращаем результаты распознавания текста
    info = {
        'passportNum': text['passportNum'],
        'surname': text['surname'],
        'pname': text['pname'],
        'patronymic': text['patronymic'],
        'birth_date': text['birth_date'],
        'issue_date': text['issue_date'],
        'expiration_date': text['expiration_date'],
        'national_id': text['national_id']

    }
'''

