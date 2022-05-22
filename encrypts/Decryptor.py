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


# объединить три части по 4, 3 и 1 биту в целый байт
def join_byte(pixels: list):
    """
    pixels: list -- пиксель 
    """
    result = "0b"
    result += bin(pixels[0])[2:].zfill(3)
    result += bin(pixels[1])[2:].zfill(1)
    result += bin(pixels[2])[2:].zfill(4)
    return int(result, 2)


# считать из пикселя разделенный байт
def read_byte(pixel):
    result = []
    for i in range(3):
        result.append(pixel[i] & for_decode[i])
    return result


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


# алгоритм расшифровки
def decrypt(image):
    pixels = image.load()
    image_row = image.size[1]           # высота изображения
    image_column = image.size[0]        # ширина изображения

    # чтение сида
    decrypted = read_byte(pixels[(0, 0)])
    seed = join_byte(decrypted)

    # чтение длины сообщения
    decrypted = read_byte(pixels[(1, 0)])
    bytes_count = join_byte(decrypted)

    # чтение сообщения из изображения
    pixel_gen = pixel_generator(seed, image_row, image_column)
    bytes_list = [] # список байт сообщения
    for _ in range(bytes_count):
        pixel = next(pixel_gen)
        decrypted = read_byte(pixels[pixel])
        decrypted = join_byte(decrypted)
        bytes_list.append(decrypted)
    return bytes(bytes_list).decode('UTF-8')
        
