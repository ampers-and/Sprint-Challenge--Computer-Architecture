"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 7 + [0xF4]
        self.ram = [0] * 256
        self.pc = 0
        self.running = True
        self.fl = 0b00000000
                #   00000LGE

        #stack pointer
        self.sp = self.reg[7]

        # # Load Immediate - 130
        # LDI = 0b10000010 
        # # Print - 71
        # PRN = 0b01000111 
        # # Multiply - 162
        # MUL = 0b10100010
        # # Add - 160
        # ADD = 0b10100000
        # # Push - 69
        # PUSH = 0b01000101
        # # Pop - 70
        # POP = 0b01000110
        # # Call - 80
        # CALL = 0b01010000
        # # Return - 17
        # RET = 0b00010001
        # # Halt - 1
        # HLT = 0b00000001
        # # CMP 167
        # CMP = 0b10100111
        # # JMP 84
        # JMP = 0b01010100
    # # # JNE check if not equal flag 86
        # JNE = 0b01010110
    # # # JEQ check if equal flag 85
        # JEQ = 0b01010101

        self.instructions = {
            130: self.ldi,
            71: self.prn,
            1: self.hlt,
            162: self.mul,
            160: self.add,
            69: self.push,
            70: self.pop,
            80: self.call,
            17: self.ret,
            167: self.cmp_,
            84: self.jmp,
            85: self.jeq,
            86: self.jne,
        }

    def ram_read(self, MAR):
      return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
      self.ram[MAR] = MDR

    def hlt(self):
        self.running = False
        self.pc += 1

    def ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
        self.pc += 3

    def prn(self, reg_a, reg_b):
        #reg_b not used
        print(self.reg[reg_a])
        self.pc += 2

    def mul(self, reg_a, reg_b):
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def add(self, reg_a, reg_b):
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def push(self, reg_a, reg_b):
        #reg_b not used
        self.sp -=  1
        val = self.reg[reg_a]
        self.ram_write(self.sp, val)
        self.pc +=2

    def pop(self, reg_a, reg_b):
        #reg_b not used
        val = self.ram_read(self.sp)
        self.reg[reg_a] = val
        self.sp += 1
        self.pc += 2

    def call(self):
        value = self.pc + 2
        self.sp -= 1
        self.ram_write(self.sp, value)

        reg = self.ram_read(self.pc + 1)
        subroutine_address = self.reg[reg]
        self.pc = subroutine_address

    def ret(self):
        self.pc = self.ram_read(self.sp)
        self.sp += 1

    def cmp_(self, reg_a, reg_b):
        self.alu("CMP", reg_a, reg_b)

    def jmp(self, reg_a, reg_b):
        #reg_b not used
        pass

    def jeq(self, reg_a, reg_b):
        #reg_b not used
        pass

    def jne(self, reg_a, reg_b):
        #reg_b not used
        pass

    def load(self):
        """Load a program into memory."""


        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT
        ]

        file = sys.argv[1]

        with open(file) as f:
                for line in f:
                    text = line.split('#')
                    num = text[0].strip()
                    if num != '':
                        program.append(int(num, 2))


        print(program)
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        #mul
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            #   00000LGE
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print('ir', ir)
            if ir in self.instructions:
                if ir == 80 or ir == 17 or ir == 1:
                    self.instructions[ir]()
                else:
                    self.instructions[ir](operand_a, operand_b)
                    #self.pc move handled in specific instructions

            else:
                print(f"Unknown instruction at index {self.pc}")
                sys.exit(1)
