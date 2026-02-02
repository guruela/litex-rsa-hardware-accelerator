
def hex_to_int(h):
    return int(h.replace(" ", ""), 16)

N_str = "99925173ad65686715385ea800cd28120288fc70a9bc98dd4c90d676f8ff768d"
E_str = "0000000000000000000000000000000000000000000000000000000000010001"
D_str = "0cea1651ef44be1f1f1476b7539bed10d73e3aac782bd9999a1e5a790932bfe9"
M_str = "000000000000000000000000000048656c6c6f20525341200000576f726c6421"

N = hex_to_int(N_str)
E = hex_to_int(E_str)
D = hex_to_int(D_str)
M = hex_to_int(M_str)

print(f"N: {N:x}")
print(f"E: {E:x}")
print(f"D: {D:x}")
print(f"M: {M:x}")

# Verify D * E mod phi(N) == 1
# Factor N? No, we trust the keys or check consistency.
# But we can just check Encryption/Decryption.

C = pow(M, E, N)
print(f"Expected Ciphertext (C): {C:x}")

Decrypted = pow(C, D, N)
print(f"Expected Decrypted (M'): {Decrypted:x}")

if Decrypted == M:
    print("Keys are valid!")
else:
    print("KEYS ARE INVALID!")

# Check the Hardware Output
# HW Ciphertext: 75e7f0ffe76bf15fa1d577bed20ed271b332041517111e9c7064e9a3d6e96ca6
HW_C_str = "75e7f0ffe76bf15fa1d577bed20ed271b332041517111e9c7064e9a3d6e96ca6"
HW_C = hex_to_int(HW_C_str)

if C == HW_C:
    print("Hardware Encryption MATCHES Software!")
else:
    print("Hardware Encryption FAILED!")
    print(f"HW: {HW_C:x}")
