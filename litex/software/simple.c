#include <stdint.h>
#include <generated/csr.h>

// Direct register access macros
#define CSR_WRITE(v, addr) (*((volatile uint32_t *)(addr)) = (v))
#define CSR_READ(addr) (*((volatile uint32_t *)(addr)))

// Simple polling UART write
void putc_raw(char c) {
    if (c == '\n') {
        putc_raw('\r');
    }
    // Wait until TX buffer is not full
    while (CSR_READ(CSR_UART_TXFULL_ADDR));
    // Write character
    CSR_WRITE(c, CSR_UART_RXTX_ADDR);
}

void puts_raw(const char *s) {
    while (*s) {
        putc_raw(*s++);
    }
    putc_raw('\n');
}

// Simple delay
void delay(int count) {
    volatile int i = count;
    while(i > 0) i--;
}

int main(void) {
    // Note: We are assuming UART is already initialized by the BIOS
    // (Baudrate etc are set).
    // We are NOT enabling interrupts.

    puts_raw("Hello from Bare Metal Simple App!");
    puts_raw("This is writing directly to CSRs.");

    int counter = 0;
    while(1) {
        puts_raw("Alive...");
        
        // Print a character to show activity
        putc_raw('0' + (counter % 10));
        putc_raw('\n');
        counter++;

        delay(5000000);
    }
    return 0;
}
