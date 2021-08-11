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
        "F":["hlt"]}
arr = []
inst = []
inst_counter = 0
while True:
    s = input()
    inst = list(s.split(" "))
    inst_counter+=1
    if inst[0] in typ["A"]:
        bin = op_cod[inst[0]] +"00"+ reg[inst[1]] + reg[inst[2]] + reg[inst[3]]    
    if inst[0] in typ["B"]:
        bin = op_cod[inst[0][0]] + reg[inst[1]] + bin(int(inst[2][1]))
    if inst[0] in typ["C"]:
        bin = op_cod[inst[0][1]]+"00000"+reg[inst[1]] + reg[inst[2]]
    if inst[0] in typ["D"]:
        bin = op_cod[inst[0]]+reg[inst[1]] + memadress
    if inst[0] in typ["E"]:
        bin = op_cod[inst[0]]+"000" + memadress
    if inst[0] in typ["F"]:
        bin = op_cod[inst[0]]+"00000000000"
        arr.append(bin)
        break
    if inst[0] == "mov" and inst[2][0] == "$":
        bin = op_cod[inst[0]][0] + reg[inst[1]] + bin(int(inst[2][1]))
    if inst[0] == "mov" and inst[2][0] == "R":
        bin = op_cod[inst[0]][1]+"00000"+reg[inst[1]] + reg[inst[2]]
    arr.append(bin)
for i in range(inst_counter):
    print(arr[i])