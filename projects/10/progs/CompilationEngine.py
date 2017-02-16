#!/usr/local/bin/python3


#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the Core Engine of the Analyzer
#
#       Handels program structure, statements, expressions
#
#***********************************************************

from Defines import *

class CompilationEngine:

  # Creates a new compilation engine
  def __init__(self, listOfTokens, fobj_out):
    self.listOfTokens = listOfTokens
    self.fobj_out = fobj_out
    self.token = ""
    
  def run(self):
    while (len(self.listOfTokens) > 0):
      self.token = self.listOfTokens.pop(0)
      if self.token == "class":
        self.CompileClass()
    
  # Compiles a complete class
  def CompileClass(self):
    tree = self.head("class")
    # tree += self.newline()
    # self.token = self.next()
    # if not self.checkSymbol(self.token):
      # raise Exception("class opening bracket missing")
      
    # self.token = self.next()
    # if not self.checkSymbol(self.token):
      # raise Exception("class closing bracket missing")
    tree += self.tail("class")
    
    self.fobj_out.write(tree)
    
  # Compiles a static variable declaration of a field declaration
  def CompileClassVarDec(self):
    pass
    
  # Compiles a complete method, function or constructor
  def CompileSubroutineDec(self):
    pass
    
  # Compiles an expression
  def CompileExression(self):
    pass
    
  # Compiles a term
  #   If the token is an identifier, the routine must distinguish beteen a variable,
  #   an array entry or a subroutine call.
  #   A single look-ahead token, which may be one of "[", "(" or ".", suffices to
  #   distinguish between the possibilities.
  #   Any other token is not part of this term
  def CompileTerm(self):
    pass
    
  # Compiles a comma-separated list of expressions
  def CompileExpressionList(self):
    pass
   
  # Compiles a possible emtpy parameter list
  #   Does not handle the enclosing "()"
  def compileParameterList(self):
    pass
    
  # Compiles a subroutine's body
  def compileSubroutineBody(self):
    pass
    
  # Compiles a var declaration
  def comileVarDec(self):
    pass
    
  # Compiles a sequence of statements
  #    Does not handle the enclosing "{}"
  def compileStatements(self):
    pass
  
  # Compiles a let statement
  def compileLet(self):
    pass
    
  # Compiles an if statement
  #   possibly with a trailing else statement
  def compileIf(self):
    pass
    
  # Compiles a while statement
  def compileWhile(self):
    pass
    
  # Compiles a do statement
  def compileDo(self):
    pass
    
  # Compiles a return statemetn
  def compileReturn(self):
    pass
    
    
  #.................................................
  # next token from listOfTokens
  def next(self):
    if (len(self.listOfTokens) > 0):
      ret = self.listOfTokens.pop(0)
    else:
      ret = null
    return ret
  
  # check token
  def checkSymbol(self, tkn):
    for name, tag in symbolList.items():
      if name is tkn:
        return True
      else:
        return False
  
  # helpers for xml tags
  def head(self, str):
    return "<" + str + ">"
    
  def tail(self, str):
    return "</" + str + ">"
    
  def newline(self):
    return "\n"