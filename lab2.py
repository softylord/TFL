import sys

class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left  = left
        self.right = right

    def __str__(self):
        return str(self.cargo)

tree=Tree()

"""def make_tree(regex):
    global tree
    left=0
    right=0
    counter=0
    for i in regex:
        if
        counter+=1"""

def get_token(token_list, expected):
    if token_list[0] == expected:
        del token_list[0]
        return True
    else:
        return False

def get_number(token_list):
    if get_token(token_list, '('):
        x = get_sum(token_list)         # get the subexpression
        get_token(token_list, ')')      # remove the closing parenthesis
        return x
    else:
        x = token_list[0]
        if type(x) != type(0): return None
        token_list[0:1] = []
        return Tree(x, None, None)

def get_product(token_list):
    a = get_number(token_list)
    if get_token(token_list, '*'):
        b = get_product(token_list)
        return Tree('*', a, b)
    else:
        return a
    
def get_sum(token_list):
    a = get_product(token_list)
    if get_token(token_list, '+'):
        b = get_sum(token_list)
        return Tree('+', a, b)
    else:
        return a
    



regex = input()
regex = regex.replace(' ', '')

balance=0
for i in range(len(regex)):
    a = regex[i]
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

#aci(regex)