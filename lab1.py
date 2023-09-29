from z3 import *
import sys

def liner_func(term):
    left_ind = []
    left = 0
    right = 0
    counter = 0

    while counter == 0:
        # print(term)
        for i in term:
            if i == "(":
                left += 1
                left_ind.append(counter)
            if i == ")":
                right += 1
                if left == right == 1:
                    f = term[0]
                    # print(coefs[f])
                    va = term[term.index('(')+1:term.index(')')].split(',')
                    # print(f, va)
                    lin = ""
                    for j in range(len(va)):
                        temp = va[j].split("+")
                        for s in temp:
                            lin += coefs[f][j]+"*"+s+"+"
                    lin += coefs[f][len(coefs[f])-1]
                    return lin
                else:
                    ind = left_ind.pop()
                    new = liner_func(term[ind-1:counter+1])
                    old = term[ind-1:counter+1]
                    term = term.replace(old, new)
                    # print(term)
                    counter = 0
                    break
            counter += 1

    return term

def mult(term):
    multipliers = {}
    # print(term)
    free = ""
    for v in var:
        # print(v)
        counter = 0
        index = 0
        m = ""
        flag = True
        for i in term:
            # print(i, counter, term)
            if i == v:
                m += term[index:counter-1]+"+"
                # print(i, index, counter, term)
                term = term[:index]+term[counter+2:]
                # print(m)
                counter = index
                index = 0
                # print(i, index, counter, term)
                flag = True
                continue
            if i == "+" and counter != 0:
                for j in term[index:counter]:
                    if j in var:
                        index = counter+1
                        flag = False
                        break
                if flag:
                    # print(index, counter, term)
                    free += term[index:counter]+"+"
                    # print(free)
                    term = term[:index]+term[counter+1:]
                    # print("fffffffffffffffff",term)
                    counter = index
                    index = 0
                    continue
            if i == "+" and counter == 0:
                continue
            counter += 1

        if len(m) > 0:
            if m[-1] == "+":
                m = m[:-1]
                multipliers[v] = m
                # print(v, m)
    free += term
    multipliers["free"] = free
    return multipliers
    # print(term)

def parse(terms):
    balance = 0
    term1 = terms[:terms.find("=")]
    term2 = terms[terms.find("=")+1:]
    # print(term1, term2)

    # просто ищем конструкторы и проверяем сбалансированность собок
    for i in range(len(term1)):
        a = term1[i]
        if a != "(" and a != ")" and a != ",":
            if a not in constr and a not in var:
                constr.append(a)
        else:
            if a == '(':
                balance += 1
            elif a == ")":
                balance -= 1
    # print(constr, "\n", balance)
    if balance > 0:
        print("Error! Some \")\" was missed")
        sys.exit()
    elif balance < 0:
        print("Error! Some \"(\" was missed")
        sys.exit()

    for i in range(len(term2)):
        a = term2[i]
        if a != "(" and a != ")" and a != ",":
            if a not in constr and a not in var:
                constr.append(a)
        else:
            if a == '(':
                balance += 1
            elif a == ")":
                balance -= 1
    # print(constr, "\n", balance)
    if balance > 0:
        print("Error! Some \")\" was missed")
        sys.exit()
    elif balance < 0:
        print("Error! Some \"(\" was missed")
        sys.exit()

    # ищем количество коэфов у каждой функции
    global co_counter, file, s

    exp = "And( "
    for f in constr:
        ex1 = ""
        ex2 = "And("
        left = 0
        right = 0
        constr_find = False
        counter = 1
        for i in terms:
            if i == f:
                constr_find = True
            if constr_find:
                if i == '(':
                    left += 1
                if i == ')':
                    right += 1
                if left-right == 1 and i == ',':
                    counter += 1
                if left == right and left != 0:
                    counter += 1
                    break
        # print(f, counter)
        amount.append(counter)
        co = []
        for i in range(counter):
            a = "a"+str(co_counter)
            co.append(a)
            co_counter += 1
            if i == counter-1:
                ex1 = a+">0"
            else:
                ex2 += a+">1, "
        if len(ex2) > 4:
            ex2 = ex2[:-2]+"), "
        else:
            ex2 = ""
        exp += "Or( "+ex2+ex1+"), "
        # print (exp)
        coefs[f] = co
    exp = exp[:-2]+")"

    # print(coefs, "yyyyyy")
    # print(co)
    expr = "And("
    for i in coefs:
        for j in coefs[i]:
            # print(i, "jjjjjjj")
            globals()[j] = Int(j)
    for i in coefs:
        for j in coefs[i]:
            if i == "free":
                expr += j+">=0, "
            else:
                expr += j+">=1, "
            # s.add(eval(j+">=0"))
    # print (expr[:-2]+")")
    # print(exp)
    s.add(eval(exp))
    s.add(eval(expr[:-2]+")"))
    # составляем линейную функцию
    term1 = liner_func(term1)
    term2 = liner_func(term2)

    # теперь нада посчитаить множители при каждой переменной
    # print(term1, "\n", term2)
    mu1 = mult(term1)
    mu2 = mult(term2)
    # print(mu1, "\n", mu2)
    # print(len(mu1), len(mu2))
    if not "free" in var:
        var.append("free")
    # print(var)

    expr1 = "Or("

    # записываем неравенства
    for v in var:
        if not v in mu1:
            mu1[v] = "0"
        if not v in mu2:
            mu2[v] = "0"
        # print(mu1[v]+'>='+mu2[v])
        s.add(eval(mu1[v]+'>='+mu2[v]))
        expr1 += "("+mu1[v]+'>'+mu2[v]+"), "
    expr1 = expr1[:-2]+")"
    # print(expr1)
    s.add(eval(expr1))
    # print(mu1,"\n", mu2)
    # записываем неравенства


# типа  main
print('''Input stops, when it recive "end"
  Input example:
      variables= x, y
      f(g(x,y))=g(h(y),x)
      h(f(x))=f(x)
      end''')
var = input()
var = var.replace(' ', '')
var = var[var.find("=")+1:]
var = var.split(",")
terms = []
constr = []
amount = []
coefs = {}
co_counter = 0

s = Solver()

while True:
    inp = input()
    inp = inp.replace(' ', '')
    if inp == "end":
        break

    terms.append(inp)

# print(terms)

for i in range(len(terms)):
    parse(terms[i])

print(s.check())
if s.check() == z3.sat:
    print(s.model())