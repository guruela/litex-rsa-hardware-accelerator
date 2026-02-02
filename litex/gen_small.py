
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def modinv(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def int_to_hex_array(val):
    arr = []
    for i in range(8):
        word = val & 0xFFFFFFFF
        arr.append(word)
        val >>= 32
    return arr

def print_array(name, arr):
    print(f"const uint32_t {name}[8] = {{")
    lines = []
    for i in range(0, 8, 4):
        line = "    " + ", ".join([f"0x{x:08x}" for x in arr[i:i+4]]) + ","
        lines.append(line)
    print("\n".join(lines))
    print("};")

# Small RSA params
# p = 61, q = 53
# N = 3233 (0xCA1)
# phi = 60 * 52 = 3120
# E = 17
# D = inv(17, 3120) = 2753 (0xAC1)

p = 61
q = 53
N = p * q
phi = (p - 1) * (q - 1)
E = 17
D = modinv(E, phi)

# Hardware Logic check:
# The core loops based on MSB of N.
# N = 0xCA1 = 1100 1010 0001.
# Bit length = 12.
# So R should be 2^12.

bit_len = N.bit_length()
R = 1 << bit_len

r_mod_n = R % N
r2_mod_n = (R * R) % N

print(f"// Params: p={p}, q={q}, N={N}, E={E}, D={D}, bits={bit_len}")
print_array("key_n", int_to_hex_array(N))
print_array("key_e", int_to_hex_array(E))
print_array("key_d", int_to_hex_array(D))
print_array("r_mod_n", int_to_hex_array(r_mod_n))
print_array("r2_mod_n", int_to_hex_array(r2_mod_n))

# Test Message
M = 123
print(f"\n// Message = {M}")
print_array("message", int_to_hex_array(M))

C = pow(M, E, N)
print(f"// Expected C = {C}")
print(f"// Expected M' = {pow(C, D, N)}")
