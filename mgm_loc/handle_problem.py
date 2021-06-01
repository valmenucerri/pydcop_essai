import handle_file as hf
import sys
import random as r
import matplotlib.pyplot as plt
import pylab

file = hf.file_name(sys.argv)
domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(file)
print("domain :", domain)
print("variables : ", variables)
print("constraints :", constraints)
print("cons_dict : ", cons_dict)
print("cons_for_var : ", cons_for_var)
print(agents)


def config_agents(variables, agents, constraints):
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


def init_agents_contr(agents_param, domain):
    '''
    Initialize the algorithm, assigning one random value per variable
    :param agents_param:  all the agents with their parameters (variable, var value, neighbors). type : dict
    :param domain: all the values in the domain for this problem
    :return: agents_param:  all the agents with their parameters, and a random value. type : dict
    '''
    for agent in agents_param.values():
        if agent["variable"] == "vA":
            agent["value"] = str(2)
        if agent["variable"] == "vB":
            agent["value"] = str(2)
        if agent["variable"] == "vC":
            agent["value"] = str(0)
    return agents_param


def init_agents(agents_param, domain):
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
                agent["value"] = random_val
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

def min_function_result(cons,var_value):
    """
    Compute the constraint's cost if its formula is a min function.
    :param cons: the formula of the constraint. type : str
    :param var_value: the values of all variables. type : dict
    :return: value_returned: value of the considered constraint. type : float
    """
    operator = ["+", "-", "/", "*"]
    cons = cons.strip("min" +"max" + "(" + ")" + "[" + "]")
    cons_list = cons.split(',')
    for element in range(len(cons_list)):
        nbr = False
        opera = False

        try:
            value = eval(cons_list[element])
            tot = [element, value]
            nbr = True
        except:
            el = cons_list[element].split()
            for j in operator:
                if j in el:
                    opera = True
                    break
            for e in el:
                if opera:
                    break
                elif e in var_value.keys():
                    cons_list[element] = float(var_value[e])

        if nbr:
            cons_list[tot[0]] = tot[1]
        if opera:
            formula = prepare_formula(cons_list[element], var_value)
            tot2 = [element, RVN(formula)]
            cons_list[tot2[0]] = tot2[1]

    value_returned = min(cons_list)
    return value_returned
def max_function_result(cons, var_value):
    """
    Compute the constraint's cost if its formula is a max function.
    :param cons: the formula of the constraint. type : str
    :param var_value: the values of all variables. type : dict
    :return: value_returned: value of the cosidered costaint. type : float
    """
    operator = ["+", "-", "/", "*"]
    cons = cons.strip("max" + "(" + ")" + "[" + "]")
    cons_list = cons.split(',')
    for element in range(len(cons_list)):
        nbr = False
        opera = False

        try:
            value = eval(cons_list[element])
            tot = [element, value]
            nbr = True
        except:
            el = cons_list[element].split()
            for j in operator:
                if j in el:
                    opera = True
                    break
            for e in el:
                if opera:
                    break
                elif e in var_value.keys():
                    cons_list[element] = float(var_value[e])

        if nbr:
            cons_list[tot[0]] = tot[1]
        if opera:
            formula = prepare_formula(cons_list[element], var_value)
            tot2 = [element, RVN(formula)]
            cons_list[tot2[0]] = tot2[1]

    value_returned = max(cons_list)
    return value_returned


def condition_function_result(cons_details, var_value):
    """
    Compute the valor of a constraint in case of conditional function, with if / else
    :param cons_details: details about the constraint, conditions. type : list
    :return: result: the value of the constraint. type : float
    """
    comparison = ["<", ">", "<=", ">=", "==", "!="]
    result = {}
    cons_list = []
    for c in cons_details:
        cons_list.append(c.split())
    for element in cons_list:
        if "=" in element:
            formula = []
            indice = 1000
            for l in range(len(element)):

                if element[l] == "=":
                    res_ind = element[l - 1]
                    result[res_ind] = None
                    indice = l
                if l > indice:
                    formula.append(element[l])

            formula = " ".join(formula)
            formula_ready = prepare_formula(formula, var_value)

            resultat = RVN(formula_ready)
            result[res_ind] = resultat

        if "if" in element:
            element.remove("if")
            line = " ".join(element)
            line = line.strip(":")
            line = line.split()
            for e in line:
                try:
                    eval(e)
                    ind = line.index(e)
                    val = float(e)
                    tot = [ind, val]
                except:
                    if e in comparison:
                        ind_comp = line.index(e)
                    else:
                        value = float(result[e])
                        ind_val = line.index(e)
            # build the final condition
            line[tot[0]] = str(tot[1])
            line[ind_val] = str(value)
            strline = " ".join(line)
            cond = eval(strline)
            if cond:
                good_ind = cons_list.index(element) + 1
            else:
                good_ind = cons_list.index(element) + 3

            for final_res in range(len(cons_list[good_ind])):
                if cons_list[good_ind][final_res] == "return":
                    value_returned = eval(cons_list[good_ind][final_res + 1])

            return value_returned


def calculate_constraint(agents_param, cons_dict, var_value):
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
            for i in range(len(agent["constraint"])):
                constraint = agent["constraint"][i]
                if len(cons_dict[constraint]) != 1:

                    cons_details = cons_dict[constraint]
                    value = condition_function_result(cons_details, var_value)
                else:
                    if cons_dict[constraint][0].find("max") != -1:
                        constraint_formula = cons_dict[constraint][0]
                        value = max_function_result(constraint_formula, var_value)
                    elif cons_dict[constraint][0].find("min") != -1:
                        constraint_formula = cons_dict[constraint][0]
                        value = min_function_result(constraint_formula, var_value)

                    else:
                        constraint_formula = cons_dict[constraint][0]
                        formula = prepare_formula(constraint_formula, var_value)
                        value += RVN(formula)
            agent["prev_cons_value"] = agent["cons_value"]
            agent["cons_value"] = str(value)
    return agents_param


def calculate_constraint_init(agents_param, cons_dict, var_value):
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
            for i in range(len(agent["constraint"])):
                constraint = agent["constraint"][i]
                if len(cons_dict[constraint]) != 1:
                    cons_details = cons_dict[constraint]
                    value = condition_function_result(cons_details, var_value)
                else:
                    if cons_dict[constraint][0].find("max") != -1:
                        constraint_formula = cons_dict[constraint][0]
                        value = max_function_result(constraint_formula, var_value)
                    elif cons_dict[constraint][0].find("min") != -1:
                        constraint_formula = cons_dict[constraint][0]
                        value = min_function_result(constraint_formula, var_value)

                    else:
                        constraint_formula = cons_dict[constraint][0]
                        formula = prepare_formula(constraint_formula, var_value)
                        value += RVN(formula)
            agent["cons_value"] = str(value)
            agent["prev_cons_value"] = str(value)
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
    for element in formula:
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
    cons_value = pile.pop()  # Keep only the final result by popping the last operator
    return cons_value


def share_constraint_2(agent, prev_var_value):
    '''
    Update constraint value if it's necessary
    :param agent: an agent of the problem. type : dict
    :param prev_var_value: values of the variables during previous cycle. type : dict
    :return: cons_to_send: value of the constraints that have to be transfered, and the recipient. type : dict
    :return: agent: an agent of the problem, with his constraint updated
    '''
    cons_to_send = {}
    cond = False
    agent2 = agent.copy()
    for neighbor in agent["neighbors"]:
        prev_var_value[neighbor] = float(agent["neighbors"][neighbor])
        actual_cons = calculate_constraint_agent(agent2, cons_dict, prev_var_value)
        delta = float(agent["prev_cons_value"]) - float(actual_cons["cons_value"])
        try:
            if delta > 0:
                cond = True
                cons_to_send[neighbor] = agent["constraint"]
        except:
            pass

    if cond:
        agent["cons_value"] = 0
    return agent, cons_to_send


def share_constraint_1(agent, prev_var_value):
    '''
    Update constraint value if it's necessary
    :param agent: an agent of the problem. type : dict
    :param prev_var_value: values of the variables during previous cycle. type : dict
    :return: cons_to_send: value of the constraints that have to be transfered, and the recipient. type : dict
    :return: agent: an agent of the problem, with his constraint updated
    '''
    cons_to_send = {}
    cond = False
    agent2 = agent.copy()
    var = prev_var_value.copy()
    for neighbor in agent["neighbors"]:
        prev_var_value[neighbor] = float(agent["neighbors"][neighbor])
        actual_cons = calculate_constraint_agent(agent2, cons_dict, prev_var_value)
        delta = float(agent["prev_cons_value"]) - float(actual_cons["cons_value"])
        try:
            if delta > float(agent["neighbors_LR"][neighbor]):
                cond = True
                cons_to_send[neighbor] = agent["constraint"]

        except:
            pass

    if cond:
        agent["cons_value"] = 0
    return agent, cons_to_send


def update_cons(cons_to_send, agents_param):
    '''
    Update constraints for each variable by distributing constraints that must be transferred
    :param cons_to_send: the constraints that must be transferred. type : dict
    :param agents_param: all the agents with their parameters. type : dict
    :return: agents_param: all the agents with their parameters and the constraits updated. type : dict
    '''
    for agent in agents_param.values():
        for var, cons in cons_to_send.items():
            if var == agent["variable"]:
                for i in range(len(cons)):
                    if cons[i] not in agent["constraint"]:
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


def calculate_constraint_agent(agent, cons_dict, var_value):
    '''
    Compute the value of the constraint for each variable
    :param agents_param: all the agents with their parameters. type : dict
    :param cons_dict: formula of all the constraints. type : dict
    :param variables: all the variables with the domain they take their values from. type : dict
    :return: agents_param. All the agents with their parameters and their constraints value. type : dict
    '''

    if len(agent["constraint"]) != 0:
        value = 0
        for i in range(len(agent["constraint"])):
            constraint = agent["constraint"][i]
            if len(cons_dict[constraint]) != 1:
                cons_details = cons_dict[constraint]
                value = condition_function_result(cons_details, var_value)
            else:
                if cons_dict[constraint][0].find("max") != -1:
                    constraint_formula = cons_dict[constraint][0]
                    value = max_function_result(constraint_formula, var_value)
                elif cons_dict[constraint][0].find("min") != -1:
                    constraint_formula = cons_dict[constraint][0]
                    value = min_function_result(constraint_formula, var_value)

                else:
                    constraint_formula = cons_dict[constraint][0]
                    formula = prepare_formula(constraint_formula, var_value)
                    value += RVN(formula)
        agent["cons_value"] = str(value)
    return agent


def compute_LR(agent, domain):
    '''
    Try all the values with the constraint of a variable in order to find the best LR.
    :param: agent: an agent of the problem. type : dict
    :return: best_LR : the best possible local reduction in cost, with the value associated. type : list
    '''

    each_LR = {}
    var_values = {}
    cons_init = agent["cons_value"]
    for neighbor, neigh_val in agent["neighbors"].items():
        var_values[neighbor] = float(neigh_val)
    old_cons = float(agent["prev_cons_value"])
    for new_value in domain["cost"]:
        var_values[agent["variable"]] = float(new_value)
        new_cons = float(calculate_constraint_agent(agent, cons_dict, var_values)["cons_value"])
        LR = old_cons - new_cons
        each_LR[new_value] = [LR]
    value_best_LR = max_dict(each_LR)
    assoc_LR = each_LR[value_best_LR][0]
    best_LR = [assoc_LR, value_best_LR]
    agent["current_LR"] = float(assoc_LR)
    agent["cons_value"] = cons_init
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
        current_best_LR = compute_LR(agent, domain)
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


def update_value(agents_param, all_LR):
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


def show_result(agents_param, file, algo, final_result, cost_init):
    '''
    how the results; with the value of each variable and the constraints cost for each variable
    :param agents_param: all the agents with the final parameters. type : dict
    :param file: the name of the file we want to study. type : str
    :param algo: the name of the algorithm that has been used. type : str
    :param final_result: all the costs, considering only the constraints given in the initialization part. type : dict
    :param cost_init: the initial cost, before solving the problem. type : float
    :return: None
    '''
    if algo != "all":
        with open("Results/{}_results_{}.yaml".format(file.strip(".yaml"), algo.strip(".py")), 'w') as f:
            f.write("Assignments :" + "\n")
            for agent in agents_param.values():
                f.write(agent["variable"] + " : " + str(agent["value"]) + "\n")
            f.write("\n")
            f.write("Costs :" + "\n")
            for var, cons_val in final_result.items():
                f.write(var + " : " + str(cons_val) + "\n")
            f.write("\n")
            f.write("Final cost : ")
            cost = 0
            for val in final_result.values():
                cost += float(val)
            f.write(str(cost) + "\n")
            f.write("Initial cost : " + str(cost_init))


def result_final(cons_dict, var_value, constraint):
    """
    Compute the final result with only the constraints given in the initialization part
    :param cons_dict: formulas of all the constraints. type : dict
    :param var_value: all the values of the variables. type : dict
    :param constraint: constraint for each variable. type: dict
    :return: final_cost: all the costs, considering only the constraints given in the initialization part. type : dict
    """
    final_cost = {}

    for var, cons in constraint.items():
        if len(cons_dict[cons[0]]) != 1:
            cons_details = cons_dict[cons[0]]
            final_cost[var] = str(condition_function_result(cons_details, var_value))
        else:
            if cons_dict[cons[0]][0].find("max") != -1:
                constraint_formula = cons_dict[cons[0]][0]
                final_cost[var] = str(max_function_result(constraint_formula, var_value))
            if cons_dict[cons[0]][0].find("min") != -1:
                constraint_formula = cons_dict[cons[0]][0]
                final_cost[var] = str(min_function_result(constraint_formula, var_value))

            else:
                constraint_formula = cons_dict[cons[0]][0]
                formula = prepare_formula(constraint_formula, var_value)
                final_cost[var] = str(RVN(formula))

    return final_cost


def draw_histo(histo, nbr_launch, file):
    """
    Create an histogram in order to compare the results found by the algorithms.
    :param histo: all the values and the number of occurrence of each value, for each algorithm. type : dict
    :param nbr_launch: the number of iterations desired. type : int
    :param file: the name of the file that is treated. type: str
    :return: None
    """
    values = []
    for v in histo["mgm"]:
        if float(v) not in values:
            values.append(float(v))
    for v2 in histo["mcs_mgm"]:
        if float(v2) not in values:
            values.append(float(v2))
    for v3 in histo["gca_mgm"]:
        if float(v3) not in values:
            values.append(float(v3))
    for j in range(int(min(values)), int(max(values))):
        if j not in values:
            values.append(j)

    values = sorted(values)
    # mgm
    y = []
    for element in values:
        if element in histo["mgm"].keys():
            y.append(float(histo["mgm"][element][0]))
        else:
            y.append(0)
    width = 0.7
    plt.bar(values, y, width, color='r', label="MGM")

    # mcs_mgm
    y = []
    for element in values:
        if element in histo["mcs_mgm"].keys():
            y.append(float(histo["mcs_mgm"][element][0]))
        else:
            y.append(0)
    width = 0.4
    plt.bar(values, y, width, color='g', label="MCS_MGM")

    # gca_mgm
    y = []
    for element in values:
        if element in histo["gca_mgm"].keys():
            y.append(float(histo["gca_mgm"][element][0]))
        else:
            y.append(0)
    width = 0.2
    axe = plt.gca()
    axe.xaxis.set_ticks(range(int(min(values)), int(max(values)) + 1))
    axe.yaxis.set_ticks(range(nbr_launch))
    plt.tick_params(axis='y', labelsize=7)
    plt.bar(values, y, width, color='b', label="GCA_MGM")

    plt.legend(loc='upper right')
    plt.savefig("Results/Histogram_{}_{}.pdf".format(nbr_launch, file.strip(".yaml")))
