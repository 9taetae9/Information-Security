# Define the S-Box for SubNibbles
S_BOX = {
    '0': '9', '1': '4', '2': 'A', '3': 'B',
    '4': 'D', '5': '1', '6': 'E', '7': 'F',
    '8': '2', '9': 'C', 'A': '3', 'B': '7',
    'C': '5', 'D': '0', 'E': '6', 'F': '8'
}

# Galois field multiplication for MixColumns
GF4 = {
    '0': '0', '1': '4', '2': '8', '3': 'C', 
    '4': '3', '5': '7', '6': 'B', '7': 'F', 
    '8': '6', '9': '2', 'A': 'E', 'B': 'A', 
    'C': '5', 'D': '1', 'E': '9', 'F': 'D'
}

def gf_multiply(x, y):
    # Convert y to its hexadecimal string representation
    y_hex = hex(y)[2:].upper()

    if x == 1:
        return y
    elif x == 4:
        return int(GF4[y_hex], 16)  # Return the result as an integer
    else:
        return 0


def sub_nibbles(input_block):
    """Substitute each nibble using the S-Box."""
    return ''.join(S_BOX[nibble] for nibble in input_block)

def shift_rows(input_block):
    """Shift rows for a 2x2 matrix representation."""
    return input_block[0] + input_block[3] + input_block[2] + input_block[1]

def mix_columns(input_block):
    s00 = input_block[0]
    s01 = input_block[1]
    s10 = input_block[2]
    s11 = input_block[3]
    r00 = hex(gf_multiply(1, int(s00, 16)) ^ gf_multiply(4, int(s10, 16)))[2:].upper().zfill(1)
    r01 = hex(gf_multiply(1, int(s01, 16)) ^ gf_multiply(4, int(s11, 16)))[2:].upper().zfill(1)
    r10 = hex(gf_multiply(4, int(s00, 16)) ^ gf_multiply(1, int(s10, 16)))[2:].upper().zfill(1)
    r11 = hex(gf_multiply(4, int(s01, 16)) ^ gf_multiply(1, int(s11, 16)))[2:].upper().zfill(1)
    return r00 + r01 + r10 + r11

def differential_cryptanalysis(delta_input):
    """Perform differential cryptanalysis."""
    input1 = "1234"  # Some arbitrary input
    input2 = hex(int(input1, 16) ^ int(delta_input, 16))[2:].upper().zfill(4)  # XOR with delta
    output1 = sub_nibbles(shift_rows(mix_columns(input1)))
    output2 = sub_nibbles(shift_rows(mix_columns(input2)))
    delta_output = hex(int(output1, 16) ^ int(output2, 16))[2:].upper().zfill(4)
    return delta_output

# Test
delta_input = "0001"
print(f"Delta Input: {delta_input}")
print(f"Delta Output: {differential_cryptanalysis(delta_input)}")
