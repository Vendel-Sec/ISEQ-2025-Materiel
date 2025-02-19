#!/bin/bash
# Flash firmware
espflash flash --flash-size 8mb firmware.elf

# Flash NVS
source ~/esp/esp-idf/export.sh
python ~/esp/esp-idf/components/partition_table/parttool.py -b 921600 write_partition --partition-name=nvs --input=nvs.bin