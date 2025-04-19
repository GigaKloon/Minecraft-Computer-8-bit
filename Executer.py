class Byte:
    def __init__(self):
        self.bits = [False for _ in range(8)]

    def __int__(self):
        ret = 0
        for bit in self.bits:
            ret *= 2
            ret += bit
        return ret

    def __or__(self, other):
        ret = Byte()
        for index in range(8):
            ret.bits[index] = self.bits[index] or other.bits[index]
        return ret

    def __and__(self, other):
        ret = Byte()
        for index in range(8):

            ret.bits[index] = self.bits[index] and other.bits[index]
        return ret

    def __xor__(self, other):
        ret = Byte()
        for index in range(8):
            ret.bits[index] = self.bits[index] ^ other.bits[index]
        return ret

    def __invert__(self):
        ret = Byte()
        for index in range(8):
            ret.bits[index] = not self.bits[index]
        return ret
    
    def __str__(self):
        ret = ""
        for bit in self.bits:
            if bit:
                ret += "1"
            else:
                ret += "0"
        return ret
    
    def __add__(self, other):
        self_num = int(self)
        other_num = int(other)
        bits = bin((self_num + other_num) % 256)[2:]
        padding_zeros = "0"*(8 - len(bits))
        ret = Byte()
        for index, bit in enumerate(padding_zeros + bits):
            if bit == "0":
                ret.bits[index] = False
            else:
                ret.bits[index] = True
        return ret

    def __sub__(self, other):
        self_num = int(self)
        other_num = int(other)
        bits = bin((self_num - other_num) % 256)[2:]
        padding_zeros = "0" * (8 - len(bits))
        ret = Byte()
        for index, bit in enumerate(padding_zeros + bits):
            if bit == "0":
                ret.bits[index] = False
            else:
                ret.bits[index] = True
        return ret

    @staticmethod
    def from_int(num):
        bits = bin(num % 256)[2:]
        padding_zeros = "0" * (8 - len(bits))
        ret = Byte()
        for index, bit in enumerate(padding_zeros + bits):
            if bit == "0":
                ret.bits[index] = False
            else:
                ret.bits[index] = True
        return ret


class Core:
    def __init__(self, console):
        # Step 1. Generate Register File
        self.register_file = [Byte() for _ in range(16)]
        # Step 2. Generate Main Memory
        self.ram = [Byte() for _ in range(256)]
        self.carry_flag = False
        self.zero_flag = False
        self.program_counter = 0
        self.call_stack = []
        self.console = console

    def _add(self, r1=0, r2=0, r3=0):
        r1 %= 16
        r2 %= 16
        r3 %= 16
        r1_value = self.register_file[r1]
        r2_value = self.register_file[r2]
        if (int(r1_value) + int(r2_value)) % 256 == 0:  # If the integer sum of both values, modulo 256, is 0
            self.zero_flag = True
        else:
            self.zero_flag = False
        if int(r1_value) + int(r2_value) > 255:  # If the integer sum of both values exceed 255
            self.carry_flag = True
        else:
            self.carry_flag = False
        self.register_file[r3] = (r1_value + r2_value)

    def _sub(self, r1=0, r2=0, r3=0):
        r1 %= 16
        r2 %= 16
        r3 %= 16
        r1_value = self.register_file[r1]
        r2_value = self.register_file[r2]
        if int(r1_value) == int(r2_value):
            self.zero_flag = True
        else:
            self.zero_flag = False
        if int(r1_value) < int(r2_value):
            self.carry_flag = True
        else:
            self.carry_flag = False
        self.register_file[r3] = (r1_value - r2_value)

    def _or(self, r1=0, r2=0, r3=0):
        r1 %= 16
        r2 %= 16
        r3 %= 16
        r1_value = self.register_file[r1]
        r2_value = self.register_file[r2]
        self.carry_flag = False  # Remind me exactly how a bitwise OR could carry over.
        result = r1_value | r2_value
        if int(result) == 0:
            self.zero_flag = True  # I really don't see how I need to make this obvious
        else:
            self.zero_flag = False
        self.register_file[r3] = result

    def _nor(self, r1=0, r2=0, r3=0):
        r1 %= 16
        r2 %= 16
        r3 %= 16
        r1_value = self.register_file[r1]
        r2_value = self.register_file[r2]
        self.carry_flag = False  # Remind me exactly how a bitwise NOR could carry over.
        result = ~(r1_value | r2_value)  # Whopper whopper whopper whopper a plane hit the second tower
        if int(result) == 0:
            self.zero_flag = True
        else:
            self.zero_flag = False
        self.register_file[r3] = result

    def _and(self, r1=0, r2=0, r3=0):
        r1 %= 16
        r2 %= 16
        r3 %= 16
        r1_value = self.register_file[r1]
        r2_value = self.register_file[r2]
        self.carry_flag = False  # Remind me exactly how a bitwise NOR could carry over.
        result = r1_value & r2_value
        if int(result) == 0:
            self.zero_flag = True
        else:
            self.zero_flag = False
        self.register_file[r3] = result

    def _xor(self, r1=0, r2=0, r3=0):
        r1 %= 16
        r2 %= 16
        r3 %= 16
        r1_value = self.register_file[r1]
        r2_value = self.register_file[r2]
        self.carry_flag = False  # Remind me exactly how a bitwise XOR could carry over.
        result = r1_value ^ r2_value
        if int(result) == 0:
            self.zero_flag = True
        else:
            self.zero_flag = False
        self.register_file[r3] = result

    def _inc(self, r1=0, r2=0):
        r1 %= 16
        r2 %= 16
        r1_value = self.register_file[r1]
        result = r1_value + Byte.from_int(1)
        if int(result) % 256 == 0:
            self.zero_flag = True
        else:
            self.zero_flag = False
        if int(result) > 255:
            self.carry_flag = True
        else:
            self.carry_flag = False
        self.register_file[r2] = result

    def _dec(self, r1=0, r2=0):
        r1 %= 16
        r2 %= 16
        r1_value = self.register_file[r1]
        result = r1_value + Byte.from_int(255)
        if int(result) % 256 == 0:
            self.zero_flag = True
        else:
            self.zero_flag = False
        if int(result) > 255:
            self.carry_flag = True
        else:
            self.carry_flag = False
        self.register_file[r2] = result

    def _rsh(self, r1=0, r2=0):
        r1 %= 16
        r2 %= 16
        r1_value = self.register_file[r1]
        result = Byte.from_int(int(r1_value) >> 1)
        self.carry_flag = False
        if int(result) % 256 == 0:
            self.zero_flag = True
        else:
            self.zero_flag = False
        self.register_file[r2] = result

    def _ldi(self, r1=0, immediate=0):
        r1 %= 16
        self.register_file[r1] = Byte.from_int(immediate)

    def _lod(self, dest=0, pointer=0):
        pointer %= 16
        dest %= 16
        pointer_value = self.register_file[pointer]
        self.register_file[dest] = self.ram[(int(pointer_value))]

    def _str(self, data, pointer):
        pointer %= 16
        data %= 16
        pointer_value = self.register_file[pointer]
        self.ram[(int(pointer_value))] = self.register_file[data]

    def _jmp(self, address):
        self.program_counter = address

    def _bif(self, flag, address):
        jump = False
        if flag == 0b00:
            jump = self.zero_flag
        elif flag == 0b01:
            jump = self.carry_flag
        elif flag == 0b10:
            jump = not self.zero_flag
        elif flag == 0b11:
            jump = not self.carry_flag
        else:
            raise ValueError("Invalid flag")
        if jump:
            self.program_counter = address
        else:
            self.program_counter += 1

    def _call(self, address):
        self.call_stack.append(self.program_counter)
        self.program_counter = address

    def _return(self):
        self.program_counter = self.call_stack.pop() + 1  # If we returned to where we called,
        # we would just call function again

    def _exec(self, instruction):
        opcode = instruction[0:4]
        NOP = "0000"
        HLT = "0001"
        ADD = "0010"
        SUB = "0011"
        ORR = "0100"
        NOR = "0101"
        AND = "0110"
        XOR = "0111"
        RSH = "1000"
        LDI = "1001"
        LOD = "1010"
        STR = "1011"
        JMP = "1100"
        BIF = "1101"
        CAL = "1110"
        RET = "1111"
        r1 = int(instruction[4:8], 2)
        r2 = int(instruction[8:12], 2)
        r3 = int(instruction[12:16], 2)
        if opcode == NOP:
            print(f"No Operation On Instruction {self.program_counter}")
            self.program_counter += 1
        elif opcode == HLT:
            print("Halting Operation")
            return 1
        elif opcode == ADD:
            self._add(r1, r2, r3)
            self.program_counter += 1
        elif opcode == SUB:
            self._sub(r1, r2, r3)
            self.program_counter += 1
        elif opcode == ORR:
            self._or(r1, r2, r3)
            self.program_counter += 1
        elif opcode == NOR:
            self._nor(r1, r2, r3)
            self.program_counter += 1
        elif opcode == AND:
            self._and(r1, r2, r3)
            self.program_counter += 1
        elif opcode == XOR:
            self._xor(r1, r2, r3)
            self.program_counter += 1
        elif opcode == RSH:
            self._rsh(r1, r2)
            self.program_counter += 1
        elif opcode == LDI:
            immediate = int(instruction[8:16], 2)
            self._ldi(r1, immediate)
            self.program_counter += 1
        elif opcode == LOD:
            self._lod(r1, r2)
            self.program_counter += 1
        elif opcode == STR:
            print(f"STORING {r1} into {r2}")
            self._str(r1, r2)
            self.program_counter += 1
        elif opcode == JMP:
            address = int(instruction[6:16], 2)
            self._jmp(address)
        elif opcode == BIF:
            address = int(instruction[6:16], 2)
            flag = int(instruction[4:6], 2)
            self._bif(flag, address)
        elif opcode == CAL:
            address = int(instruction[6:16], 2)
            self._call(address)
        elif opcode == RET:
            self._return()
        else:
            raise ValueError("Excuse how in the actual fuck")
        return 0

    def exec(self, instructions):
        self.program_counter = 0
        counters = []
        while True:
            counters.append(self.program_counter)
            print(self.program_counter, instructions[self.program_counter])
            result = self._exec(instructions[self.program_counter])
            self.console.exec()
            if result == 1:
                break
        return counters

    def exec_with_debug(self, instructions):
        self.program_counter = 0
        counters = []
        while True:
            counters.append(self.program_counter)
            input(f"We are executing instruction {self.program_counter}: ")
            print(instructions[self.program_counter])
            result = self._exec(instructions[self.program_counter])
            self.console.exec()
            print(f"Flags: {self.carry_flag}, {self.zero_flag}")
            for index, byte in enumerate(self.register_file):
                print(hex(index)[2:], byte, int(byte))
            if result == 1:
                break
        return counters


class Console:
    def __init__(self, core):
        self.core = core
        self.data = ["\x00"] * 256

    def exec(self):
        # Read core data
        if int(self.core.ram[255]) == 1:
            # Received clock signal
            self.core.ram[255] = Byte.from_int(0)  # Remember. You can write to it as much as the main core can.
            pointer = int(self.core.ram[254])
            data = int(self.core.ram[253])
            self.data[pointer] = chr(data)
        print("".join(self.data))





if __name__ == "__main__":
    core = Core(console=None)  # Temporarily pass None

    console = Console(core)

    core = Core(console)

    console.core = core

    assert console.core is core
    assert core.console is console
    age = 17
    age_string = "0" * (8 - len(bin(age)[2:])) + bin(age)[2:]
    data = open("HelloWorld.duck", "r").read()
    instructions = data.split("\n")
    print(core.exec(instructions))
    for index, byte in enumerate(core.register_file):
        print(hex(index)[2:], byte, int(byte))
