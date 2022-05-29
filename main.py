import numpy as np
import cv2

def receive_msg(img,value_key):
    height, width, channel = img.shape
    lista = []
    i_width = 1
    while value_key != 0:
        last_pixel = img[height-1,width-i_width,2]
        bit_last_pixel = bitfield(last_pixel)
        lista.append(bit_last_pixel[-1])
        value_key = value_key - 1
        i_width = i_width + 1
    print(converter_mensagem(lista))

def add_msg_img(img,bits_int,debug):
    height, width, channel = img.shape
    i_height = 1
    i_width = 1
    for bit_atual in bits_int:
        last_pixel = img[height-i_height,width-i_width,2]
        bit_last_pixel = bitfield(last_pixel)
        if bit_last_pixel[-1] != bit_atual:
            if last_pixel == 0:
                img[height-i_height,width-i_width,2] = img[height-i_height,width-i_width,2]+1
                if debug:
                    print(f"Bit  {last_pixel} alterado para {last_pixel+1}")

            else:
                img[height-i_height,width-i_width,2] = img[height-i_height,width-i_width,2]-1
                if debug:
                    print(f"Bit  {last_pixel} alterado para {last_pixel-1}")

        if debug:
            last_pixel = img[height-i_height,width-i_width,2]
            bit_last_pixel = bitfield(last_pixel)
            if bit_last_pixel[-1] != bit_atual:
                print(f"Necessário alterar de {bit_last_pixel[-1]} para {bit_atual}")

        i_width = i_width + 1

    return img

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]

def gerar_mensagem(mensagem):
    lista = []
    for m in mensagem:
        val = ord(m)
        bits = bitfield(val)

        if len(bits) < 8:
            for a in range(8-len(bits)):
                bits.insert(0,0)
        lista.append(bits)
    arr = np.array(lista)
    arr = arr.flatten()
    return arr


def converter_mensagem(saida):
    bits = np.array(saida)
    mensagem_out = ''
    bits = bits.reshape((int(len(saida)/8), 8))
    for b in bits:
        sum = 0
        for i in range(8):
            sum += b[i]*(2**(7-i))
        mensagem_out += chr(sum)
    return mensagem_out

texto = "comprei na pre venda e me ferrei, bait do ano"
arrayBits = gerar_mensagem(texto)
textoTraduzido = converter_mensagem(arrayBits)

img=cv2.imread("Cyberpunk_2077_capa.png")
cv2.imshow("Principal",img)
add_msg_img(img,arrayBits,True)
receive_msg(img,len(arrayBits))
cv2.imshow("Modificado",img)
cv2.waitKey(0)