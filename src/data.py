def read_imem(filepath: str) -> dict:

    with open(filepath) as fp:
        lines = fp.readlines()

    instructions = {}
    num_ins = 0
    for i in range(len(lines)):
        num_ins += 1
        instructions[i] = lines[i].strip()

    num_32_bit_ins = num_ins // 4

    pc_format = {4*k: "".join([instructions[4*k+i] for i in range(4)]) for k in range(num_32_bit_ins)}
    return pc_format    

def read_dmem(filepath: str, mem_size=1000) -> tuple:

    with open(filepath) as fp:
        lines = fp.readlines()
    
    for i in range(mem_size - len(lines)):
        lines.append("00000000")

    lines = [line.strip() for line in lines]

    data = {}
    num_data = 0
    for i in range(len(lines)):
        num_data += 1
        data[i] = lines[i].strip()

    data_format = {k: "".join([data[k+i] for i in range(4)]) for k in range(num_data-3)}
    all_data = "".join(lines)
    
    return data_format, all_data