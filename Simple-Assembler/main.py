
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
MEM = ['0000000000000000']*256
temp_MEM = inp.read_input('bin_input.txt') 
for i in range(len(temp_MEM)):
    MEM[i] = temp_MEM[i]
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
        if RF[int(instruction[7:10],2)] < 0:
            RF[int(instruction[7:10],2)] = 0
            RF[7] = 8 
    
def comparison(reg1, reg2):
    if RF[reg1] < RF[reg2]:
        RF[7] = 4
    elif RF[reg1] > RF[reg2]:
        RF[7] = 2
    else:
        RF[7] = 1

def EE(instruction):
    op_cod = instruction[0:5]
    if op_cod in typ["A"]:
        if op_cod == '00000':
            RF[int(instruction[7:10],2)] = RF[int(instruction[10:13],2)] + RF[int(instruction[13:16],2)]
            overflow(instruction)
        elif op_cod == '00001':
            RF[int(instruction[7:10],2)] = RF[int(instruction[10:13],2)] - RF[int(instruction[13:16],2)]
            overflow(instruction)
        elif op_cod == '00110':
            RF[int(instruction[7:10],2)] = RF[int(instruction[10:13],2)] * RF[int(instruction[13:16],2)]
            overflow(instruction)
        elif op_cod == '01010':
            RF[int(instruction[7:10],2)] = RF[int(instruction[10:13],2)] ^ RF[int(instruction[13:16],2)]
            RF[7] = 0
        elif op_cod == '01011':
            RF[int(instruction[7:10],2)] = RF[int(instruction[10:13],2)] | RF[int(instruction[13:16],2)]    
            RF[7] = 0
        elif op_cod == '01100':
            RF[int(instruction[7:10],2)] = RF[int(instruction[10:13],2)] & RF[int(instruction[13:16],2)]
            RF[7] = 0
    elif instruction[0:5] in typ["B"]:
        if instruction[0:5] == '00010': 
            RF[int(instruction[5:8],2)] = int(instruction[8:16],2)
        elif instruction[0:5] == '01000':
             RF[int(instruction[5:8],2)] =RF[int(instruction[5:8],2)]>>int(instruction[8:16],2)
        elif instruction[0:5] == '01001': 
            RF[int(instruction[5:8],2)] =RF[int(instruction[5:8],2)]<<int(instruction[8:16],2)
        RF[7] = 0
    elif op_cod in typ["C"]:
        if op_cod == '00011':
            RF[int(instruction[10:13],2)] = RF[int(instruction[13:16],2)]
            RF[7] = 0
        elif op_cod == '00111':
            RF[0] = int(RF[int(instruction[10:13],2)] / RF[int(instruction[13:16],2)])
            RF[1] = int(RF[int(instruction[10:13],2)] % RF[int(instruction[13:16],2)])
            RF[7] = 0
        elif op_cod == '01101':
            RF[int(instruction[10:13],2)] = ~RF[int(instruction[13:16],2)]
            RF[7] = 0
        elif op_cod == '01110':
            comparison(int(instruction[10:13],2), int(instruction[13:16],2))
    elif op_cod in typ["D"]:
        if op_cod == '00100':
            RF[int(instruction[5:8],2)] = int(MEM[int(instruction[8:16],2)],2)
        elif op_cod == '00101':
            MEM[int(instruction[8:16],2)] = to_bin(RF[int(instruction[5:8],2)],16)
        RF[7] = 0
    elif op_cod in typ["E"]:
        if op_cod == '01111':
            return int(instruction[8:16],2)
        elif op_cod == '10000':
            if RF[7] == 4:
                return int(instruction[8:16],2)
        elif op_cod == '10001':
            if RF[7] == 2:
                return int(instruction[8:16],2)
        elif op_cod == '10010':
            if RF[7] == 1:
                return int(instruction[8:16],2)
        RF[7] = 0
    return PC+1       

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
