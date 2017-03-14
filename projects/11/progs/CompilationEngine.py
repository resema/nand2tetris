#!/usr/local/bin/python3


#***********************************************************
# Nand2Tetris Part II
#
#    Implementation of the Core Engine of the Analyzer
#
#       Handels program structure, statements, expressions
#
#***********************************************************

import VMWriter, SymbolTable

from Defines import *

class CompilationEngine:

  # Creates a new compilation engine
  def __init__(self, listOfTokens, fobj_out):
    self.listOfTokens = listOfTokens
    self.fobj_out = fobj_out
    self.token = ""
    self.depth = 0
    self.tree = ""
    self.vmWriter = VMWriter.VMWriter(fobj_out)
    self.classTable = SymbolTable.SymbolTable()
    self.subroutineTable = SymbolTable.SymbolTable()
    self.className = ""
    self.nbrOfLabel = 0;
    
  def run(self):
    while (len(self.listOfTokens) > 0):
      self.token = self.listOfTokens.pop(0)
      if self.token[0] == T_KEYWORD:
        if self.token[1] == K_CLASS:
          self.CompileClass()
    
  # Compiles a complete class
  def CompileClass(self):
    self.next()
    self.checkIdentifier("class name missing")
    self.className = self.token[1]
    self.classTable.setName(self.token[1])
    self.next()
    self.openCurlyBracket("class")   
    while (len(self.listOfTokens) > 1):    # leave closing bracket to the class implementation
      self.next()
      if self.token[0] == T_KEYWORD:
        if self.token[1] == K_CONSTRUCTOR or self.token[1] == K_FUNCTION or self.token[1] == K_METHOD:
          self.CompileSubroutineDec()     # subroutine declaration
          
          #TODO Testing
          self.subroutineTable.printTable("Subroutine Symbol Table")
        elif self.token[1] == K_FIELD or self.token[1] == K_STATIC:
          self.CompileClassVarDec()
    self.closeCurlyBracket("class")
    
    #TODO Testing
    self.classTable.printTable("Class Symbol Table")
    
  # Compiles a static variable declaration of a field declaration
  def CompileClassVarDec(self):
    kind = self.token[1]    
    self.next()
    
    # locals of type variable or class
    if self.token[0] == T_KEYWORD or self.token[0] == T_IDENTIFIER:
      type = self.token[1]
      self.next()
    else:
      raise Exception("classVarDec type missing: " + self.token[1])
    if self.token[0] == T_IDENTIFIER:
      name = self.token[1]
      self.next()
    else:
      raise Exception("classVarDec identifier missing: " + self.token[1])
    
    self.classTable.define(name, type, kind)
    self.vmWriter.writePush(self.classTable.KindOf(name), self.classTable.IndexOf(name))
    
    while (self.token[1] != S_SEMICOLON):
      if self.token[1] != S_KOMMA:
        raise Exception("classVarDec initializer list komma missing: " + self.token[1])
      self.next()
      if self.token[0] != T_IDENTIFIER:
        raise Exception("classVarDec identifier missing: " + self.token[1])
      name = self.token[1]
      self.next()
      self.classTable.define(name, type, kind)
      self.vmWriter.writePush(self.classTable.KindOf(name), self.classTable.IndexOf(name))
    
  # Compiles a complete method, function or constructor
  def CompileSubroutineDec(self):
    self.next()
    if not (self.token[0] == T_KEYWORD or self.token[0] == T_IDENTIFIER):
      raise Exception("subroutine keyword missing: " + self.token[0] + ", " + self.token[1])
    self.next()
    self.checkIdentifier("subroutine identifier missing")

    # new subroutine symbol table with this
    self.subroutineTable = SymbolTable.SymbolTable()
    self.subroutineTable.setName(self.token[1])
    self.subroutineTable.define(K_THIS, self.className, ARG)
        
    self.next()
    self.openBracket("subroutine decl")  
    nbrOfArg = self.compileParameterList()   # parameter list
    
    #TODO Argument have to be pushed on the stack first
    functionName = self.classTable.getName() + "." + self.subroutineTable.getName()
    self.vmWriter.writeFunction(functionName, nbrOfArg)
    
    self.closeBracket("subroutine decl")
    self.compileSubroutineBody()  # subroutine body
    
  # Compiles an expression and returns a semicolon as token
  #  TODO returns already the next token
  def CompileExpression(self):
    self.CompileTerm()
    self.next()
    while (self.token[1] == S_PLUS or self.token[1] == S_MINUS or self.token[1] == S_STAR or
           self.token[1] == S_SLASH or self.token[1] == S_AMPERSAND or self.token[1] == S_PIPE or
           self.token[1] == S_LESSTHAN or self.token[1] == S_GREATERTHAN or self.token[1] == S_EQUALS):
      opToken = self.token
      self.next()
      self.CompileTerm()
      self.next()
      self.vmWriter.writeArithmetic(opToken[1])
    
  # Compiles a term
  #   If the token is an identifier, the routine must distinguish beteen a variable,
  #   an array entry or a subroutine call.
  #   A single look-ahead token, which may be one of "[", "(" or ".", suffices to
  #   distinguish between the possibilities.
  #   Any other token is not part of this term
  def CompileTerm(self):
    next = self.peek()
    if self.token[0] == T_INT_CONST or self.token[0] == T_STRING_CONST:
      kind = "constant"
      idx = self.token[1]
      self.vmWriter.writePush(kind, idx)
    elif self.token[1] == K_TRUE: 
      kind = "constant"
      self.vmWriter.writePush(kind, -1)
    elif self.token[1] == K_FALSE:
      kind = "constant"
      self.vmWriter.writePush(kind, 0)
    elif self.token[1] == K_THIS or self.token[1] == K_NULL:
      #TODO adapt to specific case
      kind = self.subroutineTable.KindOf(self.token[1])
      idx = self.subroutineTable.IndexOf(self.token[1])
      if kind == -1:
        kind = self.classTable.KindOf(self.token[1])
        idx = self.classTable.IndexOf(self.token[1])
      self.vmWriter.writePush(kind, idx)
    elif self.token[0] == T_IDENTIFIER:
      funcName = self.token[1]
      if next[1] == S_OANGLEBRACKETS:   # array
        self.next()
        # self.tagAsXml(self.token)
        self.next()
        self.CompileExpression()      # expression
        if self.token[1] != S_CANGLEBRACKETS:
          raise Exception("letStatement closing angle bracket missing: " + self.token[1])
        # self.tagAsXml(self.token)
      elif next[1] == S_POINT:          # subroutine call
        self.next()
        self.next()
        if self.token[0] != T_IDENTIFIER:
          raise Exception("function identifier missing: " + self.token[1])
        funcName += "." + self.token[1]
        self.next()
        self.openBracket("term")
        self.next()
        nbrOfArg = self.CompileExpressionList()
        self.closeBracket("term")
        self.vmWriter.writeCall(funcName, nbrOfArg)
      else:
        kind = self.subroutineTable.KindOf(self.token[1])
        idx = self.subroutineTable.IndexOf(self.token[1])
        if kind == -1:
          kind = self.classTable.KindOf(self.token[1])
          idx = self.classTable.IndexOf(self.token[1])
        self.vmWriter.writePush(kind, idx)
    elif self.token[0] == T_SYMBOL:
      if self.token[1] == S_MINUS or self.token[1] == S_TILDE:
        # self.tagAsXml(self.token)
        self.next()
        self.CompileTerm()
      elif self.token[1] == S_OBRACKETS:
        self.openBracket("unary op")
        self.next()
        self.CompileExpression()
        if self.token[1] == S_CBRACKETS:
          self.closeBracket("unary op")
    else:
      raise Exception("term not compilable: " + self.token[1])
    
  # Compiles a comma-separated list of expressions
  def CompileExpressionList(self):
    nbrOfArg = 0
    if self.token[1] != S_CBRACKETS:
      self.CompileExpression()
      nbrOfArg += 1
    while (self.token[1] == S_KOMMA):
      self.tagAsXml(self.token)
      self.next()
      self.CompileExpression()
      nbrOfArg += 1
    return nbrOfArg
   
  # Compiles a possible empty parameter list
  #   Does not handle the enclosing "()"
  #   Returns the number of function arguments
  def compileParameterList(self):
    nbrOfArg = 0
    self.next()
    if self.token[1] != S_CBRACKETS:
      type = self.token[1]
      self.next()
      self.checkIdentifier("parameterList first identifier missing")
      name = self.token[1]
      self.subroutineTable.define(name, type, ARG)
      # self.vmWriter.writePush(self.subroutineTable.KindOf(name), self.subroutineTable.IndexOf(name))
      nbrOfArg += 1
      self.next()
    while (self.token[1] == S_KOMMA):
      self.next()
      if self.token[0] != T_KEYWORD:
        raise Exception("parameterList type missing: " + self.token[1])
      type = self.token[1]
      self.next()
      self.checkIdentifier("parameterList identifier missing")
      name = self.token[1]
      self.subroutineTable.define(name, type, ARG)
      # self.vmWriter.writePush(self.subroutineTable.KindOf(name), self.subroutineTable.IndexOf(name))
      nbrOfArg += 1
      self.next()
    return nbrOfArg
    
  # Compiles a subroutine's body
  def compileSubroutineBody(self):
    self.next()
    self.openCurlyBracket("subroutine body")   
    self.next()
    while (self.token[1] == K_VAR):
        self.compileVarDec()
        self.next()
    self.compileStatements()
    self.closeCurlyBracket("subroutine body")
    
  # Compiles a var declaration
  def compileVarDec(self):
    self.next()
    if self.token[0] == T_KEYWORD or self.token[0] == T_IDENTIFIER:
      type = self.token[1]
      self.next()
    else:
      raise Exception("varDec type missing: " + self.token[1])
    if self.token[0] == T_IDENTIFIER:
      name = self.token[1]
      self.next()
    else:
      raise Exception("varDec identifier missing: " + self.token[1])      
    self.subroutineTable.define(name, type, LOCAL)
    while (self.token[1] != S_SEMICOLON):
      if self.token[1] != S_KOMMA:
        raise Exception("varDec initializer list komma missing: " + self.token[1])
      self.next()
      if self.token[0] != T_IDENTIFIER:
        raise Exception("varDec identifier missing: " + self.token[1])
      name = self.token[1]
      self.next()
      self.subroutineTable.define(name, type, LOCAL)
    if self.token[1] != S_SEMICOLON:
      raise Exception("varDec semicolon missing: " + self.token[1])
    
  # Compiles a sequence of statements
  #    Does not handle the enclosing "{}"
  def compileStatements(self):
    while (self.token[1] != S_CCURLYBRACKETS):
      if self.token[1] == K_LET:
        self.compileLet()
      elif self.token[1] == K_DO:
        self.compileDo()
      elif self.token[1] == K_WHILE:
        self.compileWhile()
      elif self.token[1] == K_IF:
        self.compileIf()
      elif self.token[1] == K_RETURN:
        self.compileReturn()
      self.next()
  
  # Compiles a let statement
  def compileLet(self):
    # letStatement = "letStatement"
    # self.head(letStatement, self.depth)
    # self.depth += 1
    # self.newline()
    # self.tagAsXml(self.token)
    self.next()
    self.checkIdentifier("letStatement identifier missing")
    varName = self.token[1]
    # self.tagAsXml(self.token)
    self.next()    
    if self.token[0] == T_SYMBOL:
      if self.token[1] == S_OANGLEBRACKETS:
        # self.tagAsXml(self.token)
        self.next()
        self.CompileExpression()    # expression
        if self.token[1] != S_CANGLEBRACKETS:
          raise Exception("letStatement closing angle bracket missing: " + self.token[1])
        # self.tagAsXml(self.token)
        self.next()
    if self.token[1] != S_EQUALS:   # equal sign
      raise Exception("letStatement equal symbol missing: " + self.token[1])
    # self.tagAsXml(self.token)
    self.next()
    self.CompileExpression()        # expression
    if self.token[1] != S_SEMICOLON:
      raise Exception("letStatement semicolon missing: " + self.token[1])
    # self.tagAsXml(self.token)
    # self.depth -= 1
    # self.tail(letStatement, self.depth)
    self.vmWriter.writePop(self.subroutineTable.KindOf(varName), self.subroutineTable.IndexOf(varName))
    
  # Compiles an if statement
  def compileIf(self):
    ifStatement = "ifStatement"
    self.head(ifStatement, self.depth)
    self.depth += 1
    self.newline()
    self.tagAsXml(self.token)
    self.next()
    self.openBracket("ifStatement")
    self.next()
    self.CompileExpression()
    self.closeBracket("ifStatement")
    self.next()
    self.openCurlyBracket("ifStatement")
    self.next()
    self.compileStatements()
    self.closeCurlyBracket("ifStatement")
    if self.peek()[1] == K_ELSE:
      self.next()
      self.tagAsXml(self.token)
      self.next()
      self.openCurlyBracket("elseStatement")
      self.next()
      self.compileStatements()
      self.closeCurlyBracket("elseStatement")
    self.tail(ifStatement, self.depth)
      
  # Compiles a while statement
  def compileWhile(self):
    # whileStatement = "whileStatement"
    # self.head(whileStatement, self.depth)
    # self.depth += 1
    # self.newline()
    # self.tagAsXml(self.token)
    whileLbl = self.createUniqueLabel("WHILE")
    continueLbl = self.createUniqueLabel("CONTINUE")
    exitLbl = self.createUniqueLabel("EXIT")
    self.vmWriter.writeLabel(whileLbl)
    self.next()
    self.openBracket("whileStatement")
    self.next()
    self.CompileExpression()
    self.closeBracket("whileStatement")
    self.vmWriter.writeIf(continueLbl)
    self.vmWriter.writeGoto(exitLbl)
    self.vmWriter.writeLabel(continueLbl)
    self.next()
    self.openCurlyBracket("whileStatement")
    self.next()
    self.compileStatements()
    self.closeCurlyBracket("whileStatement")
    # self.tail(whileStatement, self.depth)
    self.vmWriter.writeGoto(whileLbl)
    self.vmWriter.writeLabel(exitLbl)
    
  # Compiles a do statement
  def compileDo(self):
    self.next()
    self.checkIdentifier("doStatement identifier missing")
    funcName = self.token[1]
    self.next()
    if self.token[1] == S_POINT:
      self.next()
      self.checkIdentifier("doStatement subroutine identifier missing")
      funcName += "." + self.token[1]
      self.next()
    self.openBracket("doStatement")
    self.next()
    nbrOfArg = self.CompileExpressionList()
    self.closeBracket("doStatement")
    self.next()
    if self.token[1] != S_SEMICOLON:
      raise Exception("doStatement semicolon missing: " + self.token[1])
    self.vmWriter.writeCall(funcName, nbrOfArg)
      
  # Compiles a return statemetn
  def compileReturn(self):
    self.next()
    if self.token[1] != S_SEMICOLON: 
      self.CompileExpression()
    else:
      self.vmWriter.writePush("constant", 0)
    if self.token[1] != S_SEMICOLON:
      raise Exception("returnStatement semicolon missing: " + self.token[1])
    self.vmWriter.writeReturn()
 
  #.................................................
  # compilation helps
   
  # check for identifier
  def checkIdentifier(self, exception):
    if self.token[0] != T_IDENTIFIER:
      raise Exception(exception + ": " + self.token[1])
   
  # Compile opening bracket
  def openBracket(self, exception):
    if self.token[1] != S_OBRACKETS:
      raise Exception(exception + " opening bracket is missing: " + self.token[1])
    # self.tagAsXml(self.token)
   
  # Compile clsing bracket
  def closeBracket(self, exception):
    if self.token[1] != S_CBRACKETS:
      raise Exception(exception + " closing bracket is missing: " + self.token[1])
    # self.tagAsXml(self.token)
    
  # Compile open curly brackets
  def openCurlyBracket(self, exception):
    if self.token[0] != T_SYMBOL and self.token[1] != S_OCURLYBRACKETS:
      raise Exception(exception + " opening curly bracket missing: " + self.token[1])
    # self.tagAsXml(self.token)

  # Compile close curly brackets
  def closeCurlyBracket(self, exception):
    if self.token[1] != S_CCURLYBRACKETS:
      raise Exception(exception + " closing curly bracket missing: " + self.token[1])
    # self.tagAsXml(self.token)
    # self.depth -= 1
   
  # increase the counter of the labels
  def createUniqueLabel(self, identifier):
    ident = identifier + "@" + str(self.nbrOfLabel)
    self.nbrOfLabel += 1
    return ident
   
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