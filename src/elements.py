class Register:
    
    def __init__(self, index:str, binary_val:str, int_val:int):
        self.index = index
        self.binary_index = format(index, '05b')
        self.binary_val = binary_val
        self.int_val = int_val

class Instruction:

    def __init__(self):
        self.opcode: str = None
        self.rs1: Register = None
        self.rs2: Register = None
        self.rd: Register = None
        self.imm: Register = None
        self.operation: str = None