from new_processor import *

code_location = 'Machine.out'
memory_location = 0b00000001


def write_code(code_location, memory_location, memory):
  n = 0
  with open(code_location, "r") as txt_file:
    lines = txt_file.readlines()
    for line in lines:
      if ('\n' in line):
        line = line[:-1]
      line = line[2:]
      line = int(line, 2)
      memory.write(memory_location, line)
      memory_location += 1
      n += 1
  return n


pc = PC(memory_location)
mar = MAR(0b00000000)
mem = MEM()
mbr = MBR(instruction=[0b00000000, 0b000000000000, 0b00000000, 0b000000000000],
          data=0b00000000)
alu = ALU()
ac = AC(69)
ibr = IBR()
ir = IR(opcode=0b00000000)
ctrl = CTRL(ir.opcode, ac, alu, mar, mbr, mem, pc, ibr)

computer = IASComputer(pc, mar, mem, mbr, alu, ac, ibr, ir, ctrl)
lines = write_code(code_location, memory_location, computer.MEM)
computer.MEM.write(200, 3)  #array elements
computer.MEM.write(201, 1)
computer.MEM.write(202, 2)
computer.MEM.write(203, 7)
computer.MEM.write(204, 9)
computer.MEM.write(205, 4)
computer.MEM.write(250, 200)  # array starting index
computer.MEM.write(251, 0)  #i
computer.MEM.write(252, 0)  #j
computer.MEM.write(253, 4)  #N-2
computer.MEM.write(254, 1)  #1
computer.MEM.write(255, 1)  #temp2
print('After loading code, ', computer.MEM.memory)
computer.start(lines)
