import time
from SmallScaleAES import SmallScaleAES
from gMul4 import gMul_4

### Set equations solving for delta1 ###
#   2*delta_1 = S_Inv[ x_01 XOR k_01 ] XOR S_Inv[ x'_01 XOR k_01 ]
#   1*delta_1 = S_Inv[ x_14 XOR k_14 ] XOR S_Inv[ x'_14 XOR k_14 ]
#   1*delta_1 = S_Inv[ x_11 XOR k_11 ] XOR S_Inv[ x'_11 XOR k_11 ]
#   3*delta_1 = S_Inv[ x_08 XOR k_08 ] XOR S_Inv[ x'_08 XOR k_08 ]
#       indexes = (1, 14, 11, 8)    factors = (2, 1, 1, 3)

### Set equations solving for delta2 ###
#   3*delta_2 = S_Inv[ x_05 XOR k_05 ] XOR S_Inv[ x'_05 XOR k_05 ]
#   2*delta_2 = S_Inv[ x_02 XOR k_02 ] XOR S_Inv[ x'_02 XOR k_02 ]
#   1*delta_2 = S_Inv[ x_15 XOR k_15 ] XOR S_Inv[ x'_15 XOR k_15 ]
#   1*delta_2 = S_Inv[ x_12 XOR k_12 ] XOR S_Inv[ x'_12 XOR k_12 ]
#       indexes = (5, 2, 15, 12)    factors = (3, 2, 1, 1)

### Set equations solving for delta3 ###
#   1*delta_3 = S_Inv[ x_09 XOR k_09 ] XOR S_Inv[ x'_09 XOR k_09 ]
#   3*delta_3 = S_Inv[ x_06 XOR k_06 ] XOR S_Inv[ x'_06 XOR k_06 ]
#   2*delta_3 = S_Inv[ x_03 XOR k_03 ] XOR S_Inv[ x'_03 XOR k_03 ]
#   1*delta_3 = S_Inv[ x_16 XOR k_16 ] XOR S_Inv[ x'_16 XOR k_16 ]
#       indexes = (9, 6, 3, 16)    factors = (1, 3, 2, 1)

### Set equations solving for delta4 ###
#   1*delta_4 = S_Inv[ x_13 XOR k_13 ] XOR S_Inv[ x'_13 XOR k_13 ]
#   1*delta_4 = S_Inv[ x_10 XOR k_10 ] XOR S_Inv[ x'_10 XOR k_10 ]
#   3*delta_4 = S_Inv[ x_07 XOR k_07 ] XOR S_Inv[ x'_07 XOR k_07 ]
#   2*delta_4 = S_Inv[ x_04 XOR k_04 ] XOR S_Inv[ x'_04 XOR k_04 ]
#       indexes = (13, 10, 7, 4)    factors = (1, 1, 3, 2)


def find_key_from_group(indexes, factors):     
    for delta in range(1, 16):
        found_delta = True
        for i in range(4):
            found_k = False
            idx = indexes[i] - 1
            coe = factors[i]
            rhs = gMul_4(coe, delta)
            for k in range(16):
                lhs = aes.m_InverseSBox[ct[idx] ^ k] ^ aes.m_InverseSBox[ct_f[idx] ^ k]
                if (lhs == rhs): 
                    res_k[idx] = k
                    found_k = True
                    break               # solving equation for next k
            if not found_k:
                found_delta = False     # discard delta & restart
                break       
        if found_delta:
            print("Delta = ", delta)    # Stop when found delta
            break        

##############################################################################                    
aes = SmallScaleAES(rounds=10, rows=4, cols=4, wordSize=4)

data = [0x0, 0x0, 0x0, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
key = [0xF, 0xE, 0xD, 0xC,0xB,0xA,0x9,0x8,0x7,0x6,0x5,0x4,0x3,0x2,0x1,0x0]
f_round = 8
fault = [0xF, 0x0, 0x0, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
res_k = [0xF, 0xF, 0xF, 0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF,0xF]
aes.Encrypt(data, key)
ct = aes.m_Data.copy()
aes.EncryptWithFault(data, key, f_round, fault)
ct_f = aes.m_Data.copy()

print("\n-----------------------------------------------------------------------------")
print("Correct Ciphertext: ", ct)
print("Faulty Ciphertext :", ct_f)
print("-----------------------------------------------------------------------------")
find_key_from_group( (1, 14, 11, 8), (2, 1, 1, 3) )
print("Key after finding delta1: ", res_k)
print("-----------------------------------------------------------------------------")
find_key_from_group( (5, 2, 15, 12) , (3, 2, 1, 1) )
print("Key after finding delta1: ", res_k)
print("-----------------------------------------------------------------------------")
find_key_from_group( (9, 6, 3, 16), (1, 3, 2, 1) )
print("Key after finding delta1: ", res_k)
print("-----------------------------------------------------------------------------")
find_key_from_group( (13, 10, 7, 4) , (1, 1, 3, 2) )
print("Key after finding delta1: ", res_k)
print("-----------------------------------------------------------------------------")