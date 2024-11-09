from elements import Instruction, Register
from operations import Operations

operations = Operations()

def instruction_decode(instruction: str, registers: list) -> Instruction:

    
    opcode = instruction[25:32]
    
    
    non_funct3_instructions = ["1101111", "0110111", "0010111"]
    funct3 = None
    if opcode not in non_funct3_instructions:
        funct3 = instruction[17:20]

    rs2, rd, imm = None, None, None        
    rs1 = instruction[12:17]

    operation = None

    if opcode == "0110011":
        rs2 = instruction[7:12]
        rd = instruction[20:25] 
        funct7 = instruction[0:7]
        if funct3 == "000":
            if funct7 == "0000000":
                operation = "ADD"
            elif funct7 == "0100000":
                operation = "SUB"
        elif funct3 == "100":
            operation = "XOR"
        elif funct3 == "110":
            operation = "OR"
        elif funct3 == "111":
            operation = "AND"
        else:
           pass 
    
    if opcode == "0010011":
        imm = instruction[0:12]
        rd = instruction[20:25]
        if funct3 == "000":
            operation = "ADDI"
        elif funct3 == "100":
            operation = "XORI"
        elif funct3 == "110":
            operation = "ORI"
        elif funct3 == "111":
            operation = "ANDI"
        else:
            pass

    if opcode == "1100011":
        imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + "0"
        rs2 = instruction[7:12]
        rd = instruction[20:25]
        if funct3 == "000":
            operation = "BEQ"
        elif funct3 == "001":
            operation = "BNE"
        else:
            pass

    if opcode == "1101111":
        imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + "0" 
        rd = instruction[20:25]
        operation = "JAL"

    if opcode == "0100011":
        imm = instruction[0:7] + instruction[20:25]
        rs2 = instruction[7:12]
        rd = instruction[20:25]
        if funct3 == "000":
            operation = "SB"
        elif funct3 == "001":
            operation = "SH"
        elif funct3 == "010":
            operation = "SW"
        else:
            pass
    
    if opcode == "0000011":
        imm = instruction[0:12]
        rd = instruction[20:25]
        if funct3 == "000":
            operation = "LB"
        elif funct3 == "001":
            operation = "LH"
        elif funct3 == "010":
            operation = "LW"
        else:
            pass

    if opcode == "1111111":
        operation = "END"
    
    if rs1:
        rs1 = registers[int(rs1, 2)]
    
    if rs2:
        rs2 = registers[int(rs2, 2)]
    
    if rd:
        rd = registers[int(rd, 2)]
    if imm:
        imm = Register(-100, imm, int(imm, 2))

    instruction = Instruction()
    instruction.opcode = opcode
    instruction.rs1 = rs1
    instruction.rs2 = rs2
    instruction.rd = rd
    instruction.imm = imm
    instruction.operation = operation
    
    return instruction

def execute(instruction: Instruction, PC: int) -> dict:
    
    op = instruction.operation
    load_store_ins = ["lb", "lh", "lw", "sb", "sh", "sw"]

    if op.lower() not in load_store_ins:
        if op.lower() != "end":

            rs1 = instruction.rs1
            rs2 = instruction.rs2
            imm = instruction.imm

            response = getattr(operations, op)(rs1, rs2, imm, PC)
            update_vars = {
                "index": instruction.rd.index,
                "value": response[0],
                "PC": response[1]
            }
        else:
            update_vars = {
                "index": None,
                "value": "0"*32,
                "PC": 0
            }
            
    
    else:
        update_vars = {
            "index": instruction.rd.index,
            "value": 0,
            "PC": 0
        }
    
    return update_vars

def memory_read_write(instruction: Instruction, update_vars: dict, memory: tuple) -> tuple:
    
    load_ins = ["lb", "lh", "lw"]
    store_ins = ["sb", "sh", "sw"]
    imem, dmem_data, dmem_string = memory

    if instruction.operation.lower() in load_ins:
        address = instruction.rs1.int_val + int(instruction.imm.binary_val, 2)
        update_vars["value"] = dmem_data[address]
        update_vars["PC"] = 4
        update_vars["index"] = instruction.rd.index
    
    elif instruction.operation.lower() in store_ins:

        address = (instruction.rs1.int_val + int(instruction.imm.binary_val, 2))*8
        update_val = instruction.rs2.binary_val
        dmem_string = dmem_string[:address] + update_val + dmem_string[address+len(update_val):]
        update_vars["PC"] = 4
        update_vars["index"] = instruction.rd.index
        update_vars["value"] = "0"*32

    memory = (imem, dmem_data, dmem_string)
    return memory, update_vars        