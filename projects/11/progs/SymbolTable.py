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

from Defines import *

class SymbolTable:
  
  # cstor
  #   creates new symbol table
  def __init__(self):
    self.tableName = ""
    self.symbolTable = {}
    self.staticCnt = 0
    self.fieldCnt = 0
    self.localCnt = 0
    self.argCnt = 0
    
  # Give the table an identifier name
  def setName(self, tableName):
    self.tableName = tableName
  
  # Return the table identifier name
  def getName(self):
    return self.tableName
    
  # Adds a new identifier and assigns a running index
  def define(self, name, type, kind):
    if name not in self.symbolTable:
      self.symbolTable[name] = [type, kind, self.increaseCounter(kind)]
    else:
      raise Exception("*ERROR* \"" + kind + " " + type + " " + name + "\" redefinition")
    
  # Returns the number of variables of the given kind
  def VarCount(self, kind):
    varCount = -1
    if kind == STATIC:
      varCount = self.staticCnt
    elif kind == FIELD:
      varCount = self.fieldCnt
    elif kind == LOCAL:
      varCount = self.localCnt
    elif kind == ARG:
      varCount = self.argCnt
    return varCount
    
  # Returns the kind of the named identifier
  def KindOf(self, name):
    kind = -1
    entry = self.findEntry(name)
    if entry != []:
      kind =  entry[1]
    return kind
    
  # Returns the type of the named identifier
  def TypeOf(self, name):
    type = ""
    entry = self.findEntry(name)
    if entry != []:
      type = entry[1]
    return type
    
  # Returns the index assigned to the named identifier
  def IndexOf(self, name):
    idx = -1
    entry = self.findEntry(name)
    if entry != []:
      idx = entry[2]
    return idx
    
  #......................................................
  # Helper functions
  def increaseCounter(self, type):
    counter = 0;
    if type == STATIC:
      counter = self.staticCnt
      self.staticCnt += 1
    elif type == THIS:
      counter = self.fieldCnt
      self.fieldCnt += 1
    elif type == LOCAL:
      counter = self.localCnt
      self.localCnt += 1
    elif type == ARG:
      counter = self.argCnt
      self.argCnt += 1
    return counter
      
  # Finds the entry in the hash table / dictionary
  def findEntry(self, name):
    retVal = []
    if name in self.symbolTable:
      retVal = self.symbolTable[name]
    return retVal
      
  # print the symbol table
  def printTable(self, iden):
    print()
    print(iden + ": " + self.tableName)
    for e in self.symbolTable:
      print('\t' + e + ' ' + str(self.symbolTable[e]))
    print()
      
      
      
      
      
      
      
      
      
      
      
      
      