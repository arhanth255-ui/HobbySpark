from .Helpers import *
class FromImportNode(Node):
    def __init__(self,module,func,as_=None):
        self.module=module
        self.func=func
        self.as_=as_

class ImportNode(Node):
    def __init__(self,module, as_=None):
        self.module=module
        self.as_=as_
