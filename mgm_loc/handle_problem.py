import handle_file as hf
import sys
import random as r
file = hf.file_name(sys.argv)
domain, variables , constraints , cons_dict , cons_for_var , agents= hf.get_data(file)
print("domain :",domain)
print("variables : ",variables)
print("constraints :",constraints)
print("cons_dict : ",cons_dict)
print("cons_for_var : ",cons_for_var)


def config_agents(variables,agents,constraints):
    '''
    Create a dictionary with all the details for each agent.
    :param variables: all the variables of the file, with their domain. type : dict
    :param agents: all the agents of the file. type : list
    :return: agents_param: all the agents with their parameters (variable, var value, neighbors). type : dict
    '''
    agents_param = {}
    all_var = []
    for var in variables.keys():
        all_var.append(var)
    for ag in range(len(agents)):
        actual_agent = {}
        actual_agent["variable"] = all_var[ag]
        actual_agent["constraint"] = constraints[all_var[ag]]
        actual_agent["value"] = None
        actual_agent["neighbors"] = {}
        actual_agent["neighbors_LR"] = {}
        agents_param[agents[ag]] = actual_agent
        for var2 in all_var:
            if var2 != actual_agent["variable"]:
                actual_agent["neighbors"][var2] = None
                actual_agent["neighbors_LR"][var2] = None
        actual_agent["cons_value"] = 0
        actual_agent["prev_cons_value"] = 0
        actual_agent["current_LR"] = None

    return agents_param


def init_agents(agents_param,domain):
    '''
    Initialize the algorithm, assigning one random value per variable
    :param agents_param:  all the agents with their parameters (variable, var value, neighbors). type : dict
    :param domain: all the values in the domain for this problem
    :return: agents_param:  all the agents with their parameters, and a random value. type : dict
    '''
    for agent in agents_param.values():
        for values in domain.values():
            random_val = r.choice(values)
            try:
                agent["value"]= random_val
            except:
                pass
    return agents_param

def send_values(agents_param):
    '''
    Create an iterable (a message) and put the new values of the variable inside.
    :param agents_param: all the agents with their parameters. type : dict
    :return: value_mess: all the new values of the variables. type : dict
    '''
    value_mess = {}
    for agent in agents_param.values():
        value_mess[agent["variable"]] = agent["value"]

    return value_mess

def collect_values(agents_param, value_mess):
    '''
    Indicate to each agent his neighbors' variable's value.
    :param agents_param: all the agents with their parameters. type : dict
    :param value_mess: all the values that the agents have sent. type : dict
    :return: agents_param: all the agents with their parameters and their neighbors new values. type : dict
    '''
    for agent in agents_param.values():
        for neighbor in agent["neighbors"]:
            for var in value_mess:
                if neighbor == var:
                    agent["neighbors"][neighbor] = value_mess[var]
    return agents_param


def calculate_constraint(agents_param,cons_dict,var_value):
    '''
    Compute the value of the constraint for each variable
    :param agents_param: all the agents with their parameters. type : dict
    :param cons_dict: formula of all the constraints. type : dict
    :param variables: all the variables with the domain they take their values from. type : dict
    :return: agents_param. All the agents with their parameters and their constraints value. type : dict
    '''


    for agent in agents_param.values():
        if len(agent["constraint"]) != 0:
            value = 0
            for i in range (len(agent["constraint"])):
                constraint = agent["constraint"][i]
                constraint_formula = cons_dict[constraint][0]
                formula = prepare_formula(constraint_formula, var_value)
                value += RVN(formula)
            agent["cons_value"] = str(value)
    return agents_param

def prepare_formula(constraint_formula, var_value):
    '''
    Get the formula of a constraint and change it in order to have an iterable, that can be used with Reverse Polish
    Notation
    :param constraint_formula:the formula of the constraint. type : str
    :param var_value:the variables and all their values. type : dict
    :return: formula_ready. The formula that can be used with the RVN. type : list
    '''
    formula = constraint_formula.split()
    formula_ready = []
    operator = ["+", "-", "/", "*"]
    for element in (formula):
        try:
            eval(element)
            value = float(element)
        except:
            if element in operator:
                opera = element
                continue
            else:
                value = var_value[element]
        formula_ready.append(value)
        try:
            formula_ready.append(opera)
        except:
            pass
    return formula_ready

def RVN(formula_ready):
    '''
    Use the RVN technic in order to get the value of a constraint, if this constraint depends of other variables.
    :param formula_ready: the formula that gives the value of the constrait. type : list
    :return: cons_value: the value of the constraint. type : float
    '''
    pile = []
    for elt in formula_ready:
        if elt == '+':
            b, a = pile.pop(), pile.pop()
            pile.append(a + b)
        elif elt == '-':
            b, a = pile.pop(), pile.pop()
            pile.append(a - b)
        elif elt == '*':
            b, a = pile.pop(), pile.pop()
            pile.append(a * b)
        elif elt == '/':
            b, a = pile.pop(), pile.pop()
            pile.append(a / b)
        else:
            pile.append(int(elt))
    cons_value = pile.pop() #Keep only the final result by popping the last operator
    return cons_value

def share_constraint_2(agent,prev_var_value):
    '''
    Update constraint value if it's necessary
    :param agent: an agent of the problem. type : dict
    :param prev_var_value: values of the variables during previous cycle. type : dict
    :return: cons_to_send: value of the constraints that have to be transfered, and the recipient. type : dict
    :return: agent: an agent of the problem, with his constraint updated
    '''
    cons_to_send = {}
    agent["prev_cons_value"] = agent["cons_value"]
    cond = False
    for neighbor in agent["neighbors"]:
        prev_var_value[neighbor]=float(agent["neighbors"][neighbor])
        actual_cons = calculate_constraint_agent(agent,cons_dict,prev_var_value)
        delta = float(agent["prev_cons_value"]) - float(actual_cons["cons_value"])
        if delta > 0:
            cond = True
            cons_to_send[neighbor] = agent["constraint"]

    if cond:
        agent["cons_value"] = 0
    return agent, cons_to_send

def share_constraint_1(agent,prev_var_value):
    '''
    Update constraint value if it's necessary
    :param agent: an agent of the problem. type : dict
    :param prev_var_value: values of the variables during previous cycle. type : dict
    :return: cons_to_send: value of the constraints that have to be transfered, and the recipient. type : dict
    :return: agent: an agent of the problem, with his constraint updated
    '''
    cons_to_send = {}
    agent["prev_cons_value"] = agent["cons_value"]
    cond = False
    for neighbor in agent["neighbors"]:
        prev_var_value[neighbor]=float(agent["neighbors"][neighbor])
        actual_cons = calculate_constraint_agent(agent,cons_dict,prev_var_value)
        delta = float(agent["prev_cons_value"]) - float(actual_cons["cons_value"])
        try :
            if delta > float(agent["neighbors_LR"][neighbor]):
                cond = True
                cons_to_send[neighbor] = agent["constraint"]
        except:
            pass

    if cond:
        agent["cons_value"] = 0
    return agent, cons_to_send

def update_cons(cons_to_send,agents_param):
    '''
    Update constraints for each variable by distributing constraints that must be transferred
    :param cons_to_send: the constraints that must be transferred. type : dict
    :param agents_param: all the agents with their parameters. type : dict
    :return: agents_param: all the agents with their parameters and the constraits updated. type : dict
    '''
    for agent in agents_param.values():
        for var,cons in cons_to_send.items():
            if var == agent["variable"]:
                for i in range (len(cons_to_send[var])):
                    agent["constraint"].append(cons[i])

    return agents_param

def get_var_value(agents_param):
    '''
    Get the values of each variable, anytime
    :param agents_param: all the agents with their parameters
    :return: var_value: values of each variable. type : dict
    '''
    var_value = {}

    for agent in agents_param.values():
        var_value[agent["variable"]] = int(agent["value"])
    return var_value

def calculate_constraint_agent(agent,cons_dict,var_value):
    '''
    Compute the value of the constraint for each variable
    :param agents_param: all the agents with their parameters. type : dict
    :param cons_dict: formula of all the constraints. type : dict
    :param variables: all the variables with the domain they take their values from. type : dict
    :return: agents_param. All the agents with their parameters and their constraints value. type : dict
    '''

    if len(agent["constraint"]) != 0:
        value = 0
        for i in range (len(agent["constraint"])):
            constraint = agent["constraint"][i]
            constraint_formula = cons_dict[constraint][0]
            formula = prepare_formula(constraint_formula, var_value)
            value += RVN(formula)
        agent["cons_value"] = str(value)
    return agent

def compute_LR(agent,domain):
    '''
    Try all the values with the constraint of a variable in order to find the best LR.
    :param: agent: an agent of the problem. type : dict
    :return: best_LR : the best possible local reduction in cost, with the value associated. type : list
    '''
    each_LR = {}
    var_values = {}
    for neighbor,neigh_val in agent["neighbors"].items():
        var_values[neighbor] = float(neigh_val)

    for new_value in domain["cost"]:
        var_values[agent["variable"]] = float(new_value)
        old_cons = float(agent["prev_cons_value"])
        new_cons = float(calculate_constraint_agent(agent,cons_dict,var_values)["cons_value"])
        LR = old_cons - new_cons
        each_LR[new_value] = [LR]
    value_best_LR = max_dict(each_LR)
    assoc_LR = each_LR[value_best_LR][0]
    best_LR = [assoc_LR,value_best_LR]
    agent["current_LR"] = float(assoc_LR)
    return best_LR

def all_LR(agents_param):
    '''
    Create an iterable with all the best LRs and the value associated, for all variables.
    :param agents_param: agents_param: all the agents with their parameters. type : dict
    :return: all_LR: all the LRs with their associated variable and value for this variable. type : dict
    '''
    all_LR = {}
    for agent in agents_param.values():
        current_var = agent["variable"]
        current_best_LR = compute_LR(agent,domain)
        all_LR[current_var] = current_best_LR

    return all_LR

def collect_LR(agents_param, all_LR):
    '''
    Indicate to each agent his neighbors' LR's value.
    :param agents_param: all the agents with their parameters. type : dict
    :param all_LR: all the LRs that the agents have sent. type : dict
    :return: all the agents with their parameters and their neighbors LRs. type : dict
    '''

    for agent in agents_param.values():
        for neighbor in agent["neighbors_LR"]:
            for var in all_LR:
                if neighbor == var:
                    agent["neighbors_LR"][neighbor] = all_LR[var][0]
    return agents_param

def update_value(agents_param,all_LR):
    '''
    Update the value of a variable chosen thanks to its LR.
    :param agents_param: all the agents with their parameters. type : dict
    :param all_LR: all the LRs with their associated variable and value for this variable. type : dict
    :return: agents_param: all the agents with their parameters, and the value updated. type : dict
    '''
    key = max_dict(all_LR)
    for agent in agents_param.values():
        if agent["variable"] == key:
            agent["value"] = all_LR[key][1]

    return agents_param


def max_dict(dictio):
    '''
    Compute the index associated to the max value in a dictionary of iterable.
    :param dictio: the iterable in which we want to ave the index of the max value. type : dict
    :return: key: the index of the maximum value. type : str
    '''
    values = []
    for i in dictio.values():
        values.append(float(i[0]))

    maximum = max(values)
    for k, val in dictio.items():
        if maximum == float(val[0]):
            key = k

    return key

def show_result(agents_param,file,algo):
    '''
    how the results; with the value of each variable and the constraints cost for each variable
    :param agents_param: all the agents with the final parameters. type : dict
    :return: None
    '''
    with open("Results/{}_results_{}.yaml".format(file.strip(".yaml"),algo.strip(".py")),'w') as f:
        f.write("Assignments :"+"\n")
        for agent in agents_param.values():
            f.write(agent["variable"]+" : "+ str(agent["value"])+"\n")
        f.write("\n")
        f.write("Costs :"+"\n")
        for agent in agents_param.values():
            f.write(agent["variable"]+" : "+str(agent["cons_value"])+"\n")
        f.write("\n")
        f.write("Total cost : ")
        cost = 0
        for agent in agents_param.values():
            cost += float(agent["cons_value"])
        f.write(str(cost))


