#include <stdint.h>
#include <generated/csr.h>

#include "rsa_driver.h"

// Direct register access macros
#define CSR_WRITE(v, addr) (*((volatile uint32_t *)(addr)) = (v))
#define CSR_READ(addr) (*((volatile uint32_t *)(addr)))

// Simple polling UART write
void putc_raw(char c) {
    if (c == '\n') {
        putc_raw('\r');
    }
    while (CSR_READ(CSR_UART_TXFULL_ADDR));
    CSR_WRITE(c, CSR_UART_RXTX_ADDR);
}

void puts_raw(const char *s) {
    while (*s) {
        putc_raw(*s++);
    }
    putc_raw('\n');
}

void puthex_raw(uint32_t v) {
    char buf[9];
    buf[8] = 0;
    const char hex[] = "0123456789abcdef";
    for (int i = 7; i >= 0; i--) {
        buf[i] = hex[v & 0xF];
        v >>= 4;
    }
    for (int i = 0; i < 8; i++) {
        putc_raw(buf[i]);
    }
}

// Minimal memcmp
int memcmp(const void *s1, const void *s2, size_t n) {
    const unsigned char *p1 = s1, *p2 = s2;
    while (n--) {
        if (*p1 != *p2) {
            return *p1 - *p2;
        }
        p1++;
        p2++;
    }
    return 0;
}

// Delay
void delay(int count) {
    volatile int i = count;
    while(i > 0) i--;
}

// Params: p=61, q=53, N=3233, E=17, D=2753, bits=12
const uint32_t key_n[8] = {
    0x00000ca1, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
};
const uint32_t key_e[8] = {
    0x00000011, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
};
const uint32_t key_d[8] = {
    0x00000ac1, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
};
const uint32_t r_mod_n[8] = {
    0x0000035f, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
};
const uint32_t r2_mod_n[8] = {
    0x0000049b, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
};

// Message = 123
const uint32_t message[8] = {
    0x0000007b, 0x00000000, 0x00000000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000,
};

static void print_block(const char *label, const uint32_t *data) {
    puts_raw(label);
    puts_raw(": 0x");
    for (int i = 7; i >= 0; i--) {
        puthex_raw(data[i]);
    }
    putc_raw('\n');
}

int main(void) {
    puts_raw("\nRSA Hardware Accelerator Test (Small Values)");
    puts_raw("==========================================");

    uint32_t encrypted[8];
    uint32_t decrypted[8];

    // 1. Encryption
    puts_raw("Configuring for Encryption...");
    rsa_set_keys(key_n, key_e, r_mod_n, r2_mod_n);
    delay(1000); 
    
    puts_raw("Encrypting...");
    print_block("Plaintext", message);
    rsa_process_block(message, encrypted);
    print_block("Ciphertext", encrypted);

    // 2. Decryption
    puts_raw("Configuring for Decryption...");
    rsa_set_keys(key_n, key_d, r_mod_n, r2_mod_n);
    delay(1000);

    puts_raw("Decrypting...");
    rsa_process_block(encrypted, decrypted);
    print_block("Decrypted", decrypted);

    // 3. Verify
    if (memcmp(message, decrypted, sizeof(message)) == 0) {
        puts_raw("SUCCESS: Decrypted message matches original!");
    } else {
        puts_raw("FAILURE: Decrypted message does NOT match!");
    }

    while(1);
    return 0;
}
