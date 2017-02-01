import os
import re
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--file", help="input file")
  args = parser.parse_args()
  
  fobj_in = open(args.file)
  
  for line in fobj_in:
    newline = re.sub("\s*//.*?\n", "", line) # remove comments
    newline = re.sub("\\n", "", newline) # remove empty lines
    print(newline)
    
  fobj_in.close()