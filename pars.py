class Tree:
    def __init__(self, cargo, left=None, right=None):
        self.cargo = cargo
        self.left  = left
        self.right = right

    def __str__(self):
        return str(self.cargo)
    

def check_char(token_list):
    if token_list[0]!='|' and token_list[0]!='end' and token_list[0]!='*' and token_list[0]!=')':
        return True
    else:
        return False

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
        subtree=a
        #print(token_list, "b")
        while token_list[0]=='*':
            helper=Tree('*', subtree, None)
            subtree=helper
            token_list[0:1] = []
        #b = get_product(token_list)
        return Tree('*', subtree, None)
    else:
        return a


def get_conc(token_list):
    a=get_star(token_list)
    if check_char(token_list):
        #print("hi", token_list)
        b=get_alt(token_list)
        return Tree('conc', a, b)
    else:
        return a

def get_alt(token_list):
    a = get_conc(token_list)
    if get_token(token_list, '|'):
        #print("hhh")
        b = get_alt(token_list)
        return Tree('|', a, b)
    else:
        return a
    
def print_tree(tree):
    if tree == None: return
    print (tree.cargo)
    print_tree(tree.left)
    print_tree(tree.right)

def back(tree):
    s=""
    #print("fooooo", tree.cargo, type(tree.cargo))
    if tree.left!=None:
        left=back(tree.left)
        #print('left', left, type(left))
        right=None
        if tree.right!=None: 
            right=back(tree.right)
        if tree.cargo=='conc':
            s=left+right
            return s
        elif tree.cargo=='*':
            if tree.left.cargo=='|' or tree.left.cargo == 'conc':
                s="("+left+")"+"*"
            else:
                #print("gggggg", left)
                s=left+"*"
            return s
        elif tree.cargo=='|':
            s=left+'|'+right
            return s
        else:
            #print("why")
            return tree.cargo
    else:
        return str(tree.cargo)
    
def ssnf(tree):
    if tree.cargo==None:
        print("baaad")
        return 
    if tree.cargo!='conc' and tree.cargo!='|' and tree.cargo!='*':
        return Tree(tree.cargo, None, None)
    if tree.cargo=='|':
        return Tree('|', ssnf(tree.left), ssnf(tree.right))
    if tree.cargo=='conc':
        return Tree('conc', ssnf(tree.left), ssnf(tree.right))
    if tree.cargo == '*':
        """print('llllllllllllllllllll0')
        print_tree(ss(tree.left))
        print('llllllllllllllllllll2')"""

        return Tree('*', ss(tree.left), None)

def ss(tree):
    if tree.cargo==None:
        return 
    if tree.cargo!='conc' and tree.cargo!='|' and tree.cargo!='*':
        #print("oo", tree.cargo)
        return Tree(tree.cargo, None, None)
    if tree.cargo=='|':
        return Tree('|', ss(tree.left), ss(tree.right))
    if tree.cargo=='conc':
        if tree.left.cargo=='*' and tree.right.cargo=='*':
            return Tree('|', ss(tree.left), ss(tree.right))
        else:
            #print("ppppp", ssnf(tree.left), ssnf(tree.right))
            return Tree('conc', ssnf(tree.left), ssnf(tree.right))
    if tree.cargo == '*':
        """print("aaaaaaaaaaaaaaaaaaaaaaaa")
        print_tree(ss(tree.left))
        print(';;;;;;;;;;')"""
        return ss(tree.left)
    
regex=input()
tok=list(regex)
tok.append('end')
#print(tok)
#token_list = ['a', '|', 'b', '*', 'end']
#token_list = ['a, '|', b', 'end']

tree = get_alt(tok)
#print_tree(tree)
#print('-----------------')
tree2=ssnf(tree)
#print_tree(tree2)
print(back(tree2))