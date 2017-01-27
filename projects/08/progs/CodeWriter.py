#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the second part of the CodeWriter
#
#***********************************************************


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
    self.filename = ""
    self.namespace = ["main"]
    
  def setFileName(self, fileName):
    path = fileName.split("/")
    nameext = path[-1]
    name = nameext.split(".")
    self.filename = name[-2]
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
    code = "@SP" + "\n" 
    code += "A=M" + "\n" 
    code += "M=D" + "\n"
    return code
    
  # access the specified segment address
  def accessSegmentAddr(self, segment, index):    # accessing LCL, ARG, THIS, THAT
    code = "@" + str(index) + "\n"
    code += "D=A" + "\n"  # D=pointer offset (index)
    code += "@" + self.segments[segment] + "\n"
    code += "A=M+D" + "\n"  # M=RAM[LCL+offset]
    return code
  
  # access the segment directly and apply and offset
  def accessSpecialAddr(self, segment, index):      # accessing temp, static, poitner
    code = "@" + str(index) + "\n"
    code += "D=A" + "\n"  # D=pointer offset (index)
    code += "@" + self.segments[segment] + "\n"
    code += "A=A+D" + "\n"  # M=RAM[R5+offset]
    return code
    
  #returns the content of the register with an negative offset from the LCL
  def restoreCaller(self, offset, target):
    code = "@" + str(offset) + "\n"
    code += "D=A" + "\n"
    code += "@LCL" + "\n"
    code += "A=M-D" + "\n"    # *(LCL - offset)
    code += "D=M" + "\n"
    code += "@" + target + "\n"
    code += "M=D" + "\n"                                      # retAddr = R6 = "(frame-5)
    return code
   
  # writes the bootstrap bod
  def writeInit(self):
    code = "// Bootstrap init" + "\n"
    code += "@256" + "\n"
    code += "D=A" + "\n"
    code += "@SP" + "\n"
    code += "M=D" + "\n"  #set SP 256
    code += self.increaseSP()
    code += "@LCL" + "\n"
    code += "M=D" + "\n"  #set LCL 256
    code += self.increaseSP()
    code += "@ARG" + "\n"
    code += "M=-1" + "\n"  #set ARG -1
    code += self.increaseSP()
    code += "@THIS" + "\n"
    code += "M=-1" + "\n"  #set THIS -1
    code += self.increaseSP()
    code += "@THAT" + "\n"
    code += "M=-1" + "\n"  #set THAT -1
    code += self.increaseSP()
    self.fobj_out.write(code + "\n")
    self.writeCall(self.filename + ".init", 0)
   
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
    gLabel = self.namespace[len(self.namespace)-1] + "$" + label
    code = ""
    code += "// " + gLabel + "\n"
    code += "(" + gLabel + ")" + "\n"
    self.fobj_out.write(code + "\n")
    
  # writes the assembly code for goto
  def writeGoto(self, label):
    gLabel = self.namespace[len(self.namespace)-1] + "$" + label
    code = ""
    code += "// goto " + gLabel + "\n"
    code += "@" + gLabel + "\n"
    code += "0;JMP" + "\n"
    self.fobj_out.write(code + "\n")
    
  # writes the assembly code for the if-goto
  def writeIf(self, label):
    gLabel = self.namespace[len(self.namespace)-1] + "$" + label
    code = ""
    code += "// if-goto " + gLabel + "\n"
    code += self.decreaseAndAccessSP()
    code += "D=M" + "\n"  # D=top of stack
    code += "@" + gLabel + "\n"
    code += "D;JNE" + "\n"
    self.fobj_out.write(code + "\n")

  # writes the assembly code for the call command
  def writeCall(self, functionName, numArgs):
    code = "// call " + functionName + " " + str(numArgs) + "\n"    
    code += "// save returnAddress" + "\n"
    code += "(returnAddress)" + "\n"
    code += "@returnAddress" + "\n"
    code += "D=A" + "\n"
    code += self.pushDtoSP()
    code += self.increaseSP()
    code += "// save LCL" + "\n"
    code += "@LCL" + "\n"
    code += "D=A" + "\n"
    code += self.pushDtoSP()
    code += self.increaseSP()
    code += "// save ARG" + "\n"
    code += "@ARG" + "\n"
    code += "D=A" + "\n"
    code += self.pushDtoSP()
    code += self.increaseSP()
    code += "// save THIS" + "\n"
    code += "@THIS" + "\n"
    code += "D=A" + "\n"
    code += self.pushDtoSP()
    code += self.increaseSP()
    code += "// save THAT" + "\n"
    code += "@THAT" + "\n"
    code += "D=A" + "\n"
    code += self.pushDtoSP()
    code += self.increaseSP()
    code += "// reposition SP for called function" + "\n"
    code += "@" + str(numArgs+5) + "\n"
    code += "D=A" + "\n"
    code += "@SP" + "\n"
    code += "D=M-D" + "\n"
    code += "@ARG" + "\n"
    code += "M=D" + "\n"
    self.fobj_out.write(code + "\n")
  
  # writes the assembly code for the return command
  def writeReturn(self):
    code = "// return " + "\n" 
    code += self.accessSegmentAddr("local", 0)
    code += "D=M" + "\n"
    code += self.accessSpecialAddr("temp", 0)
    code += "// frame = R5 = LCL" + "\n"
    code += "M=D" + "\n"                                      # frame = R5 = LCL
    code += "// retAddr = R6 = *(frame-5)" + "\n"
    code += self.restoreCaller(5, "R6")                    # retAddr = R6 = *(frame-5)
    code += "// D = top of stack = pop" + "\n"
    code += self.decreaseAndAccessSP()
    code += "D=M" + "\n"                                      # D = top of stack = pop
    code += "@ARG" + "\n"
    code += "A=M" + "\n"
    code += "// *ARG = pop" + "\n"
    code += "M=D" + "\n"                                      # *ARG = pop
    code += "@ARG" + "\n"
    code += "A=M" + "\n"
    code += "D=A" + "\n"
    code += "// SP = ARG + 1" + "\n"
    code += "@SP" + "\n"
    code += "M=D+1" + "\n"                                  # SP=ARG+1
    code += "// THAT = *(frame -1)" + "\n"  
    code += self.restoreCaller(1, "THAT")                # THAT = *(frame-1)
    code += "// THIS = *(frame -2)" + "\n"
    code += self.restoreCaller(2, "THIS")                # THIS = *(frame-2)
    code += "// ARG = *(frame -3)" + "\n"
    code += self.restoreCaller(3, "ARG")                 # ARG = *(frame-3)
    code += "// LCL = *(frame -4)" + "\n"
    code += self.restoreCaller(4, "LCL")                  # LCL = *(frame-4)    
    code += "// goto returnAddr" + "\n"
    code += "@R6" + "\n"                                      # goto returnAddress
    code += "A=M" + "\n"
    code += "0;JMP" + "\n"
    self.fobj_out.write(code + "\n")
    self.namespace.pop()    # removes the last nested namespace from the list
    
  # writes the translation of the given function
  def writeFunction(self, functionName, numLocals):
    self.namespace.append(functionName)   # appends a new nested namespace to the lsit
    code = ""
    code += "// function " + functionName + " " + numLocals + "\n"
    code += "(" + functionName + ")" + "\n"
    self.fobj_out.write(code + "\n")
    for idx in range(int(numLocals)):
      self.writePushPop("C_PUSH", "constant", str(0))
      self.writePushPop("C_POP",  "local", idx)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   