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
    self.checkIdentifier("class name missing")
    # if self.token[0] != T_IDENTIFIER:
      # raise Exception("class name missing")
    self.tagAsXml(self.token)
    self.next()
    self.openCurlyBracket()
    
    while (len(self.listOfTokens) > 1):    # leave closing bracket to the class implementation
      self.next()
      if self.token[0] == T_KEYWORD:
        if self.token[1] == K_CONSTRUCTOR or self.token[1] == K_FUNCTION or self.token[1] == K_METHOD:
          self.CompileSubroutineDec()     # subroutine declaration
        elif self.token[1] == K_LET:
          self.compileLet()
        elif self.token[1] == K_VAR:
          self.compileVarDec()

    self.closeCurlyBracket()
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
    self.checkIdentifier("subroutine identifier missing")
    # if self.token[0] != T_IDENTIFIER:
      # raise Exception("subroutine identifier missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.next()
    self.openBracket()  
    self.compileParameterList()   # parameter list
    self.closeBracket()
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
    while (self.token[1] == S_PLUS or self.token[1] == S_MINUS or self.token[1] == S_STAR or
           self.token[1] == S_SLASH or self.token[1] == S_AMPERSAND or self.token[1] == S_PIPE or
           self.token[1] == S_LESSTHAN or self.token[1] == S_GREATERTHAN or self.token[1] == S_EQUALS):
      if self.token[0] == T_SYMBOL:
        self.tagAsXml(self.token)               # op 
        self.next()
      self.CompileTerm()
      self.next()
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
    next = self.peek()
    self.head(term, self.depth)
    self.depth += 1
    self.newline()
    if self.token[0] == T_INT_CONST or self.token[0] == T_STRING_CONST:
      self.tagAsXml(self.token)
    elif self.token[0] == T_IDENTIFIER:
      self.tagAsXml(self.token)
      if next[1] == S_OANGLEBRACKETS:   # array
        self.next()
        self.tagAsXml(self.token)
        self.next()
        self.CompileExpression()      # expression
        if self.token[1] != S_CANGLEBRACKETS:
          raise Exception("letStatement closing angle bracket missing: " + self.token[1])
        self.tagAsXml(self.token)
      elif next[1] == S_POINT:          # subroutine call
        self.next()
        self.tagAsXml(self.token)
        self.next()
        if self.token[0] != T_IDENTIFIER:
          raise Exception("function identifier missing: " + self.token[1])
        self.tagAsXml(self.token)
        self.next()
        self.openBracket()
        self.next()
        self.CompileExpressionList()
        self.closeBracket()
    elif self.token[0] == T_SYMBOL:     # unary op
      if self.token[1] == S_MINUS or self.token[1] == S_TILDE:
        self.tagAsXml(self.token)
        self.next()
        self.tagAsXml(self.token)
      else:
        raise Exception("unary op missing" + self.token[1])
    else:
      raise Exception("term not compilable: " + self.token[1])
    self.depth -= 1
    self.tail(term, self.depth)   
    
  # Compiles a comma-separated list of expressions
  def CompileExpressionList(self):
    expressionList = "expressionList"
    self.head(expressionList, self.depth)
    self.depth += 1
    self.newline()
    if self.token[0] == T_IDENTIFIER or self.token[0] == T_STRING_CONST or self.token[0] == T_INT_CONST:
      self.tagAsXml(self.token)
      self.next()
      # while
    self.depth -= 1
    self.tail(expressionList, self.depth)
   
  # Compiles a possible emtpy parameter list
  #   Does not handle the enclosing "()"
  def compileParameterList(self):
    parameterList = "parameterList"
    self.head(parameterList, self.depth)
    self.depth += 1
    self.newline()
    self.next()
    while (self.token[1] != S_CBRACKETS):
      self.tagAsXml(self.token)
      self.next()
      if self.token[1] == S_KOMMA:
        self.tagAsXml(self.token)
        self.next()
        if self.token[0] != T_KEYWORD:
          raise Exception("parameterList type missing: " + self.token[1])
        self.tagAsXml(self.token)
        self.next()
        self.checkIdentifier("parameterList identifier missing")
        self.tagAsXml(self.token)
        self.next()
    self.depth -= 1
    self.tail(parameterList, self.depth)
    
  # Compiles a subroutine's body
  def compileSubroutineBody(self):
    subroutineBody = "subroutineBody"
    self.head(subroutineBody, self.depth)
    self.depth += 1
    self.newline()
    self.next()
    self.openCurlyBracket()   
    while (self.token[1] != S_CCURLYBRACKETS):
      self.next()
      if self.token[1] == K_LET:
        self.compileLet()
      elif self.token[1] == K_VAR:
        self.compileVarDec()
    self.closeCurlyBracket()
    self.tail(subroutineBody, self.depth)
    
  # Compiles a var declaration
  def compileVarDec(self):
    varDec = "varDec"
    self.head(varDec, self.depth)
    self.depth += 1
    self.newline()
    self.tagAsXml(self.token)
    self.next()
    if self.token[0] == T_KEYWORD or self.token[0] == T_IDENTIFIER:
      self.tagAsXml(self.token)
      self.next()
    else:
      raise Exception("varDec type missing: " + self.token[1])
    if self.token[0] == T_IDENTIFIER:
      self.tagAsXml(self.token)
      self.next()
    else:
      raise Exception("varDec identifier missing: " + self.token[1])
    while (self.token[1] != S_SEMICOLON):
      if self.token[1] != S_KOMMA:
        raise Exception("varDec initializer list komma missing: " + self.token[1])
      self.tagAsXml(self.token)
      self.next()
      if self.token[0] != T_IDENTIFIER:
        raise Exception("varDec identifier missing: " + self.token[1])
      self.tagAsXml(self.token)
      self.next()
    if self.token[1] != S_SEMICOLON:
      raise Exception("letStatement semicolon missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.depth -= 1
    self.tail(varDec, self.depth)
    
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
    self.checkIdentifier("letStatement identifier missing")
    # if self.token[0] != T_IDENTIFIER:
      # raise Exception("letStatement identifier missing: " + self.token[1])
    self.tagAsXml(self.token)
    self.next()    
    if self.token[0] == T_SYMBOL:
      if self.token[1] == S_OANGLEBRACKETS:
        self.tagAsXml(self.token)
        self.next()
        self.CompileExpression()    # expression
        if self.token[1] != S_CANGLEBRACKETS:
          raise Exception("letStatement closing angle bracket missing: " + self.token[1])
        self.tagAsXml(self.token)
        self.next()
    if self.token[1] != S_EQUALS:   # equal sign
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
    doStatement = "doStatement"
    self.head(doStatement, self.depth)
    self.depth += 1
    self.newline()
    self.tagAsXml(self.token)
    self.next()
    # Idenifier not must-have...
    # self.checkIdentifier("doStatement identifier missing")
    # self.tagAsXml(self.token)
    # self.next()

    # TODO finish doStatement
    
  # Compiles a return statemetn
  def compileReturn(self):
    pass
 
 
  #.................................................
  # compilation helps
   
  # check for identifier
  def checkIdentifier(self, exception):
    if self.token[0] != T_IDENTIFIER:
      raise Exception(exception + ": " + self.token[1])
   
  # Compile opening bracket
  def openBracket(self):
    if self.token[1] != S_OBRACKETS:
      raise Exception("subroutine opening bracket is missing: " + self.token[1])
    self.tagAsXml(self.token)
   
  # Compile clsing bracket
  def closeBracket(self):
    if self.token[1] != S_CBRACKETS:
      raise Exception("subroutine closing bracket is missing: " + self.token[1])
    self.tagAsXml(self.token)
    
  # Compile open curly brackets
  def openCurlyBracket(self):
    if self.token[0] != T_SYMBOL and self.token[1] != S_OCURLYBRACKETS:
      raise Exception("opening curly bracket missing: " + self.token[1])
    self.tagAsXml(self.token)

  # Compile close curly brackets
  def closeCurlyBracket(self):
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
  
  # peek the next token from listofTokens
  def peek(self):
    if (len(self.listOfTokens) > 1):
      ret = self.listOfTokens[0]
    else:
      ret = null
    return ret
  
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