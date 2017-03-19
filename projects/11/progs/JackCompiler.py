#!/usr/local/bin/python3


#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the Analyzer part of the compiler
#
#       Last procession step
#       usage: prompt> JackAnalyzer input
#       input:  filename.jack
#                 directory
#       output: single file -> filename.xml
#                   directory -> one .xml for every .jack file in the same directory
#
#***********************************************************

import argparse
import os

import JackTokenizer, CompilationEngine

from Defines import *


# ******************
# MAIN
# ******************
if __name__ == "__main__":
  # parse command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", help = "input file")
  parser.add_argument("-d", "--dir", help = "input directory")
  args = parser.parse_args()
  
  # separate file from directory
  fileList = []
  if args.dir:
    files = [args.dir + "/" + f for f in os.listdir(args.dir) if f.endswith(".jack")]
    print(files)
    path = args.dir.split("/")
    dirName = path[-1]
    fileList = files
  else:
    fileList.append(args.file)
    
  # Main logic 
  #   1. Creates a JackTokenizer from filename.jack
  #   2. Creates output file filename.xml
  #   3. Creates and uses a CompilationEngine to comple the input into the output file
  for file in fileList:
    # create filename for in and output file
    path = file.split(".")
    noExt = path[-2]
    filename = noExt + ".vm"
    # print(filename)
    fobj_in = open(file)
    fobj_out = open(filename, 'w')
    
    tknzr = JackTokenizer.JackTokenizer(fobj_in)
    tknzr.tokenize();
    
    listOfTokens = []
    while (tknzr.hasMoreTokens()):
      tknzr.advance()
      type = tknzr.tokenType()
      try:
        if type == T_KEYWORD:
          listOfTokens.insert(len(listOfTokens), tknzr.keyWord())
        elif type == T_SYMBOL:
          listOfTokens.insert(len(listOfTokens), tknzr.symbol())
        elif type == T_IDENTIFIER:
          listOfTokens.insert(len(listOfTokens), tknzr.identifier())
        elif type == T_INT_CONST:
          listOfTokens.insert(len(listOfTokens), tknzr.intVal())
        elif type == T_STRING_CONST:
          listOfTokens.insert(len(listOfTokens), tknzr.stringVal())
      except TypeError as err:
        print("Handling TypeError:", err)
    
    # for l in listOfTokens:
      # print(l)
    
    engine = CompilationEngine.CompilationEngine(listOfTokens, fobj_out)
    engine.run()
  
  fobj_in.close()
  fobj_out.close()
  
  