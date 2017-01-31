#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the second part of the parser
#
#***********************************************************

import re


class Parser:

  def __init__(self, fileName):
    self.rawCmds = []
    self.curCmd = ""
    self.cmd = []
    self.typeCmd = { "add": "C_ARITHMETIC",
                      "sub": "C_ARITHMETIC",
                      "neg": "C_ARITHMETIC",
                      "eq"  : "C_ARITHMETIC",
                      "gt"  : "C_ARITHMETIC",
                      "lt"   : "C_ARITHMETIC",
                      "and": "C_ARITHMETIC",
                      "or" : "C_ARITHMETIC",
                      "not": "C_ARITHMETIC",
                      "push": "C_PUSH",
                      "pop": "C_POP",
                      "label": "C_LABEL",
                      "goto": "C_GOTO",
                      "if-goto"   : "C_IF",
                      "function": "C_FUNCTION",
                      "return": "C_RETURN",
                      "call" : "C_CALL"
                      }
                      
    # open input file
    self.fobj_in = open(fileName)
    
    for line in self.fobj_in:
      newline = re.sub("//\s.*", "", line) # remove comments
      newline = re.sub("//.*?\n", "", newline) # remove comments
      newline = re.sub("\\n", "", newline) # remove empty lines
      if newline != "":
        self.rawCmds.insert(len(self.rawCmds), newline)

  def close(self):
      self.fobj_in.close()
    
  # are there more commands in the input
  def hasMoreCommands(self):
    return len(self.rawCmds) > 0
    
  # reads the next command from the input and makes it the current command
  # shall only be called if hasMoreCommands() is true
  def advance(self):
    self.curCmd = self.rawCmds.pop(0)
    self.cmd = self.curCmd.split(" ")
    
  # returns an entry from the list
  def commandType(self):
    return self.typeCmd[self.cmd[0]]
    
  # should not be called if cmd is return
  # returns a string
  def arg1(self):
    if len(self.cmd) == 1:
      return self.cmd[0]
    else:
      return self.cmd[1]
    
  # should only be called if cmd is push, pop, function or call
  # returns  an int
  def arg2(self):
    return self.cmd[2]
   
