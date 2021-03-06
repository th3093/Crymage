# encode and decode messages into and from pictures with .png file format
from PIL import Image
from PIL import ImageChops


# read message from .txt file
# Input:    path as string containing path of file
# Output:   message as string containing message from file
def __read_message(path):
    with open(path, 'r') as message_file:
        __message = message_file.read()
    return __message


# encrypt message to nested list of Unicode value minus faktor 97 (value of lower 'a'); e.g. Hello -> 'Hel' 'lo '
# -> [['H','e','l'],['l','o','']] -> [[-25, 4, 11], [11, 14, 0]]
# Input:    message as string containing message from file
# Output:   enc as nested list of integers
def __encrypt_message(message):
    __enc = []
    __splitted_message = [message[i:i+3] for i in range(0, len(message), 3)]
    for block in __splitted_message:
        __current = []
        for x in block:
            __current.append((ord(x)-97))
        while len(__current) < 3:
            __current.append(0)
        __enc.append(__current)
    return __enc


# decrypt message from nested list of Unicode to string
# Input:    enc as nested list of integers
# Output:   dec as string of decrypted message
def __decrypt_message(enc):
    __dec = ''
    for block in enc:
        __dec += ''.join(chr(block[i]+97) for i in range(3))
    return __dec


# change RGB values of original image by adding the values of enc and creating new image
# Input:    img as PIL.Image.Image object containing the original image
#           enc as nested list of integers
# Output:   new_image as PIL.Image.Image object containing the new encrypted image
def __change_create(org_img, enc):
    __new_image_data = []
    __new_image = Image.new(org_img.mode, org_img.size)
    while len(enc) < len(org_img.getdata()):
        enc.append([0, 0, 0])
    for count, pixel_color in enumerate(org_img.getdata()):
        __orig_color_list = list(pixel_color)
        __changed_color_list = [__orig_color_list[i]+enc[count][i] for i in range(3)]
        for c in range(3):
            if __changed_color_list[c] > 255:
                __changed_color_list[c] %= 255
        __new_image_data.append(tuple(__changed_color_list))
    __new_image.putdata(__new_image_data)
    return __new_image


# get the difference of the original reference image and the encrypted one
# Input:    org_img as original PIL.Image.Image object as reference
#           enc_img as encrypted PIL.Image.Image object
# Output:   enc_list as list of integers
def __changed_colors(org_img, enc_img):
    __enc_list = []
    __diff = ImageChops.difference(org_img, enc_img)
    for el in __diff.getdata():
        if el != (0, 0, 0):
            __enc_list.append(list(el))
        else:
            break
    return __enc_list


# main procedure for encrypting
# Input:    msg_path as string containing path of message file
#           org_img as PIL.Image.Image object
# Output:   enc_img as PIL.Image.Image object containing encrypted image
def encrypt_picture(msg_path, org_path, out_path):
    msg_path.replace('/', '\\')
    org_path.replace('/', '\\')
    out_path.replace('/', '\\')
    __org_img = Image.open(org_path)
    __org_img.convert('RGB')
    __msg = __read_message(msg_path)
    __enc_list = __encrypt_message(__msg)
    __enc_img = __change_create(__org_img, __enc_list)
    __enc_img.save(out_path)
    __enc_img.show()
    return


# main procedure for decrypting
# Input:    org_img as PIL.Image.Image object containing original image for reference
#           enc_img as PIL.Image.Image object containing encrypted image
# Output:   dec_msg as string containing decrypted message
def decrypt_picture(org_path, enc_path):
    org_path.replace('/', '\\')
    enc_path.replace('/', '\\')
    __org_img = Image.open(org_path)
    __org_img.convert('RGB')
    __enc_img = Image.open(enc_path)
    __enc_img.convert('RGB')
    __en_li = __changed_colors(__org_img, __enc_img)
    __dec_msg = __decrypt_message(__en_li)
    return __dec_msg


if __name__ == '__main__':

    __original_path = '../examples/key_image_1.png'
    __output_path = '../examples/encrypted_1_preview.png'
    __message_path = '../examples/message.txt'
    __encrypted_path = '../examples/encrypted_1_preview.png'

    while True:
        try:
            __choose = str(input('[e]ncrypt or [d]ecrypt?'))
            if __choose not in ['e', 'd']:
                raise AttributeError
            else:
                break
        except AttributeError:
            pass

    if __choose == 'e':
        encrypt_picture(__message_path, __original_path, __output_path)

    elif __choose == 'd':
        __dmsg = decrypt_picture(__original_path, __encrypted_path)
        print(__dmsg)


