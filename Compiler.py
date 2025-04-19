# Compile a .alice file into a .duck file

with open("HelloWorld.alice", "r") as f:
    data = f.read()

# parse labels. The difference between a reference and a definition of a label is where it is located.
labels = {}
# This code gets us all the labels
for line_number, line in enumerate(data.split("\n")):
    instruction = line.split(" ")
    if instruction[0].startswith("."):
        label_name = instruction.pop(0)
        labels[label_name] = str(line_number)


# This code replaces all instances of the label with its variable
program_with_parsed_labels = ""
for line_number, line in enumerate(data.split("\n")):
    instruction = line.split(" ")
    if instruction[0].startswith("."):  # Make sure that the label definition is not referenced
        instruction.pop(0)
    for index, instr in enumerate(instruction):
        if instr in labels:
            instruction[index] = labels[instr]
    program_with_parsed_labels += " ".join(instruction) + "\n"


# And then this code does the rest
print(program_with_parsed_labels)

machine_code = ""
for line in program_with_parsed_labels.rstrip().split("\n"):
    parsed_line = ""
    arguments = line.split(" ")
    temp = []
    for arg in arguments:
        if arg == "" or arg == ";":
            break
        temp.append(arg)
    arguments = temp
    print(arguments)
    head = arguments.pop(0)
    TRIPLE_ARGUMENTS = ["ADD", "SUB", "ORR", "NOR", "AND", "XOR"]  # 6 for the ALU to do
    DOUBLE_ARGUMENTS = ["RSH", "STR", "LOD"]  # Takes 2 4 bit
    r1 = "0000"
    r2 = "0000"
    r3 = "0000"
    if head in TRIPLE_ARGUMENTS:
        # We can safely assume we have 3 registers.
        r1, r2, r3 = arguments
        r1 = bin(int(r1.removeprefix("r")))[2:]  # Remove prefix r
        r2 = bin(int(r2.removeprefix("r")))[2:]
        r3 = bin(int(r3.removeprefix("r")))[2:]
        r1 = "0"*(4-len(r1)) + r1
        r2 = "0"*(4-len(r2)) + r2
        r3 = "0"*(4-len(r3)) + r3
    if head in DOUBLE_ARGUMENTS:
        r1, r2 = arguments
        r1 = bin(int(r1.removeprefix("r")))[2:]  # Remove prefix r
        r2 = bin(int(r2.removeprefix("r")))[2:]
        r1 = "0" * (4 - len(r1)) + r1
        r2 = "0" * (4 - len(r2)) + r2
    if head == "NOP":
        parsed_line = "0000000000000000"
    elif head == "HLT":
        parsed_line = "0001000000000000"
    elif head == "ADD":
        parsed_line = f"0010{r1}{r2}{r3}"
    elif head == "SUB":
        parsed_line = f"0011{r1}{r2}{r3}"
    elif head == "ORR":
        parsed_line = f"0100{r1}{r2}{r3}"
    elif head == "NOR":
        parsed_line = f"0101{r1}{r2}{r3}"
    elif head == "AND":
        parsed_line = f"0110{r1}{r2}{r3}"
    elif head == "XOR":
        parsed_line = f"0111{r1}{r2}{r3}"
    elif head == "RSH":
        parsed_line = f"1000{r1}{r2}0000"
    elif head == "STR":
        parsed_line = f"1011{r1}{r2}0000"
    elif head == "LOD":
        parsed_line = f"1010{r1}{r2}0000"
    elif head == "LDI":
        r1, immediate = arguments
        r1 = bin(int(r1.removeprefix("r")))[2:]  # Remove prefix r
        r1 = "0" * (4 - len(r1)) + r1
        immediate = bin(int(immediate))[2:]
        immediate = "0" * (8 - len(immediate)) + immediate
        parsed_line = f"1001{r1}{immediate}"
    elif head == "JMP":
        address = arguments.pop(0)
        address = bin(int(address))[2:]
        address = "0" * (10 - len(address)) + address
        parsed_line = f"110000{address}"
    elif head == "BIF":
        flag, address = arguments
        flag = flag.lower()
        if flag == "carry":
            flag = "01"
        elif flag == "zero":
            flag = "00"
        elif flag == "!carry":
            flag = "11"
        elif flag == "!zero":
            flag = "10"
        address = bin(int(address))[2:]
        address = "0" * (10 - len(address)) + address
        parsed_line = f"1101{flag}{address}"
    elif head == "CAL":
        address = arguments.pop(0)
        address = bin(int(address))[2:]
        address = "0" * (10 - len(address)) + address
        parsed_line = f"111000{address}"
    elif head == "RET":
        parsed_line = "1111000000000000"
    machine_code += parsed_line + "\n"


with open("HelloWorld.duck", "w") as output_file:
    output_file.write(machine_code.rstrip())









