// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Define variables
    @R0
    D=M
    @x
    M=D
    
    @R1
    D=M
    @y
    M=D
    
    @i
    M=0
    
    @result
    M=0
    
// Initialize output memory to zero
    @R2
    M=0
    
// Calculation
(LOOP)
     // Check Condition
    @i
    D=M
    @x
    D=M-D
    @RESULT
    D;JLE
    
    // increase Counter
    @i
    M=M+1
    
    // Sum up
    @y
    D=M
    @result
    M=M+D
    
    @LOOP
    0;JMP 

// Assign result to RAM[2]
(RESULT)
    @result
    D=M
    @R2
    M=D
    
(END)
    @END
    0;JMP