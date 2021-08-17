from SimpleSimulator.inp import read_input
import inp
typ = {"A":["00000","00001","00110","01010","01011","01100"],
        "B":["00010","01000","01001"],
        "C":["00011","00111","01101","01110"],
        "D":["00100","00101",],
        "E":["01111","10000","10001","10010"],
        "F":"10011"}

# RF = [R0, R1, R2, ....,R6,FLAGS]
RF = [0]*8
inp.write_input('bin_input.txt')
MEM = ['']*256
MEM = inp.read_input('bin_input.txt') + MEM
PC = 0
halted = False

def to_bin(n,no_of_bits):  # function to covert decimal no. to binary no.
    s = ["0"]*no_of_bits
    while(no_of_bits != 0):
        i = int(n%2)
        s[no_of_bits-1] = str(i)
        no_of_bits -= 1
        n = int(n/2)
    binary = ""
    binary = binary.join(s)
    return binary

def overflow(instruction):
    if instruction[0:5] == "00000" and instruction[0:5] == "00110":
        if RF[int(instruction[7:10],2)] > 65535:
            RF[instruction[7:10]] = int(to_bin(RF[instruction[7:10]],16),2)
            RF[7] = 8 
    elif instruction[0:5] == "00001":
        if RF[instruction[7:10]] < 0:
            RF[instruction[7:10]] = 0
            RF[7] = 8 
    
def comparison(instruction):
    if RF[int(instruction[10:13],2)] < RF[int(instruction[13:16],2)]:
        RF[7] = 4
    elif RF[int(instruction[10:13],2)] > RF[int(instruction[13:16],2)]:
        RF[7] = 2
    else:
        RF[7] = 1

def EE(instruction):
    if instruction[0:5] in typ["A"]:
        if instruction[0:5] == '00000':
            RF[int(instruction[7:10],2)] = RF[int(instruction[10:13],2)] + RF[int(instruction[13:16],2)]
            overflow(instruction)
        elif instruction[0:5] == '00001':
            RF[int(instruction[7:10],2)] = RF[int(instruction[10:13],2)] - RF[int(instruction[13:16],2)]
            overflow(instruction)

while(halted != True):
    instruction = MEM[PC]
    if instruction[0:5] == '10011':
        halted = True
    new_PC = EE(instruction)
    print(to_bin(PC,8),end=' ')
    for i in RF:
        print(to_bin(i,16),end=' ')
    print()
    PC = new_PC

for i in MEM:
    print(i)
