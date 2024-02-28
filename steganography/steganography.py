# Convert characters into 8-bit binary form using ASCII value of characters
def generate_binary_data(data):
    binary_data_list = []
    for char in data:
        binary_data_list.append(format(ord(char), '08b'))
    return binary_data_list

# Modify pixels according to the 8-bit binary data and return the modified image data
def modify_pixels(image_pixels, data):
    binary_data_list = generate_binary_data(data)
    data_length = len(binary_data_list)
    image_data = iter(image_pixels)

    for i in range(data_length):
        pixels = [value for value in image_data.__next__()[:3] +
                                 image_data.__next__()[:3] +
                                 image_data.__next__()[:3]]

        for j in range(0, 8):
            if (binary_data_list[i][j] == '0' and pixels[j] % 2 != 0):
                pixels[j] -= 1
            elif (binary_data_list[i][j] == '1' and pixels[j] % 2 == 0):
                if pixels[j] != 0:
                    pixels[j] -= 1
                else:
                    pixels[j] += 1

        if i == data_length - 1:
            if pixels[-1] % 2 == 0:
                if pixels[-1] != 0:
                    pixels[-1] -= 1
                else:
                    pixels[-1] += 1
        else:
            if pixels[-1] % 2 != 0:
                pixels[-1] -= 1

        pixels = tuple(pixels)
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]

# Encode data into image
def encode_data_into_image(image, data):
    width = image.size[0]
    (x, y) = (0, 0)

    for pixel in modify_pixels(image.getdata(), data):
        image.putpixel((x, y), pixel)
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1

# Decode the data from the image
def decode(image):
    decoded_data = ''
    image_data = iter(image.getdata())

    while True:
        pixels = [value for value in image_data.__next__()[:3] +
                             image_data.__next__()[:3] +
                             image_data.__next__()[:3]]

        binary_string = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                binary_string += '0'
            else:
                binary_string += '1'

        decoded_data += chr(int(binary_string, 2))
        if pixels[-1] % 2 != 0:
            return decoded_data


# Define the delimiter
DELIMITER = "&^@~&%$!"

def encode_data_with_password(image, data, password):
    # Convert password, data, and delimiter to binary
    password_binary = ''.join(format(ord(char), '08b') for char in password)
    data_binary = ''.join(format(ord(char), '08b') for char in data)
    delimiter_binary = ''.join(format(ord(char), '08b') for char in DELIMITER)
    
    # Combine password, delimiter, and data
    data_with_password = f"{password_binary}{delimiter_binary}{data_binary}"
    
    # Encode combined data into the image
    encode_data_into_image(image, data_with_password)

def decode_with_password(image, password):
    raw_data = decode(image)
    
    # Convert password and delimiter to binary
    password_binary = ''.join(format(ord(char), '08b') for char in password)
    delimiter_binary = ''.join(format(ord(char), '08b') for char in DELIMITER)
    
    # Split raw data into password and message using the delimiter
    password_end_index = raw_data.find(delimiter_binary)
    if password_end_index != -1:
        decoded_password = raw_data[:password_end_index]
        message_binary = raw_data[password_end_index + len(delimiter_binary):]
        
        # Check if the decoded password matches the provided password
        if decoded_password == password_binary:
            message = ''.join(chr(int(message_binary[i:i+8], 2)) for i in range(0, len(message_binary), 8))
            return message
        else:
            return None 
    else:
        return None
        
def has_password(image):
    raw_data = decode(image)
    
    delimiter_binary = ''.join(format(ord(char), '08b') for char in DELIMITER)
    
    # Check if the delimiter exists in the raw data
    if delimiter_binary in raw_data:
        return True
    else:
        return False
