import sys

def decode_code(code_path):
  with open(code_path, 'r') as file:
    lines = file.readlines()

  mapper = {
      'ADD': '00000001',
      'SUB': '00000010',
      'STORE': '00000011',
      'LOAD': '00000100',
      'JUMP_RIGHT': '00000101',
      'JUMP_LEFT': '00000110',
      'JUMP+': '00000111',
      'SETZERO' : '00010000',
      'WC1' : '00010001',
      'WC2' : '00010010',
      'SC1' : '00100000',
      'SC2' : '00100001'
  }

  decoded_lines = []
  for line in lines:
    decoded_line = '0b'
    code_parts = line.split()
    for part in code_parts:
      if part in mapper:
        decoded_line += mapper[part]
      elif part.isdigit():
        decoded_line += bin(int(part))
      elif part.startswith('M(') and part.endswith(')'):
        part = part[2:-1]
        if '+' in part:
          address, offset = part.split('+')
          address = int(address)
          offset = int(offset)
          part = f'{(address+offset):012b}'
        decoded_line += f'{int(part):012b}'
      elif part == 'NOP':
        decoded_line += '10000000000000000000'
      elif part == 'CHECKC1C2':
        decoded_line += '01000000000000000000'

    decoded_lines.append(decoded_line.strip())

  return decoded_lines


code_path = sys.argv[1]
decoded_code = decode_code(code_path)
for line in decoded_code:
  print(line)

with open("Machine.out", "w") as txt_file:
  for line in decoded_code:
    if line == decoded_code[-1]:
      txt_file.write(line)
    else:
      txt_file.write(line +"\n")  # works with any number of elements in a line
print('Machine code dumped into Machine.out')