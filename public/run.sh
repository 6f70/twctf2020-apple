#!/bin/sh
cd $(dirname "$0")

if [ ! -f esp32-r0-rom.bin ]; then
	wget https://github.com/espressif/qemu/raw/0ff3da8d3c797dcf33a45c419204f39f684376cf/pc-bios/esp32-r0-rom.bin
fi

./qemu-system-xtensa -nographic -machine esp32 -drive file=flash_image.bin,if=mtd,format=raw
