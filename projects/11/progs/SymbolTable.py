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
    self.symbolTable = {}
    self.staticCnt = 0
    self.fieldCnt = 0
    self.localCnt = 0
    self.argCnt = 0
    
  # Adds a new identifier and assigns a running index
  def define(self, name, type, kind):
    if name not in self.symbolTable:
      self.symbolTable[name] = [type, kind, self.increaseCounter(kind)]
    
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
    entry = findEntry(name)
    if entry != []:
      kind =  entry[2]
    return kind
    
  # Returns the type of the named identifier
  def TypeOf(self, name):
    type = ""
    entry = findEntry(name)
    if entry != []:
      type = entry[2]
    return type
    
  # Returns the index assigned to the named identifier
  def IndexOf(self, name):
    idx = -1
    entry = findEntry(name)
    if entry != []:
      idx = entry[3]
    return idx
    
  #......................................................
  # Helper functions
  def increaseCounter(self, type):
    counter = 0;
    if type == STATIC:
      counter = self.staticCnt
      self.staticCnt += 1
    elif type == FIELD:
      counter = self.fieldCnt
      self.fieldCnt += 1
    elif type == LOCAL:
      coutner = self.localCnt
      self.localCnt += 1
    elif type == ARG:
      coutner = self.argCnt
      self.argCnt += 1
    return counter
      
  # Finds the entry in the hash table / dictionary
  def findEntry(self, name):
    retVal = []
    if name in self.symbolTable:
      retVal = self.symbolTable[name]
    return retVal
      
  # print the symbol table
  def printTable(self):
    for e in self.symbolTable:
      print(e + ' ' + str(self.symbolTable[e]))
      
      
      
      
      
      
      
      
      
      
      
      
      
      