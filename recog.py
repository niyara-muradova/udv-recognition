from PIL import Image
import pytesseract
import cv2
import os

def photo_recog(filename):
    image = f'uploads/{filename}'

    preprocess = "thresh"

    # загрузить образ и преобразовать его в оттенки серого
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.THRESH_OTSU)[1]

    # если нужно медианное размытие, чтобы удалить шум
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    # сохраним временную картинку в оттенках серого, чтобы можно было применить к ней OCR

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    # загрузка изображения в виде объекта image Pillow, применение OCR, а затем удаление временного файла
    text = pytesseract.image_to_string(Image.open(filename), lang='eng')

    extracted = text[text.index('ID'):]

    os.remove(filename)

    return extracted
