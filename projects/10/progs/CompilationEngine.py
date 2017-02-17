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
    self.depth = 0
    self.tree = ""
    
  def run(self):
    while (len(self.listOfTokens) > 0):
      self.token = self.listOfTokens.pop(0)
      if self.token[0] == T_KEYWORD:
        if self.token[1] == K_CLASS:
          self.CompileClass()
    
  # Compiles a complete class
  def CompileClass(self):
    classHead = self.token
    self.tree += self.head(classHead[1])
    self.depth += 1
    self.tree += self.newline()
    self.tree += self.tagAsXml(self.token)
    self.token = self.next()
    if self.token[0] != T_IDENTIFIER:
      raise Exception("class name missing")
    self.tree += self.tagAsXml(self.token)
    self.token = self.next()
    self.openCurlyBracket(self.token)
    
    while (len(self.listOfTokens) > 1):    # leave closing bracket to the class implementation
      self.token = self.next()
      if self.token[0] == T_KEYWORD:
        if self.token[1] == K_CONSTRUCTOR or self.token[1] == K_FUNCTION:
          self.CompileSubroutineDec()

    self.closeCurlyBracket(self.token)
    self.tree += self.tail(classHead[1])
    
    self.fobj_out.write(self.tree)
    
  # Compiles a static variable declaration of a field declaration
  def CompileClassVarDec(self):
    pass
    
  # Compiles a complete method, function or constructor
  def CompileSubroutineDec(self):
    subroutineDec = "subroutineDec"
    self.tree += self.head(subroutineDec, self.depth)
    self.depth += 1
    self.tree += self.newline()
    self.tree += self.tagAsXml(self.token)
    self.token = self.next()
    if self.token[0] != T_KEYWORD:
      raise Exception("subroutine keyword missing: " + self.token[1])
    self.tree += self.tagAsXml(self.token)
    self.token = self.next()
    if self.token[0] != T_IDENTIFIER:
      raise Exception("subroutine identifier missing: " + self.token[1])
    self.tree += self.tagAsXml(self.token)
    self.token = self.next()
    if self.token[0] != T_SYMBOL and self.token[1] == S_OBRACKETS:
      raise Exception("subroutine opening bracket is missing: " + self.token[1])
    self.tree += self.tagAsXml(self.token)
    self.token = self.next()
    if self.token[0] != T_SYMBOL and self.token[1] == S_CBRACKETS:
      raise Exception("subroutine closing bracket is missing: " + self.token[1])
    self.tree += self.tagAsXml(self.token)
    self.token = self.next()
    self.openCurlyBracket(self.token)
    self.compileSubroutineBody()
    
    self.closeCurlyBracket(self.token)
    self.tree += self.tail(subroutineDec, self.depth)
    
  # Compiles an expression
  def CompileExpression(self):
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
    
  # Compile open curly brackets
  def openCurlyBracket(self, token):
    if self.token[0] != T_SYMBOL and self.token[1] != S_OCURLYBRACKETS:
      raise Exception("opening curly bracket missing: " + self.token[1])
    self.tree += self.tagAsXml(self.token)

  # Compile close curly brackets
  def closeCurlyBracket(self, token):
    if self.token[0] != T_SYMBOL and self.token[1] != S_CCURLYBRACKETS:
      raise Exception("closing curly bracket missing: " + self.token[1])
    self.tree += self.tagAsXml(self.token)
    self.depth -= 1
    
  #.................................................
  # next token from listOfTokens
  def next(self):
    if (len(self.listOfTokens) > 0):
      ret = self.listOfTokens.pop(0)
    else:
      ret = null
    return ret
  
  # helpers for xml tags
  def head(self, str, depth=0):
    ret = ""
    for i in range(depth):
      ret += "\t"
    ret += "<" + str + ">"
    return ret
    
  def tail(self, str, depth=0):
    ret = ""
    for i in range(depth):
      ret += "\t"
    ret += "</" + str + ">\n" 
    return ret
    
  def tagAsXml(self, token):
    ret = ""
    for i in range(self.depth):
      ret += "\t"
    ret += self.head(token[0]) + token[1] + self.tail(token[0])
    return ret
    
  def newline(self):
    return "\n"