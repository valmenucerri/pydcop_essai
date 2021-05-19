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
        agents_param[agents[ag]] = actual_agent
        for var2 in all_var:
            if var2 != actual_agent["variable"]:
                actual_agent["neighbors"][var2] = None
        actual_agent["cons_value"] = 0
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
    Create an iterable and put the new values of the variable inside.
    :param agents_param: all the agents with their parameters. type : dict
    :return: value_mess: all the new values of the variables. type : dict
    '''
    value_mess = {}
    for agent in agents_param.values():
        value_mess[agent["variable"]] = agent["value"]

    return value_mess

def collect_values(agents_param, value_mess):
    '''
    Indicate to each agent his variable's neighbor's value.
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


def calculate_constraint(agents_param,cons_dict):
    '''
    Compute the value of the constraint for each variable
    :param agents_param:
    :param cons_dict:
    :param variables:
    :return:
    '''
    var_value = {}

    for agent in agents_param.values():
        var_value[agent["variable"]] = int(agent["value"])

    for agent in agents_param.values():
        constraint = agent["constraint"][0]
        constraint_formula = cons_dict[constraint][0]
        formula = prepare_formula(constraint_formula, var_value)
        agent["cons_value"] = str(RVN(formula))
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
    cons_value = pile.pop()
    return cons_value
agents_param = config_agents(variables, agents,constraints)

agents_param = init_agents(agents_param,domain)
nouvelle = send_values(agents_param)
print("valeurs envoyees : ",nouvelle)
nouv = collect_values(agents_param,nouvelle)
print("après collecte : ",nouv)
print(calculate_constraint(agents_param,cons_dict))