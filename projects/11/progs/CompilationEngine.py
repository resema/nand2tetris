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
    self.nbrOfClassVar = 0
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
          self.nbrOfClassVar += self.CompileClassVarDec()
    self.closeCurlyBracket("class")
    
    #TODO Testing
    self.classTable.printTable("Class Symbol Table")
    
  # Compiles a static variable declaration or a field declaration
  def CompileClassVarDec(self):
    if self.token[1] == K_FIELD:
      kind = K_THIS
    elif self.token[1] == K_STATIC:
      kind = K_STATIC
    else:
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
    nbrOfClassVar = 1    
    while (self.token[1] != S_SEMICOLON):
      if self.token[1] != S_KOMMA:
        raise Exception("classVarDec initializer list komma missing: " + self.token[1])
      self.next()
      if self.token[0] != T_IDENTIFIER:
        raise Exception("classVarDec identifier missing: " + self.token[1])
      name = self.token[1]
      self.next()
      self.classTable.define(name, type, kind)
      nbrOfClassVar += 1   
    return nbrOfClassVar
    
  # Compiles a complete method, function or constructor
  def CompileSubroutineDec(self):
    self.nbrOfArg = 0
    if self.token[1] == K_METHOD:
      self.methodFlag = K_METHOD
    elif self.token[1] == K_CONSTRUCTOR:
      self.methodFlag = K_CONSTRUCTOR
    else:
      self.methodFlag = K_FUNCTION
    self.next()
    if not (self.token[0] == T_KEYWORD or self.token[0] == T_IDENTIFIER):
      raise Exception("subroutine keyword missing: " + self.token[0] + ", " + self.token[1])
    self.next()
    self.checkIdentifier("subroutine identifier missing")
    
    # new subroutine symbol table with this
    self.subroutineTable = SymbolTable.SymbolTable()
    self.subroutineTable.setName(self.token[1])
    if self.methodFlag == K_METHOD:
      self.subroutineTable.define(K_THIS, self.className, ARG)
      self.nbrOfArg += 1
    elif self.methodFlag == K_CONSTRUCTOR:
      self.subroutineTable.define(K_THIS, self.className, "pointer")
    self.next()
    self.openBracket("subroutine decl")  
    self.nbrOfArg += self.compileParameterList()   # parameter list
    self.functionName = self.classTable.getName() + "." + self.subroutineTable.getName()    
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
    if self.token[0] == T_INT_CONST:
      kind = "constant"
      idx = self.token[1]
      self.vmWriter.writePush(kind, idx)
    elif self.token[0] == T_STRING_CONST:
        strSize = len(self.token[1])           # size of string
        self.vmWriter.writePush(CONST, strSize)
        self.vmWriter.writeCall("String.new", 1)       
        for letter in self.token[1]:
          self.vmWriter.writePush(CONST, ord(letter))
          self.vmWriter.writeCall("String.appendChar", 2)          
    elif self.token[1] == K_TRUE: 
      kind = "constant"
      self.vmWriter.writePush(kind, 0)
      self.vmWriter.writeArithmetic(S_NOT)
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
        kind = self.subroutineTable.KindOf(self.token[1])   # root address of array
        idx = self.subroutineTable.IndexOf(self.token[1])
        if kind == -1:
          kind = self.classTable.KindOf(self.token[1])
          idx = self.classTable.IndexOf(self.token[1])
        self.next()
        self.next()
        self.CompileExpression()      # expression
        self.vmWriter.writePush(kind, idx)                  # root address of array
        self.vmWriter.writeArithmetic(S_PLUS)
        self.vmWriter.writePop("pointer", 1)
        self.vmWriter.writePush(THAT, 0)
        if self.token[1] != S_CANGLEBRACKETS:
          raise Exception("letStatement closing angle bracket missing: " + self.token[1])
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
      if self.token[1] == S_TILDE:
        notToken = self.token
        self.next()
        self.CompileTerm()
        self.vmWriter.writeArithmetic(notToken[1])
      elif self.token[1] == S_MINUS:
        self.next()
        self.CompileTerm()
        self.vmWriter.writeArithmetic(S_NEG)
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
      # self.tagAsXml(self.token)
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
      nbrOfArg += 1
      self.next()
    return nbrOfArg
    
  # Compiles a subroutine's body
  def compileSubroutineBody(self):
    nbrOfVarDec = 0
    self.next()
    self.openCurlyBracket("subroutine body")   
    self.next()
    while (self.token[1] == K_VAR):
        nbrOfVarDec += self.compileVarDec()
        self.next()
    self.vmWriter.writeFunction(self.functionName, nbrOfVarDec)
    if self.methodFlag == K_METHOD:
      self.vmWriter.writePush("argument", 0) #THIS
      self.vmWriter.writePop("pointer", 0)
    elif self.methodFlag == K_CONSTRUCTOR:
      self.vmWriter.writePush("constant", self.nbrOfClassVar)
      self.vmWriter.writeCall("Memory.alloc", 1)
      self.vmWriter.writePop("pointer", 0)
    # for idx in range(self.nbrOfArg):
      # self.vmWriter.writePush("argument", idx) #TODO this is missing
    self.compileStatements()
    self.closeCurlyBracket("subroutine body")
    
  # Compiles a var declaration
  def compileVarDec(self):
    nbrOfVarDec = 1
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
      nbrOfVarDec += 1
    if self.token[1] != S_SEMICOLON:
      raise Exception("varDec semicolon missing: " + self.token[1])
    return nbrOfVarDec
    
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
    that = False
    self.next()
    self.checkIdentifier("letStatement identifier missing")
    varName = self.token[1]
    self.next()    
    if self.token[0] == T_SYMBOL:
      if self.token[1] == S_OANGLEBRACKETS:
        kind = self.subroutineTable.KindOf(varName)         # root address of array
        idx = self.subroutineTable.IndexOf(varName)
        if kind == -1:
          kind = self.classTable.KindOf(varName)
          idx = self.classTable.IndexOf(varName)
        self.next()
        self.CompileExpression()    # expression
        self.vmWriter.writePush(kind, idx)                  # root address of array
        self.vmWriter.writeArithmetic(S_PLUS)
        self.vmWriter.writePop("pointer", 1)
        that = True
        if self.token[1] != S_CANGLEBRACKETS:
          raise Exception("letStatement closing angle bracket missing: " + self.token[1])
        self.next()
    if self.token[1] != S_EQUALS:   # equal sign
      raise Exception("letStatement equal symbol missing: " + self.token[1])
    self.next()
    self.CompileExpression()        # expression
    if self.token[1] != S_SEMICOLON:
      raise Exception("letStatement semicolon missing: " + self.token[1])
    kind = self.subroutineTable.KindOf(varName)
    idx = self.subroutineTable.IndexOf(varName)
    if kind == -1:
      kind = self.classTable.KindOf(varName)
      idx = self.classTable.IndexOf(varName)
    if that == True:
      self.vmWriter.writePop(THAT, 0)
    else:
      self.vmWriter.writePop(kind, idx)
    
  # Compiles an if statement
  def compileIf(self):
    ifLbl = self.createLabel("IF")
    elseLbl = self.createLabel("ELSE")
    exitLbl = self.createLabel("EXIT")
    self.increaseLabelCounter()
    
    self.next()
    self.openBracket("ifStatement")
    self.next()
    checkVar = False
    if self.peek()[1] == S_CBRACKETS:
      checkVar = True
    self.CompileExpression()
    if checkVar:
      kind = "constant"
      self.vmWriter.writePush(kind, 0)
      self.vmWriter.writeArithmetic(S_NOT)
      self.vmWriter.writeArithmetic(S_EQUALS)
    self.vmWriter.writeIf(ifLbl)
    self.vmWriter.writeGoto(elseLbl)
    self.vmWriter.writeLabel(ifLbl)
    self.closeBracket("ifStatement")
    self.next()
    self.openCurlyBracket("ifStatement")
    self.next()
    self.compileStatements()
    self.vmWriter.writeGoto(exitLbl)
    self.closeCurlyBracket("ifStatement")
    self.vmWriter.writeLabel(elseLbl)
    if self.peek()[1] == K_ELSE:
      self.next()
      self.next()
      self.openCurlyBracket("elseStatement")
      self.next()
      self.compileStatements()
      self.closeCurlyBracket("elseStatement")
    self.vmWriter.writeLabel(exitLbl)
      
  # Compiles a while statement
  def compileWhile(self):
    whileLbl = self.createLabel("WHILE")
    continueLbl = self.createLabel("CONTINUE")
    exitLbl = self.createLabel("EXIT")
    self.increaseLabelCounter()
    
    self.vmWriter.writeLabel(whileLbl)
    self.next()
    self.openBracket("whileStatement")
    self.next()
    checkVar = False
    if self.peek()[1] == S_CBRACKETS:
      checkVar = True
    self.CompileExpression()
    if checkVar:
      kind = "constant"
      self.vmWriter.writePush(kind, 0)
      self.vmWriter.writeArithmetic(S_NOT)
      self.vmWriter.writeArithmetic(S_EQUALS)
    self.closeBracket("whileStatement")
    self.vmWriter.writeIf(continueLbl)
    self.vmWriter.writeGoto(exitLbl)
    self.vmWriter.writeLabel(continueLbl)
    self.next()
    self.openCurlyBracket("whileStatement")
    self.next()
    self.compileStatements()
    self.closeCurlyBracket("whileStatement")
    self.vmWriter.writeGoto(whileLbl)
    self.vmWriter.writeLabel(exitLbl)
    
  # Compiles a do statement
  def compileDo(self):
    nbrOfArg = 0
    self.next()
    self.checkIdentifier("doStatement identifier missing")

    funcName = self.subroutineTable.TypeOf(self.token[1])
    table = self.subroutineTable
    if funcName == "":
      funcName = self.classTable.TypeOf(self.token[1])
      table = self.classTable
    if self.peek()[1] != S_POINT:
      funcName = self.className
      self.vmWriter.writePush("pointer", 0)
      nbrOfArg += 1
    elif funcName != "":
      kind = table.KindOf(self.token[1])
      idx = table.IndexOf(self.token[1])
      self.vmWriter.writePush(kind, idx)
      nbrOfArg += 1
      self.next()
    else:
      funcName = self.token[1]
      self.next()
    
    if self.token[1] == S_POINT:
      self.next()
      self.checkIdentifier("doStatement subroutine identifier missing")
      funcName += "." + self.token[1]
      self.next()
    else:
      funcName += "." + self.token[1]
      self.next()
    
    self.openBracket("doStatement")
    self.next()
    nbrOfArg += self.CompileExpressionList()
    self.closeBracket("doStatement")
    self.next()
    if self.token[1] != S_SEMICOLON:
      raise Exception("doStatement semicolon missing: " + self.token[1])
    self.vmWriter.writeCall(funcName, nbrOfArg)
    self.vmWriter.writePop("temp", 0)
      
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
  def increaseLabelCounter(self):
    self.nbrOfLabel += 1
    
  def createLabel(self, identifier):
    return identifier + "@" + str(self.nbrOfLabel)
    
  
   
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