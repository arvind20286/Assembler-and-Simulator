def to_bin(n):
    s = ["0","0","0","0","0","0","0","0"]
    length = len(s)
    while(n != 0):
        i = int(n%2)
        s[length-1] = str(i)
        length -= 1
        n = int(n/2)
    binary = ""
    binary = binary.join(s)
    return binary


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
typ = {"A":["add","sub","mul","xor","or","and"],
        "B":["rs","ls",""],
        "C":["div","not","cmp"],
        "D":["ld","st",],
        "E":["jmp","jlt","jgt","je"],
        "F":"hlt"}
variables = {}
labels = {}
arr = []
inst_list  = []
inst_counter = 0
var_counter = 0
bi = ""
while True:
    s = input()
    inst_counter += 1
    if s[0:3] == "var":
        var_counter += 1
        variables[s[4:]] = var_counter
    if ":" in s:
        lab = list(s.split(" "))
        lab = lab[0]
        labels[lab] = inst_counter - var_counter - 1
    inst_list.append(s)
    if "hlt" in s:
        inst_list.append("hlt")
        break
for i in variables:
    variables[i] = inst_counter - var_counter 
    var_counter -= 1

for i in inst_list:
    inst = []
    inst = list(i.split(" "))
    if inst[0] in labels:
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
                result = bin(reg[inst[1]][1])
                result = result[3:]
                reg[inst[1]][1] = int(result,2)
                reg["FLAGS"][1] = 8 
        

        bi = op_cod[inst[0]] +"00"+ reg[inst[1]][0] + reg[inst[2]][0] + reg[inst[3]][0]    
    if inst[0] in typ["B"]:
        bi = op_cod[inst[0]] + reg[inst[1]][0] + to_bin(int(inst[2][1:]))
    if inst[0] in typ["C"]:
        bi = op_cod[inst[0]] +"00000"+reg[inst[1]][0] + reg[inst[2]][0]
    if inst[0] in typ["D"]:
        bi = op_cod[inst[0]]+reg[inst[1]] + to_bin(variables[inst[2]])
    if inst[0] in typ["E"]:
        bi = op_cod[inst[0]]+"000" + to_bin(labels[lab])
    if inst[0] in typ["F"]:
        bi = op_cod[inst[0]]+"00000000000"
    if inst[0] == "mov" and inst[2][0] == "$":
        reg[inst[1]][1] = int(inst[2][1:])
        bi = op_cod[inst[0]][0] + reg[inst[1]][0] + to_bin(int(inst[2][1:]))
    if inst[0] == "mov" and inst[2][0] == "R":
        reg[inst[1]][1] = reg[inst[2]][1]
        bi = op_cod[inst[0]][1]+"00000"+reg[inst[1]][0] + reg[inst[2]][0]
    arr.append(bi)
for i in range(inst_counter):
    print(arr[i])