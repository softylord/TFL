class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left  = left
        self.right = right

    def __str__(self):
        return str(self.cargo)


def get_token(token_list, expected):
    if token_list[0] == expected:
        del token_list[0]
        return True
    else:
        return False

def get_char(token_list):
    if get_token(token_list, '('):
        x = get_alt(token_list)         # get the subexpression
        get_token(token_list, ')')      # remove the closing parenthesis
        return x
    else:
        x = token_list[0]
        #print("ffffffffffffffffffffff", x)
        if type(x) != type('') or x=='end': return None
        token_list[0:1] = []
        return Tree(x, None, None)

def get_star(token_list):
    #print(token_list, "a")
    a = get_char(token_list)
    #print(token_list, "aa")
    if get_token(token_list, '*'):
        #print(token_list, "b")

        #b = get_product(token_list)
        return Tree('*', a, None)
    else:
        return a

def get_conc(token_list):
    a=get_star(token_list)
    b=get_star(token_list)
    return Tree('conc', a, b)

def get_alt(token_list):
    a = get_conc(token_list)
    if get_token(token_list, '|'):
        print("hhh")
        b = get_alt(token_list)
        return Tree('|', a, b)
    else:
        return a
    
def print_tree(tree):
    if tree == None: return
    print (tree.cargo)
    print_tree(tree.left)
    print_tree(tree.right)
    
regex=input()
tok=list(regex)

tok.append('end')
print(tok)

token_list = ['a', '|', 'b', '*', 'end']
#token_list = ['a, '|', b', 'end']
tree = get_alt(tok)
print_tree(tree)