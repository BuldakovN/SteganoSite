import deepapi as DA
from encrypts import Decryptor, Encryptor
from encrypts.Decryptor import decrypt
from encrypts.Encryptor import encrypt
import requests
from PIL import Image, ImageDraw
import os
import datetime


class Controller:
    def __init__(self):
        pass


    def to_encrypt(self, text, filename):
        """
        Зашифровать представленный текст в представленное изображение

        text: строка для шифровки

        filename: название файла для зашифровки
        """
        image = Image.open(os.path.abspath(filename))
        image = Encryptor.encrypt(image, text)
        image.save('static/b.jpg')
        print(os.path.abspath(filename))
        return image


    def to_encrypt_with_generated_image(self, text, theme, filename=None):
        """
        Зашифровать представленный текст в изображение,
        сгенерированное нейросетями
        
        text: строка для шифровки
        
        request: запрос для генерации изображения
        """
        if filename is None:
            filename = f"static/deepapi_image_{datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S')}.png"
        # сохранение изображения
        image = DA.text_to_image(theme)
        url = image['output_url']
        image = requests.get(url)
        # если изображение не получено
        if not image.ok:
            with open('log error.txt', 'a') as f:
                f.write("Ошибка получения изображения " + theme + '\n')
            raise requests.exceptions.ConnectionError
        # сохранение изображения
        with open(filename, 'wb') as f:
            f.write(image.content)
        # преобразование изображения в формат PNG
        image = Image.open(filename, formats=["JPEG"])
        image.save(filename, "PNG")
        # кодирование изображения
        image = Image.open(filename)
        Encryptor.encrypt(image, text)
        image.save(os.path.abspath(filename))
        return image


    def to_decrypt(self, image):
        """
        Расшифровать зашифрованный в изображении текст

        image -- изображение для расшифровки
        """
        if type(image) == str:
            image = Image.open(os.path.abspath(image))
        try:
            return Decryptor.decrypt(image)
        except Exception as e:
            with open('log error.txt', 'a') as f:
                f.write("Ошибка декодирования " + '\n')
            return None
