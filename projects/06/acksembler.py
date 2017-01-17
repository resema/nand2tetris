import argparse
import re

  
class Parser:
    
  def __init__(self, input, output):
    self.lines = []
    self.input = input
    self.output = output
    self.symbolTable = {"SP":  "0",
                                  "LCL": "1",
                                  "ARG": "2",
                                  "THIS": "3",
                                  "THAT": "4",
                                  "R0": "0",
                                  "R1": "1",
                                  "R2": "2",
                                  "R3": "3",
                                  "R4": "4",
                                  "R5": "5",
                                  "R6": "6",
                                  "R7": "7",
                                  "R8": "8",
                                  "R9": "9",
                                  "R10": "10",
                                  "R11": "11",
                                  "R12": "12",
                                  "R13": "13",
                                  "R14": "14",
                                  "R15": "15",
                                  "SCREEN": "16384",
                                  "KBD": "24576"
                                  }
    self.symbolIdx=16
      
  def removeComments(self):
    for line in self.input:
      newline = re.sub("//.*?\n", "", line) # remove comments
      newline = re.sub("\\n", "", newline) # remove em
      newline = re.sub("\s", "", newline) # remove spaces
      if newline != "":
        self.lines.insert(len(self.lines), newline)
    return self.lines
    
  def removeSymbols(self):
    symbolIdx = 0
    for line in self.lines:
      # replace symbols
      symbol = re.search("\(.*\)", line)
      if symbol != None:
        addr = symbol.group().split("(")
        addr = addr[1].split(")")
        if addr[0] not in self.symbolTable:
          self.symbolTable[addr[0]] = str(symbolIdx)
      else:
        symbolIdx += 1
        
    # replace references and variables
    idx = 0
    self.symbolIdx = 16
    for line in self.lines:
      reference = re.search("@R\d+", line)
      if reference != None:
        addr = reference.group().split("@")
        # if addr[1] not in self.symbolTable:
          # self.symbolTable[addr[1]] = str(self.symbolIdx)
          # self.symbolIdx += 1
        self.lines[idx] = "@" + self.symbolTable[addr[1]]
      variable = re.search("@\D.*", line)
      if variable != None:
        # print(variable.group())
        addr = variable.group().split("@")
        if addr[1] not in self.symbolTable:
          self.symbolTable[addr[1]] = str(self.symbolIdx)
          self.symbolIdx += 1
        self.lines[idx] = "@" + self.symbolTable[addr[1]]
      idx += 1
      
    # Eliminate all Symbols
    self.lines = [cmd for cmd in self.lines if re.search("\(.*\)", cmd) == None]
      
    return self.lines
        
  def printLines(self):
    for line in self.lines:
      print(line)
   
  def printTable(self):
    for line in self.symbolTable:
      print(line + ":" + self.symbolTable[line])
 
      
class Code:

  def __init__(self, cmds, output):
    self.binaries = []
    self.cmds = cmds
    self.output = output
    self.CompTable = {"0": "0101010", 
                               "1": "0111111",
                               "-1": "0111010",
                               "D": "0001100",
                               "A": "0110000",
                               "M": "1110000",                               
                               "!D": "0001101",
                               "!A": "0110001",
                               "!M": "1110001",
                               "-D": "0001111",
                               "-A": "0110011",
                               "-M": "1110011",
                               "D+1": "0011111",
                               "A+1": "0110111",
                               "M+1": "1110111",
                               "D-1": "0001110",
                               "A-1": "0110010",
                               "M-1": "1110010",
                               "D+A": "0000010",
                               "D+M": "1000010",
                               "D-A": "0010011",
                               "D-M": "1010011",
                               "A-D": "0000111",
                               "M-D": "1000111",
                               "D&A": "0000000",
                               "D&M": "1000000",
                               "D|A": "0010101",
                               "D|M": "1010101"
                               }
    self.DestTable = {"NULL": "000",
                             "M": "001",
                             "D": "010",
                             "MD": "011",
                             "A": "100",
                             "AM": "101",
                             "AD": "110",
                             "AMD" : "111"
                             }                           
    self.JumpTable = {"NULL": "000",
                              "JGT": "001",
                              "JEQ": "010",
                              "JGE": "011",
                              "JLT": "100",
                              "JNE": "101",
                              "JLE": "110",
                              "JMP": "111"
                              }
    
  def addAInstruction(self, cmd):
    val = re.search("\d+", cmd)
    valInt = int(float(val.group()))
    valBin = format(valInt, '016b')
    self.binaries.insert(len(self.binaries), valBin)
  
  def addCInstruction(self, cmd):
    dest = "NULL"
    jump = "NULL"
    idx = 0
    lhs = cmd.split("=")
    if (len(lhs) > 1):
      dest = lhs[0]
      idx+=1
    rhs = lhs[idx].split(";")
    comp = rhs[0]
    if (len(rhs) > 1):
      jump = rhs[1]
    
    binStr = "111" + self.CompTable[comp] + self.DestTable[dest] + self.JumpTable[jump]
    self.binaries.insert(len(self.binaries), binStr)
    
  def createBinary(self):
    for cmd in self.cmds:
      if cmd[0] == "@":
        self.addAInstruction(cmd)
      else:
        self.addCInstruction(cmd)
    
  def writeToFile(self):
    for bin in self.binaries:
      self.output.write(bin)
      self.output.write("\n")


if __name__ == "__main__":
  
  # Parse cmd argument
  parser = argparse.ArgumentParser()
  parser.add_argument("input", help="input file")
  parser.add_argument("output", help="output file")
  args = parser.parse_args()
  
  # Open input and output file
  fobj_in = open(args.input)
  fobj_out = open(args.output, "w")
      
  # First pass
  parser_ = Parser(fobj_in, fobj_out)
  cmds = parser_.removeComments()  
  cmds = parser_.removeSymbols() 
  # parser_.printLines()
  # parser_.printTable()
  
  # Second pass
  code_ = Code(cmds, fobj_out)
  code_.createBinary()
  code_.writeToFile()
  
  # Clean up
  fobj_in.close()
  fobj_out.close()
  
