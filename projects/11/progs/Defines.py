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
S_AMPERSAND       = "&amp;"
S_PIPE            = "|"
S_LESSTHAN        = "&lt;"
S_GREATERTHAN     = "&gt;"
S_EQUALS          = "="
S_TILDE           = "~"

# symbol list
symbolList = { 
            "{"     :   S_OCURLYBRACKETS, 
            "}"     :   S_CCURLYBRACKETS,
            "["     :   S_OANGLEBRACKETS,
            "]"     :   S_CANGLEBRACKETS,
            "("     :   S_OBRACKETS,
            ")"     :   S_CBRACKETS,
            "."     :   S_POINT,
            ","     :   S_KOMMA,
            ";"     :   S_SEMICOLON,
            "+"     :   S_PLUS,
            "-"     :   S_MINUS,
            "*"     :   S_STAR,
            "/"     :   S_SLASH,
            "&amp;" :   S_AMPERSAND,
            "|"     :   S_PIPE,
            "&lt;"  :   S_LESSTHAN,
            "&gt;"  :   S_GREATERTHAN,
            "="     :   S_EQUALS,
            "~"     :   S_TILDE
          }

# virtual memory type and additional segments
STATIC  = "static"
FIELD   = "field"
LOCAL   = "local"
ARG     = "argument" 
CONST   = "const"
THIS    = "this"
THAT    = "that"
POINTER = "pointer"
TEMP    = "temp"

# arithmetic logical commands
ADD     = "add"
SUB     = "sub"
NEG     = "neg"
EQ      = "eq"
GT      = "gt"
LT      = "lt"
AND     = "and"
OR      = "or"
NOT     = "not"














