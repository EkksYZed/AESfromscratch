import os
import math
import copy

padding_needed = 0

# Define the S-box as a dictionary
s_box = {
    '00': '63', '01': '7c', '02': '77', '03': '7b', '04': 'f2', '05': '6b', '06': '6f', '07': 'c5', '08': '30', '09': '01', '0a': '67', '0b': '2b', '0c': 'fe', '0d': 'd7', '0e': 'ab', '0f': '76',
    '10': 'ca', '11': '82', '12': 'c9', '13': '7d', '14': 'fa', '15': '59', '16': '47', '17': 'f0', '18': 'ad', '19': 'd4', '1a': 'a2', '1b': 'af', '1c': '9c', '1d': 'a4', '1e': '72', '1f': 'c0',
    '20': 'b7', '21': 'fd', '22': '93', '23': '26', '24': '36', '25': '3f', '26': 'f7', '27': 'cc', '28': '34', '29': 'a5', '2a': 'e5', '2b': 'f1', '2c': '71', '2d': 'd8', '2e': '31', '2f': '15',
    '30': '04', '31': 'c7', '32': '23', '33': 'c3', '34': '18', '35': '96', '36': '05', '37': '9a', '38': '07', '39': '12', '3a': '80', '3b': 'e2', '3c': 'eb', '3d': '27', '3e': 'b2', '3f': '75',
    '40': '09', '41': '83', '42': '2c', '43': '1a', '44': '1b', '45': '6e', '46': '5a', '47': 'a0', '48': '52', '49': '3b', '4a': 'd6', '4b': 'b3', '4c': '29', '4d': 'e3', '4e': '2f', '4f': '84',
    '50': '53', '51': 'd1', '52': '00', '53': 'ed', '54': '20', '55': 'fc', '56': 'b1', '57': '5b', '58': '6a', '59': 'cb', '5a': 'be', '5b': '39', '5c': '4a', '5d': '4c', '5e': '58', '5f': 'cf',
    '60': 'd0', '61': 'ef', '62': 'aa', '63': 'fb', '64': '43', '65': '4d', '66': '33', '67': '85', '68': '45', '69': 'f9', '6a': '02', '6b': '7f', '6c': '50', '6d': '3c', '6e': '9f', '6f': 'a8',
    '70': '51', '71': 'a3', '72': '40', '73': '8f', '74': '92', '75': '9d', '76': '38', '77': 'f5', '78': 'bc', '79': 'b6', '7a': 'da', '7b': '21', '7c': '10', '7d': 'ff', '7e': 'f3', '7f': 'd2',
    '80': 'cd', '81': '0c', '82': '13', '83': 'ec', '84': '5f', '85': '97', '86': '44', '87': '17', '88': 'c4', '89': 'a7', '8a': '7e', '8b': '3d', '8c': '64', '8d': '5d', '8e': '19', '8f': '73',
    '90': '60', '91': '81', '92': '4f', '93': 'dc', '94': '22', '95': '2a', '96': '90', '97': '88', '98': '46', '99': 'ee', '9a': 'b8', '9b': '14', '9c': 'de', '9d': '5e', '9e': '0b', '9f': 'db',
    'a0': 'e0', 'a1': '32', 'a2': '3a', 'a3': '0a', 'a4': '49', 'a5': '06', 'a6': '24', 'a7': '5c', 'a8': 'c2', 'a9': 'd3', 'aa': 'ac', 'ab': '62', 'ac': '91', 'ad': '95', 'ae': 'e4', 'af': '79',
    'b0': 'e7', 'b1': 'c8', 'b2': '37', 'b3': '6d', 'b4': '8d', 'b5': 'd5', 'b6': '4e', 'b7': 'a9', 'b8': '6c', 'b9': '56', 'ba': 'f4', 'bb': 'ea', 'bc': '65', 'bd': '7a', 'be': 'ae', 'bf': '08',
    'c0': 'ba', 'c1': '78', 'c2': '25', 'c3': '2e', 'c4': '1c', 'c5': 'a6', 'c6': 'b4', 'c7': 'c6', 'c8': 'e8', 'c9': 'dd', 'ca': '74', 'cb': '1f', 'cc': '4b', 'cd': 'bd', 'ce': '8b', 'cf': '8a',
    'd0': '70', 'd1': '3e', 'd2': 'b5', 'd3': '66', 'd4': '48', 'd5': '03', 'd6': 'f6', 'd7': '0e', 'd8': '61', 'd9': '35', 'da': '57', 'db': 'b9', 'dc': '86', 'dd': 'c1', 'de': '1d', 'df': '9e',
    'e0': 'e1', 'e1': 'f8', 'e2': '98', 'e3': '11', 'e4': '69', 'e5': 'd9', 'e6': '8e', 'e7': '94', 'e8': '9b', 'e9': '1e', 'ea': '87', 'eb': 'e9', 'ec': 'ce', 'ed': '55', 'ee': '28', 'ef': 'df',
    'f0': '8c', 'f1': 'a1', 'f2': '89', 'f3': '0d', 'f4': 'bf', 'f5': 'e6', 'f6': '42', 'f7': '68', 'f8': '41', 'f9': '99', 'fa': '2d', 'fb': '0f', 'fc': 'b0', 'fd': '54', 'fe': 'bb', 'ff': '16'
}


def expand_key(key, rounds):
    rc=['01', '02', '04', '08', '10', '20', '40', '80', '1B', '36']

    key_grid = format_to_matrix(key)
    final_key=[]
    final_hex_key=[]
    final_hex_key+=key_grid
    final_key+=key_grid
    for k in range(0,rounds):
        new_key=[[0]*4,[0]*4,[0]*4,[0]*4]
        hex_key=[[0]*4,[0]*4,[0]*4,[0]*4]
        temp_column=[0]*4

        temp_column[0]=key_grid[-1][1]
        temp_column[1]=key_grid[-1][2]
        temp_column[2]=key_grid[-1][3]
        temp_column[3]=key_grid[-1][0]
        rcon=[rc[k],'0', '0', '0']
        for i in range(0,4):
            if len(temp_column[i]) < 2:
                 temp_column[i]='0'+temp_column[i]
            temp_column[i]=int(s_box[temp_column[i]], 16)^int(rcon[i],16)

            new_key[0][i]=temp_column[i]^int(key_grid[0][i],16)
            hex_key[0][i]=hex(temp_column[i]^int(key_grid[0][i],16))[2:]

        for j in range(1,4):
            for i in range(0,4):
                new_key[j][i]=new_key[j-1][i]^int(key_grid[j][i],16)
                if len(hex(new_key[j-1][i]^int(key_grid[j][i],16))[2:]) < 2:
                    hex_key[j][i]='0'+hex(new_key[j-1][i]^int(key_grid[j][i],16))[2:]
                else: 
                    hex_key[j][i]=hex(new_key[j-1][i]^int(key_grid[j][i],16))[2:]

        key_grid=hex_key

        final_key.extend(new_key)
        final_hex_key.extend(hex_key)

    return final_hex_key

Nr = 10  # Number of rounds (10 for AES128)

#EACH LIST IN KEY IS COLUMN
#EACH LIST IN INPUT IS ROW
# AES block size in bytes
BLOCK_SIZE = 16  # 128 bits = 16 bytes

def add_pkcs7_padding(hex_str):
        global padding_needed
        # If multiple of 32, then dummy block
        if len(hex_str) % 32 == 0:
            hex_str=hex_str+(16*'10')
        else:
            factor=len(hex_str) // 32
            padding_needed = 16*(factor+1) - len(hex_str) // 2
            padding=hex(padding_needed)[2:].zfill(2)
            padded_text=hex_str+(padding*padding_needed).zfill(2)
            hex_str=padded_text
        return hex_str



def format_to_matrix(hex_str):


        chunks = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]


        matrix = [chunks[i:i+4] for i in range(0, len(chunks), 4)]

        return matrix

def keygenerate():

    key_bytes = os.urandom(16)
    hex_key = key_bytes.hex()
    return hex_key



Mix_Matrix=[[2, 3, 1, 1],[1, 2, 3, 1],[1, 1, 2, 3],[3, 1, 1, 2]]

def multiply_by_2(v):
    s = int(v,16) << 1

    s &= int("ff", 16)
    if (int(v,16) & 128) != 0:
        s = s ^ int("1b", 16)
    return s


def multiply_by_3(v):
    return multiply_by_2(v) ^ int(v,16)


def mix_columns(grid):
    new_grid = [[], [], [], []]
    for j in range(4):
        col = [grid[i][j] for i in range(4)]
        col = mix_column(col)

        for i in range(4):
            col[i]=hex(col[i])[2:].zfill(2)

            new_grid[i].append(col[i])
    main_one=matrix_to_lists(new_grid)
    return main_one


def mix_column(column):
    r = [
        multiply_by_2(column[0]) ^ multiply_by_3(column[1]) ^ int(column[2],16) ^ int(column[3],16), 
        multiply_by_2(column[1]) ^ multiply_by_3(column[2]) ^ int(column[3], 16) ^ int(column[0], 16),

        multiply_by_2(column[2]) ^ multiply_by_3(column[3]) ^ int(column[0],16) ^ int(column[1],16),
        multiply_by_2(column[3]) ^ multiply_by_3(column[0]) ^ int(column[1], 16) ^ int(column[2],16)
    ]
    return r

def matrix_to_lists(matrix):

    column_lists = [[] for _ in range(len(matrix[0]))]


    for row in matrix:
        for i, element in enumerate(row):

            column_lists[i].append(element)
    
    return column_lists



def aes_encrypt(plaintext, key):
    

    hex_result = ''.join(hex(ord(char))[2:].zfill(2) for char in plaintext)

    # Add PKCS#7 padding
    hex_result = add_pkcs7_padding(hex_result)


    expanded_key=expand_key(key,10)
    # Format the hexadecimal string into a 4x4 matrix
    input_matrix = format_to_matrix(hex_result)

    #FIRST KEY
    roundkey = [[0]*4 for _ in range(4)]
    resultant1 = [[0]*4 for _ in range(4)]
    encrypted_blocks =[[0]*4 for _ in range(4)]
    encrypted_output = []
    blocks=len(hex_result)//32
    encrypted_string=''
    for block in range(blocks):
        ipslicer1=4*block
        ipslicer2=4*(block+1)

        input_block=input_matrix[ipslicer1:ipslicer2]

        for no in range(0,10):
            slicer1=4*no
            slicer2=4*(no+1)
            roundkey=expanded_key[slicer1:slicer2]

            #First XOR Key and Input

            for i in range(0,4):
                for j in range(0,4):

                    result=hex(int(roundkey[i][j],16)^int(input_block[i][j],16))[2:].zfill(2)
                    resultant1[j][i]=result
            #Sbox of resultant
            resultant2 = [[0]*4 for _ in range(4)]
            for i in range (0, 4):
                for j in range (0, 4):
                    resultant2[i][j] = s_box[resultant1[i][j]]
            #Pbox of resultant
                    
            resultant3 = [[0]*4 for _ in range(4)]
            for j in range (0,4):
                    resultant3[0][j]=resultant2[0][j]
            for i in range(1,4):
                for j in range (0,4):
                    resultant3[i][j-i]=resultant2[i][j]
            if no==9:
                break
            resultant4=mix_columns(resultant3)
            input_block=resultant4


        final_key=expanded_key[-4:]

        for i in range(0,4):
                for j in range(0,4):
                    result=hex(int(final_key[i][j],16)^int(resultant3[j][i],16))[2:].zfill(2)
                    encrypted_blocks[j][i]=result

        transposed_list = list(map(list, zip(*encrypted_blocks)))
        flattened_string = ''.join(str(element) for sublist in transposed_list for element in sublist)
        encrypted_string=encrypted_string+flattened_string
        temp = copy.deepcopy(encrypted_blocks)
        encrypted_output.extend(temp)
    return encrypted_string
