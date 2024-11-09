from elements import Register
from utils import to_twos_complement, sign_extend

class Operations():

    def __init__(self):
        pass

    def ADD(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:
        
        int_val = rs1.int_val + rs2.int_val
        if int_val < 0:
            binary_val = to_twos_complement(int_val, 32)
        else:
            binary_val = format(int_val, '032b')

        append_PC = 4
        return binary_val, append_PC

    def SUB(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:

        int_val = rs1.int_val - rs2.int_val
        if int_val < 0:
            binary_val = to_twos_complement(int_val, 32)
        else:
            binary_val = format(int_val, '032b')
        
        append_PC = 4
        return binary_val, append_PC
    
    def XOR(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:
        
        int_val = int(rs1.binary_val, 2) ^ int(rs2.binary_val, 2)
        binary_val = format(int_val, '032b')

        append_PC = 4
        return binary_val, append_PC
    
    def OR(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:

        int_val = int(rs1.binary_val, 2) | int(rs2.binary_val, 2)
        binary_val = format(int_val, '032b')

        append_PC = 4
        return binary_val, append_PC
    
    def AND(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:
        
        int_val = int(rs1.binary_val, 2) & int(rs2.binary_val, 2)
        binary_val = format(int_val, '032b')
        append_PC = 4
        return binary_val, append_PC
    
    def ADDI(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:
        
        int_val = rs1.int_val + sign_extend(imm.binary_val)
        if int_val < 0:
            binary_val = to_twos_complement(int_val, 32)
        else:
            binary_val = format(int_val, '032b')
        append_PC = 4
        return binary_val, append_PC
    
    def XORI(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:
        
        int_val = int(rs1.binary_val, 2) ^ (sign_extend(imm.binary_val))

        if int_val < 0:
            binary_val = to_twos_complement(int_val, 32)
        else:  
            binary_val = format(int_val, '032b')
        append_PC = 4
        return binary_val, append_PC
    
    def ORI(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:

        int_val = int(rs1.binary_val, 2) | (sign_extend(imm.binary_val))
        if int_val < 0:
            binary_val = to_twos_complement(int_val, 32)
        else:  
            binary_val = format(int_val, '032b')
        
        append_PC = 4
        return binary_val, append_PC
    
    def ANDI(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:
        
        int_val = int(rs1.binary_val, 2) & (sign_extend(imm.binary_val))
        if int_val < 0:
            binary_val = to_twos_complement(int_val, 32)
        else:  
            binary_val = format(int_val, '032b')

        append_PC = 4
        return binary_val, append_PC
    
    def BEQ(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:

        if rs1.int_val == rs2.int_val:
            append_PC = sign_extend(imm.binary_val)
        else:
            append_PC = 4
        
        binary_val = "0"*32
        return binary_val, append_PC

    def BNE(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:
        if rs1.int_val != rs2.int_val:
            append_PC = sign_extend(imm.binary_val)
        else:
            append_PC = 4

        binary_val = "0"*32
        return binary_val, append_PC

    def JAL(self, rs1: Register, rs2: Register, imm: Register, PC: int) -> tuple:
        ## PC becomes PC + sign_extended_imm
        append_PC = sign_extend(imm.binary_val)
        binary_val = format(PC + 4, '032b')
        
        return binary_val, append_PC
