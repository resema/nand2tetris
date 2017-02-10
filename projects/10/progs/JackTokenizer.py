#!/usr/local/bin/python3


#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the Tokenizer part of the Analyzer
#
#       Handles lexical elements, encapsulates the input
#       - Ignoring white spaces
#       - Advancing the input, one token at a time
#       - Getting the value and type of the current token
#
#***********************************************************

class JackTokenizer:

  # cstor
  def __init__(self, fobj_in):
    self.fobj_in = fobj_in    

  # has the input more tokens to process
  def hasMoreTokens(self): 
    pass
  
  # returns next token
  #   should ONLY be called, if "hasMoreTokens" is true
  # groups inputs into tokens
  def advance(self):
    pass
    
  # returns the type of the current process token 
  def tokenType(self):
    pass
    
  def keyWord(self):
    pass
    
  def symbol(self):
    pass
    
  def identifier(self):
    pass
    
  def intVal(self):
    pass
    
  def stringVal(self):
    pass
    
    
    