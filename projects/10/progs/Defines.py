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

# T_KEYWORD         = 0
# T_SYMBOL          = 1
# T_IDENTIFIER      = 2
# T_INT_CONST       = 3
# T_STRING_CONST    = 4


# Keywords types

K_CLASS       = 1
K_CONSTRUCTOR = 2
K_FUNCTION    = 3
K_METHOD      = 4
K_FIELD       = 5
K_STATIC      = 6
K_VAR         = 7
K_INT         = 8
K_CHAR        = 9
K_BOOLEAN     = 10
K_VOID        = 11
K_TRUE        = 12
K_FALSE       = 13
K_NULL        = 14
K_THIS        = 15
K_LET         = 16
K_DO          = 17
K_IF          = 18
K_ELSE        = 19
K_WHILE       = 20
K_RETURN      = 21

# Key word list
keywordList = {
            "class"       :   K_CLASS,
            "constructor" :   K_CONSTRUCTOR,
            "function"    :   K_FUNCTION,
            "method"      :   K_METHOD,
            "field"       :   K_FIELD,
            "static"      :   K_STATIC,
            "var"         :   K_VAR,
            "int"         :   K_INT,
            "char"        :   K_CHAR,
            "boolean"     :   K_BOOLEAN,
            "void"        :   K_VOID,
            "true"        :   K_TRUE,
            "false"       :   K_FALSE,
            "null"        :   K_NULL,
            "this"        :   K_THIS,
            "let"         :   K_LET,
            "do"          :   K_DO,
            "if"          :   K_IF,
            "else"        :   K_ELSE,
            "while"       :   K_WHILE,
            "return"      :   K_RETURN
          }


# Sybmols

S_OCURLYBRACKETS  = 22
S_CCURLYBRACKETS  = 23
S_OANGLEBRACKETS  = 24
S_CANGLEBRACKETS  = 25
S_OBRACKETS       = 26
S_CBRACKETS       = 27
S_POINT           = 28
S_KOMMA           = 29
S_SEMICOLON       = 30
S_PLUS            = 31
S_MINUS           = 32
S_STAR            = 33
S_SLASH           = 34
S_AMPERSAND       = 35
S_PIPE            = 36
S_LESSTHAN        = 37
S_GREATERTHAN     = 38
S_EQUALS          = 39
S_TILDE           = 40 

# symbol list
symbolList = { 
            "{"   :   S_OCURLYBRACKETS, 
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















