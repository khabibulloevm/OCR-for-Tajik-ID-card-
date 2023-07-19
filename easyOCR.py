import easyocr
import cv2
import re
import datetime


def easyOCR(image_path):
    image = cv2.imread(image_path)
    reader = easyocr.Reader(['tjk', 'en'], gpu=False)
    results = reader.readtext(image, detail=True, contrast_ths=0.3, adjust_contrast=0.7, width_ths=0.3)

    # Так как EasyOCR в качество выхода вернет нам список состоящий из кортежей (bbox, text, confidence),
    # превращаем эти кортежи в списки, чтобы в дальнейшем изменять какие-то данные при необходимости

    results_list = [list(tup) for tup in results]

    # Создаем пустой список в котором будет добавить значение нужных полей паспорта
    data = []
    # Поиск номер паспорта по указанным условия
    for item in results_list:
        if len(item[1]) == 9:
            if len(item[1]) == 9 and item[1][1:].isdigit() and item[1][:1].isalpha():
                data.append(item[1])

            if len(item[1]) == 9 and item[1].isdigit():
                item[1] = 'A' + item[1][1:]
                data.append(item[1])

        # Поиск фамилии, имени и отчество
        if re.match(r'^[А-Я,Ҷ,Ҳ,Қ,Ғ,Ӣ\s]+$', item[1]) and len(item[1]) > 2:
            data.append(item[1])

        # Поиск всех дат которые в паспорте (дата рождения, дата выдачи и дата окончания срока)
        try:
            datetime.datetime.strptime(item[1], '%d.%m.%Y')
            data.append(item[1])
        except ValueError:
            pass

        # Поиск единого национального номера (ID)
        if len(item[1]) == 13 and item[1].isdigit():
            data.append(item[1])

        # Поиск значение поля "пол"
        if 2 <= len(item[1]) <= 3 and item[1] == "З/F" or item[1] == "М/M":
            data.append(item[1][0])

    info = {
        'passportNum': data[8],
        'surname': data[0],
        'pname': data[1],
        'patronymic': data[2],
        'gender': data[3],
        'birth_date': data[4],
        'issue_date': data[5],
        'expiration_date': data[6],
        'national_id': data[7]
    }

    return info

'''
# Пример использования
image_path = 'images/11.jpg'
res = easyOCR(image_path)

# Можно сохарнить распознованные данные в txt
# Путь к новому файлу .txt
txt_file_path = "ocr_result.txt"

# Создание нового файла .txt и запись данных
with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
    for key, value in res.items():
        txt_file.write(f"{key}: {value}\n")

print("Словарь успешно записан в текстовый файл.")

'''
