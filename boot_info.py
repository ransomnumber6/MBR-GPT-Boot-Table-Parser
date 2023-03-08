import hashlib
import argparse
import struct
import pandas as pd


class MBR:
    status = [0x1BE, 0x1CE, 0x1DE, 0x1EE]
    size_start = [0x1CA, 0x1DA, 0x1EA, 0x1FA]
    size_end = [0x1CE, 0x1DE, 0x1EE, 0x1FE]
    types = [0x1C2, 0x1D2, 0x1E2, 0x1F2]
    lba_start = [0x1C6, 0x1D6, 0x1E6, 0x1F6]
    lba_end = [0x1CA, 0x1DA, 0x1EA, 0x1FA]
    firstoflast_sixteen = [0x1BE, 0x1CE, 0x1DE, 0x1EE]
    lastoflast_sixteen = [0x1CE, 0x1DE, 0x1EE, 0x1FE]


class GPT:
    type_start = [0x200, 0x280, 0x300, 0x380]
    type_end = [0x20F, 0x28F, 0x30F, 0x38F]
    lba_start = [0x220, 0x2A0, 0x320, 0x3A0]
    lba_end = [0x228, 0x2A8, 0x328, 0x3A8]
    zero = 00000000000000
    ending_lba_start = [0x227, 0x2A7, 0x327, 0x3A7]
    ending_lba_end = [0x22F, 0x2AF, 0x32F, 0x3AF]


def hasher(args):
    # Use a breakpoint in the code line below to debug your script.

    md5 = hashlib.md5(open(f"{args.file}", 'rb').read()).hexdigest()
    sha = hashlib.sha256(open(f"{args.file}", 'rb').read()).hexdigest()
    with open(f'MD5-{args.file}.txt', 'w') as f:
        f.write(md5)
    with open(f'SHA-256-{args.file}.txt', 'w') as f:
        f.write(sha)
    file_operations(args)


def check_type(ftype):
    data = pd.read_csv('PartitionTypes.csv')
    ftype = str(ftype)
    value = ftype.split('0x')
    file_type = data.loc[data['A'] == value[1]]['B']
    file_type = str(file_type).split()
    return file_type[1]


def file_operations(args):
    if args.type == 'mbr':
        mbr = bytearray()  # We want each index of our array to be a byte
        binary_file = open(args.file, 'rb')
        mbr = binary_file.read(512)  # The first 512 bytes are the first sector, which is the MBR
        print()
        for i in range(len(MBR.status)):
            status_flag = mbr[MBR.status[i]]
            key = str(hex(mbr[MBR.types[i]])[2:])
            partition_type = check_type(str(hex(mbr[MBR.types[i]])))
            partition_size = struct.unpack('<I', mbr[MBR.size_start[i]:MBR.size_end[i]])
            lba = struct.unpack('<I', mbr[MBR.lba_start[i]:MBR.lba_end[i]])
            if len(key) < 2:
                key = f"{0x0}{int(key, 16)}"
            else:
                key = key
            print(f'({key}) {partition_type} , {lba[0]}, ' + str(partition_size[0] * 512))
        rawfile = open(args.file, "rb")
        for i in range(len(MBR.status)):
            offset = int(MBR.status[i])
            partition_info = mbr[offset:offset + 16]
            first_sector = int.from_bytes(partition_info[8:12], byteorder="little")
            rawfile.seek(first_sector)              # search file for given sector
            boot_info = rawfile.read(512)           # read 512 bytes (32 lines)
            partition_num = i + 1
            print(f"Partition number: {str(partition_num)}")
            print(f"Last 16 bytes of boot record: {boot_info.hex(' ')[-47:]}")  # with spaces print last 47 characters (spaces count as chars)

    elif args.type == 'gpt':
        gpt = bytearray()
        binary_file = open(args.file, 'rb')
        gpt = binary_file.read(7500)  # The first 7500 bytes
        print()
        for i in range(len(GPT.type_end)):
            partition_type = gpt[GPT.type_start[i]:GPT.type_end[i]]
            print(f"Partition Type GUID : {(partition_type.hex()).upper()}")
            lba = struct.unpack('<Q', gpt[GPT.lba_start[i]:GPT.lba_end[i]])
            lba = lba[0]
            lbaHex = hex(lba * 512)
            print(f"Starting LBA address in hex: {lbaHex}")
            endlba = struct.unpack('<Q', gpt[GPT.ending_lba_start[i]:GPT.ending_lba_end[i]])
            endlba = endlba[0]
            endlbaHex = hex(endlba * 512)
            print(f"Ending LBA address in hex: {endlbaHex}")
            print(f"Starting LBA address in decimal: {lba}")
            print(f"Ending LBA address in decimal: {endlba}")


class Parser:
    def build_args(self):
        """
        Constructs command line arguments for the chain-of-custody tool
        """
        parser = argparse.ArgumentParser(description="Parser for hashing tool")
        parser.add_argument('-t', dest='type', help='Enter gpt or mbr')
        parser.add_argument('-f', dest='file', help='Enter filetype')
        parser.set_defaults(func=hasher)
        arguments = parser.parse_args()
        arguments.func(arguments)



if __name__ == '__main__':
    parser = Parser()
    parser.build_args()

