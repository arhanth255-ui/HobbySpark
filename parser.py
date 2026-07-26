from znode import *
from nodes import *


#######################################################
#Errors
#######################################################
class InvalidSyntaxError(Exception):
    def __init__(self, syntax, adder=""):
        self.mes=f"SyntaxError: '{syntax}' is not valid syntax in python. "+adder
        super().__init__(self.mes)


#######################################################
#Parser
#######################################################
class Parser:
    def __init__(self,tokens:list[Token]):
        self.tokens=tokens
        self.pos=-1
        self.current_token:Token=None
        self.global_class_name=None
        self.advance()

    def advance(self):
        self.pos+=1
        if self.pos<len(self.tokens):
            self.current_token=self.tokens[self.pos]
        else:
            self.current_token=None
    
    def peek(self,num=1) -> Token:
        if self.pos + num < len(self.tokens):
            return self.tokens[self.pos + num]
        return Token(TT_EOF)

    def parse(self):
        body = []

        while self.current_token is not None:
            before = self.pos

            if self.current_token.type==TT_NEWLINE:
                self.advance()
                continue

            st = self.parse_statement()
            if st:
                body.append(st)
            

            # safety: prevent infinite loop
            if self.pos == before:
                self.advance()
        
        return ProgramNode(body)
    
    def parse_statement(self):
        print("STATEMENT:", self.current_token)
        if self.current_token is None:
            return None
        elif self.current_token.type==TT_KEYWORDS["if"]:
           return self.parse_if()
        
        elif self.current_token.type==TT_KEYWORDS["else"]:
            return self.parse_else()
        
        elif self.current_token.type==TT_KEYWORDS["elif"]:
           return self.parse_elif()
        
        elif self.current_token.type==TT_KEYWORDS["while"]:
            return self.parse_while()
        
        elif self.current_token.type==TT_KEYWORDS["for"]:
           return self.parse_for()
        
        elif self.current_token.type==TT_KEYWORDS["return"]:
            return self.parse_return()
        
        elif self.current_token.type==TT_KEYWORDS["yield"]:
            return self.parse_yield()

        elif self.current_token.type==TT_KEYWORDS["def"]:
           return self.parse_def()
        
        elif self.current_token.type==TT_KEYWORDS["class"]:
            return self.parse_class()

        elif self.current_token.type==TT_MATRIX_MUL:
            return self.parse_decorator()

        elif self.current_token.type==TT_KEYWORDS["from"]:
           return self.parse_import()
        
        elif self.current_token.type==TT_KEYWORDS["raise"]:
            return self.parse_raise()
        
        elif self.current_token.type==TT_KEYWORDS["assert"]:
            return self.parse_assert()
        
        elif self.current_token.type==TT_KEYWORDS["try"]:
            return self.parse_try()
        
        elif self.current_token.type==TT_KEYWORDS["with"]:
            return self.parse_with()

        elif self.current_token.type==TT_KEYWORDS["unless"]:
            return self.parse_unless()

        elif self.current_token.type==TT_KEYWORDS["forever"]:
            return self.parse_forever()

        elif self.current_token.type==TT_KEYWORDS["raise_if"]:
            return self.parse_raise_if()
        
        elif self.current_token.type==TT_KEYWORDS["until"]:
            return self.parse_until()

        elif self.current_token.type==TT_KEYWORDS["repeat"]:
            return self.parse_repeat()
        
        elif self.current_token.type==TT_KEYWORDS["stop_if"]:
            return self.parse_stop_if()
        
        elif self.current_token.type==TT_KEYWORDS["skip_if"]:
            return self.parse_skip_if()
        
        elif self.current_token.type==TT_KEYWORDS["raise_ifnot"]:
            return self.parse_raise_if_not()

        elif self.current_token.type==TT_KEYWORDS["match"]:
            return self.parse_match()

        elif self.current_token.type==TT_KEYWORDS["case"]:
            return self.parse_case()

        elif self.current_token.type==TT_KEYWORDS["global"]:
            self.advance()
            varname=self.parse_atom()
            return GlobalNode(varname)
        
        elif self.current_token.type==TT_KEYWORDS["async"]:
            front=self.peek().type
            if front==TT_KEYWORDS["def"]:
                return self.parse_async_def()

            elif front==TT_KEYWORDS["for"]:
                print("enter for")
                self.advance()
                forloop=self.parse_for()
                actualnode=AsyncForLoopNode(forloop.iterable,forloop.body,forloop.var)
                return actualnode

            elif front==TT_KEYWORDS["with"]:
                self.advance()
                withnode=self.parse_with()
                actualnode= AsyncWithNode(withnode.name,withnode.as_,withnode.body)
                return actualnode


        elif self.current_token.type==TT_KEYWORDS["continue"]:
           self.advance()
           return ContinueNode()
        
        elif self.current_token.type==TT_KEYWORDS["pass"]:
           self.advance()
           return PassNode()
        
        elif self.current_token.type==TT_KEYWORDS["break"]:
           self.advance()
           return BreakNode()
        
        
        
        elif self.current_token.type == TT_IDENTIFIER:
            line=self.tokens[self.pos:self.tokens.index(Token(TT_NEWLINE),self.pos)]
            depth=0
            for tok in line:
                if tok.type in (TT_LPAREN, TT_LBRACE, TT_LBRACKET):
                    depth+=1
                elif tok.type in (TT_RPAREN, TT_RBRACE, TT_RBRACKET):
                    depth-=1
                if tok.type in (TT_ASSIGN,TT_ADD_COMPOUND, TT_MIN_COMPOUND, TT_MULTIPLY_COMPOUND, TT_DIV_COMPOUND, TT_POWER_COMPOUND, TT_FLOOR_DIV_COMPOUND) and depth==0:
                    return self.parse_assign()
            return self.parse_expression()
        return self.parse_expression()
    
        
    
    def parse_name(self, exc=tuple()):
        if self.current_token.type not in (TT_IDENTIFIER,TT_KEYWORDS["None"])+tuple(exc):
            raise InvalidSyntaxError(self.current_token, "Expected a identifier.")
        else:
            name=self.current_token.value
        self.advance()
        print("name:",name)
        return name
    
    def parse_lambda(self):
        self.advance()
        args=[]
        while self.current_token.type!=TT_COLON:
            if self.current_token.type==TT_COMMA:
                self.advance()
                continue
            args.append(self.parse_name())
        self.advance()
        expr=self.parse_expression()
        return LamdaNode(args,expr)

    def parse_raise(self):
        self.advance()
        err=self.parse_expression()
        return RaiseNode(err)
    
    def parse_assert(self):
        self.advance()
        expr=self.parse_expression((TT_COMMA,))
        mes=None
        if self.current_token is not None and self.current_token.type==TT_COMMA:
            self.advance()
            mes=self.parse_expression()
        return AssertNode(expr,mes)
    
    def parse_try(self):
        self.advance()
        self.advance()
        body=self.parse_block()
        excepts=[]
        finally_=None
        else_=None
        as_=None
        while self.current_token is not None and self.current_token.type==TT_KEYWORDS["except"]:
            self.advance()
            if self.current_token.type == TT_COLON:
                self.advance()
                except_body=self.parse_block()
                excepts.append(ExceptNode("BaseException",except_body,as_))
            else:
                error=self.parse_expression()
                if self.current_token.type==TT_KEYWORDS["as"]:
                    self.advance()
                    as_=self.parse_expression((TT_COLON,))                 
                self.advance()
                except_body=self.parse_block()
                excepts.append(ExceptNode(error,except_body,as_))
        if self.current_token is not None and self.current_token.type==TT_KEYWORDS["else"]:
            self.advance()
            self.advance()
            else_body=self.parse_block()
            else_=TryElseNode(else_body)
        if self.current_token is not None and self.current_token.type==TT_KEYWORDS["finally"]:
            self.advance()
            self.advance()
            finally_body=self.parse_block()
            finally_=FinallyNode(finally_body)
        if any([excepts,finally_,else_])!=True:
            raise InvalidSyntaxError(self.current_token,"Expected any one of except, finally, or else. ")
        return TryNode(body,excepts,else_,finally_)
    
    def parse_case(self):
        self.advance()
        val=self.parse_expression(end=(TT_COLON,)) if self.current_token.value !="_" else "_"
        if val=="_": 
            self.advance()
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':' after a case statement.")
        self.advance()
        body=self.parse_block()
        return CaseNode(val,body)

    def parse_match(self):
        self.advance()
        name=self.parse_expression((TT_COLON,))
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':' after a match statement.")
        self.advance()
        block=self.parse_block()
        cases=[]
        for node in block:
            if not isinstance(node, CaseNode):
                raise InvalidSyntaxError(self.current_token, "Expected only a case statement in a match statement. ")
            cases.append(node)
        default=cases[-1] if cases[-1].val=="_" else None
        cases=cases[:-1] if default is not None else cases
        return MatchNode(cases, name, default)

    def parse_with(self):
        self.advance()
        ctxm=self.parse_expression((TT_COLON,TT_KEYWORDS["as"]))
        as_=None
        if self.current_token.type==TT_KEYWORDS["as"]:
            self.advance()
            as_=self.parse_atom()
        self.advance()
        body=self.parse_block()
        return WithNode(ctxm, as_, body)  

    def parse_import(self):
        self.advance()
        name=self.parse_name()
        self.advance()
        func=self.parse_name(exc=[TT_MUL,TT_KEYWORDS["as"]])
        alias=None
        if func is None:
            func="ALL"
        if self.current_token.type==TT_KEYWORDS["as"]:
            self.advance()
            alias=self.parse_atom()
            self.advance()
        return FromImportNode(name,func,alias)

    def parse_class(self,decorator=[]):#[CLASS, IDENTIFIER:hello, LEFT_PARAN, IDENTIFIER:hello, RIGHT_PARAN, COLON, NEWLINE, INDENT, PASS, EXIT]
        self.advance()
        name=self.parse_name()
        self.global_class_name=name
        inheritence=[]
        
        if self.current_token.type==TT_LPAREN:
            self.advance()
            while self.current_token.type!=TT_RPAREN:
                if self.current_token.type==TT_COMMA:
                    self.advance()
                    continue
                if self.current_token.type != TT_IDENTIFIER:
                    raise InvalidSyntaxError(self.current_token, f"Expected class name. Pos:{self.pos}")
                class_=self.current_token.value
                inheritence.append(class_)
                self.advance()
            self.advance()


        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        
        block=self.parse_block(in_class=True)
        return ClassDefineNode(name,block,decorator,inheritence)

    def parse_if(self):
        self.advance()
        statement=self.parse_expression((TT_COLON, TT_NEWLINE, TT_DEDENT))
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        block=self.parse_block()
        elifs=[]
        else_=None
        while self.current_token.type==TT_KEYWORDS["elif"]:
            elifs.append(self.parse_elif())
        if self.current_token.type==TT_KEYWORDS["else"]:
            else_=self.parse_else()
        return IfConditionNode(statement, block, elifs, else_)
    
    def parse_unless(self):
        self.advance()
        statement=self.parse_expression((TT_COLON,))
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        statement=UnaryOpNode(TT_KEYWORDS["not"],statement)
        block=self.parse_block()
        return IfConditionNode(statement,block)

    def parse_forever(self):
        self.advance()
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        block=self.parse_block()
        return WhileLoopNode(BoolNode("TRUE"),block)

    def parse_until(self):
        self.advance()
        statement=self.parse_expression((TT_COLON,))
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        statement=UnaryOpNode(TT_KEYWORDS["not"],statement)
        block=self.parse_block()
        return WhileLoopNode(statement,block)

    def parse_raise_if(self):
        self.advance()
        expr=self.parse_expression((TT_COMMA,))
        error=None
        if self.current_token is not None and self.current_token.type==TT_COMMA:
            self.advance()
            error=self.parse_expression()
        return RaiseIfNode(expr,error)

    def parse_raise_if_not(self):
        self.advance()
        expr=self.parse_expression((TT_COMMA,))
        error=None
        if self.current_token is not None and self.current_token.type==TT_COMMA:
            self.advance()
            error=self.parse_expression()
        expr=UnaryOpNode(TT_KEYWORDS["not"],expr)
        return RaiseIfNode(expr,error)


    def parse_stop_if(self):
        self.advance()
        expr=self.parse_expression()
        return_=IfConditionNode(
            expr,
            [
                BreakNode()
            ]
        )
        return return_
    
    def parse_skip_if(self):
        self.advance()
        expr=self.parse_expression()
        return_=IfConditionNode(
            expr,
            [
                ContinueNode()
            ]
        )
        return return_

    def parse_repeat(self):
        self.advance()
        times=self.parse_expression((TT_COLON,))
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        block=self.parse_block()
        return_ = ForLoopNode(
            CallNode(
                VariableNameNode("range"),
                [
                    times
                ],
                {}
            ),
            block,
            VariableNameNode("i")
        )
        return return_

    def parse_elif(self):
        self.advance()
        statement=self.parse_expression((TT_COLON, TT_NEWLINE, TT_DEDENT))
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        block=self.parse_block()
        return ElifConditionNode(statement, block)

    def parse_else(self):
        self.advance()
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        block=self.parse_block()
        return ElseNode(block)
    
    def parse_for(self):
        self.advance()
        var=self.parse_name((TT_KEYWORDS["in"],TT_COMMA))
        if self.current_token.type==TT_COMMA:
            var=[var]

        while self.current_token is not None and self.current_token.type!=TT_KEYWORDS["in"]:
            if self.current_token.type==TT_COMMA:
                self.advance()
                continue
            var.append(self.parse_name((TT_COMMA,TT_COLON,TT_KEYWORDS["in"])))

        if self.current_token.type != TT_KEYWORDS["in"]:
            raise InvalidSyntaxError(self.current_token, "Expected 'in' in for-loop.")
        self.advance()

        iterable=self.parse_expression((TT_COLON, TT_NEWLINE, TT_DEDENT))
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        block=self.parse_block()
        return ForLoopNode(iterable, block, var)
    
    def parse_while(self):
        self.advance()
        statement=self.parse_expression((TT_COLON, TT_NEWLINE, TT_DEDENT))
        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")
        self.advance()
        block=self.parse_block()
        return WhileLoopNode(statement, block)

    def parse_return(self):
        self.advance()
        val=self.parse_expression()
        return ReturnNode(val)
    
    def parse_yield(self):
        from_=None
        val=None
        self.advance()
        if self.current_token.type == TT_KEYWORDS["from"]:
            self.advance()
            from_ = self.parse_expression()
        else:
            val=self.parse_expression((TT_KEYWORDS["from"], ))
        return YieldNode(val, from_)


    def parse_fstring(self):
        inside = self.current_token.value
        parts=[]
        for value in inside:
            if value["type"]=="string":
                parts.append(StringNode(value["value"]))
            else:
                expr=Parser(value["content"]).parse_expression()
                parts.append(FstringExpression(expr, value["grammer"]))
        return FormattedStringNode(parts)


    def parse_decorator(self):
        self.advance()
        decs=[self.parse_expression(end=(TT_MATRIX_MUL,))]
        while self.current_token is not None and self.current_token.type not in (TT_KEYWORDS["def"],TT_KEYWORDS["async"],TT_KEYWORDS["class"]):
            print("DEC TOKEN:", self.current_token)
            if self.current_token.type==TT_MATRIX_MUL:
                self.advance()
                continue
            elif self.current_token.type==TT_NEWLINE:
                self.advance()
                continue
            decs.append(self.parse_expression(end=(TT_MATRIX_MUL,)))

        if self.current_token.type==TT_KEYWORDS["def"]:
            return self.parse_def(decs)

        elif self.current_token.type==TT_KEYWORDS["class"]:
            return self.parse_class(decs)

        elif self.current_token.type==TT_KEYWORDS["async"]:
            front=self.peek().type
            if front==TT_KEYWORDS["def"]:
                print(self.current_token)
                return self.parse_async_def(decs)
                
            elif front==TT_KEYWORDS["for"]:
                self.advance()
                forloop=self.parse_for()
                actualnode=AsyncForLoopNode(forloop.iterable,forloop.body,forloop.var)
                return actualnode

            elif front==TT_KEYWORDS["with"]:
                self.advance()
                withnode=self.parse_with()
                actualnode= AsyncWithNode(withnode.name,withnode.as_,withnode.body)
                return actualnode

        else:
            raise InvalidSyntaxError(self.current_token.pos.char,f"Expected any one of 'async', 'def' or 'class' after a decorator. Got {self.current_token.type}. ")
               


    def parse_def(self,decorator=[]):#[DEF, IDENTIFIER:hello, LEFT_PARAN, IDENTIFIER:x, RIGHT_PARAN, FUNCTION TYPE, IDENTIFIER:int, COLON]
        self.advance()
        name=self.parse_name((TT_LPAREN,))
        if self.current_token.type!=TT_LPAREN:
            raise InvalidSyntaxError(self.current_token, "Expected a '(' after function. ")
        self.advance()
        args=[]
        a=1
        while self.current_token.type!=TT_RPAREN:
            a+=1
            print("number=",a)
            if self.current_token.type==TT_COMMA:
                self.advance()
                continue
            speciality=None
            if self.current_token.type != TT_IDENTIFIER:
                if self.current_token.type==TT_MUL:
                    self.advance()
                    speciality="args"
                elif self.current_token.type==TT_POWER:
                    self.advance()
                    speciality="kwargs"
                else:
                    raise InvalidSyntaxError(self.current_token, f"Expected argument name. Error at {self.current_token.pos}")
            argname=self.current_token.value
            argtype=None
            default=None
            self.advance()
            if self.current_token.type!=TT_COLON:
                if self.global_class_name and argname=="self":
                    argtype="Class_"
                else:
                    argtype="int"
            print("token",self.current_token)

            if self.current_token.type==TT_COLON:
                self.advance()
                argtype=self.current_token.value
                self.advance()

            if self.current_token.type==TT_ASSIGN:
                self.advance()
                default=self.parse_expression((TT_COMMA,))

            args.append(ArgNode(argname,argtype,default,speciality))
        self.advance()
        returntype=None
        infer_type=False
        if self.current_token.type!=TT_FUNCTION_TYPE: 
            infer_type=True
        else:
            self.advance()
            if self.current_token.type not in [TT_KEYWORDS["None"],TT_IDENTIFIER]:
                raise InvalidSyntaxError(self.current_token, "Invalid type annotation.")
            returntype=self.parse_name()

        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")

        self.advance()
        is_generator=False
        if not infer_type:
            block=self.parse_block()
        else:
            block,returntype,is_generator,return_types=self.parse_block(infer=True)

        if is_generator:
            return GeneratorNode(name,args,block,return_types,decorator)
        return FunctionDefineNode(name,args,block,returntype,decorator)
    
    def parse_async_def(self,decorator=[]):#[DEF, IDENTIFIER:hello, LEFT_PARAN, IDENTIFIER:x, RIGHT_PARAN, FUNCTION TYPE, IDENTIFIER:int, COLON]
        self.advance()
        self.advance()
        name=self.parse_name((TT_LPAREN,))

        if self.current_token.type!=TT_LPAREN:
                raise InvalidSyntaxError(self.current_token, "Expected a '(' after async function. ")

        self.advance()

        args=[]
        while self.current_token.type!=TT_RPAREN:
            if self.current_token.type==TT_COMMA:
                self.advance()
                continue
            if self.current_token.type != TT_IDENTIFIER:
                if self.current_token.type==TT_MUL:
                    self.advance()
                    speciality="args"
                elif self.current_token.type==TT_POWER:
                    self.advance()
                    speciality="kwargs"
                else:
                    raise InvalidSyntaxError(self.current_token, f"Expected argument name. Error at {self.current_token.pos}")
            argname=self.current_token.value
            argtype=None
            default=None
            self.advance()
            if self.current_token.type==TT_ASSIGN:
                self.advance()
                default=self.parse_expression((TT_COMMA,))

            if self.current_token.type!=TT_COLON:
                if self.global_class_name and argname=="self":
                    argtype="Class_"
                else:
                    argtype="int"
            if argtype is None:
                self.advance()
                argtype=self.current_token.value
                self.advance()
            args.append(ArgNode(argname,argtype,default))
        self.advance()
        returntype=None
        infer_type=False
        if self.current_token.type!=TT_FUNCTION_TYPE: 
            infer_type=True
        else:
            self.advance()
            if self.current_token.type not in [TT_KEYWORDS["None"],TT_IDENTIFIER]:
                raise InvalidSyntaxError(self.current_token, "Invalid type annotation.")
            returntype=self.parse_name()

        if self.current_token.type!=TT_COLON:
            raise InvalidSyntaxError(self.current_token, "Expected a ':'.")

        self.advance()

        if not infer_type:
            block=self.parse_block()
        else:
            block,returntype,is_generator,return_types=self.parse_block(infer=True)

        if is_generator:
            return AsyncGeneratorNode(name,args,block,return_types,decorator)
        return AsyncFunctionDefineNode(name,args,block,returntype,decorator)

    def parse_block(self, infer=False, in_class=False):
        if self.current_token is not None and self.current_token.type!=TT_NEWLINE:
            raise InvalidSyntaxError(self.current_token, "Expected a newline. ")
        
        self.advance()

        while self.current_token.type==TT_NEWLINE:
            self.advance()

        if self.current_token is not None and self.current_token.type!=TT_INDENT:
            raise InvalidSyntaxError(self.current_token, "Expected an indent. ")

        self.advance()
        block=[]
        inferred=None
        generator=False
        returntypes = []
        while self.current_token is not None and self.current_token.type!=TT_DEDENT:
            if self.current_token.type==TT_NEWLINE:
                self.advance()
                continue
            node = self.parse_statement()
            block.append(node)
            print("STUCK ON TOKEN:", self.current_token)
            if isinstance(node,ReturnNode) and infer:
                inferred=node.type_
                continue
            
            elif isinstance(node,YieldNode) and infer:
                generator=True
                returntypes.append(node.type_)
                continue
            
            elif infer:
                inferred="None"
            
        if self.current_token and self.current_token.type==TT_DEDENT:
            self.advance()
        
        if in_class:
            self.global_class_name=None
        
        if infer:
            return block, inferred, generator, returntypes

        return block


    def parse_ternary_if(self,left,end):
        self.advance()
        cond=self.parse_expression((TT_KEYWORDS["else"],))
        if self.current_token.type!=TT_KEYWORDS["else"]:
            raise InvalidSyntaxError(self.current_token.pos.char,f"Expected a 'else' after a ternary expression. Error at {self.current_token.pos}")
        self.advance()
        false_expr=self.parse_expression_no_comprehension(end)
        return TernaryOperationNode(cond,left,false_expr)

    def parse_comp_for(self,left):
        self.advance()
        while self.current_token.type!=TT_KEYWORDS["in"]:
            if self.current_token.type==TT_COMMA:
                self.advance()
                continue
            var=self.parse_expression((TT_KEYWORDS["in"],TT_COMMA))
        self.advance()
        iterable=self.parse_expression((TT_KEYWORDS["if"],))
        cond=None
        if self.current_token.type==TT_KEYWORDS["if"]:
            self.advance()
            cond = self.parse_expression()
        return ListComprehensionNode(iterable, var, left, cond)


    def parse_dict_comp(self, key, value):
        self.advance()
        while self.current_token.type!=TT_KEYWORDS["in"]:
            if self.current_token.type==TT_COMMA:
                self.advance()
                continue
            variable=self.parse_expression((TT_KEYWORDS["in"],TT_COMMA))
        self.advance()
        iterable=self.parse_expression((TT_KEYWORDS["if"],))
        cond=None
        if self.current_token.type==TT_KEYWORDS["if"]:
            self.advance()
            cond = self.parse_expression()
        return DictComprehensionNode(iterable,variable, key, value, cond)

    def parse_assign(self,end=(TT_COLON,TT_NEWLINE,TT_INDENT)):
        left=self.parse_expression(end=(TT_ASSIGN,TT_ADD_COMPOUND, TT_MIN_COMPOUND, TT_MULTIPLY_COMPOUND, TT_DIV_COMPOUND, TT_POWER_COMPOUND, TT_FLOOR_DIV_COMPOUND))
        if not isinstance(left,(VariableNameNode, SliceNode, GetItemNode, AttributeAccessNode, ImplicitTupleNode)):
            raise InvalidSyntaxError(self.current_token,f"Token {self.current_token} is not a valid variable name.")
        print("self",self.current_token)
        while self.current_token is not None and self.current_token.type in (TT_ASSIGN,TT_ADD_COMPOUND, TT_MIN_COMPOUND, TT_MULTIPLY_COMPOUND, TT_DIV_COMPOUND, TT_POWER_COMPOUND, TT_FLOOR_DIV_COMPOUND) and self.current_token.type not in end:
            print("left",left)
            op=self.current_token.type

            self.advance()

            namelength=len(left.items) if isinstance(left,ImplicitTupleNode) else 1

            value=self.parse_expression((TT_ASSIGN,))

            vallength=len(value.items) if isinstance(value,ImplicitTupleNode) else namelength

            if vallength!=namelength:
                raise InvalidSyntaxError(self.current_token,f"Cannot unpack {vallength} values into {namelength} variables. ")

            if op!=TT_ASSIGN:
                left=VariableCompAssignNode(left,value,op)

            if isinstance(left, GetItemNode):
                print("hello")
                left=SetItemNode(left, value)

            else:
                left=VariableAssignNode(left,value)
        
        return left

    
    def parse_expression(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        base=self.parse_comprehension(end)
        print(type(base))
        print(self.current_token)
        return base

    def parse_expression_no_comprehension(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        return self.parse_ternary(end)

    def parse_comprehension(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        left=self.parse_expression_no_comprehension((TT_KEYWORDS["for"],TT_KEYWORDS["async"])+end)
        while self.current_token is not None and self.current_token.type not in end and self.current_token.type == TT_KEYWORDS["for"]:
            left=self.parse_comp_for(left)
        if self.current_token is not None and self.current_token.type not in end and self.current_token.type == TT_KEYWORDS["async"] and self.peek().type==TT_KEYWORDS["for"]:
            self.advance()
            left = self.parse_comp_for(left)
            left = AsyncListComprehensionNode(left.iterable,left.variable,left.left, left.condition)
        return left if left else self.parse_logical()

    def parse_ternary(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        left=self.parse_logical(end+(TT_KEYWORDS["if"],))
        while self.current_token is not None and self.current_token.type not in end and self.current_token.type in (TT_KEYWORDS["if"],):
            left=self.parse_ternary_if(left,end)
        return left

    def parse_logical(self,end=(TT_COLON,TT_NEWLINE,TT_DEDENT)):
        if self.current_token.type==TT_KEYWORDS["lambda"]:
            return self.parse_lambda()
        left=self.parse_comparison(end)
        while self.current_token is not None and (self.current_token.type not in end) and self.current_token.type in (TT_KEYWORDS["or"],TT_KEYWORDS["and"]):
            op=self.current_token.type
            self.advance()

            right=self.parse_comparison(end)

            left=BiNopNode(left,op,right)
        return left
    
    def parse_comparison(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        left=self.parse_pipe_xor_addresive(end)
        while self.current_token is not None and (self.current_token.type not in end)  and self.current_token.type in (TT_EQ, TT_NEQ, TT_LT, TT_LTE, TT_GT, TT_GTE):
            op=self.current_token.type
            self.advance()

            right=self.parse_term(end)

            left=BiNopNode(left,op,right)
        return left
    

    def parse_pipe_xor_addresive(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        left=self.parse_shift(end)
        while self.current_token is not None and (self.current_token.type not in end)  and self.current_token.type in (TT_PIPE, TT_XOR, TT_ADDRESSIVE):
            op=self.current_token.type
            self.advance()

            right=self.parse_term(end)

            left=BiNopNode(left,op,right)
        return left


    def parse_shift(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        left=self.parse_term(end)
        while self.current_token is not None and (self.current_token.type not in end)  and self.current_token.type in (TT_SHIFTL,TT_SHIFTR):
            op=self.current_token.type
            self.advance()

            right=self.parse_term(end)

            left=BiNopNode(left,op,right)
        return left

    def parse_term(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        left=self.parse_factor(end)
        while self.current_token is not None and (self.current_token.type not in end)  and self.current_token.type in (TT_ADD,TT_MINUS):
            op=self.current_token.type
            self.advance()

            right=self.parse_factor(end)

            left=BiNopNode(left,op,right)
        return left
    
    def parse_factor(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        left=self.parse_power(end)
        while self.current_token is not None and (self.current_token.type not in end)  and self.current_token.type in (TT_MUL, TT_DIV, TT_FLOOR_DIV, TT_MATRIX_MUL, TT_MODULUS, TT_KEYWORDS["in"], TT_KEYWORDS["is"], TT_NOT_IS, TT_NOT_IN):
            op=self.current_token.type
            self.advance()

            right=self.parse_power(end)

            left=BiNopNode(left,op,right)
        return left
    
    def parse_power(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        left=self.parse_unary(end)
        while self.current_token is not None and (self.current_token.type not in end)  and self.current_token.type in (TT_POWER):
            op=self.current_token.type
            self.advance()

            right=self.parse_power(end)

            left=BiNopNode(left,op,right)
        return left
    
    def parse_unary(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        node=None
        if self.current_token.type==TT_KEYWORDS["await"]:
            self.advance()
            func=self.parse_unary()
            return AwaitNode(func)

        if self.current_token.type==TT_ADD:
            self.advance()
            return UnaryOpNode(TT_ADD, self.parse_unary())

        elif self.current_token.type==TT_MINUS:
            self.advance()
            return UnaryOpNode(TT_MINUS, self.parse_unary())

        elif self.current_token.type==TT_MUL:
            self.advance()
            return UnaryOpNode(TT_MUL, self.parse_unary())

        elif self.current_token.type==TT_POWER:
            self.advance()
            return UnaryOpNode(TT_POWER, self.parse_unary())

        elif self.current_token.type==TT_KEYWORDS["not"]:
            self.advance()
            return UnaryOpNode(TT_KEYWORDS["not"], self.parse_unary())
            
        return self.parse_call(end)
    
    def parse_call(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        base=self.parse_atom(end)
        while self.current_token is not None and (self.current_token.type not in end)  and self.current_token.type in (TT_LPAREN,TT_LBRACKET,TT_DOT):
            type_=self.current_token.type
            self.advance()
            if type_==TT_LPAREN:
                args=[]
                kwargs={}
                while self.current_token.type!=TT_RPAREN:
                    if self.current_token.type==TT_COMMA:
                        self.advance()
                        continue
                    elif (
                    self.current_token.type == TT_IDENTIFIER and
                    self.peek() is not None and
                    self.peek().type == TT_ASSIGN
                    ):
                        arg=self.current_token.value
                        self.advance()
                        self.advance()
                        value=self.parse_expression((TT_COMMA,))
                        kwargs[arg]=value
                        continue
                        print("CURRENT TOKEN: ", self.current_token)
                    else:
                        print("BEFORE:", self.current_token)
                        args.append(self.parse_expression((TT_COMMA,)))
                        print("AFTER:", self.current_token)
                base=CallNode(base,args,kwargs)
                self.advance()
            
            elif type_==TT_LBRACKET:
                val = None
                index=self.parse_expression((TT_COLON,TT_RBRACKET))
                if self.current_token.type==TT_COLON:
                    self.advance()
                    stop = None
                    if self.current_token.type not in (TT_COLON, TT_RBRACKET):stop = self.parse_expression((TT_COLON,TT_RBRACKET))
                    tick=None
                    if self.current_token.type == TT_COLON:
                        self.advance()
                        tick=self.parse_expression((TT_RBRACKET,))
                    val = SliceNode(base,index,stop,tick)
                    if self.current_token.type==TT_RBRACKET:
                        self.advance()
                    continue
                    
                self.advance()
                val=GetItemNode(base,index)
                if self.current_token is not None and self.current_token.type==TT_COMMA and self.current_token.type not in end:
                    val=[val]
                    while self.current_token is not None and self.current_token.type not in (TT_NEWLINE,) and self.current_token.type not in end:
                        if self.current_token.type == TT_COMMA:
                            self.advance()
                            continue
                        val.append(self.parse_expression((TT_COMMA,)))
                    base=ImplicitTupleNode(val)
                else:
                    base=val
            
            elif type_==TT_DOT:
                name=self.current_token.value
                self.advance()
                if self.current_token is not None and self.current_token.type==TT_LPAREN:
                    self.advance()
                    args=[]
                    kwargs={}

                    while self.current_token.type!=TT_RPAREN:
                        if self.current_token.type==TT_COMMA:
                            self.advance()
                            continue
                        elif (
                        self.current_token.type == TT_IDENTIFIER and
                        self.peek() is not None and
                        self.peek().type == TT_ASSIGN
                        ):
                            arg=self.current_token.value
                            self.advance()
                            self.advance()
                            value=self.parse_expression((TT_COMMA,))
                            kwargs[arg]=value
                            continue
                        else:
                            args.append(self.parse_expression((TT_RPAREN,TT_COMMA)))

                    if self.current_token is not None and self.current_token.type!=TT_RPAREN:
                        raise InvalidSyntaxError(self.current_token, "Expected a ')'.")
                    self.advance()
                    base=MethodCallNode(
                                        base,
                                        name,
                                        args,
                                        kwargs
                                    )
                else:
                    val=AttributeAccessNode(base,name)
                    if self.current_token is not None and self.current_token.type==TT_COMMA and self.current_token.type not in end:
                        val=[val]
                        while self.current_token is not None and self.current_token.type not in (TT_NEWLINE,) and self.current_token.type not in end:
                            if self.current_token.type == TT_COMMA:
                                self.advance()
                                continue
                            val.append(self.parse_expression((TT_COMMA,)))
                        base=ImplicitTupleNode(val)
                    else:
                        base=val
                
        return base
    
    def parse_atom(self,end=(TT_COLON, TT_NEWLINE, TT_DEDENT)):
        base=None
        print("ENTER parse_atom:", self.current_token)
        if self.current_token.type in (TT_NUMBER, TT_STRING,TTFSTRINGP,TT_KEYWORDS["None"]):
            if self.current_token.type==TT_NUMBER:
                val = NumberNode(self.current_token.value)

            elif self.current_token.type==TT_STRING:
                val = StringNode(self.current_token.value)

            elif self.current_token.type==TTFSTRINGP:
                val=self.parse_fstring()

            elif self.current_token.type==TT_KEYWORDS["None"]:
                val = NoneNode()

            self.advance()

            if self.current_token is not None and self.current_token.type==TT_COMMA and self.current_token.type not in end:
                val=[val]
                while self.current_token is not None and self.current_token.type not in (TT_NEWLINE,) and self.current_token.type not in end:
                    if self.current_token.type == TT_COMMA:
                        self.advance()
                        continue
                    val.append(self.parse_expression((TT_COMMA,)))
                base=ImplicitTupleNode(val)
            else:
                base=val

        elif self.current_token.type in (TT_KEYWORDS["True"], TT_KEYWORDS["False"]):
            base=BoolNode(self.current_token.type)
            self.advance()   
                    

        elif self.current_token.type==TT_LPAREN:
            self.advance()
            inside=self.parse_expression((TT_RPAREN, TT_COMMA))
            if self.current_token.type==TT_COMMA:
                inside=[inside]
                while self.current_token.type!=TT_RPAREN:
                    if self.current_token.type==TT_COMMA:
                        self.advance()
                        continue
                    inside.append(self.parse_expression((TT_COMMA,TT_RPAREN)))

                base=TupleNode(inside)
            else:
                if self.current_token.type !=TT_RPAREN :
                    raise InvalidSyntaxError(self.current_token, f"Expected a ')' after '('. Pos:{self.pos}")
                if isinstance(inside, ListComprehensionNode):
                    base=GeneratorComprehensionNode(inside.iterable, inside.variable, inside.left, inside.condition)
                elif isinstance(inside, AsyncListComprehensionNode):
                    base=AsyncGeneratorComprehensionNode(inside.iterable, inside.variable, inside.left, inside.condition)
                else:
                    base=inside
            self.advance()
            
        elif self.current_token.type==TT_LBRACKET:
            self.advance()
            vals=[]
            while self.current_token.type!=TT_RBRACKET:
                if self.current_token.type==TT_COMMA:
                    self.advance()
                    continue
                vals.append(self.parse_expression((TT_RBRACKET,TT_COMMA)))
            self.advance()
            print("self.current_token",self.current_token)
            base=ListNode(vals)

        elif self.current_token.type==TT_LBRACE:
            self.advance()
            vals={}
            comp=False
            while self.current_token.type!=TT_RBRACE:
                if self.current_token.type==TT_COMMA:
                    self.advance()
                    continue

                key=self.parse_expression(end=(TT_COMMA,TT_COLON))
                if self.current_token.type==TT_COLON:
                    self.advance()
                    value = self.parse_expression(end=(TT_COMMA,TT_COLON,TT_KEYWORDS["for"]))
                    if self.current_token.type==TT_KEYWORDS["for"]:
                        base = self.parse_dict_comp(key,value)
                        comp=True
                        break
                    elif self.current_token.type not in end and self.current_token.type == TT_KEYWORDS["async"] and self.peek().type==TT_KEYWORDS["for"]:
                        self.advance()
                        base = self.parse_dict_comp(key,value)
                        base = AsyncDictComprehensionNode(base.iterable,base.variable, base.key,base.value,base.condition)
                        comp=True
                        break
                else:
                    if self.current_token.type!=TT_RBRACE: raise InvalidSyntaxError(self.current_token, "Expected a colon after each key in the dictionary.")
                    else: 
                        self.advance()
                        break
                vals[key]=value

                    
            self.advance()
            if not comp:
                base=DictNode(vals)
       
        elif self.current_token.type==TT_IDENTIFIER:
            val=VariableNameNode(self.current_token.value)
            self.advance()
            if self.current_token is not None and self.current_token.type==TT_COMMA and self.current_token.type not in end:
                val=[val]
                while self.current_token is not None and self.current_token.type not in (TT_NEWLINE,) and self.current_token.type not in end:
                    if self.current_token.type == TT_COMMA:
                        self.advance()
                        continue
                    val.append(self.parse_expression((TT_COMMA,)))
                base=ImplicitTupleNode(val)
            else:
                base=val
        elif self.current_token.type in end:
            pass
        
        elif self.current_token.type==TT_COMMENT:
            pass

        else:
            raise InvalidSyntaxError(self.current_token, f"Error at {str(self.current_token.pos)}")
        
        return base
            

        
    

    
    
    

        
        
        

