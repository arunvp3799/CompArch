import os
from elements import Register, Instruction
from data import read_imem, read_dmem
from process import instruction_decode, execute, memory_read_write
from utils import to_twos_complement, sign_extend

class State:
    def __init__(self, name: str):
        self.name: str = name
        self.PC: int = 0
        self.NOP: bool = False
        self.registers: list = [Register(i, "0"*32, 0) for i in range(32)]
        self.memory: tuple = None
        self.halt: bool = False
        self.num_instructions: int = 0

    def update_register(self, index: int, value: str) -> None:
        value = int(value, 2)
        if value < 0:
            self.registers[index].binary_val = to_twos_complement(value, 32)
        else:
            self.registers[index].binary_val = format(value, '032b')
        self.registers[index].int_val = sign_extend(self.registers[index].binary_val)
        
    def get_register(self, index: int) -> Register:
        return self.registers[index]
    

class SingleStageProcessing():
    def __init__(self, state: State, ioDir: str):
        self.state = state
        self.instruction = None
        self.decoded_instruction: Instruction = None
        self.update_vars = None
        self.ioDir = ioDir

    def IF(self) -> None:
        self.instruction = self.state.memory[0][self.state.PC]
        
    def ID(self) -> None:
        self.decoded_instruction = instruction_decode(self.instruction, self.state.registers)

    def EX(self) -> None:
        self.update_vars = execute(self.decoded_instruction, self.state.PC)
    
    def MEM(self) -> None:
        memory, self.update_vars = memory_read_write(self.decoded_instruction, self.update_vars, self.state.memory)
        self.state.memory = memory
       
    def WB(self) -> None:
        
        if self.update_vars["index"] is not None:
            if self.update_vars["index"] != 0:
                self.state.update_register(self.update_vars["index"], self.update_vars["value"])
            self.state.PC += self.update_vars["PC"]
        
        if self.state.NOP:
            self.state.halt = True
            self.decoded_instruction.opcode = None

        if self.update_vars["PC"] == 0:
            self.state.NOP = True

    def process(self) -> None:

        count = 0
        output = []
        state_output = []
        while not self.state.halt:
            self.IF()
            self.ID()   
            self.EX()
            self.MEM()
            self.WB()

            if self.decoded_instruction.opcode is not None:
                self.state.num_instructions += 1
            
            output.append("-"*70)
            output.append(f"State of RF after executing cycle:{count}")
            for i in range(32):
                output.append(f"{self.state.registers[i].binary_val}")

            state_output.append("-"*70)
            state_output.append(f"State after executing cycle: {count}")
            state_output.append(f"IF.PC: {self.state.PC}")
            state_output.append(f"IF.NOP: {self.state.NOP}")

            count += 1

        savepath = os.path.join(self.ioDir, "SS_RFResult.txt")
        with open(savepath, "w") as f:
            for item in output:
                f.write("%s\n" % item)

        dmem_string = self.state.memory[2]
        savepath = os.path.join(self.ioDir, "SS_DMEMResult.txt")
        with open(savepath, "w") as f:
            for i in range(0, len(dmem_string), 8):
                f.write("%s\n" % dmem_string[i:i+8])            
        
        savepath = os.path.join(self.ioDir, "StateResult_SS.txt")
        with open(savepath, "w") as f:
            for item in state_output:
                f.write("%s\n" % item)

        performance_metrics_output = []
        performance_metrics_output.append(f"-----------------------------Single Stage Core Performance Metrics-----------------------------")
        performance_metrics_output.append(f"Number of cycles taken: {count}")
        performance_metrics_output.append(f"Total Number of Instructions: {self.state.num_instructions}")
        performance_metrics_output.append(f"Cycles per instruction: {count/self.state.num_instructions}")
        performance_metrics_output.append(f"Instructions per cycle:: {self.state.num_instructions/count}")
        savepath = os.path.join(self.ioDir, "PerformanceMetrics_Result.txt")
        with open(savepath, "w") as f:
            for item in performance_metrics_output:
                f.write("%s\n" % item)
        

def pipeline(ioDir: str) -> None:

    MEMORY_SIZE=1000
    imem = read_imem(os.path.join(ioDir, "imem.txt"))
    dmem, all_data = read_dmem(os.path.join(ioDir, "dmem.txt"), mem_size=MEMORY_SIZE)
    state = State("IF")
    state.memory = (imem, dmem, all_data)

    ssp = SingleStageProcessing(state, ioDir)
    ssp.process()