import string
#######################################################
#Char errors
#######################################################
class InvalidCharacterError(Exception):
    def __init__(self, char, extra):
        mes=f"Invalid character {char!r}."+extra
        super().__init__(mes)


#######################################################
#Token types
#######################################################
TT_IDENTIFIER="IDENTIFIER"
TT_NUMBER="NUMBER"
TT_STRING="STRING"
TTFSTRINGP="FSTRING (GUARENTEED PTSD FOR LEXER)"

TT_ASSIGN="ASSIGN"

TT_ADD="ADD"
TT_ADD_COMPOUND="ADD_COMPOUND"

TT_MINUS="MINUS"
TT_MIN_COMPOUND="MIN_COMPOUND"

TT_MUL="MULTILPY"
TT_MULTIPLY_COMPOUND="MULTIPLY_COMPOUND"

TT_DIV="DIVISION"
TT_DIV_COMPOUND="DIV_COMPOUND"


TT_FLOOR_DIV="FLOOR_DIVISION"
TT_FLOOR_DIV_COMPOUND="FLOOR_DIV_COMPOUND"

TT_POWER="POWER"
TT_POWER_COMPOUND="POWER_COMPOUND"


TT_MODULUS="MODULUS"
TT_MODULUS_COMPOUND="MODULUS_COMPOUND"


TT_LPAREN="LEFT_PARAN"
TT_RPAREN="RIGHT_PARAN"

TT_LBRACE="LEFT_BRACE"
TT_RBRACE="RIGHT_BRACE"

TT_COMMA="COMMA"
TT_COLON="COLON"
TT_DOT="DOT"

TT_LBRACKET="LEFT_BRACKET"
TT_RBRACKET="RIGHT_BRACKET"

TT_EQ="EQUALS"
TT_NEQ="NOT_EQUALS"

TT_LT="LESS_THAN"
TT_GT="GREATER_THAN"

TT_LTE="LESS_THAN_OR_EQUALS"
TT_GTE="GREATER_THAN_OR_EQUALS"

TT_INDENT="INDENT"
TT_DEDENT="EXIT"

TT_NEWLINE="NEWLINE"
TT_COMMENT="COMMENT"
TT_EOF="END_OF_FILE"

TT_FUNCTION_TYPE="FUNCTION TYPE"

TT_MATRIX_MUL="MATRIX_MUL OR DECORATOR"

TT_SHIFTL="SHIFT_LEFT"
TT_SHIFTR="SHIFT_RIGHT"

TT_PIPE="PIPE"
TT_XOR="XOR"
TT_ADDRESSIVE="ADDRESSIVE(&)"

TT_NOT_IN="NOT_IN"
TT_NOT_IS="NOT_IS"

TT_KEYWORDS={
    "if":"IF",
    "elif":"ELIF",
    "else":"ELSE",
    "while":"WHILE",
    "for":"FOR",
    "break":"BREAK",
    "continue":"CONTINUE",
    "return":"RETURN",
    "def":"DEF",
    "class":"CLASS",
    "import":"IMPORT",
    "from":"FROM",
    "True":"TRUE",
    "False":"FALSE",
    "None":"NOTHING well er.... sort of. ",
    "pass":"PASS",
    "and":"AND",
    "or":"OR",
    "not":"NOT",
    "in":"IN",
    "is":"IS",
    "lambda":"LAMBDA",
    "assert":"ASSERT",
    "try":"TRY",
    "except":"EXCEPT",
    "finally":"FINALLY",
    "raise":"RAISE",
    "unless":"UNLESS",
    "forever":"FOREVER",
    "raise_if":"RAISE_IF",
    "until":"UNTIL",
    "repeat":"REPEAT",
    "stop_if":"STOP_IF",
    "skip_if":"SKIP_IF",
    "raise_ifnot":"RAISE_IF_NOT",
    "as":"AS",
    "with":"WITH",
    "global":"GLOBAL",
    "yield":"YIELD",
    "async":"ASYNC",
    "await":"AWAIT",
    "match":"MATCH",
    "case":"CASE (It is the last feature. OHHHHH no!!!!!)"
}

#######################################################
#Position class
#######################################################
class Position:
    def __init__(self, line, char, char_pos):
        self.line=line
        self.char=char
        self.char_pos=char_pos
    def copy(self):
        return Position(self.line, self.char, self.char_pos)
    def __str__(self):
        return f"Position line: {self.line}, character: {self.char} and character position: {self.char_pos}"


#######################################################
#Token class
#######################################################
class Token:
    def __init__(self, type, value=None, pos:Position=None):
        self.type=type
        self.value=value
        self.pos=pos

    def __repr__(self):
        if self.value is not None: return f"{self.type}:{self.value}"
        return f"{self.type}"
    
    def __eq__(self, value):
        return self.type==value.type and self.value==value.value
    
#######################################################
#Lexer
#######################################################
class Lexer:
    def __init__(self, text:str):
        self.text=text
        self.current_char=None
        self.current_pos=Position(0,self.text[0],-1)
        self.paran_count=0
        self.did_a_backflip=False
        self.advance()

    def advance(self):
        self.current_pos.char_pos+=1
        if self.current_pos.char_pos<len(self.text):
            self.current_char=self.text[self.current_pos.char_pos]
            self.current_pos.char=self.current_char
        else:
            self.current_char=None
            self.current_pos.char=self.current_char
    
    def peek(self, needed=1):
        text=""
        for i in range(needed):
            if len(self.text)<=i+self.current_pos.char_pos+1:
                break
            text+=self.text[self.current_pos.char_pos+i+1] if len(self.text)>self.current_pos.char_pos+i+1 else ""
        return text
    
    def evaluate(self):
        self.tokens=[]
        indent=[0]

        while self.current_char is not None:
            if self.current_char=="\n":
                self.current_pos.line+=1
                if self.paran_count>0 or self.did_a_backflip:
                    self.advance()
                    print("ENETR")
                    continue

                self.tokens.append(Token(TT_NEWLINE,pos=self.current_pos.copy()))
                self.advance()
                spaces=0
                while self.current_char==" " or self.current_char=="\t":
                    if self.current_char=="\t":
                        spaces+=4
                    else:
                        spaces+=1
                    self.advance()
                
                if self.current_char == "\n":
                    continue

                spaces=spaces//4
                if indent[-1]<spaces:
                    indent.append(spaces)
                    self.tokens.append(Token(TT_INDENT,pos=self.current_pos.copy()))
                if indent[-1]>spaces:
                    while indent[-1]>spaces:
                        indent.pop()
                        self.tokens.append(Token(TT_DEDENT,pos=self.current_pos.copy()))

            elif self.current_char==" " or self.current_char=="\t":
                self.advance()
                continue

            elif self.current_char in ("'",'"','“', '‘'):
                self.tokens.append(self.handle_string())
            
            elif self.peek() in ("'",'"','“', '‘') and self.current_char == "f":
                self.tokens.append(self.handle_PTSDfstring())

            elif self.current_char=="#":
                self.handle_comment()

            elif self.current_char.isalpha() or self.current_char=="_":
                self.tokens.append(self.handle_char())

            elif self.current_char.isdigit():
                self.tokens.append(self.handle_number())

            elif self.current_char=="=":
                self.tokens.append(self.handle_equals())
            
            elif self.current_char=="!":
                self.tokens.append(self.handle_not())
            
            elif self.current_char==">":
                self.tokens.append(self.handle_greater())
            
            elif self.current_char=="<":
                self.tokens.append(self.handle_lesser())
            
            elif self.current_char=="/" or self.current_char=="*":
                self.tokens.append(self.handle_special(self.current_char))
            
            elif self.current_char=="-":
                self.tokens.append(self.handle_minus())
            
            elif self.current_char=="+":
                self.tokens.append(self.handle_add())
            
            elif self.current_char=="%":
                self.tokens.append(self.handle_modulus())
                self.advance()
            
            elif self.current_char=="(":
                self.tokens.append(Token(TT_LPAREN,pos=self.current_pos.copy()))
                self.advance()
                self.paran_count+=1
            
            elif self.current_char==")":
                self.tokens.append(Token(TT_RPAREN,pos=self.current_pos.copy()))
                self.advance()
                self.paran_count-=1
            
            elif self.current_char=="[":
                self.tokens.append(Token(TT_LBRACKET,pos=self.current_pos.copy()))
                self.advance()
                self.paran_count+=1
            
            elif self.current_char=="]":
                self.tokens.append(Token(TT_RBRACKET,pos=self.current_pos.copy()))
                self.advance()
                self.paran_count-=1

            elif self.current_char=="{":
                self.tokens.append(Token(TT_LBRACE,pos=self.current_pos.copy()))
                self.advance()
                self.paran_count+=1
            
            elif self.current_char=="}":
                self.tokens.append(Token(TT_RBRACE,pos=self.current_pos.copy()))
                self.advance()
                self.paran_count-=1
            
            elif self.current_char==":":
                self.tokens.append(Token(TT_COLON,pos=self.current_pos.copy()))
                self.advance()
            
            elif self.current_char==",":
                self.tokens.append(Token(TT_COMMA,pos=self.current_pos.copy()))
                self.advance()
            
            elif self.current_char==".":
                self.tokens.append(Token(TT_DOT,pos=self.current_pos.copy()))
                self.advance()
            
            elif self.current_char=="@":
                self.tokens.append(Token(TT_MATRIX_MUL,pos=self.current_pos.copy()))
                self.advance()

            elif self.current_char=="&":
                self.tokens.append(Token(TT_ADDRESSIVE,pos=self.current_pos.copy()))
                self.advance()

            elif self.current_char=="|":
                self.tokens.append(Token(TT_PIPE,pos=self.current_pos.copy()))
                self.advance()
                
            elif self.current_char=="^":
                self.tokens.append(Token(TT_XOR,pos=self.current_pos.copy()))
                self.advance()
                     
            elif self.current_char=="\\":
                self.did_a_backflip=True
                self.advance()
                continue

            elif self.current_char==" ":
                self.advance()
                continue

            elif self.current_char==";":
                self.tokens.append(Token(TT_NEWLINE,pos=self.current_pos.copy()))
                self.advance()         
                
            else:
                raise InvalidCharacterError(self.current_char,f"Expected a valid character, not {self.current_char!r}. Error at {self.current_pos}. TABS: {self.paran_count}")
        
        for ind in indent[::-1]:
            if ind!=0:
                indent.pop()
                self.tokens.append(Token(TT_DEDENT,pos=self.current_pos.copy()))
            else:
                break
            


        self.tokens.append(Token(TT_NEWLINE,pos=self.current_pos.copy()))
        return self.tokens
            

                

    def handle_char(self):
        word=""

        while(not self.current_char is None) and self.current_char.isalnum() or self.current_char=="_":
            word+=self.current_char
            self.advance()
        if word in TT_KEYWORDS:
            if word in ("not", "is"):
                return self.handle_in_is(word)
            else: 
                return Token(TT_KEYWORDS[word],pos=self.current_pos.copy())
        else:
                                
                return Token(TT_IDENTIFIER,word,pos=self.current_pos.copy())
        
    def handle_number(self):
        number=""
        dot="."
        dotcount=0
        hex_ = False
        while not self.current_char is None and (self.current_char.isdigit() or self.current_char==dot or self.current_char.isalpha()):
            if self.current_char==dot:
                dotcount+=1
            
            if dotcount>1:
                dot=""
            elif self.current_char.isalpha():
                if hex_:
                    raise InvalidCharacterError(self.current_char, f"A letter in a hex muts come before a number. Error at {str(self.current_pos)}")
                number+=self.current_char
                self.advance()
                hex_ = True 
            else:
                number+=self.current_char
                self.advance()
            
            
        return Token(TT_NUMBER,int(number) if number.isdigit() else number,pos=self.current_pos.copy())
    
    def handle_equals(self):
        self.advance()
        if self.current_char=="=":
            self.advance()
            return Token(TT_EQ,pos=self.current_pos.copy())
        else:
            return Token(TT_ASSIGN,pos=self.current_pos.copy())
    
    def handle_not(self):
        self.advance()
        if self.current_char=="=":
            self.advance()
            return Token(TT_NEQ,pos=self.current_pos.copy())
        else:
            raise InvalidCharacterError(self.current_char,f"Expected a '=' after '!'")

    def handle_greater(self):
        self.advance()
        if self.current_char=="=":
            self.advance()
            return Token(TT_GTE,pos=self.current_pos.copy())

        elif self.current_char==">":
            self.advance()
            return Token(TT_SHIFTR,pos=self.current_pos.copy())

        else:
            return Token(TT_GT,pos=self.current_pos.copy())
        
    def handle_lesser(self):
        self.advance()
        if self.current_char=="=":
            self.advance()
            return Token(TT_LTE,pos=self.current_pos.copy())

        elif self.current_char=="<":
            self.advance()
            return Token(TT_SHIFTL,pos=self.current_pos.copy())

        else:
            return Token(TT_LT,pos=self.current_pos.copy())
        
    def handle_special(self,char):
        self.advance()
        if self.current_char==char:
            self.advance()
            if self.current_char=="=":
                return Token(TT_POWER_COMPOUND if char=="*" else TT_FLOOR_DIV_COMPOUND,pos=self.current_pos.copy())
            return Token(TT_POWER if char=="*" else TT_FLOOR_DIV,pos=self.current_pos.copy())
        else:
            if self.current_char=="=":
                return Token(TT_MULTIPLY_COMPOUND if char=="*" else TT_DIV_COMPOUND,pos=self.current_pos.copy())
            return Token(TT_MUL if char=="*" else TT_DIV,pos=self.current_pos.copy())

    def handle_string(self):
        quote_type=self.current_char
        text=""
        self.advance()
        while(not self.current_char is None) and (self.current_char in string.printable) and self.current_char!=quote_type:
            text+=self.current_char
            self.advance()
        self.advance()
        if text.startswith("I am a Dev at harry potter."):
            return Token(TT_STRING, text+"\nYou found the cure for HP!!!!!!"*int(text[-1] if text[-1].isdigit() else 3)+ "\nEASTER EGG!!!",pos=self.current_pos.copy())
        return Token(TT_STRING, text,pos=self.current_pos.copy())
    

    def handle_PTSDfstring(self):   
        textparts=[]
        bracecount=0
        content=""
        grammmer_part=" "
        stringcontent=[]
        self.advance()
        quote_type=self.current_char
        self.advance()
        
        while self.current_char is not None and self.current_char in string.printable and self.current_char!=quote_type:
            if self.current_char=="{":
                if self.peek()=="{":
                    self.advance()
                    self.advance()
                    stringcontent.append(
                            {
                                "type":"string",
                                "value":"{"
                            }
                        )
                    continue
                bracecount+=1
                self.advance()
                content=""
                grammmer_part=" "
                while True:
                    if self.current_char=="}" and bracecount==1:
                        bracecount-=1
                        self.advance()
                        break
                    if self.current_char=="}":
                        bracecount-=1
                        self.advance()

                    if self.current_char==":" and bracecount==1:
                        while self.current_char not in ("}",quote_type):
                            grammmer_part+=self.current_char if self.current_char is not None else ""
                            self.advance()
                        self.advance()
                        break
                    content+=self.current_char
                    self.advance()
                content=Lexer(content).evaluate()
                stringcontent.append({
                                        "type":"expr",
                                        "content":content,
                                        "grammer":grammmer_part
                                    })
                
                continue
            if self.current_char=="}" and self.peek()=="}":
                stringcontent.append(
                            {
                                "type":"string",
                                "value":"}"
                            }
                        )
                self.advance()
                self.advance()
                continue
            stringcontent.append(self.current_char)
            self.advance()
        cur_str=""
        for part in stringcontent:
            if isinstance(part,str):
                cur_str+=part
            else:
                if cur_str:
                    print("cur_str ",cur_str)
                    textparts.append(
                            {
                                "type":"string",
                                "value":cur_str
                            }
                        )
                    cur_str=""

                textparts.append(part)

        if cur_str!="" or cur_str not in quote_type:
            textparts.append({
                "type":"string",
                "value":cur_str
                })
        self.advance()
        print("TEXTPARTS:", textparts)
        return Token(TTFSTRINGP, textparts,pos=self.current_pos.copy())




    def handle_comment(self):
        text=""
        self.advance()
        while(not self.current_char is None) and (self.current_char in string.printable and self.current_char!="\n"):
            text+=self.current_char
            self.advance()
        self.current_pos.line+=1
        self.advance()

    
    def handle_minus(self):
        self.advance()
        if self.current_char==">":
            self.advance()
            return Token(TT_FUNCTION_TYPE,pos=self.current_pos.copy())
        elif self.current_char=="=":
            return Token(TT_MIN_COMPOUND,pos=self.current_pos.copy())
        else:
            return Token(TT_MINUS,pos=self.current_pos.copy())
    def handle_add(self):
        self.advance()
        if self.current_char=="=":
            self.advance()
            return Token(TT_ADD_COMPOUND,pos=self.current_pos.copy())
        return Token(TT_ADD,pos=self.current_pos.copy())
    
    def handle_modulus(self):
        self.advance()
        if self.current_char=="=":
            self.advance()
            return Token(TT_MODULUS_COMPOUND,pos=self.current_pos.copy())
        return Token(TT_MODULUS,pos=self.current_pos.copy())
    def handle_in_is(self,word):
        token=None
        if word=="not":
            if self.current_char is not None and self.current_char.isalpha() or self.current_char in ("_"," "):
                next_word=self.peek(2)
                print("word =", repr(next_word))
                if next_word is not None and next_word=="in":
                    self.advance()
                    self.handle_char()
                    token = Token(TT_NOT_IN,pos=self.current_pos.copy())
                else:
                    token = Token(TT_KEYWORDS["not"],pos=self.current_pos.copy())
            else:
                token = Token(TT_KEYWORDS["not"],pos=self.current_pos.copy())
        else:
            if self.current_char is not None and self.current_char.isalpha() or self.current_char in ("_"," "):
                next_word=self.peek(3)

                if next_word is not None and next_word=="not":
                    self.advance()
                    self.handle_char()
                    token = Token(TT_NOT_IS,pos=self.current_pos.copy())
                else:
                    token = Token(TT_KEYWORDS["is"],pos=self.current_pos.copy())
            else:
                token = Token(TT_KEYWORDS["is"],pos=self.current_pos.copy())
        
        return token
    








