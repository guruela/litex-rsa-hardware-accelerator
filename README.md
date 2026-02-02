# LiteX Port of RSA Hardware Accelerator

This directory contains the LiteX port for the RSA Hardware Accelerator on the Digilent Basys 3 board.

## Structure

*   `rsa_core.py`: The LiteX wrapper for the VHDL core. It exposes the RSA core interfaces (Message In, Message Out, Keys) as CSRs (Control/Status Registers) to the soft CPU (VexRiscv).
*   `basys3_rsa.py`: The SoC build script for the Basys 3 board.
*   `software/`: Contains C driver examples and test application.

## Prerequisites

You need a working installation of:
*   [LiteX](https://github.com/enjoy-digital/litex)
*   [LiteX Boards](https://github.com/litex-hub/litex-boards)
*   [Migen](https://github.com/m-labs/migen)
*   [Vivado](https://www.xilinx.com/products/design-tools/vivado.html) (for synthesis and implementation)
*   RISC-V Toolchain (for compiling the BIOS/Software)

## Building Hardware

To build the bitstream for Basys 3:

```bash
python3 basys3_rsa.py --build --csr-csv csr.csv
```

This command will:
1.  Parse the VHDL sources and the LiteX wrapper.
2.  Generate the Verilog wrapper and the SoC.
3.  Run Vivado to synthesize and route the design.
4.  Generate the bitstream (`soc_basys3_rsa.bit`).
5.  Generate a `csr.csv` file containing the memory map of the new core.

## Loading Hardware

To load the bitstream to the FPGA (assuming connected via USB):

```bash
python3 basys3_rsa.py --load
```

## Software

The software directory contains a test application `main.c` that demonstrates how to drive the RSA core.

### Building Software

```bash
cd software
make
```

This produces `app.bin` (self-test), `simple.bin` (hello world), and `demo.bin` (interactive shell).

### Running Software

After loading the bitstream, the VexRiscv CPU will start executing the BIOS from ROM.
You can load the application into the SRAM and execute it using `litex_term` (provided by LiteX).

First, try the simple test to verify CPU and UART:

```bash
litex_term /dev/ttyUSB1 --kernel simple.bin
```

If that works (prints "Hello..."), try the self-test:

```bash
litex_term /dev/ttyUSB1 --kernel app.bin
```

For the interactive shell (RSA>), run:

```bash
litex_term /dev/ttyUSB1 --kernel demo.bin
```

Note: Since the Basys 3 has limited RAM (configured to 16KB Main RAM), the application is linked to run entirely from Main RAM (`0x40000000`).

## Software Driver

The `software/rsa_driver.h` file provides a simple C API:

*   `rsa_set_keys(n, e_d, r_mod_n, r2_mod_n)`: Configures the 256-bit keys.
*   `rsa_process_block(input, output)`: Encrypts or decrypts a 256-bit block.

Note: The default `c_block_size` is 256 bits. This means keys and data blocks are 256 bits (32 bytes) long.
The CSRs split these 256-bit values into 8x 32-bit registers.
