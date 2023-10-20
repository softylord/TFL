import sys

class Tree:
    def __init__(self, cargo, left=None, right=None, parent=None):
        self.cargo = cargo
        self.left  = left
        self.right = right
        self.parent=parent

    def __str__(self):
        return str(self.cargo)
    def __eq__(self, other):
        if self is None and other is None:
            return True
        if self is not None and other is None:
            return False
        if self is None and other is not None:
            return False
        if self is not None and other is not None:
            return (self.cargo==other.cargo) \
              and (self.left == other.left) and (self.right == other.right)
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
    if get_token(token_list, '<'):
        token_list[:token_list.index('>')+1]=[]
        x='<eps>'
        return Tree(x, None, None)
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
        b=get_conc(token_list)
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
    if tree!=None:
        if tree.left!=None:
            left=back(tree.left)
            #print('left', left, type(left))
            right=None
            if tree.right!=None: 
                right=back(tree.right)
                #print(right)
            if tree.cargo=='conc':
                #print(tree.right.cargo, tree.left.cargo)
                if left=='<eps>':
                    s=right
                elif right=='<eps>':
                    s=left
                else:
                    s=left+right
                if tree.parent=='*' and len(s)>1:
                    s='('+s+')'
                return s
            elif tree.cargo=='*':
                if left!='<eps>':
                    s=left+'*'
                return s
            elif tree.cargo=='|':
                if left!='<eps>' or right!='<eps>':
                    ind=len(right)
                    if right.find('|')!=-1:
                        ind=right.find('|')
                    if left == right[:ind]:
                        s=right
                    else:
                        #print(left,right)
                        s=left+'|'+right

                    if tree.parent=='*' or tree.parent=='conc':
                        s='('+s+')'
                else:
                    s='<eps>'
                #print("fff", s)
                return s
            else:
                #print("why")
                return tree.cargo
        else:
            return str(tree.cargo)
    else:
        return s
    
def find_star(tree):
    if tree==None:
        return False
    elif tree.cargo=='*':
        #print("888888", tree.cargo)
        return True
    else:
        #print("999", tree.cargo)
        return (find_star(tree.left)) or (find_star(tree.right))
    
def ssnf(tree):
    if tree!=None:
        if tree.cargo==None:
            #print("baaad")
            return 
        if tree.cargo!='conc' and tree.cargo!='|' and tree.cargo!='*':
            return Tree(tree.cargo, None, None)
        if tree.cargo=='|':
            tree.left=ssnf(tree.left)
            tree.right=ssnf(tree.right)
            return Tree('|', ssnf(tree.left), ssnf(tree.right))
        if tree.cargo=='conc':
            tree.left=ssnf(tree.left)
            tree.right=ssnf(tree.right)
            return Tree('conc', ssnf(tree.left), ssnf(tree.right))
        if tree.cargo == '*':
            """print('llllllllllllllllllll0')
            print_tree(ss(tree.left))
            print('llllllllllllllllllll2')"""
            tree.left=ss(tree.left)

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
        #tree.left=ss(tree.left)
        #tree.right=ss(tree.right)
       # print('++++++++++++++')
        #print_tree(tree.left)
        #print_tree(tree.right)
        if find_star(tree):
           
            
            return Tree('|', ss(tree.left), ss(tree.right))
        else:
            #print("ppppp", ssnf(tree.left), ssnf(tree.right))
            tree.left=ssnf(tree.left)
            tree.right=ssnf(tree.right)
            return Tree('conc', ssnf(tree.left), ssnf(tree.right))
    if tree.cargo == '*':
        """print("aaaaaaaaaaaaaaaaaaaaaaaa")
        print_tree(ss(tree.left))
        print(';;;;;;;;;;')"""
        return ss(tree.left)

def rotate(tree):
    if tree.cargo==None:
        return
    temp=tree.left
    tree.left=tree.right
    tree.right=temp

def aci(tree):
    op=['|', 'conc', '*']
    if tree==None:
        return
    elif tree.cargo!='|':
        tree.left=aci(tree.left)
        tree.right=aci(tree.right)
        return Tree(back(tree), None, None, tree.parent)
        return tree
    else:
        tree.left=aci(tree.left)
        tree.right=aci(tree.right)

        left=tree.left.cargo
        right=tree.right.cargo
        if left not in op and right not in op:
            #print(left, right)
            charl=""
            charr=""
            i=0
            if left!="":
                while left[i]=='(':
                    i+=1
                    #print(i)
                if i!=0:
                    charl=left[i:left.find(')')]
                else:
                    charl=left

            i=0
            if right!="":
                while right[i]=='(':
                    i+=1
                if i!=0:
                    charr=right[i:right.find(')')]
                else:
                    charr=right
            #print(charl, charr)
            if charl>charr:
                rotate(tree)
            
        if left=='*':
            lt_lt=tree.left.left.cargo
            if lt_lt not in op:
                #print(left, rt_lt)
                i=0
                while left[i]=='(':
                    i+=1
                char=left[i:left.find(')')]
                if char>rt_lt:
                    temp=tree.left
                    tree.left=tree.right.left
                    tree.right.left=temp
                    """print("---------------")
                    print_tree(tree)
                    print("---------------")"""
            tree.left=aci(tree.left)
            tree.right=aci(tree.right)

        if right=='|':
            #print("pp", left)
            #tree = Tree(tree.cargo, aci(tree.left), aci(tree.right), tree.parent)
            """print('===========')
            print_tree(tree)
            print('===========')"""
            rt_lt=tree.right.left.cargo
            #print("gg", left, rt_lt, rt_rt)
            if rt_lt not in op:
                print(left, rt_lt)
                i=0
                while left[i]=='(':
                    i+=1
                ind=1
                if left.find(')')!=-1:
                    ind=left.find(')')
                char=left[i:ind]
                if char>rt_lt:
                    temp=tree.left
                    tree.left=tree.right.left
                    tree.right.left=temp
                    """print("---------------")
                    print_tree(tree)
                    print("---------------")"""
            tree.left=aci(tree.left)
            tree.right=aci(tree.right)

                
        return tree

def init_parents(tree):
    if tree!=None:
        if tree.left!=None:
            tree.left.parent=tree.cargo
            tree.left=init_parents(tree.left)
        if tree.right!=None:
            tree.right.parent=tree.cargo
            tree.right=init_parents(tree.right)
        return tree
    return

def dstr(tree):
    op=['|', 'conc', '*']
    flag=False
    if tree==None:
        return
    elif tree.cargo!='|':
        tree.left=dstr(tree.left)
        tree.right=dstr(tree.right)
        #return Tree(back(tree), None, None, tree.parent)
        return tree
    else:
        tree.left=dstr(tree.left)
        tree.right=dstr(tree.right)

        left=tree.left.cargo
        right=tree.right.cargo
        #print(left, right)
        """if left not in op and right not in op:
            #print(left, right)
            i=0
            while left[i]=='(':
                i+=1
            char=left[i:left.find(')')]
            if char>right:
                rotate(tree)"""
            
        if left=='conc':
            lt_lt=tree.left.left
            lt_rt=tree.left.right
            rt_lt=tree.right.left
            rt_rt=tree.right.right
            if right =='conc':
                if lt_lt == rt_lt:
                    rt_tree= Tree('|', tree.left.right, tree.right.right, 'conc')
                    tree = Tree ('conc', tree.left.left, rt_tree, tree.parent)
                    flag=True
                elif lt_rt==rt_rt:
                    lt_tree = Tree ('|', tree.left.left, tree.right.left, 'conc')
                    tree = Tree ('conc', lt_tree, tree.left.right, tree.parent)
                    flag=True
            if right == '|':
                if rt_lt.cargo=='conc':
                    rt_lt_lt=tree.right.left.left
                    rt_lt_rt=tree.right.left.right
                    #print(lt_rt, rt_lt_rt)
                    if lt_lt == rt_lt_lt:
                        lt_rt_tree=Tree('|', tree.left.right, tree.right.left.right, 'conc')
                        lt_tree=Tree('conc', tree.left.left, lt_rt_tree, tree.cargo)
                        tree=Tree(tree.cargo, lt_tree, tree.right.right, tree.parent)
                        flag=True
                    elif lt_rt==rt_lt_rt:
                        #print("here")
                        lt_lt_tree=Tree('|', tree.left.left, tree.right.left.left, 'conc')
                        lt_tree=Tree('conc', lt_lt_tree, tree.left.right, tree.cargo)
                        tree=Tree(tree.cargo, lt_tree, tree.right.right, tree.parent)
                        flag=True
        if left not in op:
            if right=='conc':
                rt_lt=tree.right.left.cargo
                rt_rt=tree.right.right.cargo
                if left==rt_lt:
                    rt_rt_tree= Tree('<eps>', None, None, '|')
                    rt_tree= Tree('|', tree.right.right, rt_rt_tree, 'conc')
                    tree = Tree ('conc', tree.left, rt_tree, tree.parent)
                    flag=True
                elif left==rt_rt:
                    rt_rt_tree= Tree('<eps>', None, None, '|')
                    rt_tree= Tree('|', tree.right.left, rt_rt_tree, 'conc')
                    tree = Tree ('conc', rt_tree, tree.left, tree.parent)
                    flag=True
            if right=='|':
                rt_lt=tree.right.left.cargo
                rt_rt=tree.right.right.cargo
                if rt_lt=='conc':
                    rt_lt_lt=tree.right.left.left.cargo
                    rt_lt_rt=tree.right.left.right.cargo
                    
                    #print(left, rt_lt_lt)
                    if left == rt_lt_lt:
                        eps_tree=Tree('<eps>', None, None, '|')
                        lt_rt_tree=Tree('|', eps_tree, tree.right.left.right, 'conc')
                        lt_tree=Tree('conc', tree.left, lt_rt_tree, tree.cargo)
                        tree=Tree(tree.cargo, lt_tree, tree.right.right, tree.parent)
                        flag=True
                    elif left==rt_lt_rt:
                        #print("here")
                        eps_tree=Tree('<eps>', None, None, '|')
                        lt_lt_tree=Tree('|', eps_tree, tree.right.left.left, 'conc')
                        lt_tree=Tree('conc', lt_lt_tree, tree.left, tree.cargo)
                        tree=Tree(tree.cargo, lt_tree, tree.right.right, tree.parent)
                        flag=True
            
        if flag:
            tree=dstr(tree)
          
        return tree
    
def balance(regex):
    bal=0
    for i in range(len(regex)):
        a = regex[i]
        if a == '(':
            bal += 1
        elif a == ")":
            bal -= 1
        # print(constr, "\n", balance)
    if bal > 0:
        print("Error! Some \")\" was missed")
        sys.exit()
    elif bal < 0:
        print("Error! Some \"(\" was missed")
        sys.exit()

def half_norm(regex):
    regex = regex.replace(' ', '')
    balance(regex)
    tokens=list(regex)
    tokens.append('end')
    tree = get_alt(tokens)
    """print_tree(tree)
    print(back(tree))
    print('-----------------')"""
    tree2=ssnf(tree)
    #print_tree(tree2)
    #print(back(tree2))
    tree2=init_parents(tree2)
    tree3=aci(tree2)
    return back(tree3)

def normalize(regex):
    #print("here")
    regex = regex.replace(' ', '')
    balance(regex)
    tokens=list(regex)
    tokens.append('end')
    tree = get_alt(tokens)
    print_tree(tree)
    print('-----------------')
    tree2=ssnf(tree)
    #print_tree(tree2)
    #print(back(tree2))
    tree2=init_parents(tree2)
    tree3=aci(tree2)
    #print("1", back(tree3))

    tokens=list(back(tree3))
    tokens.append('end')
    tree = get_alt(tokens)
    tree = init_parents(tree)
    #print_tree(tree)
    tree2= dstr(tree)
    tree2= aci(tree2)
    return back(tree2)
    
def main():
    regex = input()
    """regex = regex.replace(' ', '')
    balance(regex)
    tokens=list(regex)
    tokens.append('end')
    tree = get_alt(tokens)
    print_tree(tree)
    print(back(tree))
    print('-----------------')
    tree2=ssnf(tree)
    #print_tree(tree2)
    #print(back(tree2))
    tree2=init_parents(tree2)
    tree3=aci(tree2)
    #print("1", back(tree3))

    tokens=list(back(tree3))
    tokens.append('end')
    tree = get_alt(tokens)
    tree = init_parents(tree)
    #print_tree(tree)
    tree2= dstr(tree)
    tree2= aci(tree2)"""

    print(normalize(regex))

main()