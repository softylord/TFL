import numpy as np
from prettytable import PrettyTable
import sys
import os


class Tree:
    def __init__(self, cargo, tabs=0, childs=None, parent=None, right_sibling=None):
        self.cargo = cargo
        self.childs = childs
        self.parent = parent
        self.tabs = tabs
        self.right_sibling = right_sibling

    def add_child(self, new_child):
        self.childs.append(new_child)

    def __str__(self):
        return str(self.cargo)

    def __eq__(self, other):

        if self is not None and other is not None:
            return (self.cargo == other.cargo) \
                and (self.cilds == other.childs)
        else:
            return False


def print_tree(tree):
    global nonterm
    if tree == None:
        return
    t = ''
    for i in range(tree.tabs):
        t += '  |'
    a = tree.cargo
    print(t + a)
    # if a in nonterm:
    #     print(t+a)
    # else:
    #     print(t+a)
    if tree.childs is not None:
        for i in tree.childs:
            print_tree(i)


def first(seq, gra, nonterm):
    first_ = set()
    """print(gra)
    print("SEEEQQQQ", seq)"""
    for i in seq:
        flag = 0
        if i in nonterm:
            for j in gra[i]:
                first_ = first_ | first(j, gra, nonterm)
                if '@' in first(j, gra, nonterm):
                    flag = 1
            if flag == 0:
                break
        else:
            first_ = first_ | {i}
            break
    return first_


def follow(var_nt, gra, nonterm):
    follow_ = set()
    start_var = (list(gra.keys())[0])
    if var_nt == start_var:
        follow_ = follow_ | {'~'}
    for left_v in gra:
        for prod in gra[left_v]:
            if prod != '@':
                for i in range(len(prod)):
                    if prod[i] == var_nt:
                        if i != (len(prod) - 1):
                            next_str = prod[(i + 1):]
                            first_str = first(next_str, gra, nonterm)
                            if '@' in first_str:
                                follow_ = follow_ | (first_str - {'@'})
                                if (left_v != var_nt):
                                    follow_ = follow_ | follow(
                                        left_v, gra, nonterm)
                            else:
                                follow_ = follow_ | first_str
                        else:
                            if (left_v != var_nt):
                                follow_ = follow_ | follow(
                                    left_v, gra, nonterm)
    return follow_


def ll1_checker(gra, nonterm, term):
    mat = np.array([["0"] * (len(term) + 2)] * (len(nonterm) + 1))
    mat = mat.astype('<U100')
    term.append('~')
    # print("Terms", term)
    for i in range((len(nonterm) + 1)):
        for j in range((len(term) + 1)):
            if i == 0 and j >= 1:
                mat[i, j] = term[j - 1]
            elif i >= 1 and j == 0:
                mat[i, j] = nonterm[i - 1]
    # print(mat)

    isll1 = True

    for left_v in gra:
        row_n = nonterm.index(left_v) + 1
        for prod in gra[left_v]:
            first_rule = first(prod, gra, nonterm)
            if '@' in first_rule:
                first_rule = first_rule - {'@'}
                first_rule = first_rule | follow_set[left_v]
            for i in first_rule:
                col_n = term.index(i) + 1
                if mat[row_n, col_n] == '0':
                    mat[row_n, col_n] = left_v + '->' + prod
                else:
                    mat[row_n, col_n] = mat[row_n, col_n] + \
                        '\n' + left_v + '->' + prod
                    isll1 = False
    x = PrettyTable()
    x.field_names = mat[0]
    for i in range(len(mat)):
        if i > 0:
            x.add_row(mat[i])
    print(x)
    if isll1:
        print("This grammar can be used for LL1 Parser")
        return mat, True
    else:
        print("This grammar cannot be used for LL1 Parser")
        return mat, False


stack = []

num_of_node = 0


def parser(word, table, nonterm, nonterm_list, tabs):
    global num_of_node
    if len(word) > 0:
        term = word[0]
    if word == '':
        term = '~'
    # ищем индекс терма в первой строке таблы,
    # потом ищем строку, начинающуюся с нонтерма,
    # в ней берем правило по индексу терма
    ind1 = np.where(table[0] == term)
    if len(ind1[0]) == 0:
        print("Word is not for this grammar, ----")
        sys.exit()
    ind2 = 0
    for i in range(1, len(table)):
        if table[i][0] == nonterm:
            ind2 = i
            break
    rule = table[ind2][ind1][0]
    # print('rule', rule)
    while rule == '0':
        exit_flag = True

        if len(stack) != 0:
            st = stack.pop()
            if term == st:
                if word != '':
                    word = word[1:]
                    if len(word) > 0:
                        term = word[0]
                    if word == '':
                        term = '~'

                    ind1 = np.where(table[0] == term)
                    if len(ind1[0]) == 0:
                        print("Word is not for this grammar 00000")
                        sys.exit()
                    if len(ind1) == 0:
                        print("Word is not for this grammar 22222")
                        sys.exit()
                    ind2 = 0
                    for i in range(len(table[1:])):
                        if table[i][0] == nonterm:
                            ind2 = i
                            break
                    rule = table[ind2][ind1][0]
                    # print('rule', rule)
                    exit_flag = False
        if exit_flag:
            print("Word is not for this grammar 3333330003")
            sys.exit()
    main_rule = rule.split('->')[1]
    # print(main_rule)
    chld = []
    last = False
    for symb in main_rule:
        if symb not in nonterm_list:
            node = Tree(symb, tabs + 1)
            chld.append(node)
            if last:
                stack.append(symb)
                # print("stack", stack)
            elif symb != '@':
                word = word[1:]
        else:
            last = True
            node, word = parser(word, table, symb, nonterm_list, tabs + 1)
            num_of_node += 1
            # print(node, num_of_node, "+++++", word)
            chld.append(node)
    tree = Tree(nonterm, tabs, chld)
    # print(tree, tree.childs[0].cargo, "________________", len(tree.childs))
    # for child in tree.childs:
    # print(child.cargo)
    # if len(tree.childs) > 0:
    #     print(tree, tree.childs[1].cargo, "________________")
    return tree, word


count_nodes = 1
nonterm_with_nums = []


def num_nodes(tree):
    global count_nodes, nonterms
    if tree.childs is not None:
        for child in tree.childs:
            if child.cargo in nonterms:
                # print("DDDDDDD", child, count_nodes+1)
                # count_nodes += 1
                # print(child.cargo, "PPPPPPPPP")
                child.cargo = str(child.cargo) + str(count_nodes)
                count_nodes += 1
                """if child.childs is None:
                    count_nodes += 1
                else:
                    if child.childs[0].cargo != '@':
                        count_nodes += 1"""
                # if child.childs[0].cargo!='@':
                #     count_nodes+=1
                nonterm_with_nums.append(child.cargo)
        for child in tree.childs:
            num_nodes(child)


chisla = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

count_new_nodes = 0


def num_new_node(tree):
    global count_new_nodes, nonterms, nonterm_with_nums
    if tree.cargo in nonterms:
        count_new_nodes += 1
        tree.cargo = str(tree.cargo) + '_' + str(count_new_nodes)
        nonterm_with_nums.append(tree.cargo)
        if tree.childs is not None:
            for child in tree.childs:
                num_new_node(child)


def eps_num(tree):
    # global chisla
    if tree.childs is not None:
        extra_num = ''
        for child in reversed(tree.childs):
            if child.cargo in nonterm_with_nums and child.childs[0].cargo == '@':
                # print(child.cargo)
                if child.right_sibling is not None:
                    eps_num(child.right_sibling)
                    r_cargo = child.right_sibling.cargo
                    # print('here',r_cargo)
                    num = ''
                    for i in range(len(r_cargo)):
                        if r_cargo[i] in chisla:
                            num = r_cargo[i:]
                            break
                    # print('num', num)
                    if num != '':
                        # print('num', num)
                        carg = child.cargo
                        for i in range(len(carg)):
                            if carg[i] in chisla:
                                carg = carg[:i]
                        child.cargo = carg + num
        for child in tree.childs:
            eps_num(child)


list_of_siblings = []


def right_sib(tree):
    list_of_nonterm_childs = []
    global list_of_siblings
    if tree.cargo in nonterms or tree.cargo in nonterm_with_nums:
        # print(len(tree.childs), "====")

        if tree.childs != None:
            for i in tree.childs:
                # print(i.cargo, "PPPPPPPPPPPPPPP", i.cargo in nonterm)
                if i.cargo in nonterms or i.cargo in nonterm_with_nums:
                    list_of_nonterm_childs.append(i)
                    # print(i, "000000000")
            for i in range(len(list_of_nonterm_childs) - 1):
                list_of_siblings.append(
                    [list_of_nonterm_childs[i].cargo, list_of_nonterm_childs[i + 1].cargo])
                # print(type(list_of_nonterm_childs[i]))
                list_of_nonterm_childs[i].right_sibling = list_of_nonterm_childs[i + 1]
                # list_of_siblings.append([tree.childs[i].cargo, tree.childs[i+1].cargo])
        if tree.right_sibling is not None and len(list_of_nonterm_childs) != 0:
            list_of_nonterm_childs[len(
                list_of_nonterm_childs) - 1].right_sibling = tree.right_sibling
            list_of_siblings.append([list_of_nonterm_childs[len(
                list_of_nonterm_childs) - 1].cargo, tree.right_sibling.cargo])
    if tree.childs is not None:
        for i in tree.childs:
            right_sib(i)


def transfer(old_tree, old_word, new_word, x_mod, m):
    if old_tree != None:
        if old_word[0] == new_word[0]:

            new_chlds = []
            node = old_tree.childs[0]
            new_chlds.append(node)
            x_mod -= 1
            m -= 1
            old_word = old_word[1:]
            new_word = new_word[1:]
            for child in old_tree.childs[1:]:
                if x_mod != 0:
                    node, old_word, new_word, x_mod, m = transfer(
                        child, old_word, new_word, x_mod, m)
                    if node != None:
                        # print('here')
                        new_chlds.append(node)
                else:
                    break
            new_tree = Tree(old_tree.cargo, old_tree.tabs, new_chlds)
            return new_tree, old_word, new_word, x_mod, m
    return


def find_node(tree, pos, r=[], res=None):
    is_found = False
    # print(tree)
    if tree.cargo in nonterm_with_nums:
        if tree.cargo[1] == str(pos):
            is_found = True
            res = tree
            # r.append(res)
            return tree
    # if not is_found:
    if tree.childs is not None:
        for child in tree.childs:
            res = find_node(child, pos)
            if res != None:
                break
    return res


def add_tabs(tree, tabs):
    tree.tabs += tabs
    if tree.childs is not None:
        for child in tree.childs:
            add_tabs(child, tabs)


def get_sibl(nonterm):
    global list_of_siblings
    for l in list_of_siblings:
        if l[0] == nonterm:
            res = l[1]
    if res is not None:
        return res
    else:
        return False


last_nonterm = []


def y_pars(word, table, nonterm, nonterm_list, tabs, start_tree, build):
    global last_nonterm
    global num_of_node
    if len(word) > 0:
        term = word[0]
    if word == '':
        term = '~'
    ind1 = np.where(table[0] == term)
    if len(ind1[0]) == 0:
        print("Word is not for this grammar, ----")
        sys.exit()
    ind2 = 0
    for i in range(1, len(table)):
        if table[i][0] == nonterm:
            ind2 = i
            break
    rule = table[ind2][ind1][0]
    # print(rule, build)

    if rule != '0' and build:
        main_rule = rule.split('->')[1]
        # print(main_rule, "{[[[[[")
        chld = []
        last = False
        for symb in main_rule:
            if symb not in nonterm_list:
                # print(symb)
                node = Tree(symb, tabs + 1)
                # print_tree(node)
                chld.append(node)
                # start_tree.add_child(node)
                if last:
                    stack.append(symb)
                    # print("stack", stack)
                elif symb != '@':
                    word = word[1:]
            else:
                last = True
                # print('here')
                node = Tree(symb, tabs + 1)
                # print(symb)
                node, _ = y_pars(word, table, symb,
                                 nonterm_list, tabs + 1, start_tree, build)

                chld.append(node)
                # print(node.cargo, "kkkkk")
        tree = Tree(nonterm, tabs, chld)
        # start_tree.add_child(tree)
        # print("0000000")
        # print_tree(tree)

        return tree, last_nonterm

    else:
        tree = Tree(nonterm, tabs)
        if tree.childs is None:
            # last_nonterm += tree.cargo
            last_nonterm.append(tree)
            # print(last_nonterm, "iiiiiiiiii")
        # print(tree.cargo, "iiiiiiiiii", last_nonterm)
        return tree, last_nonterm


def inc_par1(tree, word, nonterm, new_nonterm, table, T0, xmod, zmod, old_word, build):
    global list_of_siblings
    global nonterms
    # print_tree(tree)
    # T1, _ = parser(word.replace(z_word, ''), table, nonterm, nonterm_list, 0)
    N_T0 = last_nonterm = None
    s = 0
    if tree.cargo != nonterm:
        if tree.childs is not None:
            for child in tree.childs:
                N_T0, last_nonterm, s = inc_par1(child, word, nonterm, new_nonterm,
                                                 table, T0, xmod, zmod, old_word, build)
    else:
        # tree.add_child(Tree(new_nonterm, tree.tabs+1))
        # вот здесь он достраивает дерево до z
        T1y, last_nonterm = y_pars(
            word, table, new_nonterm, nonterms, tree.tabs + 1, tree, build)

        # print("+++++++++++++++")
        # num_nodes(T1y)
        num_new_node(T1y)
        # print_tree(T1y)
        # print("+++++++++++++++")
        if len(last_nonterm) == 0:
            last_nonterm = None
        else:
            last_nonterm = last_nonterm[0]
        tree.add_child(T1y)
        # print_tree(tree)

        # print(len(old_word) - xmod - zmod + xmod)

        N_T0 = find_node(T0, len(old_word) - xmod - zmod + xmod)
        # print_tree(last_nonterm)
        s = zmod
    return N_T0, last_nonterm, s


def count_lenSubWords(tree, l):
    global terms
    if tree.childs != None:
        for chld in tree.childs:
            if chld.cargo in terms:
                l += 1
                # print(l)
            else:
                l = count_lenSubWords(chld, l)
    return l


def correct_tabs(tree):
    for chld in tree.childs:
        chld.tabs = tree.tabs + 1
        if chld.childs is not None:
            correct_tabs(chld)


def inc_par2(T0, T1, s, wrd0, wrd1, fullT0, fullT1, table):
    global last_nonterm
    if T0 != None and T1 != None:
        # print(T0.cargo, T1.cargo, s, wrd0, wrd1)
        if T0.cargo[0] == T1.cargo[0]:
            T1.childs = T0.childs
            T1.cargo = T0.cargo
            correct_tabs(T1)
            l = count_lenSubWords(T0, 0)
            # print('l', l)
            s -= l
            right_sib(fullT1)
            # print('s', s)
            # print(len(wrd0) - s, len(wrd1) - s)

        else:
            s -= 1
            T0 = find_node(T0, len(wrd0) - s)
            inc_par2(T0, T1, s, wrd0, wrd1, fullT0, fullT1, table)

        # print_tree(fullT1)
        if T1.right_sibling == None:
            word_ = ""
            last_X = find_last_nonterm(fullT1, table)
            # print('----------------------')
            # print_tree(last_X)
            first_child = last_X.childs[0].cargo
            term = first_child
            for c in last_X.childs:
                last_child = c.cargo
            ind1 = np.where(table[0] == term)

            ind2 = 0
            for i in range(1, len(table)):
                if table[i][0] == last_X.cargo[0]:
                    # print(table[i][0], "hhhhh")
                    ind2 = i
                    break

            rule = table[ind2][ind1][0]
            # print(rule)
            rule = rule[rule.find(">") + 1:]
            # print('rule', rule)

            new_nonterm = ''
            for i in range(len(last_X.childs)):
                if rule[i] in nonterms and rule[i] == last_X.childs[i].cargo[0]:
                    # print('=========')
                    # print_tree(last_X)
                    if len(last_X.childs[i].childs) == 0:
                        new_nonterm = rule[i + 1]
                        break
            # print('new_nonterm', new_nonterm)

            last_nonterm = []
            T0_, T1_, s = inc_par1(new_tree, word_, last_X.cargo,
                                   new_nonterm, table, fullT0, x_mod, s, wrd0, False)
        else:
            # print('here', T1.cargo, T1.right_sibling.cargo)
            T1_ = T1.right_sibling
            T0_ = find_node(fullT0, len(wrd0) - s)
            # print(len(wrd0) - s)
        inc_par2(T0_, T1_, s, wrd0, wrd1, fullT0, fullT1, table)
    elif T0 != None:
        # print_tree(fullT1)
        word_ = ""
        last_X = find_last_nonterm(fullT1, table)
        # print('----------------------')
        # print_tree(last_X)
        first_child = last_X.childs[0].cargo
        term = first_child
        for c in last_X.childs:
            last_child = c.cargo
        ind1 = np.where(table[0] == term)

        ind2 = 0
        for i in range(1, len(table)):
            if table[i][0] == last_X.cargo[0]:
                # print(table[i][0], "hhhhh")
                ind2 = i
                break

        rule = table[ind2][ind1][0]
        # print(rule)
        rule = rule[rule.find(">") + 1:]
        # print('rule', rule)

        new_nonterm = ''
        for i in range(len(last_X.childs)):
            if rule[i] in nonterms and rule[i] == last_X.childs[i].cargo[0]:
                new_nonterm = rule[i + 1]
        # print('new_nonterm', new_nonterm)
        last_nonterm = []
        T0_, T1_, s = inc_par1(new_tree, word_, last_X.cargo,
                               new_nonterm, table, fullT0, x_mod, s, wrd0, False)
        inc_par2(T0_, T1_, s, wrd0, wrd1, fullT0, fullT1, table)
    return


def parent_def(tree, parent=None):
    global terms
    if tree != None:
        tree.parent = parent
        if tree.cargo not in terms:
            parent = tree
            if tree.childs != None:
                for chld in tree.childs:
                    parent_def(chld, parent)


def many_line_word(word):
    if word.count("$") > 0:
        word = word.replace("$", '')
        word = word.replace("\n", '')
    return word


def is_nonterm_child(childs):
    res = False
    global nonterm_with_nums
    for child in childs:
        # print(child, "!!!!!!!!!!!!!!!!!!!!!!!!!")
        if child.cargo in nonterm_with_nums:
            res = True
    return res


def read_gra(fname):
    f = open(fname, "r")
    raw_gra = f.read()
    lines = raw_gra.split('\n')
    for i in range(len(lines)):
        lines[i] = lines[i].replace(' ', '')
    gra = dict({})
    for i in lines:
        words = i.split('->')
        # print(words)
        prod = words[1].split('|')
        gra[words[0]] = prod
    # print("gra", gra)
    return gra


lastNon = []


def find_last_nonterm(tree, table):
    is_non_child = False

    if tree.childs is not None:
        first_child = tree.childs[0].cargo
        term = first_child
        # print(term, "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        ind1 = np.where(table[0] == term)
        ind2 = 0
        for i in range(1, len(table)):
            if table[i][0] == tree.cargo[0]:
                # print(table[i][0], "hhhhh")
                ind2 = i
                break

        rule = table[ind2][ind1][0]
        # print(rule)
        rule = rule[rule.find(">") + 1:]
        # print(rule, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        count_childs = 0
        for child in tree.childs:
            count_childs += 1
            if child.cargo in nonterm_with_nums:
                is_non_child = True
        # print(count_childs)
        if is_non_child and count_childs == len(rule):
            # print("0000000", tree.cargo)
            for child in tree.childs:
                if child.cargo in nonterm_with_nums:
                    return find_last_nonterm(child, table)
        else:
            # last_child = tree.childs[len(tree.childs)-1].cargo
            # for i in range(len(rule)):
            #     if rule[i] in nonterms and rule[i] == last_child[0]:
            #         new_nonterm = rule[i + 1]
            # print("uuuuuuuuu")
            return tree

    else:
        return tree


follow_set = dict({})
first_set = dict({})

terms = ['a', 'b', 'd', '@']
nonterms = ['S', 'A', 'B', 'C']

gra = read_gra("grammar2.txt")

word1 = 'abdd'
new_word = 'abadad'

for i in gra:
    first_set[i] = first(i, gra, nonterms)

for i in gra:
    follow_set[i] = follow(i, gra, nonterms)

print("Firsts: ", end='')
print(first_set)
print("Follows: ", end='')
print(follow_set)

word1 = 'baa'
new_word = 'bbaabaa'

word = many_line_word(word1)
new_word = many_line_word(new_word)


words = [word, new_word]
x_mod = os.path.commonprefix(words)
x_mod = len(x_mod)
# print('x', x_mod)
m = -1
z = 0
m = len(new_word) - z
# print(m)

l1 = len(new_word)
lo = len(word)
z_word = ""
while word[lo - 1] == new_word[l1 - 1] and lo-1!= x_mod and l1-1!=x_mod:
    z_word += word[lo - 1]
    lo -= 1
    l1 -= 1
z_word = z_word[::-1]
z_mod = len(z_word)
# print(z_word, "zzzzzzzzzz", z_mod)
# print(word)
table, ll = ll1_checker(gra, nonterms, terms)
if ll:
    tree, wrd = parser(word, table, 'S', nonterms, 0)
    # print('word', wrd)
    if wrd != '':
        for trm in wrd:
            # print(trm)
            st = stack.pop()
            if trm != st:
                print(word, " is wrong")
                sys.exit()
    if len(stack) > 0:
        print(word, " is wrong")
        sys.exit()

    right_sib(tree)
    num_nodes(tree)
    # print_tree(tree)
    # eps_num(tree)

    print("\nold tree")
    print_tree(tree)
    new_tree, oldword, newword, xmod, mm = transfer(
        tree, word, new_word, x_mod, m)

    # print(oldword, newword, xmod, mm, "[[[[[[[[[[[[[[[[[")
    # print_tree(new_tree)
    # print("NEW_WORD", new_word, x_mod, z_mod)

    y_ = new_word[x_mod:len(new_word)-z_mod]
    # print(y_, "-------")
    last_X = find_last_nonterm(new_tree, table)
    print_tree(last_X)
    # print("Last_X_Child", last_X.childs)
    for c in last_X.childs:
        term = c.cargo
    # print(term)
    ind1 = np.where(table[0] == term)
    # print(ind1)
    ind2 = 0
    for i in range(1, len(table)):
        if table[i][0] == last_X.cargo[0]:
            # print(table[i][0], "hhhhh")
            ind2 = i
            break
    # print(ind2, ind1)
    rule = table[ind2][ind1][0]
    # print(rule)
    rule = rule[rule.find(">") + 1:]
    # print(rule)
    for l in rule:
        if l in nonterms:
            new_nonterm = l
            break
    # print(new_nonterm)

    NT0, NT1, s = inc_par1(new_tree, y_, last_X.cargo, new_nonterm,
                           table, tree, x_mod, z_mod, word, True)

    parent_def(tree)
    parent_def(new_tree)

    inc_par2(NT0, NT1, s, word, new_word, tree, new_tree, table)

    print("\nnew tree")
    print_tree(new_tree)