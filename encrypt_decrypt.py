from PIL import Image, ImageDraw
import random

en_blue = 240   #0b11110000
en_red = 248   #0b11111000
en_green = 254   #0b11111110
for_encode = [en_red, en_green, en_blue]

dec_blue = 15    #0b00001111
dec_red = 7     #0b00000111
dec_green = 1     #0b00000001
for_decode = [dec_red, dec_green, dec_blue]

#шифрование
def encrypt(image, text, seed = None):
    if '~' in text:
        raise ValueError("Недопустиый символ (~)")
    text += '~'
    pixels_count = image.size[0]*image.size[1]
    if pixels_count/len(text) < 20:
        raise ValueError("Слишком длинный текст")
    if seed == None:
        seed = random.randint(100, 255)

    pixels = image.load()
    filename = image.filename 
    draw = ImageDraw.Draw(image)
    
    #в первый пиксель записывается сид
    draw.point((0, 0), record_seed(pixels[0, 0], seed))
    
    #запись сообщения в пиксели
    pixel_gen = pixel_generator(seed, image.size[0], image.size[1])
    for i in text:
        splited_char = split(i)
        pixel = next(pixel_gen)
        draw.point(pixel, record(pixels[pixel], splited_char))

    
    

#разделить бинарное представление символа на три группы по 4, 3 и 1 биту
def split(char):
    encoded = char.encode('windows-1251')[0]
    encoded = bin(encoded)[2:]
    encoded = encoded.zfill(8)
    result = []
    result.append(int('0b'+encoded[:3], 2)) #красный
    result.append(int('0b'+encoded[3:4], 2))  #зеленый
    result.append(int('0b'+encoded[4:], 2))  #синий
    return result


#записать группы битов в значеные пиксели
def record(old, new):
    result = [0 for i in range(3)]
    for i in range(3):
        result[i] = (old[i] & for_encode[i]) | new[i]
    return tuple(result)


#записать сид в пиксель
def record_seed(pixel, seed):
    new = [int(i) for i in str(seed)]
    result = [0 for i in range(3)]
    for i in range(3):
        result[i] = (pixel[i] & int('0b11110000', 2)) | new[i]
    return tuple(result)


#выдать последовательность пикселей по сиду
def pixel_generator(seed, columns, rows):
    random.seed(seed)
    last_pixel_in_row = 0
    last_pixel_in_column = 0
    while True:
        last_pixel_in_column += random.randint(5, 20)
        if last_pixel_in_column >= columns:
            last_pixel_in_column %= columns
            last_pixel_in_row += 1
        yield (last_pixel_in_column, last_pixel_in_row)


#получение сида из пикселя
def get_seed(pixel):
    result = 0
    for i in range(3):
        result += (pixel[i] & int('0b1111', 2))*(10**(2-i))
    return result


#чтение символа из пикселя
def read(pixel):
    result = '0b'
    result += bin(pixel[0])[2:].zfill(8)[5:]
    result += bin(pixel[1])[2:].zfill(8)[7:]
    result += bin(pixel[2])[2:].zfill(8)[4:]
    result = int(result, 2)
    result = bytes([result]).decode('windows-1251')
    return result

# декодирование
def decrypt(image):
    i = 0
    result = ""
    pixels = image.load()
    seed = get_seed(pixels[0,0])
    pixel_gen = pixel_generator(seed, image.size[0], image.size[1])
    while True:
        pixel = next(pixel_gen)
        char = read(pixels[pixel])
        if (char == '~'):
            break
        result += char
        i += 1
        if (i==1000):
            print('амогус')
            break
    return result


if __name__ == '__main__':
    img = Image.open("test1.png")
    encrypt(img, "Привет, как дела?")
    print("декодирование") 
    print(decrypt(img))
    
