import hashlib
import argparse
import struct
import pandas as pd
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
status = [0x1BE,0x1CE,0x1DE,0x1EE]
size_start =[0x1CA,0x1DA,0x1EA,0x1FA]
size_end =[0x1CE,0x1DE,0x1EE,0x1FE]
types = [0x1C2,0x1D2,0x1E2,0x1F2]
lba_start = [0x1C6,0x1D6,0x1E6,0x1F6]
lba_end = [0x1CA,0x1DA,0x1EA,0x1FA]

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

        for i in range(len(status)):
            status_flag = mbr[status[i]]
            key = str(hex(mbr[types[i]])).split('x')
            partition_type = check_type(hex(mbr[types[i]]))
            partition_size = struct.unpack('<I',mbr[size_start[i]:size_end[i]])
            lba = struct.unpack('<I',mbr[lba_start[i]:lba_end[i]])
            print(f'({key[1]}) {partition_type} , {lba[0]} , {partition_size[0]} ')
    elif args.type == 'gpt':
        print('here')

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
