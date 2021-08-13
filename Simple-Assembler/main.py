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

# op_cod = {"inst_name":"op_code"}
op_cod = {"mov":["00010","00011"],
            "hlt":"10011",
            "add":"00000",
            "sub":"00001",
            "ld":"00100",
            "st":"00101",
            "mul":"00110",
            "div":"00111",
            "rs":"01000",
            "ls":"01001",
            "xor":"01010",
            "or":"01011",
            "and":"01100",
            "not":"01101",
            "cmp":"01110",
            "jmp":"01111",
            "jlt":"10000",
            "jgt":"10001",
            "je":"10010"}

# reg = {reg_name:[reg_add,reg_value]}
reg = { "R0":["000",0],
        "R1":["001",0],
        "R2":["010",0],
        "R3":["011",0],
        "R4":["100",0],
        "R5":["101",0],
        "R6":["110",0],
        "FLAGS":["111",0]}

# typ = {"type_of_inst":["inst_names"]}
typ = {"A":["add","sub","mul","xor","or","and"],
        "B":["rs","ls",""],
        "C":["div","not","cmp"],
        "D":["ld","st",],
        "E":["jmp","jlt","jgt","je"],
        "F":"hlt"}

# variables = {"variable_name":"variable_address"}
variables = {}  #dic to store variables with their address

# labels = {"label_name":"label_address"}
labels = {}  #dic to store variables with their address
 
arr = []   # stores the output
inst_list  = [] # stores the whole assembly code
inst_counter = 0 
var_counter = 0
bi = ""    # stores the binary form of the instruction

while True:    # loop to take the input and store it in inst_list
    s = input()
    inst_counter += 1
    if s[0:3] == "var":
        var_counter += 1
        variables[s[4:]] = var_counter
    if ":" in s:
        lab = list(s.split(" "))
        lab = lab[0] # stores the name of the lable
        labels[lab] = inst_counter - var_counter - 1
    inst_list.append(s)
    if "hlt" in s:
        inst_list.append("hlt")
        break

for i in variables:  # loop to store the address of the variables
    variables[i] = inst_counter - var_counter 
    var_counter -= 1

for i in inst_list: # loop to read instruction and convert it into binary
    inst = list(i.split(" "))
    if inst[0] in labels: # condition to remove labels from inst[]
        lab = inst[0]
        inst.remove(inst[0])
    if inst[0] in typ["A"]:
        if inst[0] == "add":
            reg[inst[1]][1] = reg[inst[2]][1] + reg[inst[3]][1]
        elif inst[0] == "mul":
            reg[inst[1]][1] = reg[inst[2]][1] * reg[inst[3]][1]
        elif inst[0] == "sub":
            reg[inst[1]][1] = reg[inst[2]][1] - reg[inst[3]][1]
            if reg[inst[1]][1] < 0:
                reg[inst[1]][1] = 0
                reg["FLAGS"][1] = 8 
        if reg[inst[1]][1] > 65535:
                result = to_bin(reg[inst[1]][1],16)
                reg[inst[1]][1] = int(result,2)
                reg["FLAGS"][1] = 8 
        bi = op_cod[inst[0]] +"00"+ reg[inst[1]][0] + reg[inst[2]][0] + reg[inst[3]][0]    
    if inst[0] in typ["B"]:
        bi = op_cod[inst[0]] + reg[inst[1]][0] + to_bin(int(inst[2][1:]),8)
        reg["FLAGS"][1] = 0
    if inst[0] in typ["C"]:
        if inst[0] == "cmp":
            if reg[inst[1]][1] < reg[inst[2]][1]:
                reg["FLAGS"][1] = 4
            elif reg[inst[1]][1] > reg[inst[2]][1]:
                reg["FLAGS"][1] = 2
            else:
                reg["FLAGS"][1] = 1
        else:
            reg["FLAGS"][1] = 0
        bi = op_cod[inst[0]] +"00000"+reg[inst[1]][0] + reg[inst[2]][0]
    if inst[0] in typ["D"]:
        bi = op_cod[inst[0]]+reg[inst[1]] + to_bin(variables[inst[2]],8)
        reg["FLAGS"][1] = 0
    if inst[0] in typ["E"]:
        bi = op_cod[inst[0]]+"000" + to_bin(labels[lab],8)
        reg["FLAGS"][1] = 0
    if inst[0] in typ["F"]:
        bi = op_cod[inst[0]]+"00000000000"
        reg["FLAGS"][1] = 0
    if inst[0] == "mov" and inst[2][0] == "$":
        reg[inst[1]][1] = int(inst[2][1:])
        bi = op_cod[inst[0]][0] + reg[inst[1]][0] + to_bin(int(inst[2][1:]),8)
        reg["FLAGS"][1] = 0
    if inst[0] == "mov" and (inst[2][0] == "R" or inst[2] == "FLAGS"):
        reg[inst[1]][1] = reg[inst[2]][1]
        bi = op_cod[inst[0]][1]+"00000"+reg[inst[1]][0] + reg[inst[2]][0]
        reg["FLAGS"][1] = 0
    arr.append(bi)
for i in range(inst_counter):
    print(arr[i])