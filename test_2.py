# fuzz test
import random
import re
from subprocess import run, PIPE
abc_length = 6
star_hight = 3
max_amount_of_symbols = 12
max_amount_of_letters = 5
symbols = ["|", "", "&"]
abc = ["a", "b", "c", "d"]
abc_with_brace = ["a)", "b)", "c)", "d)"]

def use_regex(input_text):
    s = r"\(a\|b\)\|\(ab\|cc\)"
    pattern = re.compile(s, re.IGNORECASE)
    return pattern.match(input_text)

def del_or(expr):
    res = ""
    for i in range(len(expr)-1):
        if expr[i] == "|" and expr[i+1] == ")":
            res += "0"
        else:
            res += expr[i]
    return res.replace("0", "") + expr[len(expr)-1]
def del_empty_brace(str):
    str.replace("()"+"*"*star_hight, "")
    str.replace("()", "")
    return str
flag1 = False

def rand_reg(exp, res):
    amount_of_letters = 0
    if exp == []:
        exp.append(random.choice(["(", "a", "b", "c", "d"]))
        res.append(exp[0])
        # print(res)
    else:
        amount_of_letters = exp.count("a") + exp.count("b") + exp.count("c") + exp.count("d")
        if amount_of_letters + 2 < max_amount_of_letters:
            if exp[len(exp)-1] in abc or  (exp[len(exp)-1] == ")") or(exp[len(exp)-1] == ")"+"*"*star_hight):
                if exp.count("(")>(exp.count(")") + exp.count(")"+"*"*star_hight)):
                    sym = random.choice(symbols+[")", ")"+"*"*star_hight, "*"*star_hight, "("])
                    exp.append(sym)
                else:
                    sym = random.choice(symbols + ["*"*star_hight, "("])
                    exp.append(sym)
            if exp[len(exp)-1] in symbols or (exp[len(exp)-1] == "*"*star_hight) or (exp[len(exp)-1] == "("):
                sym = random.choice(abc + ["("])
                exp.append(sym)
        else:
            if exp[len(exp)-1] in abc  or  (exp[len(exp)-1] == ")"):
                if exp.count("(")>(exp.count(")") + exp.count(")"+"*"*star_hight)):
                    sym = random.choice([")", ")"+"*"*star_hight, "*"*star_hight, "("])
                    exp.append(sym)
                else:
                    sym = random.choice(["*"*star_hight, "("])
                    exp.append(sym)
            if exp[len(exp)-1] in symbols or (exp[len(exp)-1] == "(") or (exp[len(exp)-1] == "*"*star_hight) or (exp[len(exp)-1] == ")"+"*"*star_hight):
                sym = random.choice(abc + ["("])
                exp.append(sym)
    if amount_of_letters == max_amount_of_letters:
        if exp.count("(")>(exp.count(")") + exp.count(")"+"*"*star_hight)):
            sym2 = random.choice([")"*(exp.count("(") - exp.count(")") - exp.count(")"+"*"*star_hight)), ")"*(exp.count("(")-exp.count(")") - exp.count(")"+"*"*star_hight))+"*"*star_hight])
            exp.append(sym2)
        r = ""
        for i in range(len(exp)):
            r += exp[i]
        return del_empty_brace(r.replace("&", ""))
    else:
        res.append(exp)
        return rand_reg(exp, res)

def main():
    exp2=[]
    rr = rand_reg(exp2, [])
# main()