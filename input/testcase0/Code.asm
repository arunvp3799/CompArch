0: LW R1, R0, #0  add = r0 + offset = 0
4: LW R2, R0, #4  add = r0 + offset = 4 
8: ADD R3, R1, R2
12: SW R3, R0, #8
16: HALT

/*
0000000 00000 00000 000 00001 0000011
0000000 00100 00000 000 00010 0000011
0000000 00010 00001 000 00011 0110011
0000000 00011 00000 010 01000 0100011
1111111 11111 11111 111 11111 1111111
*/