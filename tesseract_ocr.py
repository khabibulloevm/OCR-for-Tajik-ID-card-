import cv2
import pytesseract
import re
import datetime

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def detectIdInfo(src):
    img = cv2.imread(src)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # print(pytesseract.image_to_string(img))

    # Detecting Words
    boxes = pytesseract.image_to_data(img, lang='tgk+eng')
    data = []
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            # print(b)
            if len(b) == 12:
                if len(b[11]) == 9 and b[11][0].isalpha() and b[11][1:].isdigit():
                    data.append(b[11])

                if len(b[11]) == 9 and b[11].isdigit():
                    b[11] = 'A' + b[11][1:]
                    data.append(b[1])

                if re.match(r'^[А-Я,Ҷ,Ҳ,Қ,Ғ,Ӣ\s]+$', b[11]) and len(b[11]) > 2:
                    data.append(b[11])

                try:
                    datetime.datetime.strptime(b[11], '%d.%m.%Y')
                    data.append(b[11])
                except ValueError:
                    pass

                if len(b[11]) == 13 and b[11].isdigit():
                    data.append(b[11])

                if 2 <= len(b[11]) <= 3:
                    if b[11] == "З/F" or b[11] == "М/M" or "З" in b[11] or "М" in b[11]:
                        data.append(b[11][0])

    # print(data)
    # print(boxes)
    return data


'''
    info = {
        'passportNum': data[0],
        'surname': data[1],
        'name': data[2],
        'patronymic': data[3],
        'birth_date': data[4],
        'issue_date': data[5],
        'expiration_date': data[6]

    }
'''

print(detectIdInfo('images/11.jpg'))

# print(detectIdInfo('images/photo.jpg'))
