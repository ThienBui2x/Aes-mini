def gMul_4(x, y):
    if (x>15 or y>15):
        print("Error: can't multiply numbers larger than 15 with gMul_4.")
        exit(0)
    
    xy = 0
    
    while (y):
        if (y & 1):
            xy = xy ^ x # if y is odd, then add the corresponding x to xy
        if (x & 0x8):
            x = (x << 1) ^ 0x13 # Overflow: XOR with the primitive polynomial x^4 + x + 1
        else:
            x <<= 1 # x*2
        y >>= 1 # x/2
    
    return xy