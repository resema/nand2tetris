#!/usr/local/bin/python3


#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the Code Writer part of the Compiler
#
#       Handels program structure, statements, expressions
#
#***********************************************************

from Defines import *

class VMWriter:
  
  # cstor
  def __init__(self, fobj_out):
    self.fobj_out = fobj_out
    
  # Writes a VM push command
  def writePush(self, segment, idx):
    self.fobj_out.write("push" + " " + str(segment) + " " + str(idx) + "\n")
    
  # Writes a VM pop command
  def writePop(self, segment, idx):
    self.fobj_out.write("pop" + " " + str(segment) + " " + str(idx) + "\n")
    
  # Writes a VM arithmetic-logical command
  def writeArithmetic(self, command):
    if command == S_STAR:
      self.fobj_out.write("call Math.multiply 2" + "\n")
    elif command == S_SLASH:
      self.obj_out.write("call Math.divide 2" + "\n")
    elif command == S_PLUS:
      self.fobj_out.write("add" + "\n")
    elif command == S_MINUS:
      self.fobj_out.write("sub" + "\n")
    elif command == S_LESSTHAN:
      self.fobj_out.write("lt" + "\n")
    elif command == S_GREATERTHAN:
      self.fobj_out.write("gt" + "\n")
    
  # Writes a VM label command
  def writeLabel(self, label):
    self.fobj_out.write("label" + " " + label + "\n")
    
  # Writes a VM goto command
  def writeGoto(self, label):
    self.fobj_out.write("goto" + " " + label + "\n")
    
  # Writes a VM if-goto command
  def writeIf(self, label):
    self.fobj_out.write("if-goto" + " " + label + "\n")
    
  # Writes a VM call command
  def writeCall(self, label, nArgs):
    self.fobj_out.write("call" + " " + label + " " + str(nArgs) + "\n")
    
  # Writes a VM function command
  def writeFunction(self, name, nLocals):
    self.fobj_out.write("function" + " " + name + " " + str(nLocals) + "\n")
    
  # Writes a VM return command
  def writeReturn(self):
    self.fobj_out.write("return" + "\n")
    
  # Closes the output file
  def close(self):
    pass
    