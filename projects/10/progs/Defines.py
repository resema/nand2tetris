#!/usr/local/bin/python3


#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the compiler
#
#       Hosts all constants used
#
#***********************************************************

# Token types

T_KEYWORD         = 0
T_SYMBOL          = 1
T_IDENTIFIER      = 2
T_INT_CONST       = 3
T_STRING_CONST    = 4


# Keywords types

K_CLASS       = "class"
K_CONSTRUCTOR = "constructor"
K_FUNCTION    = "function"
K_METHOD      = "method"
K_FIELD       = "field"
K_STATIC      = "static"
K_VAR         = "var"
K_INT         = "int"
K_CHAR        = "char"
K_BOOLEAN     = "boolean"
K_VOID        = "void"
K_TRUE        = "true"
K_FALSE       = "false"
K_NULL        = "null"
K_THIS        = "this"
K_LET         = "let"
K_DO          = "do"
K_IF          = "if"
K_ELSE        = "else"
K_WHILE       = "while"
K_RETURN      = "return"


# Sybmols

S_OCURLYBRACKETS  = 11
S_CCURLYBRACKETS  = 12
S_OANGLEBRACKETS  = 13
S_CANGLEBRACKETS  = 14
S_OBRACKETS       = 15
S_CBRACKETS       = 16
S_POINT           = 17
S_KOMMA           = 18
S_SEMICOLON       = 19
S_PLUS            = 20
S_MINUS           = 21
S_STAR            = 22
S_SLASH           = 23
S_AMPERSAND       = 24
S_PIPE            = 25
S_LESSTHAN        = 26
S_GREATERTHAN     = 27
S_EQUALS          = 28
S_TILDE           = 29 

# symbol list
symbols = { "{"   :   S_OCURLYBRACKETS, 
            "}"   :   S_CCURLYBRACKETS,
            "["   :   S_OANGLEBRACKETS,
            "]"   :   S_CANGLEBRACKETS,
            "("   :   S_OBRACKETS,
            ")"   :   S_CBRACKETS,
            "."   :   S_POINT,
            ","   :   S_KOMMA,
            ";"   :   S_SEMICOLON,
            "+"   :   S_PLUS,
            "-"   :   S_MINUS,
            "*"   :   S_STAR,
            "/"   :   S_SLASH,
            "&"   :   S_AMPERSAND,
            "|"   :   S_PIPE,
            "<"   :   S_LESSTHAN,
            ">"   :   S_GREATERTHAN,
            "="   :   S_EQUALS,
            "~"   :   S_TILDE
          }















