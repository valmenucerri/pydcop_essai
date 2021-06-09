import sys
import random as r
def create_cons(var,operator,numbers):
    '''
    Create a constraint formula with each variable, random numbers and random operators
    :param var: all the variables. type : list
    :param operator: all the possible operators. type : list
    :param numbers: all the numbers that can be added in the formula. type : list
    :return: formula: the formula for the constraint. type : str
    '''
    formula = []
    ite = r.randint(1,len(var))
    for i in range(ite):
        if len(formula) == 0:
            formula.append(r.choice(var))
            ope = r.choice(operator)
        else:
            ope = r.choice(operator)
        formula.append(ope)
        nbr_magic = r.randint(0,len(var))
        if nbr_magic%2 == 0:
            formula.append(r.choice(var))
        else:
            formula.append(str(r.choice(numbers)))
        if ope == "*":
            try:
                operator.remove("*")
                operator.remove("/")
            except:
                pass
        elif ope == "/":
            try:
                operator.remove("/")
                operator.remove("*")
            except:
                pass

    if "*" in formula:
        ind = formula.index("*")
        false_ope = formula[1]
        formula[1] = formula[ind]
        formula[ind] = false_ope
    elif "/" in formula:
        ind = formula.index("/")
        false_ope = formula[1]
        formula[1] = formula[ind]
        formula[ind] = false_ope
    if formula[2] == '0':
        formula[2] = '1'
    formula = " ".join(formula)
    return formula



nbr_var = int(sys.argv[-1])
numbers = [0 for y in range(nbr_var)]
operator = ["+", "-", "/", "*"]
for j in range(nbr_var):
    numbers.append(j)
    numbers.append(1)
var = []
cons= []
agents = []
a=ord('a')
assigned = 0
alph=[chr(i) for i in range(a,a+26)]
for letter in alph:
    for i in range(10):
        var.append("{}{}".format(letter,i))
        cons.append("C{}".format(i))
        agents.append("a{}".format(i))
        assigned += 1
        if assigned == nbr_var:
            break
    if assigned == nbr_var:
        break
agents =", ".join(agents)
with open("Graph/graph_exemple_{}.yaml".format(str(nbr_var)),'w')as f:
    f.write("name: "+"graph_exemple_{}".format(str(nbr_var))+"\n")
    f.write("objective: max"+"\n")
    f.write("\n")
    f.write("domains:"+"\n")
    f.write("  cost:"+"\n")
    f.write("    values: [0,1,2]"+"\n")
    f.write("\n")
    f.write("variables:"+"\n")
    for vars in var:
        f.write("  {}:".format(vars)+"\n")
        f.write("    domain: cost"+"\n")
    f.write("\n")
    f.write("constraints:"+"\n")
    ind_var = 0
    for c in cons:
        f.write("    {}:".format(c)+"\n")
        f.write("      type: extensional"+"\n")
        f.write("      variables: {}".format(var[ind_var])+"\n")
        f.write("      function: "+create_cons(var,operator,numbers)+"\n")
        ind_var += 1
    f.write("\n")
    f.write("\n")
    f.write("\n")
    f.write("agents: ")
    f.write("["+agents+"]")





