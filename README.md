# Student Info #
<br> Name: Trevor Ransom <br />
<br> ASU ID: 1216424209 <br />
# Description #
This program was written in python. I have written it so that the offsets for MBR and GPT are contained in an assortment of lists contained in two classes. <br />
The program will take in command line arguments for file type and name and then will pass those arguments to various methods. <br />
This methods will open the .raw file as read only and parse through it either by creating a byte array or using a for loop to move through the file. <br />
The first method is used to find the file type, LBA and sector size. The second method is used to determine the last 16 bytes of each partition. <br />
