def get_bits(binary_number, start, length):
    # Shift the number right by (40 - start - length) bits
    shifted = binary_number >> (40 - start - length)
    
    # Create a mask of 'length' number of 1s
    mask = (1 << length) - 1
    
    # Bitwise AND operation to get the specific bit sequence
    bits = shifted & mask
    
    return bits

# Test the function
# binary_number = 17704161781
# start = 8
# length = 12
# print(get_bits(binary_number, start, length))