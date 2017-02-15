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

import re

from Defines import *

class JackTokenizer:

  # cstor
  def __init__(self, fobj_in):
    self.fobj_in = fobj_in   
    self.rawlines = []
    self.tokens = []
    self.token = ""
    self.next = ""
    
    for line in self.fobj_in:
      newline = re.sub("\s*//.*?\n", "", line) # remove comments
      newline = re.sub("\s*/\*.*?\n", "", newline) # remove special comments
      newline = re.sub("\s*\n", "", newline) # remove empty lines
      newline = re.sub("^\s*", "", newline) # remove spaces at the beginning
      if newline != "":
        self.rawlines.insert(len(self.rawlines), newline)
         
  # tokenizes the input file
  def tokenize(self):
    list = []
    for line in self.rawlines:  
      list = re.split("(\W)", line);
      for l in list:
          if l != "":
            self.tokens.insert(len(self.tokens), l)
    # for t in self.tokens:
      # print(t)
    
  # has the input more tokens to process
  def hasMoreTokens(self): 
    return len(self.tokens) > 0
  
  # returns next token
  #   should ONLY be called, if "hasMoreTokens" is true
  # groups inputs into tokens
  def advance(self):
    self.token = self.tokens.pop(0)
    if (len(self.tokens)):
      self.next = self.tokens[0]
    if (self.token == ('\"')):
      tmp = ""
      while(self.next != ('\"')):
        self.token = self.next = self.tokens.pop(0)
        tmp += self.next
      self.token = tmp
    
  # returns the type of the current process token 
  def tokenType(self):
    return symbolList[self.token]
    
  # returns the keyword which is the current token
  #   only called when tokenType is KEYWORD
  def keyWord(self):
    pass
    
  # returns the character which is the current token
  #   only called when tokenType is SYMBOL
  def symbol(self):
    pass
    
  # returns the identifier which is the current token
  #   only called when tokenType is IDENTIFIER
  def identifier(self):
    pass
     
  # returns the integer of the current token
  #   only called when tokenType is INT_ONST
  def intVal(self):
    pass
    
  # returns the string value of the current token
  #   only called when tokenType is STRING_CONST
  def stringVal(self):
    pass
    
    
    