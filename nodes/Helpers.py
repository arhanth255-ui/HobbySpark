class Node:
    def __init__(self):
        pass
    def to_json(self):
        dic={"NodeType":self.__class__.__name__}|self.__dict__
        return dic
    def pretty(self,indent=0):
        pad = "    " * indent

        result = f"{pad}{self.__class__.__name__}:\n"

        for name, value in self.__dict__.items():

            if isinstance(value, Node):
                result += f"{pad}{name}:\n"
                result += value.pretty(indent + 1)

            elif isinstance(value, list):
                result += f"{pad}{name}:\n"
                for item in value:
                    if isinstance(item, Node):
                        result += item.pretty(indent + 1)
                    else:
                        result += f"{pad}   {item}\n"

            else:
                result += f"{pad}{name} = {value}\n"

        return result
    
    def __repr__(self):
        return self.pretty()


