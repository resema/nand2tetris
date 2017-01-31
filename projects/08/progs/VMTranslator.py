#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the second part of the translator
#
#***********************************************************

import sys
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
  parser.add_argument("--file", help="input file")
  parser.add_argument("--dir", help="input directory")
  args = parser.parse_args()
  
  filesToParse = []
  
  # separate file from directory
  if args.dir:
    files = [args.dir + "/" + f for f in os.listdir(args.dir) if f.endswith(".vm")]
    print(files)
    path = args.dir.split("/")
    dirName = path[-1]
    fileName = args.dir + "/" + dirName + ".asm"
    filesToParse = files
  else:
    fileName = os.path.splitext(args.file)[0] + ".asm"
    filesToParse.append(args.file)
  
  # initialize parser
  codeWriter = CodeWriter.CodeWriter()
  codeWriter.setFileName(fileName)
  
  # bootstrap init
  codeWriter.writeInit()
  
  for file in filesToParse:
    parser = Parser.Parser(file)
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
      elif cmd == "C_CALL":
        codeWriter.writeCall(parser.arg1(), parser.arg2())

    
  # close input and output file
  parser.close()
  codeWriter.close()