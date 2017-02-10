#!/usr/local/bin/python3


#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the Core Engine of the Analyzer
#
#       Handels  program structure, statements, expressions
#
#***********************************************************

class CompilationEngine:

  # Creates a new compilation engine
  def __init__(self, fobj_in, fobj_out):
    self.fobj_in = fobj_in
    self.fobj_out = fobj_out
    
  # Compiles a complete class
  def CompileClass(self):
    pass
    
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
  def compieReturn(self):
    pass