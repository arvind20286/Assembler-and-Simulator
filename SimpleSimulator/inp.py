import os
from sys import stdin
cwd =  os.path.dirname(__file__)
os.chdir(cwd)
def write_input(file_name):
    list_of_files = os.listdir()
    if file_name in list_of_files:
        myfile = open(file_name,'w')
        for line in stdin:
            if line == '\n':
                break
            myfile.write(line) 
        
    else:
        with open(file_name,'w') as myfile:
            pass
            for line in stdin:
                    if line == '\n':
                        break
                    myfile.write(line)
        myfile.close()

def read_input(file_name):
    myfile = open(file_name,'r')
    temp_inst = myfile.readlines()
    for i in range(len(temp_inst)):
        temp_inst[i] = temp_inst[i].strip('\n')
        temp_inst[i] = temp_inst[i].replace('\t',' ')

    myfile.close()
    return temp_inst

