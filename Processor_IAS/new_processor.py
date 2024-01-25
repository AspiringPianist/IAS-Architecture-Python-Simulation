#Our computer works on actual binary values and not binary strings to reduce the burden
from test import get_bits
#Left Instrction == li (8-bit), Left Address == la (12-bit)
#Right Instruction == ri (8-bit), Right Address == ra (12-bit)
#Whenever a class is referred we must capitalize it. And when it is used as a variable it should be in lowercase
class IASComputer:
  #This is the class for our IAS Computer
  def __init__(self, pc, mar, mem, mbr, alu, ac, ibr, ir, ctrl):
    self.PC = pc
    self.MAR = mar
    self.MEM = mem
    self.MBR = mbr
    self.ALU = alu
    self.AC = ac
    self.IBR = ibr
    self.IR = ir
    self.CTRL = ctrl

  def start(self, lines):
    print('lines = ', lines)
    while (self.PC.val <= lines):
      print('We are in PC = ', self.PC.val)
      print('IBR has', self.IBR.instruction)
      if (self.IBR.ri == 0b00000000):
        self.MAR.update(self.PC.val)
        self.MBR.update(instruction=self.MEM.fetch_instruction(self.MAR.address),
                        data=0)
        if (self.MBR.instruction[0] != 0b00000000):
          self.IBR.update(self.MBR.instruction[2:])
          self.IR.update(self.MBR.instruction[0])
          self.MAR.update(self.MBR.instruction[1])
          self.CTRL.execute(self.IR.opcode)
          #print(self.MEM.memory)

        else:
          self.IR.update(self.MBR.instruction[2])
          self.MAR.update(self.MBR.instruction[3])
          self.PC.update()
          self.CTRL.execute(self.IR.opcode)
          #print(self.MEM.memory)

      else:
        self.IR.update(self.IBR.ri)
        self.MAR.update(self.IBR.ra)
        self.IBR.clear()
        self.PC.update()
        self.CTRL.execute(self.IR.opcode)
        #print(self.MEM.memory)

  
    print(self.MEM.memory)


#From here on, classes are organized alphabetically
class AC:
  #The accumulator has only one function, to hold a binary value and then update it. It's value is to be updated with the update() function
  def __init__(self, val):
    self.val = val
    print('Initially, AC has value', val, 'in it.')

  def update(self, val):
    self.val = val
    print('Now, AC has value', val, 'in it.')


class ALU:
  #The ALU handles add() and sub() functions.
  #add() and sub() take in a binary value and the accumulator
  def __init__(self):
    print('Initialized ALU')
    self.c1 = 0
    self.c2 = 0

  def add(self, ac, mbr):
    ac.val += mbr.data
    print('Added', mbr.data,
          'to the accumulator. Now, the accumulator has value', ac.val,
          'in it.')

  def sub(self, ac, mbr):
    ac.val -= mbr.data
    print('Subtracted', mbr.data,
          'from the accumulator. Now, the accumulator has value', ac.val,
          'in it')

  def load(self, ac, mbr):
    ac.val = mbr.data
    print('Updated AC value to', mbr.data, '.')

  def store(self, ac, mbr):
    mbr.update(instruction=None, data=ac.val)
    print('Loaded AC value to MBR.')

  def wc1(self, mbr):
    #suppose m[200] = 600+j
    #it will go to m[600+j] and store in $1 when u pass 200 as address to it
    self.c1 = mbr.data
    print('Set $1 to',mbr.data)

  def wc2(self, mbr):
    #suppose m[200] = 600+j
    #it will go to m[600+j] and store in $1 when u pass 200 as address to it
    self.c2 = mbr.data
    print('Set $2 to',mbr.data)

  def sc1(self, mbr):
    mbr.data = self.c1
    print('Set MBR data to',self.c1)
    
  def sc2(self, mbr):
    mbr.data = self.c2
    print('Set MBR data to',self.c2)

class CTRL:
  #The control unit is rather complex
  def __init__(self, opcode, ac, alu, mar, mbr, mem, pc, ibr):
    print('Opcode in CTRL is', opcode)
    self.opcode = opcode
    self.MAR = mar
    self.MBR = mbr
    self.AC = ac
    self.ALU = alu
    self.MEM = mem
    self.PC = pc
    self.IBR = ibr

  def execute(self, opcode):
    print('Opcode is', opcode)
    self.opcode = opcode
    match self.opcode:
      case int(0b00000001):
        print('Calling Add')
        self.add()
      case int(0b00000010):
        print('Calling Sub')
        self.sub()
      case int(0b00000011): 
        print('Calling Store')
        self.store()
      case int(0b00000100): 
        print('Calling Load')
        self.load()
      case int(0b00000101): 
        self.jump_right()
      case int(0b00000110): 
        self.jump_left()
      case int(0b00000111): 
        self.jump_plus()
      case int(0b10000000): 
        print('Calling NOP')
        self.nop()
      case int(0b00010000):
        print('Setting Zero')
        self.setzero()
      case int(0b01000000):
        print('Checking $1 and $2, and triggering flag ig $1 > $2')
        self.checkc1c2()
      case int(0b00100000):
        self.sc1()
      case int(0b00100001):
        self.sc2()
      case int(0b00010001):
        self.wc1()
      case int(0b00010010):
        self.wc2()

  def add(self):
    self.MBR.update(instruction=None,
                    data=self.MEM.fetch_data(self.MAR.address))
    self.ALU.add(self.AC, self.MBR)

  def sub(self):
    self.MBR.update(instruction=None,
                    data=self.MEM.fetch_data(self.MAR.address))
    self.ALU.sub(self.AC, self.MBR)

  def store(self):
    self.ALU.store(self.AC, self.MBR)
    self.MEM.write(self.MAR.address, self.MBR.data)
    
  def load(self):
    self.MBR.update(instruction=None,data=self.MEM.fetch_data(self.MAR.address))
    self.ALU.load(self.AC, self.MBR)

  def jump_right(self):
    self.PC.set(self.MAR.address)
    print('Jumping to', self.PC.val)
    self.IBR.update(self.MEM.fetch_instruction(self.MAR.address)[2:])
    
  def jump_left(self):
    self.PC.set(self.MAR.address)
    print('Jumping to', self.PC.val)
  
  def jump_plus(self):
    if(self.AC.val >=0 ):
      print('Called Jump Plus')
      self.PC.set(self.MAR.address)
      self.IBR.clear()
      print('Jumping to', self.PC.val)

  def nop(self):
    print('Called NOP')

  def setzero(self):
    print('Set address',self.MAR.address,'to zero')
    self.MEM.write(self.MAR.address, 0)
    
  def checkc1c2(self):
    if self.ALU.c1 > self.ALU.c2:
      print('Triggering flag')
      self.AC.val = 1
    else:
      print('Didn"t trigger flag')
      self.AC.val = -1

  def wc1(self):
    self.MBR.update(instruction = None, data = self.MEM.fetch_data(self.MEM.fetch_data(self.MAR.address)))
    self.ALU.wc1(self.MBR)

  def wc2(self):
    self.MBR.update(instruction = None, data = self.MEM.fetch_data(self.MEM.fetch_data(self.MAR.address)))
    self.ALU.wc2(self.MBR)

  def sc1(self):
    self.ALU.sc1(self.MBR)
    self.MEM.write(self.MEM.fetch_data(self.MAR.address), self.MBR.data)

  def sc2(self):
    self.ALU.sc2(self.MBR)
    self.MEM.write(self.MEM.fetch_data(self.MAR.address), self.MBR.data)
    
  
class IBR:
  #The IBR stores in an array of the ri and ra
  def __init__(self):
    self.ri = 0b00000000
    self.ra = 0b000000000000
    self.instruction = [self.ri, self.ra]
    print('Contents of IBR are', self.instruction)
    
  def clear(self):
    #Puts stuff to zero
    self.ri = 0b00000000
    self.ra = 0b000000000000
    self.instruction = [self.ri, self.ra]
    print('After clearing, contents of IBR are', self.instruction)

  #update() will receive entire right instruction from MBR
  def update(self, instruction):
    self.instruction = instruction
    self.ri, self.ra = instruction[0], instruction[1]
    print('Updated IBR to', self.instruction)


class IR:
  #IR stores in the the opcode
  def __init__(self, opcode):
    self.opcode = opcode
    print('IR has opcode', self.opcode)


#update() will update the instruction in IR

  def update(self, opcode):
    self.opcode = opcode
    print('Updated IR to', self.opcode)


class MAR:
  #MAR stores in the la only
  def __init__(self, address):
    self.address = address
    print('MAR has address', self.address)

  #Only other thing it does is update the address
  def update(self, address):
    self.address = address
    print('Updated MAR address to', self.address)


class MBR:
  #MBR stores in a list of li, la, ri, ra
  def __init__(self, instruction, data):
    self.instruction = instruction
    self.data = data
    print('MBR has instruction', self.instruction, 'and data', self.data)

  #MBR can get updated
  def update(self, instruction, data):
    self.instruction = instruction
    self.data = data
    print('Updated MBR to', self.instruction, 'and MBR"s data to', self.data)


class MEM:
  #MEM has each line of code in binary converted to integer
  #right shifting by 32 bits gives us left address
  #location 0 is reserved, memory locations 1 to 500 are used for code and location
  #501 too 999 are for data
  def __init__(self):
    self.memory = [0] * 1000
    print('Memory initially is: ', self.memory)
    #CTRL will decode memory and feed it to the ALU and MBR
  def fetch_data(self, address):
    a = self.memory[address]
    print(f'Fetched {a} from memory location {address}')
    return a

  def fetch_instruction(self, address):
    a = [get_bits(self.memory[address], 0, 8), get_bits(self.memory[address], 8, 12), get_bits(self.memory[address], 20, 8), get_bits(self.memory[address], 28, 12)]
    print('Fetched instructions', a, 'from memory location', address)
    return a

  def write(self, address, data):
    self.memory[address] = data
    print(f'Wrote {data} to memory address {address}')


class PC:

  def __init__(self, value):
    self.val = value
    print('PC has value', self.val)

  def update(self):
    self.val += 1
    print('Updated PC to', self.val)

  def set(self, address):
    self.val = address
    print('Set PC to', self.val)