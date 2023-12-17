import numpy as np
from prettytable import PrettyTable
import sys


class Tree:
    def __init__(self, cargo, tabs=0, childs=None, parent=None):
        self.cargo = cargo
        self.childs = childs
        self.parent = parent
        self.tabs = tabs

    def __str__(self):
        return str(self.cargo)

    def __eq__(self, other):

        if self is not None and other is not None:
            return (self.cargo == other.cargo) \
                and (self.cilds == other.childs)
        else:
            return False


def print_tree(tree):
    if tree == None:
        return
    t = ''
    for i in range(tree.tabs):
        t += '  |'
    a = tree.cargo
    print(t+a)
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


def parser(word, table, nonterm,  nonterm_list, tabs):
    if len(word) > 0:
        term = word[0]
    if word == '':
        term = '~'
    # ищем индекс терма в первой строке таблы,
    # потом ищем строку, начинающуюся с нонтерма,
    # в ней берем правило по индексу терма
    #TODO: нафигачить многострочные слова
    ind1 = np.where(table[0] == term)
    ind2 = 0
    for i in range(1, len(table)):
        if table[i][0] == nonterm:
            ind2 = i
            break
    rule = table[ind2][ind1][0]
    #print('rule', rule)
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
            elif symb!='@':
                word = word[1:]
        else:
            last = True
            node, word = parser(word, table, symb, nonterm_list, tabs+1)
            chld.append(node)
    tree = Tree(nonterm, tabs, chld)
    return tree, word
#TODO: нафигачить ближайшего правого соседа и нумерование нод

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

word = 'aabda'
table, ll = ll1_checker(gra, nonterm, term)
if ll:
    tree, wrd = parser(word, table, 'S', nonterm, 0)
    # print('word', wrd)
    if wrd != '':
        for trm in wrd:
            #print(trm)
            st = stack.pop()
            if trm != st:
                print(word, " is wrong")
    if len(stack) > 0:
        print(word, " is wrong")
    print('\nTree:')
    print_tree(tree)
