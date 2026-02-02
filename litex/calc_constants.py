
def hex_to_int(h):
    return int(h.replace(" ", ""), 16)

def int_to_hex_array(val):
    # Split into 8 32-bit words, little endian (index 0 = LSB)
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

N_str = "99925173ad65686715385ea800cd28120288fc70a9bc98dd4c90d676f8ff768d"
N = hex_to_int(N_str)
bit_width = 256
R = 1 << bit_width

r_mod_n = R % N
r2_mod_n = (R * R) % N

print(f"// N = 0x{N:x}")
print_array("key_n", int_to_hex_array(N))

print(f"\n// R mod N = 0x{r_mod_n:x}")
print_array("r_mod_n", int_to_hex_array(r_mod_n))

print(f"\n// R^2 mod N = 0x{r2_mod_n:x}")
print_array("r2_mod_n", int_to_hex_array(r2_mod_n))
