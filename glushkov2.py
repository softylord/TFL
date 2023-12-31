import random
import re
import datetime
from test_2 import rand_reg
import lab2
import time
import multiprocessing
import timeout_decorator
# from wrapt_timeout_decorator import *


"""""
ПОСТРОЕНИЕ АВТОМАТА И ГЕНЕРАЦИЯ СТРОК
"""""

def find_closing_brac(reg, open_ind):
    count_brac = 0
    for i in range(open_ind+1, len(reg)):
        # print(i, count_brac)
        if reg[i] == "(":
            count_brac += 1

        if reg[i] == ")":
            if count_brac == 0:
                return i
            else:
                count_brac -= 1
    return "error"
def no_out_or(reg):
    i = 0
    while i < len(reg):
        if reg[i] == "|":
            return False
        if reg[i] == "(":
            i = find_closing_brac(reg, i)
        i += 1
    return True
# print(no_out_or("a(a|b)(b|cc)"))
def parsing_(reg):
    if len(reg) == 0:
        return reg

    res = ""
    for i in range(0, len(reg)-1):
        if reg[i+1] == "*" and reg[i] != ")":
            res += "("+reg[i]+")"
        else:
            res += reg[i]
    res += reg[-1]
    return parsing(res)

var_index = 0
vars = []
def parsing(reg):
    #print(reg)
    if len(reg) == 1:
        if reg == "|" or reg == "&":
            return reg
        else:
            # print('@@@', reg)
            global var_index
            var_index += 1
            global vars
            new_reg = reg + str(var_index)
            vars.append(new_reg)

            return new_reg
    elif reg[0] == "(" and find_closing_brac(reg, 0) == len(reg) - 2 and reg[-1] == "*":
        if len(reg) == 4:
            return [[parsing(reg[1])], "*"]
        return [parsing(reg[1:-2]), "*"]
    elif reg[0] == "(" and find_closing_brac(reg, 0) == len(reg)-1:
        #print("reg[1]", reg)
        #print("-----", reg[1:-1])
        if len(reg) == 3:
            return parsing(reg[1])
        # print(reg)
        return parsing(reg[1:-1])
        # return "eee"
    elif no_out_or(reg):
        # print("reg", reg)
        l = []
        start_i = 0
        i = 0
        while i < len(reg):
            # print(l, i)
            if reg[i] != "(":
                if i != len(reg) - 1 and reg[i + 1] == "*":
                    l.append([reg[start_i:i+1], "*"])
                    i+=1
                    start_i = i + 2
                else:
                    l.append(reg[start_i:i+1])
                    start_i = i+1
                l.append("&")
            else:
                i = find_closing_brac(reg, i)
                if i != len(reg)-1 and reg[i+1] == "*":
                    i += 1
                l.append(reg[start_i:i+1])
                l.append("&")
                start_i = i + 1
            i += 1
        # print("l", l)
        for j in range(len(l)):
            l[j] = parsing(l[j])
        # print("ll", l)
        return l[:-1]

    l = []
    # next, ind = get_next(reg)
    # print(find_closing_brac(reg, 1))
    # print("hello", reg)
    start_i = 0
    i = 0
    while i < len(reg):
        # print(i, l)
        if reg[i] == "(":
            i = find_closing_brac(reg, i)
        elif reg[i] == "|":
            # print("hello")
            l.append(reg[start_i:i])
            l.append("|")
            start_i = i+1
        i += 1
    l.append(reg[start_i:i])

    for j in range(len(l)):
        # print(l[j])
        l[j] = parsing(l[j])
        #print("l[j]", l[j])
    return l

def first_(reg):
    return first(reg)[0]
def first(reg):
    if isinstance(reg, str):
        return [reg], False

    elif len(reg) == 1:
        return first(reg[0])

    elif len(reg) == 2 and reg[1] == "*":
        return first(reg[0])[0], True

    elif len(reg) >= 3 and reg[1] == "&":
        lst, isStar = first(reg[0])
        if isStar:
            l, isS = first(reg[2:])
            return lst + l, isS
            # return last(reg[0:-2])+lst
        else:
            return lst, False

    else:
        res = []
        isStar = False
        for i in range(0, len(reg), 2):
            lst, isS = first(reg[i])
            res += lst
            isStar = isStar or isS

    return res, isStar

def last_(reg):
    return last(reg)[0]

def last(reg):
    if isinstance(reg, str):
        return [reg], False

    elif len(reg) == 1:
        return last(reg[0])

    elif len(reg) == 2 and reg[1] == "*":
        return last(reg[0])[0], True

    elif len(reg) >= 3 and reg[1] == "&" :
        lst, isStar = last(reg[-1])
        if isStar:
            l, isS = last(reg[0:-2])
            return l+lst, isS
        else:
            return lst, False

    else:
        res = []
        isStar = False
        for i in range(0, len(reg), 2):
            lst, isS = last(reg[i])
            res += lst
            isStar = isStar or isS

        return res, isStar

def follow_(reg, var):
    if isinstance(reg, str):
        return []
    elif len(reg) == 1:
        return follow_(reg[0], var)
    elif len(reg) == 2 and reg[1] == "*":
        res = follow_(reg[0], var)
        if var in last_(reg[0]):
            res += first_(reg[0])

        return res

    elif len(reg) >= 3 and reg[1] == "|":
        res = []
        for i in range(0, len(reg), 2):
            res += follow_(reg[i], var)
        return res
    elif len(reg) >= 3 and reg[1] == "&":
        res = []
        for i in range(0, len(reg), 2):
            res += follow_(reg[i], var)
            # if i < len(reg)-2 and var in last_(reg[i]):
            if var in last_(reg[i]):
                for j in range(i+2, len(reg), 2):
                    res += first_(reg[j])
                    if not(len(reg[j]) == 2 and reg[j][1] == "*"):
                        break

                # res += first_(reg[i+2])
        return res
    else:
        return ["!"]


def follow(reg):
    res = []
    for i in range(len(vars)):
        res.append((vars[i], follow_(reg, vars[i])))
    return res
last_qq = []
def make_automata(reg):
    r = parsing_(reg)
    #print("ppppppppppppppppppppp", r)
    f = first_(r)
    global last_qq
    last_qq = last_(r)
    # print("TTTTTTTTTTTT",last_(r))
    res = []
    # print(r)
    # print(f)
    for i in range(len(f)):
        res.append(("S", f[i][0], f[i]))

    for i in range(len(vars)):
        follows = follow_(r, vars[i])
        #print(follows, vars[i])
        for j in range(len(follows)):
            res.append((vars[i], follows[j][0], follows[j]))

    return res
def is_in_automata(q, automata):
    res = []
    for i in range(len(automata)):
        if automata[i][0] == q:
            res.append(automata[i][2])
    return res

used_q = []
def reachability_for_var(q, automata):
    res = []
    for i in range(len(automata)):
        if automata[i][0] == q:
            global used_q
            if not (automata[i][2] in used_q):
                res.append(automata[i][2])
                used_q.append(automata[i][2])
                # print(used_q, res)
                # print("  ",automata[i])
                res += reachability_for_var(automata[i][2], automata)
    return res

def reachability_matrix(automata):
    res = []
    res.append(("S", vars))
    for q in vars:
        global used_q
        used_q = []
        res.append((q, reachability_for_var(q, automata)))
    return res


def list_of_reachable_form_itself(mtx):
    res = []
    for i in range(len(mtx)):
        if mtx[i][0] in mtx[i][1]:
            # print(mtx[i][0], mtx[i][1])
            res.append(mtx[i][0])
    return res

pattern = r'(ba|b)aa(a|ab)*'
def find_next_step(q, list_of_reach, reach_mtx):
    # next_step = []
    for i in range(len(reach_mtx)):
        if reach_mtx[i][0] == q:
            next_step = []
            for j in range(len(reach_mtx[i][1])):
                if reach_mtx[i][1][j] in list_of_reach:
                    next_step.append(reach_mtx[i][1][j])
            return next_step

def find_ind(el, l):
    res = []
    for i in range(len(l)):
        if l[i][0] == el:
            res.append(i)
    if len(res) == 1:
        return res[0]
    else:
        return res

done = False
def create_cycle(Q, last, automat, done):
    next_q = []
    word = ""
    if not done:
        for i in range(len(automat)):
            if automat[i][0] == Q and last in reach_mtx[find_ind(automat[i][2], reach_mtx)][1]:
                next_q.append(automata[i][2])
        if len(next_q) == 1:
            if next_q == Q:
                word += next_q[0][0]
            else:
                word += next_q[0][0]
            nq = next_q[0]
        else:
            nq = random.choice(next_q)
            if nq == Q:
                wn = nq[0][0]
                word += wn
            else:
                word += nq[0]
        if nq == last:
            done = True
        return word + create_cycle(nq, last, automat, done)
    else:
        return ""

def create_word(first_q, last_q, automat):
    word = ""
    start_pos = first_q
    next_q = []
    if first_q == last_q and last_q in reach_mtx[find_ind(first_q, reach_mtx)][1]:
        return ""
        # return ""
    if last_q in reach_mtx[find_ind(first_q, reach_mtx)][1]:
        for i in range(len(automat)):
            if automat[i][0] == first_q:
                if last_q in reach_mtx[find_ind(automat[i][2], reach_mtx)][1] or last_q==automat[i][2]:
                    next_q.append(automat[i][2])
        if len(next_q) == 0:
            return last_q[0]
        if len(next_q) == 1:
            if next_q == first_q:
                 word += next_q[0][0]*random.randint(100, 300)
                 # repeat = random.randint(1, 5)
                 # word += next_q[0][0] * repeat
            else:
                word += next_q[0][0]
            nq = next_q[0]
        else:

            nq = random.choice(next_q)
            if nq == first_q:
                wn = nq[0][0]*random.randint(100, 300)
                # wn = nq[0][0] * random.randint(1, 5)
                word += wn
            else:
                word += nq[0][0]
        return word + create_word(nq, last_q, automat)
    else:
        return ""

@timeout_decorator.timeout(30)
def mach(pattern, word):
    return re.fullmatch(pattern, word)


if __name__ == '__main__':
    """""
    генерация регулярок
    """""
    reggg = rand_reg([],[])
    orig_reg = reggg
    orr = list(orig_reg)
    orr.append('end')
    orig_reg2 = lab2.get_alt(orr)
    res_orig = list(lab2.back(orig_reg2, True))
    res_orig_regex = ""
    for i in range(len(res_orig)):
        res_orig_regex += res_orig[i]
    # print("res_orig_regex", res_orig_regex, "olllllllld", reggg)

    # while orig_reg.find('()')!=-1:
    #     orig_reg=orig_reg.replace("()", "")

    while reggg.find('**')!=-1:
        reggg = reggg.replace("**", "*")
    while reggg.find('()')!=-1:
        reggg=reggg.replace("()", "")
    pattern3 = reggg
    # print(reggg, orig_reg)

    automata = make_automata(reggg)
    #print("automata", automata)
    reach_mtx = reachability_matrix(automata)
    #print("matrix", reach_mtx)
    list_of_reach = list_of_reachable_form_itself(reachability_matrix(automata))
    #print("список сотояний, которые достижимы сами из себя", list_of_reachable_form_itself(reachability_matrix(automata)))
    # print(vars)
    #print("конечные состояния", last_qq)
    is_cycl = False
    for i in range(len(list_of_reach)):
        if list_of_reach[i] in last_qq:
            is_cycl = True

    new_reach_list = []
    for q in last_qq:
        for i in range(len(list_of_reach)):
            #print(list_of_reach[i], i)
            if q in reach_mtx[find_ind(list_of_reach[i], reach_mtx)][1]:
                if list_of_reach[i] in reach_mtx[find_ind(q, reach_mtx)][1]:
                    new_reach_list.append(list_of_reach[i])

    #print("bbbbb", new_reach_list)
    list_of_reach = new_reach_list
    #print(list_of_reach)

    for k in range(10):
        if len(list_of_reach) == 0 or not is_cycl:
            last_q = random.choice(last_qq)
            # print(last_q)
            res_word = create_word("S", last_q, automata)
        else:
            #print("генерация фрагментов путей")
            res = ["S"]
            next_step = list_of_reach
            is_continue = 1
            while is_continue and len(next_step)!=0:
                # print(is_continue)
                r = random.randint(0, len(next_step)-1)
                res.append(next_step[r])
                res.append(next_step[r])
                if next_step[r] not in last_qq:
                    is_continue = 1
                else:
                    is_continue = random.randint(0, 1)
                next_step = find_next_step(next_step[r], list_of_reach, reach_mtx)
            # print(res)

            res_word = ""

            for i in range(len(res)-1):
                if res[i] == res[i+1]:
                    repeat = random.randint(300, 1000)
                    # if len(res_word) > 10:
                    #     repeat = random.randint(1, 10)
                    # else:
                    #     repeat = 1
                    res_word += create_cycle(res[i], res[i], automata, False)*repeat
                else:
                    res_word += create_word(res[i], res[i+1], automata)



        # print (k)

        res_word=res_word+"Ω"

        pattern1 = res_orig_regex
        pattern2 = lab2.normalize(reggg)

        s = time.time()
        f = mach(pattern2, res_word)
        e = time.time()
        print("Time with norm regex", e-s, pattern2)

        # s1 = time.time()
        # print(pattern1, res_word)
        # f = mach(pattern1, res_word.replace("Ω", ""))
        # print(f)
        """p = multiprocessing.Process(target=re.fullmatch(pattern1, res_word))
        p.start()

        # Wait for 10 seconds or until process finishes
        p.join(5)
        if p.is_alive():
            print ("running... let's kill it...")

                # Terminate - may not work if process is stuck for good
            p.terminate()
                # OR Kill - will work for sure, no chance for process to finish nicely however
                # p.kill()

            p.join()
            #f = re.fullmatch(pattern1, res_word)
            # print(f)"""

        s1 = time.time()
        try:
            f = mach(pattern1, res_word)
            e1 = time.time()
            print("Time with origin regex", e1 - s1, pattern1)
        except:
            print("Time with origin regex is more than a 30 seconds", pattern1)
        print('\n')
