from pprint import pprint as pretty
import re


def simpled(match):
    if match.group(1) is not None:
        print(match.group(1))
        return match.group(1).removeprefix("(").removesuffix(")")
    return


debug = False

code = """

y = x**2;
x = 4*z //random comment;
&getinto z;
//another one;
&display y;
&formula y;
&simpled y;

"""

scope = {
    "_": "1"
}

def pow(x, a): return x**a
def root(x, a): return x**(1/a)
def floor(x): return x // 1
def formula(x):
    if x in scope.keys():
        return scope[x]
    else:
        return "unknown"
    pass

for l in code.replace("\n","").split(";"):
    if '//' in l:
        if debug:print("comment found")
        l = l.split("//")[0]
        pass
    if not l:
        if debug:print("empty line")
        continue
    if l[0] == "&":
        if debug:print("command found")
        cmd = l.split()[0].strip()
        if debug:print("command is", cmd)
        val = l.split(" ", 1)[1].strip()
        if cmd == "&display":
            if debug:print("formula:", scope[val])
            frm = scope[val]
            rpl = 1
            while rpl:
                rpl = 0
                for i in scope.keys():
                    if i in frm:
                        frm=frm.replace(i,"("+scope[i]+")")
                        rpl+=1
                        pass
                    pass
                pass
            if debug:print("new formula:", frm)
            try:print(val,"=",str(eval(frm)))
            except:print("Calculation error, ignoring")
            pass
        if cmd == "&simpled":
            if debug:print("formula:", scope[val])
            frm = scope[val]
            rpl = 1
            while rpl:
                rpl = 0
                for i in scope.keys():
                    if i in frm:
                        frm=frm.replace(i,"("+scope[i]+")")
                        rpl+=1
                        pass
                    pass
                pass
            frm = re.sub(r"\((\d|[a-zA-Z])+\)", simpled, frm)
            print(frm)
            pass
        if cmd == "&formula":
            print(val,"=",formula(val))
            pass
        if cmd == "&getinto":
            scope[val] = input(str(val)+": ")
            pass
        pass
    if "=" in l:
        idx = l.split("=", 1)[0].strip()
        if idx in scope.keys():
            print(f"Error: name formula redefining, {idx} already defined")
            raise SystemExit(1)
        val = l.split("=", 1)[1].strip()
        scope[idx] = val
        pass
    pass
#
if debug:pretty(scope)
