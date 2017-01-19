import argparse
import re
import os 

class Parser:

  def __init__(self, input):
    self.inFile = input
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
                              "if"   : "C_IF",
                              "function": "C_FUNCTION",
                              "return": "C_RETURN",
                              "call" : "C_CALL"
                             }
    
    for line in self.inFile:
      newline = re.sub("//.*?\n", "", line) # remove comments
      newline = re.sub("\\n", "", newline) # remove empty lines
      if newline != "":
        self.rawCmds.insert(len(self.rawCmds), newline)
        
  
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
    
  def debug(self):
    print(self.curCmd)
  
  
class CodeWriter:
  
  def __init__(self, output):
    self.outFile = output
  
  # writes to the output file the assembly code that implements the given cmd
  def writeArithmetic(self):
    pass
  
  # write to the output file the assembly code the given command
  def writePushPop(self):
    pass


if __name__ == "__main__":
  # parse command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("input",  help="input file")
  args = parser.parse_args()
  
  # open input and output file
  fobj_in = open(args.input)
  
  outname = fobj_in.name
  base = os.path.splitext(outname)[0]
  fobj_out = open(base + ".asm", 'w')

  parser = Parser(fobj_in)
  while parser.hasMoreCommands():
    parser.advance()
    type = parser.commandType()
    arg1 = parser.arg1()

    print(type + " " + arg1)
    #parser.debug()
  
  # close input and output file
  fobj_in.close()
  fobj_out.close()
