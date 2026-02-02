from migen import *
from litex.soc.interconnect.csr import *

class RSACore(Module, AutoCSR):
    def __init__(self, platform, c_block_size=256, num_cores=1):
        # Parameters
        self.c_block_size = c_block_size
        self.num_cores = num_cores

        # CSRs
        # Keys and Data (256 bits default)
        # LiteX will split these into multiple 32-bit registers accessible from software.
        
        self.key_n = CSRStorage(c_block_size, description="Modulus n")
        self.key_e_d = CSRStorage(c_block_size, description="Exponent e or d")
        self.r_mod_n = CSRStorage(c_block_size, description="R mod n parameter")
        self.r2_mod_n = CSRStorage(c_block_size, description="R^2 mod n parameter")
        
        # Data Input
        self.msgin_data = CSRStorage(c_block_size, description="Message Input Data")
        self.msgin_valid = CSRStorage(1, description="Message Input Valid (Software should toggle 0->1->0)")
        self.msgin_last = CSRStorage(1, description="Message Input Last Flag")
        self.msgin_ready = CSRStatus(1, description="Message Input Ready")
        
        # Data Output
        self.msgout_data = CSRStatus(c_block_size, description="Message Output Data")
        self.msgout_valid = CSRStatus(1, description="Message Output Valid")
        self.msgout_last = CSRStatus(1, description="Message Output Last")
        self.msgout_ready = CSRStorage(1, description="Message Output Ready (Software should toggle 0->1->0)")
        
        # Status
        self.rsa_status = CSRStatus(32, description="Core Status")

        # VHDL Instance
        # We assume the VHDL files are in the project root relative to where this script is run,
        # or we add them with absolute paths.
        
        self.specials += Instance("rsa_core",
            # Generics
            p_c_block_size=c_block_size,
            p_num_cores=num_cores,
            
            # Clocks & Reset
            i_clk=ClockSignal(),
            i_reset_n=~ResetSignal(), # Active Low Reset
            
            # Input Interface
            i_msgin_valid=self.msgin_valid.storage,
            o_msgin_ready=self.msgin_ready.status,
            i_msgin_data=self.msgin_data.storage,
            i_msgin_last=self.msgin_last.storage,
            
            # Output Interface
            o_msgout_valid=self.msgout_valid.status,
            i_msgout_ready=self.msgout_ready.storage,
            o_msgout_data=self.msgout_data.status,
            o_msgout_last=self.msgout_last.status,
            
            # Keys
            i_key_e_d=self.key_e_d.storage,
            i_key_n=self.key_n.storage,
            i_r_mod_n=self.r_mod_n.storage,
            i_r2_mod_n=self.r2_mod_n.storage,
            
            # Status
            o_rsa_status=self.rsa_status.status
        )
        
        # Add VHDL Sources
        # Path relative to the root of the repository
        v_sources = [
            "source/shared/utils.vhd",
            "source/shared/alu.vhd",
            "source/shared/bitwise_masker.vhd",
            "source/shared/msb_bitscanner.vhd",
            "source/shared/mux_2to1.vhd",
            "source/shared/mux_3to1.vhd",
            "source/monpro/monpro_control.vhd",
            "source/monpro/monpro_datapath.vhd",
            "source/monpro/monpro.vhd",
            "source/modexp/modexp_control.vhd",
            "source/modexp/modexp_datapath.vhd",
            "source/modexp/modexp.vhd",
            "source/rsa_core_datapath.vhd",
            "source/rsa_core_input_control.vhd",
            "source/rsa_core_output_control.vhd",
            "source/rsa_core.vhd",
        ]
        
        import os
        # Assuming script is run from project root, or we can find the files.
        # We'll try to locate them.
        base_dir = os.path.abspath(os.path.dirname(__file__))
        # Go up one level to reach repo root (assuming litex/rsa_core.py)
        root_dir = os.path.dirname(base_dir)
        
        for src in v_sources:
            full_path = os.path.join(root_dir, src)
            if not os.path.exists(full_path):
                # Fallback: Maybe we are running from root?
                if os.path.exists(src):
                    full_path = os.path.abspath(src)
                else:
                    print(f"Warning: Could not find {src}")
            
            platform.add_source(full_path, language="vhdl")
