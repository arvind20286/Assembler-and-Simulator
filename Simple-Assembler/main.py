import inp
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
        "B":["mov","rs","ls"],
        "C":["mov","div","not","cmp"],
        "D":["ld","st",],
        "E":["jmp","jlt","jgt","je"],
        "F":"hlt"}

# variables = {"variable_name":"variable_address"}
variables = {}  #dic to store variables with their address

# labels = {"label_name":"label_address"}
labels = {}  #dic to store variables with their address
inp.write_input('input.txt')
inst_list  = inp.read_input('input.txt') # stores the whole assembly code       
output = []   # stores the output
inst_counter = 0 
var_counter = 0
hlt_counter = 0
error = 0
bi = ""    # stores the binary form of the instruction

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

# function to detect overflow and set flag accordingly
def overflow(inst):
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

# function to compare values and set register accordingly
def comparison(inst):
    if reg[inst[1]][1] < reg[inst[2]][1]:
        reg["FLAGS"][1] = 4
    elif reg[inst[1]][1] > reg[inst[2]][1]:
        reg["FLAGS"][1] = 2
    else:
        reg["FLAGS"][1] = 1

def check_reg(inst,no_of_reg):
    for i in range(1,no_of_reg+1):
        if inst[i] not in reg:
            print("ERROR: Incorrect register name in line ",inst_counter)
            return True

def check_error(inst_counter):
    if inst[0] == "var":
        # condition to check if the variables are declared in the starting or not
        if inst_counter > var_counter:
            print("ERROR: General syntax error in line ",inst_counter)
            return True
        else:
            for i in inst[1]:
                # condition to check if the variables syntax is correct or not
                if (ord(i)>=48 and ord(i)<=57) or (ord(i)>=65 and ord(i)<=90) or (ord(i)>=97 and ord(i)<=122) or (ord(i) == 95):
                    continue
                else:
                    print("ERROR: Incorrect variable name in line ",inst_counter)
                    return True
            return False
    if inst[0] in labels: 
        # to check the label syntax
        for i in inst[0]:
            if (ord(i)>=48 and ord(i)<=58) or (ord(i)>=65 and ord(i)<=90) or (ord(i)>=97 and ord(i)<=122) or (ord(i) == 95):
                continue
            else:
                print("ERROR: Incorrect label name in line ",inst_counter)
                return True

        # condition to remove labels from inst[]        
        inst.remove(inst[0])
    
    if len(inst) != 0:
        if inst[0] not in op_cod:
            print("ERROR: No such instruction name in line ",inst_counter)
        
        # for wrong syntax
        else:
            if inst[0] in typ["A"]: 
                if len(inst) != 4:
                    print("ERROR: Wrong syntax used in line ",inst_counter)
                    return True
                else:
                    if "FLAGS" in inst: # To check illegal use of registers
                        print("ERROR: Illegal use of FLAGS in line ",inst_counter)
                        return True

            elif (inst[0] in typ["B"]) or (inst[0] in typ["C"]) or (inst[0] in typ["D"]):
                if len(inst) != 3:
                    print("ERROR: Wrong syntax used in line ",inst_counter) 
                    return True
                else:
                    if inst[0] in typ["B"]:
                        if inst[2][0] != "$":
                            if inst[0] == "mov":
                                return False
                            else:
                                print("ERROR: Wrong syntax used in line ",inst_counter)
                                return True
                        elif int(inst[2][1:])>255 or int(inst[2][1:])<0: # To check illegal use of immediate values
                            print("ERROR: Illegal use of immediate value in line ",inst_counter)
                            return True
                    
                    elif inst[0] in typ["C"] and (inst[1][0] != "R" or inst[2][0] != "R"):
                        if "FLAGS" in inst:
                            if "mov" in inst:
                                return False
                            else:
                                print("ERROR: Illegal use of FLAGS in line ",inst_counter)
                        else:
                            print("ERROR: Wrong syntax used in line ",inst_counter)
                        return True
                    elif inst[0] in typ["D"]:
                        if inst[1][0] !="R":
                            if "FLAGS" in inst:
                                print("ERROR: Illegal use of FLAGS in line ",inst_counter)    
                            else:
                                print("ERROR: Wrong syntax used in line ",inst_counter)
                            return True
                        else:
                            if inst[2] in labels:
                                print("ERROR: Used labels in place of variables in line ",inst_counter)
                                return True
                            elif inst[2] not in variables:
                                print("ERROR: Variable is not defined in line ",inst_counter) # To check difined variables
                                return True
            elif inst[0] in typ["E"]:
                if len(inst) != 2:
                    print("ERROR: Wrong syntax used in line ",inst_counter)
                    return True
                elif len(inst) == 2:
                    if inst[1] in variables: # To check misuse of variables
                        print("ERROR: Used variables in place of labels in line ",inst_counter)
                        return True
                    elif (inst[1]+":") not in labels: # To check undefined labels
                                print("ERROR: label is not defined in line ",inst_counter)
                                return True
    
    if hlt_counter > 1:
        print("ERROR: More than one hlt instruction used in line ",inst_counter)
        return True
    elif "hlt" in inst and inst_counter < len(inst_list):
        print("ERROR: hlt instruction is not at last in line ",inst_counter)
        return True

    
for s in inst_list:    
    inst_counter += 1
    # condition to count no. of variables and put the name of variable in variables dic
    if s[0:3] == "var":
        var_counter += 1
        variables[s[4:].strip(' ')] = var_counter

    # condition to put name of label and its address in labels dictionary
    if ":" in s:
        label_name = list(s.split(" "))[0]
        labels[label_name] = inst_counter - var_counter - 1
    
    if 'hlt' in s:
        hlt_counter += 1

j = var_counter
# loop to store the address of the variables
for i in variables:  
    variables[i] = inst_counter - j
    j -= 1

inst_counter = 0 
if hlt_counter == 0:
        print("ERROR: No hlt instruction in code")
# loop to read instruction and convert it into binary
for i in inst_list: 
    inst_counter += 1 
    
    i= list(i.split(" "))
    inst = []
    for j in i:
        if j != '':
            inst.append(j)
    if check_error(inst_counter) == True:
        error += 1
        continue
    
    if(len(inst) != 0 and inst[0] != "var"):
        if inst[0] in typ["A"]:
            if check_reg(inst, 3) == True:
                break
            overflow(inst)
            bi = op_cod[inst[0]] +"00"+ reg[inst[1]][0] + reg[inst[2]][0] + reg[inst[3]][0]    
        
        if inst[0] in typ["B"]:
            if inst[2][0] == "$":
                if check_reg(inst, 1) == True:
                    break
                if inst[0] == "mov" :
                    reg[inst[1]][1] = int(inst[2][1:])
                    bi = op_cod[inst[0]][0] + reg[inst[1]][0] + to_bin(int(inst[2][1:]),8)
                else:
                    bi = op_cod[inst[0]] + reg[inst[1]][0] + to_bin(int(inst[2][1:]),8)
                reg["FLAGS"][1] = 0
        
        if inst[0] in typ["C"]:
            if inst[2][0] == "R" or inst[2] == "FLAGS":
                if check_reg(inst, 2) == True:
                    break
                if inst[0] == "cmp":
                    comparison(inst)
                if inst[0] == "mov":
                    reg[inst[1]][1] = reg[inst[2]][1]
                    bi = op_cod[inst[0]][1] +"00000"+reg[inst[1]][0] + reg[inst[2]][0]
                else:
                    bi = op_cod[inst[0]] +"00000"+reg[inst[1]][0] + reg[inst[2]][0]

        
        if inst[0] in typ["D"]:
            if check_reg(inst, 1) == True:
                break
            bi = op_cod[inst[0]]+reg[inst[1]][0] + to_bin(variables[inst[2]],8)
            reg["FLAGS"][1] = 0
        
        if inst[0] in typ["E"]:
            bi = op_cod[inst[0]]+"000" + to_bin(labels[label_name],8)
            reg["FLAGS"][1] = 0
        
        if inst[0] in typ["F"]:
            bi = op_cod[inst[0]]+"00000000000"
            reg["FLAGS"][1] = 0
        output.append(bi)

if error == 0:
    for i in output:
        print(i)