from ParamSelect import Param

class ParamBasic(Param):
    """Basic type, if you dont want features, you could choose this one."""

    def __init__(self, name, type, default=None):
        self.name = name
        self.type = type
        self.default = default

    @property
    def text(self):
        return "Basic parameter of type " + str(self.type)

    def okey(self, value):
        return type(value) is self.type

class ParamNumber(Param):
    """List of ranges parameter. Also has a minimum and maximum.
    Note that it has fancy bells, but hardly worth also having the less
     complicated ones.
    """
    def __init__(self, name, default=0, type=None, min=None, max=None, opts=None):
        self.name    = name
        self.default = default
        self.type    = type
        self.min     = min
        self.max     = max
        if not (self.min is None or self.max is None):
            assert self.min <=  self.max
        self.opts    = opts  # Rising list of numbers < all index 0  otherwise more.

    def okey(self, value):
        tp = type(value)
        if self.type is None:
            if not (tp is int or tp is float):
                return False
        elif self.type == tp:
            return False
        # Either wrong type or out of the range
        if not self.min is None and value < self.min:
            return False
        if not self.max is None and value > self.max:
            return False
        return True

    def _parse(self, string):
        return int(string) if (self.type == int) else float(string)

    def choose(self, value=None):
        if value is None:
            value = self.default

        if type(self.opts) is list:
            for i in range(len(self.opts)):
                if self.opts[i] > value:
                    return (i, value)
            return (0,value)
        elif type(self.opts) is float or type(self.opts) is int:
            return (int(value / self.opts), value)
        elif self.opts is None:
            return (-1,value)

    def seek_correct(self, value, mode=None):
        if not self.min is None:
            value = max(self.min, value)
        if not self.max is None:
            value = min(self.max, value)
        if self.type is int:
            value = int(value)
        return value

def ParamInt(name, default=0, min=None, max=None,opts=None):
    return ParamNumber(name, default=default, type=int,
                       min=min, max=max, opts=opts)

class ParamString(Param):
    def okey(self, value):
        return type(value) is str

    def _parse(self, string):  # Thats all it does above ParamBasic.
        return string

class ParamListBox(Param):

    def __init__(self, name, list, default=None):
        self.name = name
        self.list = list
        self.default = default

    def find(value):
        for i in range(len(self.list)):
            if list[i] == value:
                return i
        return None

    def okey(self, value):
        return self.find(value) is None

    def choose(self, value=None):
        if value is None:
            value = self.default
        i = self.find(value)
        return ((-1, value) if (i is None) else (i,list[i]))

    def tell(self):
        text = ("options:" if (self.text == "") else self.text)
        ret = (text + ("" if (self.default is None) else "(" + self.default + ")"))
        for el in self.list:
            ret += el
        return ret
    
    def seek_correct(self, value, mode=None):
        if mode is 'closest':  # Use  closest value.(Only when that makes sense, of course)
            d = abs(value - list[0])
            got = list[0]
            for el in self.list[1:]:
                if abs(value - el) < d:
                    d = abs(value - el)
                    got = el
            return got
        return None

class ParamCheckResult(Param):
    def __init__(self, name, list, default=None, fun=None):
        self.name = name
        self.list = list
        self.default = default
        self.fun = fun

    def okey(self, value):
        if self.fun is None:
            return False
        else:
            return self.fun(value)
