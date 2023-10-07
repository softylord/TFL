# fuzz test
import random
import re
from subprocess import run, PIPE
# TODO рандомайзер регулярок
# TODO cтроку по регулярке

abc_length = 6
star_hight = 3
max_amount_of_symbols = 12
max_amount_of_letters = 5
symbols = ["|", "", "&"]
abc = ["a", "b", "c", "d", "<eps>"]
abc_with_brace = ["a)", "b)", "c)", "d)", "<eps>)"]

def use_regex(input_text):
    s = r"\(a\|b\)\|\(ab\|cc\)"
    pattern = re.compile(s, re.IGNORECASE)
    # print(pattern)
    # print(pattern.match(input_text))
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
# amount_of_letters = 0

def rand_reg(exp, res):
    amount_of_letters = 0
    if exp == []:
        exp.append(random.choice(["(", "a", "b", "c", "d", "<eps>"]))
        res.append(exp[0])
        # print(res)
    else:
        amount_of_letters = exp.count("a") + exp.count("b") + exp.count("c") + exp.count("d")
        # print(amount_of_letters)
        # sym = ""
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
        # exp.append(sym)
        # print(exp)
    if amount_of_letters == max_amount_of_letters:
        if exp.count("(")>(exp.count(")") + exp.count(")"+"*"*star_hight)):
            sym2 = random.choice([")"*(exp.count("(") - exp.count(")") - exp.count(")"+"*"*star_hight)), ")"*(exp.count("(")-exp.count(")") - exp.count(")"+"*"*star_hight))+"*"*star_hight])
            exp.append(sym2)
            # res.append()
            # print(exp)
        r = ""
        for i in range(len(exp)):
            r += exp[i]
        return del_empty_brace(r.replace("&", ""))
    else:
        res.append(exp)
        return rand_reg(exp, res)




    #     flag1 = False


# def random_regex2(expr):
#     # l = amount_of_letters
#     flag1 = False
#     if expr == []:
#         expr += random.choice(["(", "a", "b", "c", "d", "|"])
#         print(expr)
#     else:
#         amount_of_letters = expr.count("a") + expr.count("b") + expr.count("c") + expr.count("d") + expr.count("eps")
#         if amount_of_letters + 2 == max_amount_of_letters:
#             if expr.count("(")-expr.count(")") != 0:
#                 expr += ")"*(expr.count("(")-expr.count(")"))+"*"*star_hight
#             else:
#                 expr += random.choice(["*"*star_hight, ""])
#             flag1 = True
#             res = expr
#             print(expr)
#         else:
#             if expr[len(expr)-1].isalpha():
#                 if expr.count("(")+expr.count(")") % 2 != 0:
#                     expr += random.choice(abc_with_brace + symbols + abc)
#                 else:
#                     expr += random.choice(symbols + abc + ["("])
#                 print(expr)
#             else:
#                 if expr.count("(")+expr.count(")") % 2 != 0:
#                     expr += random.choice(abc_with_brace + abc)
#                 else:
#                     expr += random.choice(abc)
#                 print(expr)
#     if flag1:
#         return res
#     else:
#
#         # left = expr
#         # right = ""+expr[len(expr)-1]
#         # # return random_regex2(left)+random_regex2(right)
#         # res += random_regex2(left, res)+random_regex2(right, res)
#     # return random_regex2(expr)


# def random_regex(expr):
#     len(expr)
#     if expr == "":
#         expr += random.choice(["(", "a", "b", "c", "d"])
#         # print(expr)
#     elif (len(expr) + (expr.count("(")-expr.count(")")) <=  max_amount_of_symbols):
#         last_sym = expr[len(expr)-1]
#         if last_sym == "(":
#             expr += random.choice(abc+["("])
#             # print(expr)
#         if last_sym in abc or last_sym =="*":
#             if (expr.count("(")+expr.count(")"))%2 != 0:
#                 if len(expr)+1 == max_amount_of_symbols:
#                     expr += random.choice(abc_with_brace)
#                 else:
#                     expr += random.choice(abc_with_brace + symbols)
#                     # print("1", expr)
#             else:
#                 if len(expr) == max_amount_of_symbols:
#                     expr += random.choice(abc)
#                     # print("2", expr)
#                 else:
#                     # print(len(expr), max_amount_of_symbols)
#                     expr += random.choice(abc + symbols)
#                     # print("3", expr)
#         if last_sym == ")":
#             if len(expr) != max_amount_of_symbols:
#                 expr += random.choice(["*"*star_hight, "|", ""]+abc)
#                 # print("3", expr)
#             else:
#                 expr += random.choice(["*" * star_hight] + abc)
#             # print(expr)
#         if last_sym in symbols or last_sym == "*":
#             expr += random.choice(abc)
#     else:
#         expr += ")"*(expr.count("(")-expr.count(")"))
#         # expr += random.choice(["", "*"*star_hight])
#         expr += "*"*star_hight
#     # length += 1
#     if len(expr) > max_amount_of_symbols:
#         # print("old", expr)
#         return del_or(expr)
#     else:
#         return random_regex(expr)

def main():
    # amount_of_symbols = random.randint(3, 10)
    # print(use_regex("(a|b)|(ab|cc)"))
    exp = ""
    exp2=[]
    rr = rand_reg(exp2, [])
    #for i in range(10):
        #print(rand_reg([], []))
    #ress=''
    #print(rr)
    # s = "((ddadb|cb|))***"
    # solution = run("lab2.py", stdout=PIPE, input = s, encoding="ascii")
    # print(solution.stdout)
    # l = del_or(s)
    # print(l)
    # res = random_regex2(exp, "")
    # print(res)
    # f = open("")
    # for _ in range(20):
    #     exp = ""
    #     print(random_regex(exp))
    # txt = "The rain in Spain"
    # x = re.search(r"\bS\w+", txt)
    # print(x.group())
main()