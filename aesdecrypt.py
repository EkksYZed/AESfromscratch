import os
import copy
import re
from aesencrypt import padding_needed

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


reverse_sbox = {
    '00': '52', '01': '09', '02': '6a', '03': 'd5', '04': '30', '05': '36', '06': 'a5', '07': '38',
    '08': 'bf', '09': '40', '0a': 'a3', '0b': '9e', '0c': '81', '0d': 'f3', '0e': 'd7', '0f': 'fb',
    '10': '7c', '11': 'e3', '12': '39', '13': '82', '14': '9b', '15': '2f', '16': 'ff', '17': '87',
    '18': '34', '19': '8e', '1a': '43', '1b': '44', '1c': 'c4', '1d': 'de', '1e': 'e9', '1f': 'cb',
    '20': '54', '21': '7b', '22': '94', '23': '32', '24': 'a6', '25': 'c2', '26': '23', '27': '3d',
    '28': 'ee', '29': '4c', '2a': '95', '2b': '0b', '2c': '42', '2d': 'fa', '2e': 'c3', '2f': '4e',
    '30': '08', '31': '2e', '32': 'a1', '33': '66', '34': '28', '35': 'd9', '36': '24', '37': 'b2',
    '38': '76', '39': '5b', '3a': 'a2', '3b': '49', '3c': '6d', '3d': '8b', '3e': 'd1', '3f': '25',
    '40': '72', '41': 'f8', '42': 'f6', '43': '64', '44': '86', '45': '68', '46': '98', '47': '16',
    '48': 'd4', '49': 'a4', '4a': '5c', '4b': 'cc', '4c': '5d', '4d': '65', '4e': 'b6', '4f': '92',
    '50': '6c', '51': '70', '52': '48', '53': '50', '54': 'fd', '55': 'ed', '56': 'b9', '57': 'da',
    '58': '5e', '59': '15', '5a': '46', '5b': '57', '5c': 'a7', '5d': '8d', '5e': '9d', '5f': '84',
    '60': '90', '61': 'd8', '62': 'ab', '63': '00', '64': '8c', '65': 'bc', '66': 'd3', '67': '0a',
    '68': 'f7', '69': 'e4', '6a': '58', '6b': '05', '6c': 'b8', '6d': 'b3', '6e': '45', '6f': '06',
    '70': 'd0', '71': '2c', '72': '1e', '73': '8f', '74': 'ca', '75': '3f', '76': '0f', '77': '02',
    '78': 'c1', '79': 'af', '7a': 'bd', '7b': '03', '7c': '01', '7d': '13', '7e': '8a', '7f': '6b',
    '80': '3a', '81': '91', '82': '11', '83': '41', '84': '4f', '85': '67', '86': 'dc', '87': 'ea',
    '88': '97', '89': 'f2', '8a': 'cf', '8b': 'ce', '8c': 'f0', '8d': 'b4', '8e': 'e6', '8f': '73',
    '90': '96', '91': 'ac', '92': '74', '93': '22', '94': 'e7', '95': 'ad', '96': '35', '97': '85',
    '98': 'e2', '99': 'f9', '9a': '37', '9b': 'e8', '9c': '1c', '9d': '75', '9e': 'df', '9f': '6e',
    'a0': '47', 'a1': 'f1', 'a2': '1a', 'a3': '71', 'a4': '1d', 'a5': '29', 'a6': 'c5', 'a7': '89',
    'a8': '6f', 'a9': 'b7', 'aa': '62', 'ab': '0e', 'ac': 'aa', 'ad': '18', 'ae': 'be', 'af': '1b',
    'b0': 'fc', 'b1': '56', 'b2': '3e', 'b3': '4b', 'b4': 'c6', 'b5': 'd2', 'b6': '79', 'b7': '20',
    'b8': '9a', 'b9': 'db', 'ba': 'c0', 'bb': 'fe', 'bc': '78', 'bd': 'cd', 'be': '5a', 'bf': 'f4',
    'c0': '1f', 'c1': 'dd', 'c2': 'a8', 'c3': '33', 'c4': '88', 'c5': '07', 'c6': 'c7', 'c7': '31',
    'c8': 'b1', 'c9': '12', 'ca': '10', 'cb': '59', 'cc': '27', 'cd': '80', 'ce': 'ec', 'cf': '5f',
    'd0': '60', 'd1': '51', 'd2': '7f', 'd3': 'a9', 'd4': '19', 'd5': 'b5', 'd6': '4a', 'd7': '0d',
    'd8': '2d', 'd9': 'e5', 'da': '7a', 'db': '9f', 'dc': '93', 'dd': 'c9', 'de': '9c', 'df': 'ef',
    'e0': 'a0', 'e1': 'e0', 'e2': '3b', 'e3': '4d', 'e4': 'ae', 'e5': '2a', 'e6': 'f5', 'e7': 'b0',
    'e8': 'c8', 'e9': 'eb', 'ea': 'bb', 'eb': '3c', 'ec': '83', 'ed': '53', 'ee': '99', 'ef': '61',
    'f0': '17', 'f1': '2b', 'f2': '04', 'f3': '7e', 'f4': 'ba', 'f5': '77', 'f6': 'd6', 'f7': '26',
    'f8': 'e1', 'f9': '69', 'fa': '14', 'fb': '63', 'fc': '55', 'fd': '21', 'fe': '0c', 'ff': '7d'
}

rounds=10

def multiply_by_2(v):
    s = int(v,16) << 1

    s &= int("ff", 16)
    if (int(v,16) & 128) != 0:
        s = s ^ int("1b", 16)
    return s




def matrix_to_lists(matrix):

    column_lists = [[] for _ in range(len(matrix[0]))]

    for row in matrix:
        for i, element in enumerate(row):
  
            column_lists[i].append(element)
    
    return column_lists



def multiply_by_3(v):
    return multiply_by_2(v) ^ int(v,16)


def mix_columns(grid):
    new_grid = [[], [], [], []]
    for i in range(4):
        col = [grid[j][i] for j in range(4)]

        col = mix_column(col)

        for i in range(4):
            col[i]=hex(col[i])[2:].zfill(2)

            new_grid[i].append(col[i])

    return new_grid




def mix_column(column):
    r = [
        multiply_by_2(column[0]) ^ multiply_by_3(column[1]) ^ int(column[2],16) ^ int(column[3],16), 
        multiply_by_2(column[1]) ^ multiply_by_3(column[2]) ^ int(column[3], 16) ^ int(column[0], 16),

        multiply_by_2(column[2]) ^ multiply_by_3(column[3]) ^ int(column[0],16) ^ int(column[1],16),
        multiply_by_2(column[3]) ^ multiply_by_3(column[0]) ^ int(column[1], 16) ^ int(column[2],16)
    ]
    return r

def format_to_matrix(hex_str):
 

        chunks = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]

        matrix = [chunks[i:i+4] for i in range(0, len(chunks), 4)]

        return matrix

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
rounds=10
# Perform AES decryption
def aes_decrypt(ciphertext, key):
    resultant1 = [[0]*4 for _ in range(4)]
    resultant2 = [[0]*4 for _ in range(4)]
    resultant3 = [[0]*4 for _ in range(4)]
    resultant4 = [[0]*4 for _ in range(4)]
    resultant5 = [[0]*4 for _ in range(4)]
    expanded_key =[[0]*4 for _ in range(4)]
    dummy =[]
    decrypted_block = []
    expanded_key = expand_key(key, rounds)
    blocks=len(ciphertext)//32
    cipher_matrix=[[0]*4 for _ in range(4)]
    round_1key=[[0]*4 for _ in range(4)]
    round_key=[[0]*4 for _ in range(4)]
    round_1key=expanded_key[-4:]
    decrypted_string=''
    cipher_matrix=format_to_matrix(ciphertext)
    ascii_text=""
    #first XOR
    for block in range (blocks):
        ipslicer1=(4*block)
        ipslicer2=(4*(block+1))
        last_block=matrix_to_lists(cipher_matrix[ipslicer1:ipslicer2])

        for i in range (0,4):
            for j in range (0,4):
                result=hex(int(last_block[j][i],16)^int(round_1key[i][j],16))[2:].zfill(2)
                resultant1[j][i]=result

        for no in range(rounds):
            a=40-(4*no)
            b=a-4

            round_key=expanded_key[b:a]
            if no!=0:
                mixed=matrix_to_lists(resultant1)
                unmixed = mix_columns(mixed)
                unmixed = mix_columns(unmixed)
                unmixed = mix_columns(unmixed)
                resultant2=unmixed
            else:
                resultant2=resultant1


            for j in range (0,4):
                resultant3[0][j]=resultant2[0][j]
            for i in range(1,4):
                for j in range (0,4):
                    resultant3[i][j]=resultant2[i][j-i]

            for i in range (0, 4):
                for j in range (0, 4):
                    resultant4[i][j] = reverse_sbox[resultant3[i][j]]

        
            for i in range (0,4):
                for j in range (0,4):
                    result2=hex(int(resultant4[j][i],16)^int(round_key[i][j],16))[2:].zfill(2)
                    resultant5[j][i]=result2
            resultant1=matrix_to_lists(resultant5)
        dummy=matrix_to_lists(resultant5)
        decrypted_block.extend(dummy)
        transposed_list = list(map(list, zip(*matrix_to_lists(decrypted_block))))
        flattened_string = ''.join(str(element) for sublist in transposed_list for element in sublist)
        decrypted_string=flattened_string
        print(decrypted_string)
        byte_data = bytes.fromhex(decrypted_string)
        text = byte_data.decode('utf-8')

    # Use a regular expression to remove all hex escape sequences
    matched_string = re.match(r'[\x20-\x7F]+', text)
    return matched_string.group(0)

