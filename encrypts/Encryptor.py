from PIL import Image, ImageDraw
import random
import time


en_blue = 240   #0b11110000
en_red = 248    #0b11111000
en_green = 254  #0b11111110
for_encode = [en_red, en_green, en_blue]

dec_blue = 15   #0b00001111
dec_red = 7     #0b00000111
dec_green = 1   #0b00000001
for_decode = [dec_red, dec_green, dec_blue]

MAX_INTERVAL = 100   # максимальный интервал между зашифрованными пикселями 
                
                
# разделить байт на три части по 4, 3 и 1 биту
def split_byte(byte: int):
    encoded = bin(byte)[2:]
    encoded = encoded.zfill(8)
    result = []
    result.append(int('0b'+encoded[:3], 2))     #красный
    result.append(int('0b'+encoded[3:4], 2))    #зеленый
    result.append(int('0b'+encoded[4:], 2))     #синий
    return result


# записать разделенный байт в пиксель
def write_byte(pixel, splited_byte):
    """
    pixel -- пиксель в представлении трех чисел
    splited_byte -- байт, раздлеленный на три числа после
обработки split_byte
    """
    result = []
    for i in range(3):
        encoded = pixel[i] & for_encode[i]
        encoded = encoded | splited_byte[i]
        result.append(encoded)
    return tuple(result)   


# выдать последовательность пикселей по сиду
def pixel_generator(rows, columns, seed):
    random.seed(seed)
    last_pixel_in_row = 0
    last_pixel_in_column = 2
    while last_pixel_in_row != rows:
        last_pixel_in_column += random.randint(5, MAX_INTERVAL)
        if last_pixel_in_column >= columns:
            last_pixel_in_column %= columns
            last_pixel_in_row += 1
        if last_pixel_in_row == rows:
            return
        yield (last_pixel_in_column, last_pixel_in_row)


# сгенерировать шум
def make_some_noise(image):
    noise_gen = pixel_generator(image.size[1], image.size[0], time.time())
    pixels = image.load()
    draw = ImageDraw.Draw(image)
    for pixel in noise_gen:
        digit = random.randint(0, 255)
        digit = split_byte(digit)
        digit = write_byte(pixels[pixel], digit)
        draw.point(pixel, digit)


# алгоритм зашифровки
def encrypt(image, text, seed = None, noise = True):
    if noise:
        make_some_noise(image)
    text_len = len(text)
    image_row = image.size[1]           # высота изображения
    image_column = image.size[0]        # ширина изображения
    if image_row * image_column / text_len < MAX_INTERVAL:
        raise ValueError("Слишком длинный текст")
    if seed == None:
        seed = random.randint(0, 255)
    pixels = image.load()       # список пикселей
    filename = image.filename   # название файла
    draw = ImageDraw.Draw(image)# объект редактирования изображения

    # зашифровка сида
    encrypted = split_byte(seed)
    encrypted = write_byte(pixels[(0, 0)], encrypted)
    draw.point((0, 0), encrypted)

    # запись сообщения в пиксели
    bytes_count = 0 #количество байт в сообщении
    pixel_gen = pixel_generator(seed, image_row, image_column)
    for char in text:
        char = char.encode('utf-8')
        for byte in char:
            bytes_count += 1
            pixel = next(pixel_gen)
            enctypted = split_byte(byte)
            encrypted = write_byte(pixels[pixel], enctypted)
            draw.point(pixel, encrypted)

    # зашифровка длины сообщения (в байтах)
    encrypted = split_byte(bytes_count)
    encrypted = write_byte(pixels[(1, 0)], encrypted)
    draw.point((1, 0), encrypted)
    return image


    
