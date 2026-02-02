# GEMINI Project Context

## Overview
This project is an RSA Hardware Accelerator written in VHDL, designed to perform encryption and decryption using modular exponentiation. It is structured to be integrated into a larger System-on-Chip (SoC) using LiteX.

## Architecture

### Hardware Hierarchy
- **rsa_core**: Top-level entity managing input/output interfaces (AXI-stream like) and control logic.
    - **rsa_core_control**: Splits into input and output control FSMs.
    - **rsa_core_datapath**: Manages data flow and instantiates multiple processing cores.
        - **modexp**: Modular Exponentiation core. Performs $M^e  n$.
            - **monpro**: Montgomery Product unit. Performs $(A  B  R^{-1})  n$.
                - Uses **alu** and **msb_bitscanner** for arithmetic operations.

### Shared Components
Located in `source/shared/`:
- `alu.vhd`: Arithmetic Logic Unit.
- `msb_bitscanner.vhd`: Most Significant Bit scanner (used for normalizing/sizing).
- `bitwise_masker.vhd`, `mux_*`: Utility components.

## Integration
- **LiteX**: The project includes Python scripts for LiteX integration (`litex/`).
    - `basys3_rsa.py`: Platform definition (likely for Digilent Basys3).
    - `rsa_core.py`: LiteX module definition for the accelerator.
- **Software**: Drivers and demo applications are in `litex/software/`.
    - `rsa_driver.h`: C header for interacting with the hardware.
    - `demo.c`: Interactive CLI for testing the accelerator on hardware.

## Verification
- **VHDL Testbenches**: Located in `testbench/`.
    - Uses **UVVM** (Universal VHDL Verification Methodology) found in `lib/uvvm/`.
    - `rsa_core_tb.vhd`: Top-level testbench.
- **Python Verification**: `litex/verify_rsa_math.py` for mathematical correctness.

## Current State
- **Hardware**: Stable. A refactoring attempt ("move-bitscanner") was recently reverted. The codebase uses `msb_bitscanner`.
- **Software**: 
    - Fixed a bug in `litex/software/demo.c` where UART input would loop infinitely due to uncleared event pending bits.
    - Updated `demo.c` UI text to accurately reflect that the 'k' command loads default keys instead of prompting for input.
- **Build System**: `Makefile` based workflow using GHDL for simulation and Yosys for synthesis exploration.