#!/usr/local/bin/python3
  

#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the SymbolTable part of the compiler
#
#       Handles specific symbol tables for 
#         - class
#         - current subroutine
#
#***********************************************************


class SymbolTable:
  
  # cstor
  #   creates new symbol table
  def __init__(self):
    self.symbolTable = {}
    # self.staticIdx = 0
    # self.fieldIdx = 0
    # self.localIdx = 0
    # self.argIdx = 0
    
  # Adds a new identifier and assigns a running index
  def define(self, name, type, kind):
    self.symbolTable[name] = [type, kind,]
    
  # Returns the number of variables of the given kind
  def VarCound(self, kind):
    pass
    
  # Returns the kind of the named identifier
  def KindOf(self. name):
    pass
    
  # Returns the type of the named identifier
  def TypeOf(self, name):
    pass
    
  # Returns the index assigned to the named identifier
  def IndexOf(self, name):
    pass
    
  #......................................................
  # Helper functions
  def increaseCounter(self, type):
    if type == STATIC:
      pass
    elif type == FIELD:
      pass
    elif type == LOCAL:
      pass
    elif type == ARG:
      pass