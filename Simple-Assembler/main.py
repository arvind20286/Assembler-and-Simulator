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
reg = {"R1":"001",
        "R2":"010",
        "R3":"011",
        "R4":"100",
        "R5":"101",
        "R6":"110",
        "FLAGS":"111"}
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
        bi = op_cod[inst[0]] +"00"+ reg[inst[1]] + reg[inst[2]] + reg[inst[3]]    
    if inst[0] in typ["B"]:
        bi = op_cod[inst[0]] + reg[inst[1]] + to_bin(int(inst[2][1:]))
    if inst[0] in typ["C"]:
        bi = op_cod[inst[0]] +"00000"+reg[inst[1]] + reg[inst[2]]
    if inst[0] in typ["D"]:
        bi = op_cod[inst[0]]+reg[inst[1]] + to_bin(variables[inst[2]])
    if inst[0] in typ["E"]:
        bi = op_cod[inst[0]]+"000" + to_bin(labels[lab])
    if inst[0] in typ["F"]:
        bi = op_cod[inst[0]]+"00000000000"
    if inst[0] == "mov" and inst[2][0] == "$":
        bi = op_cod[inst[0]][0] + reg[inst[1]] + to_bin(int(inst[2][1:]))
    if inst[0] == "mov" and inst[2][0] == "R":
        bi = op_cod[inst[0]][1]+"00000"+reg[inst[1]] + reg[inst[2]]
    arr.append(bi)
for i in range(inst_counter):
    print(arr[i])
