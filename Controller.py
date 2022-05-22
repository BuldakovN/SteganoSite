import deepapi as DA
from encrypts import Decryptor, Encryptor
from encrypts.Decryptor import decrypt
from encrypts.Encryptor import encrypt
import requests
from PIL import Image


class Controller:
    def __init__(self, token):
        pass


    def to_encrypt(self, text, filename):
        """
        Зашифровать представленный текст в представленное изображение

        text: строка для шифровки

        filename: название файла для зашифровки
        """
        image = Image.open(filename)
        Encryptor.encrypt(image, text)
        return image


    def to_encrypt_with_generated_image(self, text, request):
        """
        Зашифровать представленный текст в изображение,
        сгенерированное нейросетями
        
        text: строка для шифровки
        
        request: запрос для генерации изображения
        """
        # сохранение изображения
        image = DA.text_to_image(request)
        url = image['output_url']
        image = requests.get(url)
        # если изображение не получена
        if not image.ok:
            raise requests.exceptions.ConnectionError
        # сохранение изображения
        with open("deepapi_image.jpg", 'wb') as f:
            f.write(image.content)
        # кодирование изображения
        image = Image.open("deepapi_image.jpg")
        Encryptor.encrypt(image, text)
        return image


    def to_decrypt(self, image):
        """
        Расшифровать зашифрованный в изображении текст

        image -- изображение для расшифровки
        """
        return Decryptor.decrypt(image)
