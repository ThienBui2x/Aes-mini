import time
from SmallScaleAES import SmallScaleAES
from helper import hex_to_nibbles, nibbles_to_hex

# ---------- AES ----------
aes = SmallScaleAES(rounds=10, rows=4, cols=4, wordSize=4)

plaintext_hex = "0000000000000000"
target_ciphertext_hex = "609B6227BA393803"

plaintext = hex_to_nibbles(plaintext_hex)
known_suffix = "9876543210"

# ---- START TIME ----
start_time = time.time()
print("Start time:", time.ctime(start_time))

for i in range(0x1000000):

    key_hex = f"{i:06X}{known_suffix}"
    key = hex_to_nibbles(key_hex)

    if len(key) != aes.m_NoBlocks:
        continue

    aes.Encrypt(plaintext, key)
    ciphertext_hex = nibbles_to_hex(aes.m_Data)

    if ciphertext_hex.upper() == target_ciphertext_hex.upper():
        print(f"\nKEY FOUND! after {i} run times.")
        print("Key =", key_hex)
        break

# ---- END TIME ----
end_time = time.time()
print("End time:", time.ctime(end_time))
print(f"Total elapsed: {end_time - start_time:.2f} seconds")
