def aci(term):
    left_ind = []
    left = 0
    right = 0
    counter = 0
    if term[0] != "(":
        term = "("+term+")"
    print(term)
    for i in term:
        print(counter, i)
        if i == "(":
            left += 1
            left_ind.append(counter)
            counter += 1
            continue
        if i == ")":
            right += 1
            if left != right:
                ind = left_ind.pop()+1
                new = aci(term[ind:counter])
                old = term[ind:counter]
                print(old)
                term = term.replace(old, new)
                counter += 1
                continue
        if left == right:
            lind = term.find("(")
            rind = term.find(")")
            term = term[lind+1:rind]
            term = list(set(term))
            print("qqqqqq", term)
            ind = []
            c = 0
            flag = True
            r = 0
            l = 0
            #
            for j in term:
                if j == "|":
                    if r == l:
                        ind.append(c)
                if j == "(":
                    l += 1
                if j == ")":
                    r += 1
                c += 1

            """if "|"in term:
                term=term.split('|')
                term.sort()
                print("ttttttttttttt",term)
                #for j in term:
            else:
                return term"""
        counter += 1

regex = input()
regex = regex.replace(' ', '')
aci(regex)