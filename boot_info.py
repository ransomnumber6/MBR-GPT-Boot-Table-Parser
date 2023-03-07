import hashlib
import argparse
import struct
import pandas as pd

class MBR:
    status = [0x1BE,0x1CE,0x1DE,0x1EE]
    size_start =[0x1CA,0x1DA,0x1EA,0x1FA]
    size_end =[0x1CE,0x1DE,0x1EE,0x1FE]
    types = [0x1C2,0x1D2,0x1E2,0x1F2]
    lba_start = [0x1C6,0x1D6,0x1E6,0x1F6]
    lba_end = [0x1CA,0x1DA,0x1EA,0x1FA]
    firstoflast_sixteen = [0x1BE,0x1CE,0x1DE,0x1EE]
    lastoflast_sixteen = [0x1CE,0x1DE,0x1EE,0x1FE]


class GPT:
    type_start = [0x200,0x280, 0x300, 0x380]
    type_end = [0x20F,0x28F, 0x30F, 0x38F]
    lba_start = [0x220, 0x2A0,0x320, 0x3A0]
    lba_end = [0x228,0x2A8,0x328, 0x3A8]
    zero = 00000000000000
    ending_lba_start = [0x227,0x2A7,0x327,0x3A7]
    ending_lba_end = [0x22F,0x2AF,0x32F,0x3AF]


def hasher(args):
    # Use a breakpoint in the code line below to debug your script.

    md5 = hashlib.md5(open(f"{args.file}",'rb').read()).hexdigest()
    sha =  hashlib.sha256(open(f"{args.file}",'rb').read()).hexdigest()
    with open(f'MD5-{args.file}.txt', 'w') as f:
        f.write(md5)
    with open(f'SHA-256-{args.file}.txt', 'w') as f:
        f.write(sha)
    file_operations(args)


def check_type(ftype):
   data = pd.read_csv('PartitionTypes.csv')
   ftype= str(ftype)
   value = ftype.split('0x')
   file_type= data.loc[data['A']==value[1]]['B']
   file_type = str(file_type).split()
   return file_type[1]


def file_operations(args):
    if args.type == 'mbr':
        mbr = bytearray()  # We want each index of our array to be a byte
        binary_file = open(args.file, 'rb')
        mbr = binary_file.read(512)  # The first 512 bytes are the first sector, which is the MBR
        bts = bytearray()
        for i in range(len(MBR.status)):
            status_flag = mbr[MBR.status[i]]
            key = str(hex(mbr[MBR.types[i]])).split('x')
            partition_type = check_type(hex(mbr[MBR.types[i]]))
            partition_size = struct.unpack('<I',mbr[MBR.size_start[i]:MBR.size_end[i]])
            lba = struct.unpack('<I',mbr[MBR.lba_start[i]:MBR.lba_end[i]])
            if len(key[1]) < 2:
                print(f'(0{key[1]}) {partition_type} , {lba[0]}, {partition_size[0]} ')
            else:
                print(f'({key[1]}) {partition_type} , {lba[0]}, {partition_size[0]} ')
        for k in range(len(MBR.status)):
            print(f"Partition number: {k + 1}")
            bts = mbr[MBR.firstoflast_sixteen[k]:MBR.lastoflast_sixteen[k]]
            print(f"Last 16 bytes of boot record: {(bts.hex(' '))}")

    elif args.type == 'gpt':
        gpt = bytearray()  # We want each index of our array to be a byte
        binary_file = open(args.file, 'rb')
        gpt = binary_file.read(7500)  # The first 7500 bytes
        for i in range(len(GPT.type_end)):
            partition_type = gpt[GPT.type_start[i]:GPT.type_end[i]]
            if int(partition_type.hex(),16) != int(GPT.zero):
                print(f"Partition Type GUID : {partition_type.hex()}")
                lba = struct.unpack('<Q',gpt[GPT.lba_start[i]:GPT.lba_end[i]])
                lba = lba[0]
                lbaHex = hex(lba*512)
                print(f"Starting LBA address in hex: {lbaHex}")
                endlba = struct.unpack('<Q', gpt[GPT.ending_lba_start[i]:GPT.ending_lba_end[i]])
                endlba = endlba[0]
                endlbaHex =hex(endlba*512)
                print(f"Ending LBA address in hex: {endlbaHex}")
                print(f"Starting LBA address in decimal: {lba}")
                print(f"Ending LBA address in decimal: {endlba}")


class Parser:
    def build_args(self):
        """
        Constructs command line arguments for the chain-of-custody tool
        """
        parser = argparse.ArgumentParser(description="Parser for hashing tool")
        parser.add_argument('-t',dest='type', help='Enter gpt or mbr')
        parser.add_argument('-f', dest='file', help='Enter filetype')
        parser.set_defaults(func=hasher)
        arguments = parser.parse_args()
        arguments.func(arguments)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = Parser()
    parser.build_args()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
