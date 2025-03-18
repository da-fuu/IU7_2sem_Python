from PIL import Image
from crc8 import crc8


# Прочитать байт(побитно из 8 байт) из файла по индексу
def read_byte(array, ind):
    byte = 0
    for i in range(8):
        byte |= (array[ind*8 + i] & 1) << (7 - i)
    return byte.to_bytes(1, 'big')


# Расшифровать строку из файла
def decode_file(filename: str):
    with Image.open(filename) as img:
        img_bytes = img.tobytes()
    if len(img_bytes) < 8 * 3:
        return
    length = read_byte(img_bytes, 0) + read_byte(img_bytes, 1)
    length = int.from_bytes(length, 'big') + 3
    if len(img_bytes) < length * 8:
        return
    bytestring = b''
    for i in range(2, length - 1):
        bytestring += read_byte(img_bytes, i)
    if crc8(bytestring).digest() != read_byte(img_bytes, length - 1):
        return
    return bytestring.decode('utf-8')


# Зашифровать байтстроку в массив байтов
def encode_array(array, bytestring):
    counter = 0
    for byte in bytestring:
        for i in range(7, -1, -1):
            if byte >> i & 1:
                array[counter] |= 1
            else:
                array[counter] &= 2 ** 8 - 2
            counter += 1


# Зашифровать строку в файл
def encode_file(filename: str, string: str):
    bytestring = string.encode('utf-8')
    length = len(bytestring)
    if length >= 2 ** 16:
        return False
    bytestring = length.to_bytes(2, 'big') + bytestring + crc8(bytestring).digest()
    length += 3
    with Image.open(filename) as img:
        img_bytes = bytearray(img.tobytes())
        if len(img_bytes) < length * 8:
            return False
        encode_array(img_bytes, bytestring)
        img.frombytes(img_bytes)
        img.save(filename)
    return True
