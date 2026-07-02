import time
from SmallScaleAES import SmallScaleAES
from itertools import product
from gMul4 import gMul_4

### Set equations solving for delta1 ###
#   2*delta_1 = S_Inv[ x_01 XOR k_01 ] XOR S_Inv[ x'_01 XOR k_01 ]
#   1*delta_1 = S_Inv[ x_14 XOR k_14 ] XOR S_Inv[ x'_14 XOR k_14 ]
#   1*delta_1 = S_Inv[ x_11 XOR k_11 ] XOR S_Inv[ x'_11 XOR k_11 ]
#   3*delta_1 = S_Inv[ x_08 XOR k_08 ] XOR S_Inv[ x'_08 XOR k_08 ]
#       indexes = (1, 14, 11, 8)    factors = (2, 1, 1, 3)

### Set equations solving for delta4 ###
#   3*delta_4 = S_Inv[ x_13 XOR k_13 ] XOR S_Inv[ x'_13 XOR k_13 ]
#   2*delta_4 = S_Inv[ x_10 XOR k_10 ] XOR S_Inv[ x'_10 XOR k_10 ]
#   1*delta_4 = S_Inv[ x_07 XOR k_07 ] XOR S_Inv[ x'_07 XOR k_07 ]
#   1*delta_4 = S_Inv[ x_04 XOR k_04 ] XOR S_Inv[ x'_04 XOR k_04 ]
#       indexes = (13, 10, 7, 4)    factors = (3, 2, 1, 1)

### Set equations solving for delta3 ###
#   1*delta_3 = S_Inv[ x_09 XOR k_09 ] XOR S_Inv[ x'_09 XOR k_09 ]
#   3*delta_3 = S_Inv[ x_06 XOR k_06 ] XOR S_Inv[ x'_06 XOR k_06 ]
#   2*delta_3 = S_Inv[ x_03 XOR k_03 ] XOR S_Inv[ x'_03 XOR k_03 ]
#   1*delta_3 = S_Inv[ x_16 XOR k_16 ] XOR S_Inv[ x'_16 XOR k_16 ]
#       indexes = (9, 6, 3, 16)    factors = (1, 3, 2, 1)

### Set equations solving for delta2 ###
#   1*delta_2 = S_Inv[ x_05 XOR k_05 ] XOR S_Inv[ x'_05 XOR k_05 ]
#   1*delta_2 = S_Inv[ x_02 XOR k_02 ] XOR S_Inv[ x'_02 XOR k_02 ]
#   3*delta_2 = S_Inv[ x_15 XOR k_15 ] XOR S_Inv[ x'_15 XOR k_15 ]
#   2*delta_2 = S_Inv[ x_12 XOR k_12 ] XOR S_Inv[ x'_12 XOR k_12 ]
#       indexes = (5, 2, 15, 12)    factors = (1, 1, 3, 2)


def find_key_from_group(indexes, factors):     
    for delta in range(1, 16):
        temp = {}
        found_delta = True
        for i in range(4):
            idx = indexes[i] - 1
            coe = factors[i]
            lhs = gMul_4(delta, coe)
            temp[idx] = []
            for k in range(16):
                rhs = aes.m_InverseSBox[ct[idx] ^ k] ^ aes.m_InverseSBox[ct_f[idx] ^ k]
                if (lhs == rhs): 
                    temp[idx].append(k)   # finding all k solutions               
            if not temp[idx]:             # discard delta & restart
                found_delta = False
                break
        if found_delta:
            for idx in temp:
                candidates[idx] = temp[idx]       
   
def generate_all_keys(candidates):
    # build ordered candidate lists
    candidate_lists = []

    for i in range(len(candidates)):
        if i not in candidates or len(candidates[i]) == 0:
            # no candidates → no valid keys
            return []
        candidate_lists.append(candidates[i])

    # Cartesian product over all byte positions
    all_keys = []
    for combo in product(*candidate_lists):
        all_keys.append(list(combo))

    return all_keys

##############################################################################                    
aes = SmallScaleAES(rounds=10, rows=4, cols=4, wordSize=4)

data = [0x0, 0x0, 0x0, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
master = [0xF, 0xE, 0xD, 0xC,0xB,0xA,0x9,0x8,0x7,0x6,0x5,0x4,0x3,0x2,0x1,0x0]
f_round = 8
fault = [0xF, 0x0, 0x0, 0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
aes.Encrypt(data, master)
ct = aes.m_Data.copy()
aes.EncryptWithFault(data, master, f_round, fault)
ct_f = aes.m_Data.copy()

print("\n-----------------------------------------------------------------------------")
print("Correct Ciphertext: ", ct)
print("Faulty Ciphertext :", ct_f)
print("-----------------------------------------------------------------------------")

# ---- START TIME ----
start_time = time.time()
print("Start time:", time.ctime(start_time))

candidates = {}
find_key_from_group( (1, 14, 11, 8), (2, 1, 1, 3) )
find_key_from_group( (13, 10, 7, 4) , (3, 2, 1, 1) )
find_key_from_group( (9, 6, 3, 16), (1, 3, 2, 1) )
find_key_from_group( (5, 2, 15, 12) , (1, 1, 3, 2) )
print("Candidates = ", candidates)
print("-----------------------------------------------------------------------------")
keys = generate_all_keys(candidates)
for key in keys:
    result = aes.ReverseKeySchedule(key, 9)
    aes.Encrypt(data, result)
    if (ct == aes.m_Data):
        print("Found matching master key: ", result)
        break
  
# ---- END TIME ----
end_time = time.time()
print("End time:", time.ctime(end_time))
print(f"Total elapsed: {end_time - start_time:.2f} seconds")