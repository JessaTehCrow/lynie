import ast

#Enable this to see all the steps the program takes to get it's data
debug = 1

# Data to easily fetch their string equivalent
opers = {
    ast.Add : "+",
    ast.Sub : "-",
    ast.Mult : "*",
    ast.Div : "/",
    ast.FloorDiv : "//",
    ast.Pow : "**",
    ast.Mod : "%",
    ast.BitXor : "^",
    ast.LShift : "<<",
    ast.RShift : ">>",
    ast.BitAnd : "&",
    ast.BitOr : "|",

}

bool_opers = {
    ast.Eq : "==",
    ast.NotEq : "!=",
    ast.Lt : "<",
    ast.LtE : "<=",
    ast.Gt : ">",
    ast.GtE : ">=",
    ast.Is : " is ",
    ast.IsNot : " is not ",
    ast.In : " in ",
    ast.NotIn : " not in ",
    ast.Not : " not ",
    ast.Invert : "~"
}

imports = {}
local_vars = {}

# get value as a string. Uses raw to get a repr for assignments, not used if a function will use the string for something else
def _get_constant(cons:ast.Constant,raw=False): 
    out = cons.value if raw else repr(cons.value)
    if isinstance(out,str):
        out = out.replace("{","{{").replace("}","}}")
    return out

def _get_name(name:ast.Name,raw=False):
    name = name.id
    if name in imports:
        name = imports[name]

    return name

def _get_subscript(subscript:ast.Subscript,raw=False):
    name,slice = _get_values(subscript.value,subscript.slice)
    return f"{name}[{slice}]"

def _get_index(slice:ast.Index,raw=False):
    return _get_values(slice.value,raw=raw)

#Fetch data for function call
def _get_call(call:ast.Call,raw=False):
    args = _get_values(*call.args)
    attr = _get_values(call.func)
    #Get module and subfunction name or just function name
    mname,sub = [_get_values(call.func.value),call.func.attr] if isinstance(call.func,ast.Attribute) else [attr,None]

    #Check if this function or module is in the imports dict. If it is, return the one-line equivalent of it
    if mname in imports:
        attr = imports[mname]+('.'+sub if sub else "")

    args = args if isinstance(args,list) else [args]
    return f"{attr}({','.join(args)})"

def _get_tuple(tuple:ast.Tuple,raw=False):
    #Get all values from tuple, and return raw
    out = _get_values(*tuple.elts,raw=True)
    if raw: return out

    #get all values from tuple and return repr
    out = _get_values(*tuple.elts)
    return f"({','.join(out)})"

def _get_dict(dict:ast.Dict,raw=False):
    out = {}
    #Get all values from dict, and return raw
    for key,val in zip(dict.keys,dict.values):
        out[_get_values(key,raw=True)] = _get_values(val,raw=True)
    if raw: return out

    #Get all values from dict, and return repr
    out = []
    for i,x in zip(dict.keys,dict.values):
        out.append(f"{_get_values(i)}:{_get_values(x)}")
    return f"{{{','.join(out)}}}"

def _get_list(List:ast.List,raw=False):
    #Get all values from list, and return raw
    out = _get_values(*List.elts,raw=True)
    if raw: return out

    #Get all values from list, and return repr
    out = _get_values(*List.elts)
    out = out if isinstance(out,list) else [out]

    return f"[{','.join(out)}]"

def _get_binop(body:ast.BinOp,raw=False):
    left = _get_values(body.left)
    oper = opers[type(body.op)]

    #Right may be recursion if there's more than one operation. (aka: 1+3/5*3 will be recursive)
    right = _get_values(body.right)

    return f"{left}{oper}{right}"

def _get_attr(body:ast.Attribute,raw=False):
    sub = body.attr
    value = _get_values(body.value)
    return f"{value}.{sub}"

def _get_namedexpr(body:ast.NamedExpr,raw=False):
    target = (_get_values(body.target))
    value = (_get_values(body.value))
    return f"{target}:={value}"

def _get_starred(body:ast.Starred,raw=False):
    return "*"+_get_values(body.value)

def _get_slice(body:ast.Slice,raw=False):
    #Get maniuplation slice, eg: string[1:] or string[1:-1]
    out = ["",":",""]
    if body.lower:
        out[0] = _get_values(body.lower)
    if body.upper:
        out[2] = _get_values(body.upper)
    return ''.join(out)

def _get_lambda(body:ast.Lambda,raw=False):
    #just setup the lambda
    args = (_get_values(body.args))
    code = (_get_values(body.body))
    return f"lambda {args}: {code}"

def _get_args(body:ast.arguments,raw=False):
    #Too lazy to explain all of this. But it just gets the arguments of a function and stuff
    normal = [[arg.arg,arg.annotation.id if hasattr(arg.annotation,'id') else None, _get_default(body.defaults,arg)] for arg in body.args]
    varg = body.vararg
    kwarg = body.kwarg

    if varg:
        normal.append(["*"+varg.arg,(varg.annotation.id if hasattr(varg.annotation,'id') else None),None])
    if kwarg:
        normal.append(['**'+kwarg.arg,(kwarg.annotation.id if hasattr(kwarg.annotation,'id') else None),None])

    out = []
    for name,_,value in normal:
        default = ("="+repr(value)) if value!=None else ""
        out.append(f"{name}{default}")
    return ','.join(out)

def _get_boolop(body:ast.BoolOp,raw=False):
    devide_operators = {
        ast.And : " and ",
        ast.Or : " or " 
    }
    oper = devide_operators[type(body.op)]
    vals = _get_values(*body.values)
    return oper.join(vals)

def _get_compare(body:ast.Compare,raw=False):
    left = _get_values(body.left)
    oper = bool_opers[type(body.ops[0])]
    #Compatators may be recursive. (aka 2<3 and 5<2 or 43<2 will be recursive)
    compatators = _get_values(*body.comparators)
    return (f"{left}{oper}{compatators}")

def _get_expr(body:ast.Expr,raw=False):
    return _get_values(body.value)

def _get_if(body:ast.If,raw=False):
    out = _if_parse(body)[0]
    return out

def _get_return(body:ast.Return,raw=False):
    return f"__temp:={_get_values(body.value)}"

def _get_joined(body:ast.JoinedStr,raw=False):
    return f"f{''.join(_get_values(*body.values,raw=True))!r}"

def _get_formattedvalue(body:ast.FormattedValue,raw=False):
    return f"{{{_get_values(body.value)}}}"

def _get_ifexp(body:ast.IfExp,raw=False):
    boolop = _get_values(body.test)
    code = _get_values(body.body)
    orelse = _get_values(body.orelse) or "_:=None"
    return f"({code}) if {boolop} else ({orelse})"

def _get_listcomp(body:ast.ListComp,raw=False):
    code = _get_values(body.elt)
    comp = _get_values(*body.generators)

    return f"[{code}{comp}]"

def _get_assign(body:ast.Assign,raw=False):
    return _assign_parse(body)[0]

def _get_unaryop(body:ast.UnaryOp,raw=False):
    op = bool_opers[type(body.op)]
    code = _get_values(body.operand)
    return f"{op}{code}"

def _get_comprehension(body:ast.comprehension,raw=False):
    iterable = _get_values(body.iter)
    targets = _get_values(body.target)
    ifs = _get_values(*body.ifs)
    ifs = ' if '+''.join(ifs) if ifs else ""

    return f" for {targets} in {iterable}{ifs}"

def _get_for(body:ast.For,raw=False):
    code = _for_parse(body)[0]
    return code

def _get_aug(body:ast.AugAssign,raw=False):
    return _aug_parse(body)[0]

def _get_generatorexp(body:ast.ListComp,raw=False):
    code = _get_values(body.elt)
    comp = _get_values(*body.generators)

    return f"({code}{comp})"

def _get_dict_comp(body:ast.DictComp,raw=False):
    key = _get_values(body.key)
    value = _get_values(body.value)
    comp = _get_values(*body.generators)
    
    return f'{{{key}:{value}{comp}}}'

#Easily get values
get_value = {
    ast.Constant : _get_constant,
    ast.Name : _get_name,
    ast.Subscript : _get_subscript,
    ast.Index : _get_index,
    ast.Call : _get_call,
    ast.Tuple : _get_tuple,
    ast.Dict : _get_dict,
    ast.List : _get_list,
    ast.BinOp : _get_binop,
    ast.Attribute : _get_attr,
    ast.NamedExpr : _get_namedexpr,
    ast.Starred : _get_starred,
    ast.Slice : _get_slice,
    ast.Lambda : _get_lambda,
    ast.arguments : _get_args,
    ast.BoolOp : _get_boolop,
    ast.Compare : _get_compare,
    ast.Expr : _get_expr,
    ast.If : _get_if,
    ast.Return : _get_return,
    ast.JoinedStr : _get_joined,
    ast.FormattedValue : _get_formattedvalue,
    ast.IfExp : _get_ifexp,
    ast.ListComp : _get_listcomp,
    ast.GeneratorExp : _get_generatorexp,
    ast.DictComp : _get_dict_comp,
    ast.Assign : _get_assign,
    ast.UnaryOp : _get_unaryop,
    ast.comprehension : _get_comprehension,
    ast.For : _get_for,
    ast.AugAssign : _get_aug
}

def _get_values(*types,raw=False):
    #If debug is on print the incomming type
    if debug:
        for val in types:
            print("NEW:" ,type(val).__name__,"(types)")

    out = [get_value[type(val)](val,raw) for val in types]
    #If debug is on print the outgoing type
    if debug:
        if isinstance(out,list):
            for val,outv in zip(types,out):
                print(f"OUT:    {type(val).__name__} >>> {outv!r}")
        else:
            print(f"OUT:    {type(types[0]).__name__} >>> {out!r}")

    return out if len(out)-1 else out[0]

### Body handling ###

def _update_subscript(target:ast.Subscript,value):
    #Update list or dictionary
    name,slice = _get_values(target.value,target.slice)
    if local_vars[name] == ast.List:
        return f"{name}:=[*{name}[:{slice}],{value},*{name}[{slice}+1:]]"
    else:
        return f"{name}.update({{{slice}:{value}}})"

def _assign_parse(body:ast.Assign):
    global local_vars

    values = [[_get_values(x),type(x)] for x in body.value.elts] if isinstance(body.value,ast.Tuple) else [_get_values(body.value),type(body.value)]
    if not isinstance(values[0],list):
        values = [values]
    targets = body.targets

    #get variable names
    targets = [x for x in targets[0].elts] if isinstance(targets[0],ast.Tuple) else targets

    out = []
    #Set variable
    for target,(value,typ) in zip(targets,values):
        if isinstance(target,ast.Subscript):
            out.append(_update_subscript(target,value))
        else:
            local_vars[_get_values(target)] = typ
            out.append(f"{_get_values(target)}:={value}")
    return out

def _expression_parse(body:ast.Expr):
    return [_get_values(body.value)]

def _for_parse(body:ast.For):
    it = _get_values(body.iter)
    targets = _get_values(body.target)
    out = _parse_body(body.body)
    return [f"[{out} for {targets} in {it}]"]

def _import_parse(body:ast.Import):
    data = [[x.name,x.asname] for x in body.names]
    for name,asname in data:
        imports[asname or name] = f"__import__('{name}')"

def _if_parse(body:ast.If):
    boolop = _get_values(body.test)
    code = _parse_body(body.body)
    orelse = _get_values(*body.orelse) or ["_:=None"]
    orelse = ','.join(orelse) if isinstance(orelse,list) else orelse

    return [f"({code}) if {boolop} else ({orelse})"]

def _aug_parse(body:ast.AugAssign):
    target = body.target
    value = _get_values(body.value)
    oper = opers[type(body.op)]

    if isinstance(target,ast.Subscript):
        tar_get_name = _get_values(target)
        return [_update_subscript(target,f"{tar_get_name}{oper}{value}")]
    else:
        target = _get_values(target)
        return [f"{target}:={target}{oper}{value}"]

def _def_parse(body:ast.FunctionDef):
    base = ["__temp:=None"]
    name = body.name
    args = _get_values(body.args)
    #Check function args and save them in `local_vars` for type checking later
    for x in body.args.args:
        if x.annotation:
            local_vars[x.arg] = eval(_get_values(x.annotation))
    code = _parse_body(body.body)
    base.append(code)
    base.append('__temp')
    return [f"{name}:= lambda {args}: [{','.join(base)}][-1]"]

def _return_parse(body:ast.Return):
    return_val = _get_values(body.value) if body.value else None
    return [f"__temp:={return_val} if __temp==None else __temp"]

def _importfrom_parse(body:ast.ImportFrom):
    global imports
    name = body.module
    data = [[x.name,x.asname] for x in body.names]

    #Save functions in `imports` to be used if function called
    for subname,asname in data:
        if subname == "*":
            #Get all functions from it
            for x in dir(__import__(name)):
                if not str(x).startswith('_'):
                    imports[str(x)] = f"__import__('{name}').{x}"
            return
        imports[asname or subname] = f"__import__('{name}').{subname}"

parser = {
    ast.Import: _import_parse,
    ast.If : _if_parse,
    ast.Assign : _assign_parse,
    ast.Expr : _expression_parse,
    ast.For : _for_parse,
    ast.AugAssign : _aug_parse,
    ast.FunctionDef : _def_parse,
    ast.Return : _return_parse,
    ast.ImportFrom : _importfrom_parse,
}

def _parse_body(body,force_list=False):
    raw = []
    for x in body:
        if debug: print(f"\n## {type(x).__name__} ##\n")
        if type(x) in parser:
            temp = parser[type(x)](x)
            if temp: raw += temp
        elif debug:
            print('\nNEW:',type(x).__name__,end='\n\n')
    out = ','.join(raw)
    return f"[{out}]" if (len(raw)-1 or force_list) else f"{out}"

### other ###

def _get_default(defaults,arg): #Get default value from args
    for default in defaults:
        if default.col_offset == arg.end_col_offset+1: return default.value

def _parse_ast(filename): #Load AST for module
    with open(filename, "rt") as file:
        return ast.parse(file.read(), filename=filename)

def parse_file(filename:str) -> str:
    "Filename is just the directory of the file. eg: 'C:/User/%username%/python/somefile.py'"

    parsed_ast = _parse_ast(filename)
    out = _parse_body(parsed_ast.body,force_list=True)
    return out

def parse_string(string:str) -> str:
    "String is python code in the form of a string"

    parsed = ast.parse(string)
    out = _parse_body(parsed.body,force_list=True)
    return out