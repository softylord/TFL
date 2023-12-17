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
    print(t+a)
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
                        if i != (len(prod)-1):
                            next_str = prod[(i+1):]
                            first_str = first(next_str, gra, nonterm)
                            if '@' in first_str:
                                follow_ = follow_ | (first_str-{'@'})
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
    mat = np.array([["0"]*(len(term)+2)]*(len(nonterm)+1))
    mat = mat.astype('<U100')
    term.append('~')
    # print("Terms", term)
    for i in range((len(nonterm)+1)):
        for j in range((len(term)+1)):
            if i == 0 and j >= 1:
                mat[i, j] = term[j-1]
            elif i >= 1 and j == 0:
                mat[i, j] = nonterm[i-1]
    # print(mat)

    isll1 = True

    for left_v in gra:
        row_n = nonterm.index(left_v)+1
        for prod in gra[left_v]:
            first_rule = first(prod, gra, nonterm)
            if '@' in first_rule:
                first_rule = first_rule-{'@'}
                first_rule = first_rule | follow_set[left_v]
            for i in first_rule:
                col_n = term.index(i)+1
                if mat[row_n, col_n] == '0':
                    mat[row_n, col_n] = left_v+'->'+prod
                else:
                    mat[row_n, col_n] = mat[row_n, col_n]+'\n'+left_v+'->'+prod
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


def parser(word, table, nonterm,  nonterm_list, tabs):
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
        print("Word is not for this grammar")
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
                        print("Word is not for this grammar")
                        sys.exit()
                    if len(ind1) == 0:
                        print("Word is not for this grammar")
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
            print("Word is not for this grammar")
            sys.exit()
    main_rule = rule.split('->')[1]
    # print(main_rule)
    chld = []
    last = False
    for symb in main_rule:
        if symb not in nonterm_list:
            node = Tree(symb, tabs+1)
            chld.append(node)
            if last:
                stack.append(symb)
                # print("stack", stack)
            elif symb != '@':
                word = word[1:]
        else:
            last = True
            node, word = parser(word, table, symb, nonterm_list, tabs+1)
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


count_nodes = 0
nonterm_with_nums = []


def num_nodes(tree):
    global count_nodes, nonterm
    if tree.childs is not None:
        for child in tree.childs:
            if child.cargo in nonterm:

                if child.childs[0].cargo != '@':
                    count_nodes += 1
                child.cargo = str(child.cargo) + str(count_nodes)
                # if child.childs[0].cargo!='@':
                #     count_nodes+=1
                nonterm_with_nums.append(child.cargo)
        for child in tree.childs:
            num_nodes(child)


chisla = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


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
                        child.cargo = carg+num
        for child in tree.childs:
            eps_num(child)


list_of_siblings = []
# [[L,R]]


def right_sib(tree):
    list_of_nonterm_childs = []
    global list_of_siblings
    if tree.cargo in nonterm or tree.cargo in nonterm_with_nums:
        # print(len(tree.childs), "====")
        if len(tree.childs) > 0:
            for i in tree.childs:
                # print(i.cargo, "PPPPPPPPPPPPPPP", i.cargo in nonterm)
                if i.cargo in nonterm or i.cargo in nonterm_with_nums:
                    list_of_nonterm_childs.append(i)
                    # print(i, "000000000")
            for i in range(len(list_of_nonterm_childs)-1):
                list_of_siblings.append(
                    [list_of_nonterm_childs[i].cargo, list_of_nonterm_childs[i+1].cargo])
                # print(type(list_of_nonterm_childs[i]))
                list_of_nonterm_childs[i].right_sibling = list_of_nonterm_childs[i+1]
                # list_of_siblings.append([tree.childs[i].cargo, tree.childs[i+1].cargo])
        if tree.right_sibling is not None and len(list_of_nonterm_childs) != 0:
            list_of_nonterm_childs[len(
                list_of_nonterm_childs)-1].right_sibling = tree.right_sibling
            list_of_siblings.append([list_of_nonterm_childs[len(
                list_of_nonterm_childs)-1].cargo, tree.right_sibling.cargo])
    if tree.childs is not None:
        for i in tree.childs:
            right_sib(i)

def transfer(old_tree, old_word, new_word, x_mod, m):
    if old_tree!=None:
        if old_word[0]==new_word[0]:
            
            new_chlds=[]
            node=old_tree.childs[0]
            new_chlds.append(node)
            x_mod-=1
            m-=1
            old_word=old_word[1:]
            new_word=new_word[1:]
            for child in old_tree.childs[1:]:
                if x_mod!=0:
                    node, old_word, new_word, x_mod, m=transfer(child, old_word, new_word, x_mod, m)
                    if node!=None:
                        print('here')
                        new_chlds.append(node)
                else:
                    break
            new_tree=Tree(old_tree.cargo, old_tree.tabs, new_chlds)
            return new_tree, old_word, new_word, x_mod, m
    return



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

# def right_sibling()


follow_set = dict({})
first_set = dict({})

nonterm = []
term = ['a', 'b', 'd', '@']

n_nonterm = 4
nonterm = ['S', 'A', 'B', 'C']

gra = read_gra("grammar2.txt")

for i in gra:
    first_set[i] = first(i, gra, nonterm)

for i in gra:
    follow_set[i] = follow(i, gra, nonterm)

print("Firsts: ", end='')
print(first_set)
print("Follows: ", end='')
print(follow_set)


def many_line_word(word):
    if word.count("$") > 0:
        word = word.replace("$", '')
        word = word.replace("\n", '')
    return word


word1 = 'abada'
word2 = """bbbb$
bbbb$
bbbd$"""
word3 = "aabda"
word = many_line_word(word1)
new_word = 'ababd'

words=[word, new_word]
x_mod=os.path.commonprefix(words)
x_mod=len(x_mod)
print('x', x_mod)
m=-1
z=0
while word[m]==new_word[m]:
    z=m
    m-=m
m=len(new_word)-z
print(m)
# print(word)
table, ll = ll1_checker(gra, nonterm, term)
if ll:
    tree, wrd = parser(word, table, 'S', nonterm, 0)
    # print('word', wrd)
    if wrd != '':
        for trm in wrd:
            # print(trm)
            st = stack.pop()
            if trm != st:
                print(word, " is wrong")
    if len(stack) > 0:
        print(word, " is wrong")
    print('\nTree:')
    num_nodes(tree)
    right_sib(tree)
    eps_num(tree)
    new_tree, _, _ ,_, _=transfer(tree, word, new_word, x_mod, m)
    print_tree(new_tree)
