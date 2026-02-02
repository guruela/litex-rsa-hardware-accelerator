#ifndef RSA_DRIVER_H
#define RSA_DRIVER_H

#include <stdint.h>
#include <generated/csr.h>

// Assuming c_block_size = 256 bits = 8 x 32-bit words
#define RSA_BLOCK_WORDS 8

static inline void rsa_write256(uint32_t base_addr, const uint32_t *data) {
    // LiteX CSRs with "big" ordering map the lowest address to the MSB.
    // Our 'data' array is Little Endian (data[0] is LSB).
    // So we need to write data[7] to base_addr, data[6] to base_addr+4, etc.
    for (int i = 0; i < RSA_BLOCK_WORDS; i++) {
        csr_write_simple(data[RSA_BLOCK_WORDS - 1 - i], base_addr + i * 4);
    }
}

static inline void rsa_read256(uint32_t base_addr, uint32_t *data) {
    // Same logic for reading: base_addr contains MSB (data[7]).
    for (int i = 0; i < RSA_BLOCK_WORDS; i++) {
        data[RSA_BLOCK_WORDS - 1 - i] = csr_read_simple(base_addr + i * 4);
    }
}

// Function to set up keys
void rsa_set_keys(const uint32_t *n, const uint32_t *e_d, const uint32_t *r_mod_n, const uint32_t *r2_mod_n) {
    rsa_write256(CSR_RSA_KEY_N_ADDR, n);
    rsa_write256(CSR_RSA_KEY_E_D_ADDR, e_d);
    rsa_write256(CSR_RSA_R_MOD_N_ADDR, r_mod_n);
    rsa_write256(CSR_RSA_R2_MOD_N_ADDR, r2_mod_n);
}

// Function to encrypt/decrypt a block
void rsa_process_block(const uint32_t *input, uint32_t *output) {
    // 1. Check if ready
    while (rsa_msgin_ready_read() == 0);

    // 2. Write Data
    rsa_write256(CSR_RSA_MSGIN_DATA_ADDR, input);
    
    // 3. Set Last Flag
    rsa_msgin_last_write(1);

    // 4. Trigger Valid
    rsa_msgin_valid_write(1);
    rsa_msgin_valid_write(0);

    // 5. Wait for Output Valid
    while (rsa_msgout_valid_read() == 0);

    // 6. Read Data
    rsa_read256(CSR_RSA_MSGOUT_DATA_ADDR, output);

    // 7. Acknowledge
    rsa_msgout_ready_write(1);
    rsa_msgout_ready_write(0);
}

#endif // RSA_DRIVER_H