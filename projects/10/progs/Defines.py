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

T_KEYWORD         = "keyword"
T_SYMBOL          = "symbol"
T_IDENTIFIER      = "identifier"
T_INT_CONST       = "integerConstant"
T_STRING_CONST    = "stringConstant"


# Keywords types

K_CLASS       = "class"
K_CONSTRUCTOR = "constructor"
K_FUNCTION    = "function"
K_METHOD      = "method"
K_FIELD       = 5
K_STATIC      = 6
K_VAR         = "var"
K_INT         = "int"
K_CHAR        = "char"
K_BOOLEAN     = "boolean"
K_VOID        = "void"
K_TRUE        = 12
K_FALSE       = 13
K_NULL        = 14
K_THIS        = 15
K_LET         = "let"
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

S_OCURLYBRACKETS  = "{"
S_CCURLYBRACKETS  = "}"
S_OANGLEBRACKETS  = "["
S_CANGLEBRACKETS  = "]"
S_OBRACKETS       = "("
S_CBRACKETS       = ")"
S_POINT           = "."
S_KOMMA           = ","
S_SEMICOLON       = ";"
S_PLUS            = "+"
S_MINUS           = "-"
S_STAR            = "*"
S_SLASH           = "/"
S_AMPERSAND       = "&"
S_PIPE            = "|"
S_LESSTHAN        = "<"
S_GREATERTHAN     = ">"
S_EQUALS          = "="
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















