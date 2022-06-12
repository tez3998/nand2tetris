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

// Put your code here.

// （注意）動いてない

(Loop)
    @KBD // キーボードのベースアドレス
    D=M
    @White
    D; JEQ
    @Black
    0; JMP

(White)
    @0
    D=A
    @color
    M=D
    @SetColor
    0; JMP

(Black)
    //@65535 // 黒
    //D=A
    //@color
    M=-1
    @SetColor
    0; JMP

(SetColor)
    @i
    M=0
(SetColorLoop)
    @SCREEN
    D=A
    @i
    D=D+M
    @num_word
    M=D
    @color
    D=M
    @num_word
    M=D

    @i
    M=M+1
    @8192
    D=A // 画面のワード数
    @num_word
    D=D-M
    @SetColorLoop
    D; JGT

    @Loop
    0; JMP