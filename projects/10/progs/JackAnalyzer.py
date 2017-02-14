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
    filename = noExt + ".xml"
    print(filename)
    fobj_in = open(file)
    fobj_out = open(filename, 'w')
    
    tknzr = JackTokenizer.JackTokenizer(fobj_in)
    tknzr.tokenize();
  
  fobj_in.close()
  fobj_out.close()
  
  