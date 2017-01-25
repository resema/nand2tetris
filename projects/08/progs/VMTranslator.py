#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the second part of the translator
#
#***********************************************************

import argparse
import re
import os 

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
      newline = re.sub("//.*?\n", "", line) # remove comments
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
    
class CodeWriter:
  
  def __init__(self):
    self.fobj_out = ""
    self.lableCnt = 0
    self.varCnt = 0
    self.segments = { "local": "LCL",
                             "argument": "ARG",
                             "this": "THIS",
                             "that": "THAT",
                             "temp": "R5",
                             "static": "16",
                             "pointer": "3"
                             }
    self.namespace = "main"
    
  def setFileName(self, fileName):
    self.fobj_out = open(fileName, 'w')
    
  def close(self):
    self.fobj_out.close()
    
  # helper to increase SP
  def increaseSP(self):
    code = ""
    code = "@SP" + "\n"
    code += "M=M+1" + "\n"
    return code
  
  # decrease sp and access the pointee
  def decreaseAndAccessSP(self):
    code = ""
    code = "@SP" + "\n"
    code += "M=M-1" + "\n" 
    code += "A=M" + "\n"
    return code
    
  #push value in D to SP
  def pushDtoSP(self):
    code = ""
    code = "@SP" + "\n" 
    code += "A=M" + "\n" 
    code += "M=D" + "\n"
    return code
    
  # access the specified segment address
  def accessSegmentAddr(self, segment, index):
    code = ""
    code = "@" + str(index) + "\n"
    code += "D=A" + "\n"  # D=pointer offset (index)
    code += "@" + self.segments[segment] + "\n"
    code += "A=M+D" + "\n"  # M=RAM[LCL+offset]
    return code
  
  def accessSpecialAddr(self, segment, index):
    code = "@" + str(index) + "\n"
    code += "D=A" + "\n"  # D=pointer offset (index)
    code += "@" + self.segments[segment] + "\n"
    code += "A=A+D" + "\n"  # M=RAM[R5+offset]
    return code
   
  # writes the bootstrap bod
  def writeInit(self):
    pass
   
  # writes to the output file the assembly code that implements the given cmd
  def writeArithmetic(self, command):
    code = ""
    if command == "add":
      code = "// add" + "\n"
      code += self.decreaseAndAccessSP()
      code += "D=M" + "\n"  #D=y
      code += self.decreaseAndAccessSP()  #M=x
      code += "M=M+D" + "\n"
      code += self.increaseSP()
    elif command == "sub":
      code = "// sub" + "\n"
      code += self.decreaseAndAccessSP()
      code += "D=M" + "\n"  #D=y
      code += self.decreaseAndAccessSP()  #M=x
      code += "M=M-D" + "\n"
      code += self.increaseSP()
    elif command == "eq":
      code = "// eq" + "\n"
      code += self.decreaseAndAccessSP()
      code +="D=M" + "\n"   #D=y
      code += self.decreaseAndAccessSP()  #M=x
      code += "D=M-D" + "\n"
      code += "M=-1" + "\n"  #x=-1 (true)
      code += "@EQUAL"+ str(self.lableCnt)  + "\n"
      code += "D;JEQ" + "\n"    #x=y -> equal @SP = -1 (true)
      code += "@SP" + "\n"
      code += "A=M" + "\n"
      code += "M=0" + "\n"  # x!=y -> not equal @SP = 0 (false)
      code += "(EQUAL" + str(self.lableCnt) + ")" + "\n"
      code += self.increaseSP()
      self.lableCnt += 1
    elif command == "lt":
      code = "// lt" + "\n"
      code += self.decreaseAndAccessSP()
      code +="D=M" + "\n"   #D=y
      code += self.decreaseAndAccessSP()  #M=x
      code += "D=M-D" + "\n"
      code += "M=-1" + "\n"  #x=-1 (true)
      code += "@LESS"+ str(self.lableCnt)  + "\n"
      code += "D;JLT" + "\n"    #x<y -> equal @SP = -1 (true)
      code += "@SP" + "\n"
      code += "A=M" + "\n"
      code += "M=0" + "\n"  # x!=y -> not equal @SP = 0 (false)
      code += "(LESS" + str(self.lableCnt) + ")" + "\n"
      code += self.increaseSP()
      self.lableCnt += 1
    elif command == "gt":
      code = "// gt" + "\n"
      code += self.decreaseAndAccessSP()
      code +="D=M" + "\n"   #D=y
      code += self.decreaseAndAccessSP()  #M=x
      code += "D=M-D" + "\n"
      code += "M=-1" + "\n"  #x=-1 (true)
      code += "@GREATER"+ str(self.lableCnt)  + "\n"
      code += "D;JGT" + "\n"    #x<y -> equal @SP = -1 (true)
      code += "@SP" + "\n"
      code += "A=M" + "\n"
      code += "M=0" + "\n"  # x!=y -> not equal @SP = 0 (false)
      code += "(GREATER" + str(self.lableCnt) + ")" + "\n"
      code += self.increaseSP()
      self.lableCnt += 1
    elif command == "neg":
      code = "// neg" + "\n"
      code += self.decreaseAndAccessSP()
      code += "M=-M" + "\n"
      code += self.increaseSP()
    elif command == "and":
      code = "// and" + "\n"
      code += self.decreaseAndAccessSP()
      code += "D=M" + "\n"  #D=y
      code += self.decreaseAndAccessSP()  #M=x
      code += "M=D&M" +"\n"
      code += self.increaseSP()
    elif command == "or":
      code = "// and" + "\n"
      code += self.decreaseAndAccessSP()
      code += "D=M" + "\n"  #D=y
      code += self.decreaseAndAccessSP()  #M=x
      code += "M=D|M" + "\n"
      code += self.increaseSP()
    elif command == "not":
      code = "// neg" + "\n"
      code += self.decreaseAndAccessSP()
      code += "M=!M" + "\n"
      code += self.increaseSP()
      
    self.fobj_out.write(code + "\n")
    
  # writes to the output file the assembly code the given command
  def writePushPop(self, command, segment, index):
    code = ""
    if command == "C_PUSH":
      if segment == "constant":
        code = "// push constant " + str(index) + "\n"
        code += "@" + index + "\n" 
        code += "D=A" + "\n" 
        code += self.pushDtoSP()
        code += self.increaseSP()
      elif segment == "temp" or segment == "static" or segment == "pointer":
        code = "// push " + segment + " " + str(index) + "\n"
        code += self.accessSpecialAddr(segment, index)
        code += "D=M" + "\n" # D= RAM[R5+offset]
        code += self.pushDtoSP()
        code += self.increaseSP()   
      else:
        code = "// push " + segment + " " + str(index) + "\n"
        code += self.accessSegmentAddr(segment, index)
        code += "D=M" + "\n" #D = RAM[LCL+offset]
        code += self.pushDtoSP()
        code += self.increaseSP()      
    elif command == "C_POP":
      code = "// pop " + segment + " " + str(index) + "\n"
      if segment == "temp" or segment == "static" or segment == "pointer":
        code += self.accessSpecialAddr(segment, index)
      else:
        # get the RAM[seg+index]
        code += self.accessSegmentAddr(segment, index)      
      code += "D=A" + "\n" #D = add(RAM[LCL+offset])
      code += "@R13" + "\n"
      code += "M=D" + "\n"  # var n stores the address to the segment      
      code += self.decreaseAndAccessSP()
      code += "D=M" + "\n"  # D=top of stack
      code += "@R13" + "\n"
      code += "A=M" + "\n"
      code += "M=D" + "\n"
    # write assembler code to file
    self.fobj_out.write(code + "\n")

  # writes the assembly code for label
  #   Label declaration: functionName$Name (main or function name)
  def writeLabel(self, label):
    gLabel = self.namespace + "$" + label
    code = ""
    code += "// " + gLabel + "\n"
    code += "(" + gLabel + ")" + "\n"
    self.fobj_out.write(code + "\n")
    
  # writes the assembly code for goto
  def writeGoto(self, label):
    gLabel = self.namespace + "$" + label
    code = ""
    code += "// goto " + gLabel + "\n"
    code += "@" + gLabel + "\n"
    code += "0;JMP" + "\n"
    self.fobj_out.write(code + "\n")
    
  # writes the assembly code for the if-goto
  def writeIf(self, label):
    gLabel = self.namespace + "$" + label
    code = ""
    code += "// if-goto " + gLabel + "\n"
    code += self.decreaseAndAccessSP()
    code += "D=M" + "\n"  # D=top of stack
    code += "@" + gLabel + "\n"
    code += "D;JNE" + "\n"
    self.fobj_out.write(code + "\n")

  # writes the assembly code for the call command
  def writeCall(self, functionName, numArgs):
    pass
    
  # writes the assembly code for the return command
  def writeReturn(self):
    pass
    
  # writes the translation of the given function
  def writeFunction(self, functionName, numLocals):
    pass
    
# ******************
# MAIN
# ******************
if __name__ == "__main__":
  # parse command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("input",  help="input file")
  args = parser.parse_args()
  fileName = os.path.splitext(args.input )[0] + ".asm"
  
  # initialize parser and codewriter
  parser = Parser(args.input)
  codeWriter = CodeWriter()
  codeWriter.setFileName(fileName)
  
  while parser.hasMoreCommands():
    parser.advance()
    cmd = parser.commandType()
    
    if cmd == "C_PUSH" or cmd == "C_POP":
      codeWriter.writePushPop(cmd, parser.arg1(), parser.arg2())
    elif cmd == "C_ARITHMETIC":
      codeWriter.writeArithmetic(parser.arg1())
    elif cmd == "C_LABEL":
      codeWriter.writeLabel(parser.arg1())
    elif cmd == "C_GOTO":
      codeWriter.writeGoto(parser.arg1())
    elif cmd == "C_IF":
      codeWriter.writeIf(parser.arg1())

    
  # close input and output file
  parser.close()
  codeWriter.close()