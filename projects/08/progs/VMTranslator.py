#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the second part of the translator
#
#***********************************************************

import argparse
import re
import os 

import Parser, CodeWriter
   
 
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
  parser = Parser.Parser(args.input)
  codeWriter = CodeWriter.CodeWriter()
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
    elif cmd == "C_FUNCTION":
      codeWriter.writeFunction(parser.arg1(), parser.arg2())
    elif cmd == "C_RETURN":
      codeWriter.writeReturn()

    
  # close input and output file
  parser.close()
  codeWriter.close()