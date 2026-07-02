def hex_to_nibbles(hex_string):
    return [int(c, 16) for c in hex_string]

def nibbles_to_hex(nibbles):
    return ''.join(f'{x:X}' for x in nibbles)

def xor_states(a, b):
    return [x ^ y for x, y in zip(a, b)]

def print_state(label, state):
    print(f"{label}: {''.join(f'{x:X}' for x in state)}")


