
def to_twos_complement(n, bits=32):
    if n < 0:
        # Compute two's complement for negative numbers
        return bin((1 << bits) + n)[2:].zfill(bits)
    else:
        # For positive numbers, just convert to binary
        return bin(n)[2:].zfill(bits)
    
def sign_extend(binary_str):
    # Get the bit width
    bit_width = len(binary_str)
    
    # Convert binary string to integer
    value = int(binary_str, 2)    
    val = 1 << (bit_width - 1)
    val2 = 1 << bit_width

    # If the sign bit (most significant bit) is set, extend the sign
    if (value & (1 << (bit_width - 1))) != 0:  # Check the sign bit
        # Perform sign extension
        value -= (1 << bit_width)
    
    return value