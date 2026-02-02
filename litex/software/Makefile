BUILD_DIR?=../build/digilent_basys3

include $(BUILD_DIR)/software/include/generated/variables.mak

CFLAGS += -I$(BUILD_DIR)/software/include -I. -I$(SOC_DIRECTORY)/software/include -I$(SOC_DIRECTORY)/software -I$(CPU_DIRECTORY)
LIBS_PATH = -L$(BUILD_DIR)/software/libbase -L$(BUILD_DIR)/software/libcompiler_rt
LDFLAGS = -T linker.ld -L$(BUILD_DIR)/software/include \
          $(LIBS_PATH) \
          -lbase -lcompiler_rt -nostartfiles -nostdlib

CC=$(TRIPLE)-gcc
OBJCOPY=$(TRIPLE)-objcopy

all: app.bin simple.bin demo.bin

start.o: start.S
	$(CC) $(CFLAGS) $(CPUFLAGS) -c -o $@ $<

app.elf: start.o main.c
	$(CC) $(CFLAGS) $(CPUFLAGS) -o $@ $^ $(LDFLAGS)

simple.elf: start.o simple.c
	$(CC) $(CFLAGS) $(CPUFLAGS) -o $@ $^ $(LDFLAGS)

demo.elf: start.o demo.c
	$(CC) $(CFLAGS) $(CPUFLAGS) -o $@ $^ $(LDFLAGS)

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@

clean:
	rm -f start.o app.elf app.bin simple.elf simple.bin demo.elf demo.bin
