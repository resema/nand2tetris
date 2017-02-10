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