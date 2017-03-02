#!/usr/local/bin/python3
  

#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the SymbolTable part of the compiler
#
#       Handles specific symbol tables for 
#         - class
#         - current subroutine
#         - contains a dictionary with [type, kind, idx]
#
#***********************************************************


class SymbolTable:
  
  # cstor
  #   creates new symbol table
  def __init__(self):
    self.symbolTable = {}
    self.staticCnt = 0
    self.fieldCnt = 0
    self.localCnt = 0
    self.argCnt = 0
    
  # Adds a new identifier and assigns a running index
  def define(self, name, type, kind):
    self.symbolTable[name] = [type, kind, self.increaseCounter(kind)]
    
  # Returns the number of variables of the given kind
  def VarCount(self, kind):
    varCount = -1
    if type == STATIC:
      varCount = self.staticCnt
    elif type == FIELD:
      varCount = self.fieldCnt
    elif type == LOCAL:
      varCount = self.localCnt
    elif type == ARG:
      varCount = self.argCnt
    return varCount
    
  # Returns the kind of the named identifier
  def KindOf(self. name):
    kind = -1
    entry = findEntry(name)
    #TODO: insert defensive programming
    
    if entry[1] == STATIC:
      kind = STATIC
    elif entry[1] == FIELD:
      kind = FIELD
    elif entry[1] == LOCAL:
      kind = LOCAL
    elif entry[1] == ARG:
      kind = ARG
    return kind
    
  # Returns the type of the named identifier
  def TypeOf(self, name):
    varCount = -1
    if type == STATIC:
      varCount = self.staticIdx
    elif type == FIELD:
      varCount = self.fieldIdx
    elif type == LOCAL:
      varCount = self.localIdx
    elif type == ARG:
      varCount = self.argIdx
    return varCount
    
  # Returns the index assigned to the named identifier
  def IndexOf(self, name):
    varCount = -1
    if type == STATIC:
      varCount = self.staticIdx
    elif type == FIELD:
      varCount = self.fieldIdx
    elif type == LOCAL:
      varCount = self.localIdx
    elif type == ARG:
      varCount = self.argIdx
    return varCount
    
  #......................................................
  # Helper functions
  def increaseCounter(self, type):
    counter = 0;
    if type == STATIC:
      counter = self.staticIdx
      self.staticIdx += 1
    elif type == FIELD:
      counter = self.fieldIdx
      self.fieldIdx += 1
    elif type == LOCAL:
      coutner = self.localIdx
      self.localIdx += 1
    elif type == ARG:
      coutner = self.argIdx
      self.argIdx += 1
    return counter
      
  # Finds the entry in the hash table / dictionary
  def findEntry(self. name):
    retVal = []
    if name in self.symbolTable:
      retVal = self.symbolTable[name]
    return retVal
      
      
      
      
      
      
      
      
      
      
      
      
      
      