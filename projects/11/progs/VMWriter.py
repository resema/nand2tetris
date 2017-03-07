#!/usr/local/bin/python3


#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the Code Writer part of the Compiler
#
#       Handels program structure, statements, expressions
#
#***********************************************************

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
    self.fobj_out.write(command + "\n")
    
  # Writes a VM label command
  def writeLabel(self, label):
    self.fobj_out.write("label" + " " + str(label))
    
  # Writes a VM goto command
  def writeGoto(self, label):
    pass
    
  # Writes a VM if-goto command
  def writeIf(self, label):
    pass
    
  # Writes a VM call command
  def writeCall(self, label):
    pass
    
  # Writes a VM function command
  def writeFunction(self, name, nLocals):
    self.fobj_out.write("function" + " " + name + " " + str(nLocals) + "\n")
    
  # Writes a VM return command
  def writeReturn(self):
    pass
    
  # Closes the output file
  def close(self):
    pass
    