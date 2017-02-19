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
    self.head(classHead[1])
    self.depth += 1
    self.newline()
    self.tagAsXml(self.token)
    self.next()
    if self.token[0] != T_IDENTIFIER:
      raise Exception("class name missing")
    self.tagAsXml(self.token)
    self.next()
    self.openCurlyBracket(self.token)
    
    while (len(self.listOfTokens) > 1):    # leave closing bracket to the class implementation
      self.next()
      if self.token[0] == T_KEYWORD:
        if self.token[1] == K_CONSTRUCTOR or self.token[1] == K_FUNCTION or self.token[1] == K_METHOD:
          self.CompileSubroutineDec()     # subroutine declaration
        elif self.token[1] == K_LET:
          self.compileLet()

    self.closeCurlyBracket(self.token)
    self.tail(classHead[1])
    
    self.fobj_out.write(self.tree)
    
  # Compiles a static variable declaration of a field declaration
  def CompileClassVarDec(self):
    pass
    
  # Compiles a complete method, function or constructor
  def CompileSubroutineDec(self):
    subroutineDec = "subroutineDec"
    self.head(subroutineDec, self.depth)
    self.depth += 1
    self.newline()
    self.tagAsXml(self.token)
    self.next()
    if self.token[0] != T_KEYWORD:
      raise Exception("subroutine keyword missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.next()
    if self.token[0] != T_IDENTIFIER:
      raise Exception("subroutine identifier missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.next()
    self.openBracket(self.token)  
    self.compileParameterList()   # parameter list
    self.next()
    self.closeBracket(self.token)
    self.compileSubroutineBody()  # subroutine body
    self.depth -= 1
    self.tail(subroutineDec, self.depth)
    
  # Compiles an expression and returns a semicolon as token
  def CompileExpression(self):
    expression = "expression"
    self.head(expression, self.depth)
    self.depth += 1
    self.newline()
    self.CompileTerm()
    self.next()
    while (self.token[1] != S_SEMICOLON):     # TODO: earlier exit needed?
      if self.token[0] == T_SYMBOL:
        if self.token[1] != (S_PLUS or S_MINUS or S_STAR or S_SLASH or S_AMPERSAND 
                             or S_PIPE or S_LESSTHAN or S_GREATERTHAN or S_EQUALS):
          raise Exception("expression op missing: " + self.token[1])
      self.next()
      self.CompileTerm()
    self.depth -= 1
    self.tail(expression, self.depth)
    
  # Compiles a term
  #   If the token is an identifier, the routine must distinguish beteen a variable,
  #   an array entry or a subroutine call.
  #   A single look-ahead token, which may be one of "[", "(" or ".", suffices to
  #   distinguish between the possibilities.
  #   Any other token is not part of this term
  def CompileTerm(self):
    term = "term"
    self.head(term, self.depth)
    self.depth += 1
    self.newline()
    self.tagAsXml(self.token)
    self.next()
    if self.token[0] == (T_INT_CONST or T_STRING_CONST):
      self.tagAsXml(self.token)
    elif self.token[0] == T_IDENTIFIER:
      if self.token[0] == T_SYMBOL:             # angle bracket
        if self.token[1] == S_OANGLEBRACKETS:
          self.tagAsXml(self.token)
          self.next()
          self.CompileExpression()    # expression
          self.next()
          if self.token[1] != S_CANGLEBRACKETS:
            raise Exception("letStatement closing angle bracket missing: " + self.token[1])
          self.tagAsXml(self.token)
          self.next()
        elif self.token[1] == S_POINT:          # subroutine call
          self.tagAsXml(self.token)
          self.next()
          if self.token[0] != T_IDENTIFIER:
            raise Exception("subroutine call missing identifier: " + self.token[1])
          self.tagAsXm(self.token)
          self.next
          self.openBracket(self.token)
          self.CompileExpressionList()
          self.closeBracket(self.token)
      
    self.depth -= 1
    self.tail(term, self.depth)
    
    
  # Compiles a comma-separated list of expressions
  def CompileExpressionList(self):
    self.next
   
  # Compiles a possible emtpy parameter list
  #   Does not handle the enclosing "()"
  def compileParameterList(self):
    parameterList = "parameterList"
    self.head(parameterList, self.depth)
    self.depth += 1
    self.newline()
    
    self.depth -= 1
    self.tail(parameterList, self.depth)
    
  # Compiles a subroutine's body
  def compileSubroutineBody(self):
    subroutineBody = "subroutineBody"
    self.head(subroutineBody, self.depth)
    self.depth += 1
    self.newline()
    self.next()
    self.openCurlyBracket(self.token)
    
    while (self.token[1] != S_CCURLYBRACKETS):
      self.next()
      if self.token[1] == K_LET:
          self.compileLet()

    self.closeCurlyBracket(self.token)
    self.tail(subroutineBody, self.depth)
    
  # Compiles a var declaration
  def comileVarDec(self):
    pass
    
  # Compiles a sequence of statements
  #    Does not handle the enclosing "{}"
  def compileStatements(self):
    pass
  
  # Compiles a let statement
  def compileLet(self):
    letStatement = "letStatement"
    self.head(letStatement, self.depth)
    self.depth += 1
    self.newline()
    self.tagAsXml(self.token)
    self.next()
    if self.token[0] != T_IDENTIFIER:
      raise Exception("letStatement identifier missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.next()    
    if self.token[0] == T_SYMBOL:
      if self.token[1] == S_OANGLEBRACKETS:
        self.tagAsXml(self.token)
        self.next()
        self.CompileExpression()    # expression
        self.next()
        if self.token[1] != S_CANGLEBRACKETS:
          raise Exception("letStatement closing angle bracket missing: " + self.token[1])
        self.tagAsXml(self.token)
        self.next()
    if self.token[1] != S_EQUALS:
      raise Exception("letStatement equal symbol missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.next()
    self.CompileExpression()        # expression
    if self.token[1] != S_SEMICOLON:
      raise Exception("letStatement semicolon missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.depth -= 1
    self.tail(letStatement, self.depth)
    
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
    
  # Compile opening bracket
  def openBracket(self, token):
    if self.token[0] != T_SYMBOL and self.token[1] == S_OBRACKETS:
      raise Exception("subroutine opening bracket is missing: " + self.token[1])
    self.tagAsXml(self.token)
   
  # Compile clsing bracket
  def closeBracket(self, token):
    if self.token[0] != T_SYMBOL and self.token[1] == S_CBRACKETS:
      raise Exception("subroutine closing bracket is missing: " + self.token[1])
    self.tagAsXml(self.token)
    
  # Compile open curly brackets
  def openCurlyBracket(self, token):
    if self.token[0] != T_SYMBOL and self.token[1] != S_OCURLYBRACKETS:
      raise Exception("opening curly bracket missing: " + self.token[1])
    self.tagAsXml(self.token)

  # Compile close curly brackets
  def closeCurlyBracket(self, token):
    if self.token[0] != T_SYMBOL and self.token[1] != S_CCURLYBRACKETS:
      raise Exception("closing curly bracket missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.depth -= 1
   
   
  #.................................................
  # next token from listOfTokens
  def next(self):
    if (len(self.listOfTokens) > 0):
      ret = self.listOfTokens.pop(0)
    else:
      ret = null
    self.token = ret
  
  # helpers for xml tags
  def head(self, str, depth=0):
    ret = ""
    for i in range(depth):
      ret += "\t"
    ret += "<" + str + ">"
    self.tree += ret
    
  def tail(self, str, depth=0):
    ret = ""
    for i in range(depth):
      ret += "\t"
    ret += "</" + str + ">\n" 
    self.tree += ret
    
  def tagAsXml(self, token):
    for i in range(self.depth):
      self.tree += "\t"
    self.head(token[0])
    self.tree += token[1]
    self.tail(token[0])
    
  def newline(self):
    self.tree += "\n"