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

(INIT) 
    @8191 // 画面のワード数-1。-1はアドレスが0からスタートするため。 ((512 * 256) / 16) - 1
    D=A
    @SCREEN
    D=D+A
    @max_address // スクリーンのアドレスの最大値
    M=D

    @SCREEN
    D=A
    @current_address // 現在の色を変更しようと思っているスクリーンのアドレス
    M=D

(MAIN)
    @KBD
    D=M
    @kbd_status // キーボードの入力
    M=D
    @WHITEN
    D; JEQ
    @BLAKEN
    0; JMP

(LOOP1)
    @kbd_status
    D=M
    @DEC
    D; JEQ
    @INC
    0; JMP

(LOOP2)
    @MAIN
    0; JMP

(WHITEN) // アドレスcurrent_addressに対応するピクセルを白くする
    @current_address
    D=M
    A=D
    M=0
    @LOOP1
    0; JMP

(BLAKEN) // アドレスcurrent_addressに対応するピクセルを黒くする
    @current_address
    D=M
    A=D
    M=-1
    @LOOP1
    0; JMP

(DEC) // current_addressを減少させる
    @SCREEN
    D=A
    @current_address
    D=M-D
    @LOOP2
    D; JLT
    @current_address
    M=M-1
    @LOOP2
    0; JMP

(INC) // current_addressを増加させる
    @max_address
    D=M
    @current_address
    D=D-M
    @LOOP2
    D; JLT
    @current_address
    M=M+1
    @LOOP2
    0; JMP