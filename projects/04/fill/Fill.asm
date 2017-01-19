// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Initialization
    @color
    M=0     
    
    @i
    M=0

// Infinite Loop
(WHILE)

    @SCREEN
    D=A
    @addr
    M=D
    
    @i
    M=0
    
    @KBD
    D=M
    @key
    M=D
    
    @key
    D=M
    @WHITE
    D;JEQ
    
(BLACK)
    @color
    M=-1
    @DRAW
    0;JMP

(WHITE)
    @color
    M=0
    
(DRAW)
    @color
    D=M
    
    @addr
    A=M
    M=D
    
    @i
    M=M+1
    @addr
    M=M+1
    
    @i
    D=M
    @8191
    D=D-A
    @DRAW
    D;JLE

    @WHILE
    0;JMP