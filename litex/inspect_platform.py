from litex_boards.platforms import digilent_basys3

platform = digilent_basys3.Platform()
print("Available resources:")
for res in platform.constraint_manager.available:
    try:
        name = res.name
    except AttributeError:
        try:
            name = res[0]
        except:
            name = str(res)
            
    if "clk" in name:
        print(f"  {res}")