sBox  = [0x9, 0x4, 0xa, 0xb, 0xd, 0x1, 0x8, 0x5,
         0x6, 0x2, 0x0, 0x3, 0xc, 0xe, 0xf, 0x7]

sBoxI = [0xa, 0x5, 0x9, 0xb, 0x1, 0x7, 0x8, 0xf,
         0x6, 0x0, 0x2, 0x3, 0xc, 0x4, 0xd, 0xe]

w = [None] * 6

def bin_to_int(bin_str):
    return int(bin_str, 2)

def int_to_bin(int_val, padding=16):
    return format(int_val, f'0{padding}b')

def mult(p1, p2):
    p = 0
    while p2:
        if p2 & 0b1:
            p ^= p1
        p1 <<= 1
        if p1 & 0b10000:
            p1 ^= 0b11
        p2 >>= 1
    return p & 0b1111

def intToVec(n):
    return [n >> 12, (n >> 4) & 0xf, (n >> 8) & 0xf, n & 0xf]

def vecToInt(m):
    return (m[0] << 12) + (m[2] << 8) + (m[1] << 4) + m[3]

def addKey(s1, s2):
    return [i ^ j for i, j in zip(s1, s2)]

def sub4NibList(sbox, s):
    return [sbox[e] for e in s]

def shiftRow(s):
    return [s[0], s[1], s[3], s[2]]

def keyExp(key):
    key = bin_to_int(key)
    Rcon1, Rcon2 = 0b10000000, 0b00110000
    w[0] = (key & 0xff00) >> 8
    w[1] = key & 0x00ff
    w[2] = w[0] ^ Rcon1 ^ sub2Nib(w[1])
    w[3] = w[2] ^ w[1]
    w[4] = w[2] ^ Rcon2 ^ sub2Nib(w[3])
    w[5] = w[4] ^ w[3]

def sub2Nib(b):
    return sBox[b >> 4] + (sBox[b & 0x0f] << 4)

def encrypt(ptext):
    ptext = bin_to_int(ptext)
    def mixCol(s):
        return [s[0] ^ mult(4, s[2]), s[1] ^ mult(4, s[3]),
                s[2] ^ mult(4, s[0]), s[3] ^ mult(4, s[1])]
    state = intToVec(((w[0] << 8) + w[1]) ^ ptext)
    state = mixCol(shiftRow(sub4NibList(sBox, state)))
    state = addKey(intToVec((w[2] << 8) + w[3]), state)
    state = shiftRow(sub4NibList(sBox, state))
    return int_to_bin(vecToInt(addKey(intToVec((w[4] << 8) + w[5]), state)))

def decrypt(ctext):
    ctext = bin_to_int(ctext)
    def iMixCol(s):
        return [mult(9, s[0]) ^ mult(2, s[2]), mult(9, s[1]) ^ mult(2, s[3]),
                mult(9, s[2]) ^ mult(2, s[0]), mult(9, s[3]) ^ mult(2, s[1])]
    
    state = intToVec(((w[4] << 8) + w[5]) ^ ctext)
    state = sub4NibList(sBoxI, shiftRow(state))
    state = iMixCol(addKey(intToVec((w[2] << 8) + w[3]), state))
    state = sub4NibList(sBoxI, shiftRow(state))

    return int_to_bin(vecToInt(addKey(intToVec((w[0] << 8) + w[1]), state)))

# Test
plaintext = '0110111101101011'
key = '1010011100111011'
keyExp(key)
ciphertext = encrypt(plaintext)
decrypted_text = decrypt(ciphertext)
print(f'plaintext : {plaintext}')
print(f'key : {key}')
print(f'Encrypted : {ciphertext}')
print(f'Decrypted : {decrypted_text}')