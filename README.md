# Minecraft 8-Bit Computer Project

**Status**: The assembler for this Minecraft computer is complete. The hardware implementation is planned for after 2025. I remain optimistic about successfully creating a functional computer in Minecraft.

## Alice Assembly Language Guide

Named after my pet duck, Alice Waddles the First, this language features 16 instructions, labels, and comments.

### Basic Syntax
```alice
ADD r1 r2 r3  ; Adds values in r1 and r2, stores result in r3
```
List of Opcodes:
1. NOP. Does nothing. Absolutely nothing. Alice the Duck Sleep
2. HLT. Halts the program
3. ADD. This takes 3 arguments. ra, rb, and rc. a, b and c are values between 0 and 15. They represent the two operands of the ADD instruction. the third register, rc, represents the destination of the operation. Alice Add Two Numbers
4. SUB. Same for ADD. This modifies rc to become the difference between register a and register b.
5. ORR. Bitwise OR. This takes the bitwise Or for two registers, and then loads it into a final register.
6. NOR. Bitwise NOR. This takes the bitwise NOr of two registers, and then returns the result into a the third register.
7. AND. Bitwise AND. Follows identical syntax with all triple register opcodes
8. XOR. Bitwise XOR. Takes the bitwise XOR of two registers, dumps into third.
9. RSH. Takes right shift of one register, puts that into another register.
10. LDI. Loads an 8 bit number into a register.
11. LOD. Takes on two registers. The first register gets set to the value that the data memory, which has 256 bytes of memory, has at index of the second register.
12. STR. Takes on two registers. The first register sets the value that the data memory, which has 256 bytes of memory, has at index of the second register. The opposite of LOD.
13. JMP. Unconditional Jump. Jumps to the address that the program has
14. BIF. Branch If. This branches to the address if the flags match the branch. Flags can be set by the other operands that reference the ALU.
15. CAL. Calls to a address. The current address gets pushed on a call stack. Goes to the address given
16. RET. Returns to the last element sent to the call stack. Your new address is the call stack popped.

All in all, these are the instructions that you get. Good Luck.
List of removable Opcodes:
1. SUB. We can just invert a register by XOR-ing it by 255
2. NOR. We can invert the logical OR by XOR-ing it by 255
3. AND. Any fan of boolean algebra knows that A AND B is equal to !(!A OR !B). This means, we can invert each register, then take the OR, then inver the outcome.

### Writing your first program

This is a fibonacci program
```alice
LDI r1 255
LDI r2 8
LDI r3 1
LDI r4 0
LDI r5 0
.alice ADD r3 r4 r5
ADD r3 r0 r4
ADD r5 r0 r3
ADD r2 r1 r2
BIF carry .alice
HLT
```

This program first sets two constants. 8, for how long you want to run the program, and 255, which is -1. 
What then happens is, at line 9, it subtracts 1 from r2. If no carry was executed, that means that r1 was equal to 0, and that means that the program executed for 9 times, and it fails to branch. Then, the program halts.
In the "for loop", r5 gets set to r3 + r4. r4 gets set to r3, and r3 gets set to r5. They get set by just using an ADD with zero.

## Running the code

To run the <code>.alice</code> code, just compile it to machine code with file extension <code>.duck</code> with the file <code>compile.py</code>. Execute the code with <code>execute.py</code>. Happy coding
