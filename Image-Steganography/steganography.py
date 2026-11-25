
from PIL import Image

def encode_message(image, message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '00000000'

    image = image.convert("RGB")
    pixels = list(image.getdata())

    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message is too large for this image.")

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        new_pixel = []

        for channel in pixel:
            if bit_index < len(binary_message):
                channel = (channel & 254) | int(binary_message[bit_index])
                bit_index += 1

            new_pixel.append(channel)

        new_pixels.append(tuple(new_pixel))

    image.putdata(new_pixels)
    return image

def decode_message(image):
    image = image.convert("RGB")
    bits = ""

    for pixel in image.getdata():
        for channel in pixel:
            bits += str(channel & 1)

    message = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]

        if len(byte) < 8:
            break

        char = chr(int(byte, 2))

        if char == '\0':
            break

        message += char

    return message

def calculate_capacity(image):
    image = image.convert("RGB")

    total_bits = image.width * image.height * 3

    # Reserve 8 bits for the end marker
    usable_bits = total_bits - 8

    return max(0, usable_bits // 8)
