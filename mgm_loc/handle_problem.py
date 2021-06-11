import handle_file as hf
import sys
import random as r
import matplotlib.pyplot as plt
import pylab


# self.domain, variables, constraints, cons_dict, cons_for_var, agents = 0
class HP:
    def __init__(self, domain, variables, constraints, cons_dict, cons_for_var, agents):
        self.domain = domain
        self.variables = variables
        self.constraints = constraints
        self.cons_dict = cons_dict
        self.cons_for_var = cons_for_var
        self.agents = agents

    def init_problem(self, argv):
        file = hf.file_name(argv)
        self.domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(file)

    def config_agents(self):
        '''
        Create a dictionary with all the details for each agent.
        :param variables: all the variables of the file, with their self.domain. type : dict
        :param agents: all the agents of the file. type : list
        :return: agents_param: all the agents with their parameters (variable, var value, neighbors). type : dict
        '''
        agents_param = {}
        all_var = []
        for var in self.variables.keys():
            all_var.append(var)
        for ag in range(len(self.agents)):
            actual_agent = {}
            actual_agent["variable"] = all_var[ag]
            actual_agent["constraint"] = self.constraints[all_var[ag]]
            actual_agent["value"] = None
            actual_agent["neighbors"] = {}
            actual_agent["neighbors_LR"] = {}
            agents_param[self.agents[ag]] = actual_agent
            for var2 in all_var:
                if var2 != actual_agent["variable"]:
                    actual_agent["neighbors"][var2] = None
                    actual_agent["neighbors_LR"][var2] = None
            actual_agent["cons_value"] = 0
            actual_agent["prev_cons_value"] = 0
            actual_agent["current_LR"] = None

        return agents_param

    def init_agents_contr(self, agents_param):
        '''
        Initialize the algorithm, assigning one random value per variable
        :param agents_param:  all the agents with their parameters (variable, var value, neighbors). type : dict
        :param self.domain: all the values in the self.domain for this problem
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

    def init_agents(self, agents_param):
        '''
        Initialize the algorithm, assigning one random value per variable
        :param agents_param:  all the agents with their parameters (variable, var value, neighbors). type : dict
        :param self.domain: all the values in the self.domain for this problem
        :return: agents_param:  all the agents with their parameters, and a random value. type : dict
        '''
        for agent in agents_param.values():
            for values in self.domain.values():
                random_val = r.choice(values)
                try:
                    agent["value"] = random_val
                except:
                    pass
        return agents_param

    def send_values(self, agents_param):
        '''
        Create an iterable (a message) and put the new values of the variable inside.
        :param agents_param: all the agents with their parameters. type : dict
        :return: value_mess: all the new values of the variables. type : dict
        '''
        value_mess = {}
        for agent in agents_param.values():
            value_mess[agent["variable"]] = agent["value"]

        return value_mess

    def collect_values(self, agents_param, value_mess):
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

    def min_function_result(self, cons, var_value):
        """
        Compute the valor of a constraint if it's a min function.
        :param cons: the considered constraint. type : str
        :param var_value: values of all the variables. type : dict
        :return: value_returned: the value of the constraint. type : float
        """
        operator = ["+", "-", "/", "*"]
        e = cons.find(")")
        s = cons.find("min")
        min_part = cons[s:e + 1]
        other_before = cons[:s]
        other_after = cons[e + 1:]
        cons_min_list = min_part.split(',')

        for c in range(len(cons_min_list)):
            cons_min_list[c] = cons_min_list[c].strip(
                "min" + "max" + "(" + ")" + "[" + "]" + ",")  # keep only the elements that must be compared

        for element in range(len(cons_min_list)):
            nbr = False
            opera = False
            # If the considered element is a float
            try:
                value = eval(cons_min_list[element])
                tot = [element, value]  # keep the index and the value that have to be placed in the final list
                nbr = True
            except:
                # If the considered element is unknown, impossible to evaluate
                el = cons_min_list[element].split()
                for j in operator:
                    if j in el:
                        opera = True  # Check if the element is an operation
                        break
                for e in el:
                    if opera:
                        break
                    elif e in var_value.keys():  # Check if the element is only a variable
                        cons_min_list[element] = float(var_value[e])

            if nbr:  # If the considered element is a number, change it by its value
                cons_min_list[tot[0]] = tot[1]
            if opera:  # If the considered element is an operation, change it by its result
                formula = self.prepare_formula(cons_min_list[element], var_value)
                tot2 = [element, self.RVN(formula)]
                cons_min_list[tot2[0]] = tot2[1]

        value_returned = min(cons_min_list)
        final_cons = other_before + str(value_returned) + other_after
        if str(value_returned) == final_cons:
            return value_returned
        else:
            formula = self.prepare_formula(final_cons, var_value)
            value_returned = self.RVN(formula)
            return value_returned


    def max_function_result(self, cons, var_value):
        """
        Compute the valor of a constraint if it's a max function.
        :param cons: the considered constraint. type : str
        :param var_value: values of all the variables. type : dict
        :return: value_returned: the value of the constraint. type : float
        """
        operator = ["+", "-", "/", "*"]
        e = cons.find(")")
        s = cons.find("max")
        min_part = cons[s:e + 1]
        other_before = cons[:s]
        other_after = cons[e + 1:]
        cons_min_list = min_part.split(',')

        for c in range(len(cons_min_list)):
            cons_min_list[c] = cons_min_list[c].strip(
                "min" + "max" + "(" + ")" + "[" + "]" + ",")  # keep only the elements that must be compared

        for element in range(len(cons_min_list)):
            nbr = False
            opera = False
            # If the considered element is a float
            try:
                value = eval(cons_min_list[element])
                tot = [element, value]  # keep the index and the value that have to be placed in the final list
                nbr = True
            except:
                # If the considered element is unknown, impossible to evaluate
                el = cons_min_list[element].split()
                for j in operator:
                    if j in el:
                        opera = True  # Check if the element is an operation
                        break
                for e in el:
                    if opera:
                        break
                    elif e in var_value.keys():  # Check if the element is only a variable
                        cons_min_list[element] = float(var_value[e])

            if nbr:  # If the considered element is a number, change it by its value
                cons_min_list[tot[0]] = tot[1]
            if opera:  # If the considered element is an operation, change it by its result
                formula = self.prepare_formula(cons_min_list[element], var_value)
                tot2 = [element, self.RVN(formula)]
                cons_min_list[tot2[0]] = tot2[1]

        value_returned = max(cons_min_list)
        final_cons = other_before + str(value_returned) + other_after
        if str(value_returned) == final_cons:
            return value_returned
        else:
            formula = self.prepare_formula(final_cons, var_value)
            value_returned = self.RVN(formula)
            return value_returned


    def condition_function_result(self, cons_details, var_value):
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
                if "=" in element:  # Check if the element is an equality
                    formula = []
                    ind = 1000
                    for l in range(len(element)):

                        if element[l] == "=":
                            res_ind = element[l - 1]  # Get the left side of the equality
                            result[res_ind] = None
                            ind = l
                        if l > ind:
                            formula.append(element[l])  # Get the right side of the equality, which is an operation

                    formula = " ".join(formula)
                    formula_ready = self.prepare_formula(formula, var_value)

                    resultat = self.RVN(formula_ready)  # Compute the right side of the equality
                    result[res_ind] = resultat

                if "if" in element:  # Check if the element is the first condition line
                    # Prepare the line that describes the first condition
                    element.remove("if")
                    line = " ".join(element)
                    line = line.strip(":")
                    line = line.split()
                    for e in line:
                        new_value = False
                        val_equa = False
                        nbr = False
                        # Check if the e is a number, and get its value
                        try:
                            eval(e)
                            ind = line.index(e)
                            val = float(e)
                            tot = [ind, val]
                            nbr = True

                        except:
                            if e in comparison:
                                ind_comp = line.index(e)
                            # If e is a variable of the problem
                            elif e in var_value.keys():
                                ind_var = line.index(e)
                                value = float(var_value[e])
                                new_value = True
                            else:
                                # If e is the variable of the equality
                                value2 = float(result[e])
                                ind_val = line.index(e)
                                val_equa = True
                        # build the final condition
                        if nbr:
                            line[tot[0]] = str(tot[1])
                        if val_equa:
                            line[ind_val] = str(value2)
                        if new_value:
                            line[ind_var] = str(value)
                    strline = " ".join(line)
                    cond = eval(strline)
                    # Find the goodind, which is the index of the return part
                    if cond:
                        good_ind = cons_list.index(element) + 1
                    else:
                        good_ind = cons_list.index(element) + 3
                    # Find the value that has to be returned
                    for final_res in range(len(cons_list[good_ind])):
                        if cons_list[good_ind][final_res] == "return":
                            value_returned = eval(cons_list[good_ind][final_res + 1])

                    return value_returned

    def calculate_constraint(self, agents_param, var_value):
        '''
        Compute the value of the constraint for each variable
        :param agents_param: all the agents with their parameters. type : dict
        :param cons_dict: formula of all the constraints. type : dict
        :param variables: all the variables with the self.domain they take their values from. type : dict
        :return: agents_param. All the agents with their parameters and their constraints value. type : dict
        '''

        for agent in agents_param.values():
            if len(agent["constraint"]) != 0:
                value = 0
                for i in range(len(agent["constraint"])):
                    constraint = agent["constraint"][i]
                    if len(self.cons_dict[
                               constraint]) != 1:  # If the constraint is a conditional constraint with if/else

                        cons_details = self.cons_dict[constraint]
                        value = self.condition_function_result(cons_details, var_value)
                    else:
                        if self.cons_dict[constraint][0].find("max") != -1:  # If the constraint is a max function
                            constraint_formula = self.cons_dict[constraint][0]
                            value = self.max_function_result(constraint_formula, var_value)
                        elif self.cons_dict[constraint][0].find("min") != -1:  # If the constraint is a min function
                            constraint_formula = self.cons_dict[constraint][0]
                            value = self.min_function_result(constraint_formula, var_value)

                        else:
                            constraint_formula = self.cons_dict[constraint][
                                0]  # If the constraint is a simple constraint
                            formula = self.prepare_formula(constraint_formula, var_value)
                            value += self.RVN(formula)
                agent["prev_cons_value"] = agent["cons_value"]
                agent["cons_value"] = str(value)
        return agents_param

    def calculate_constraint_init(self, agents_param, var_value):
        '''
        Compute the value of the constraint for each variable
        :param agents_param: all the agents with their parameters. type : dict
        :param cons_dict: formula of all the constraints. type : dict
        :param variables: all the variables with the self.domain they take their values from. type : dict
        :return: agents_param. All the agents with their parameters and their constraints value. type : dict
        '''

        for agent in agents_param.values():
            if len(agent["constraint"]) != 0:
                value = 0
                for i in range(len(agent["constraint"])):
                    constraint = agent["constraint"][i]
                    if len(self.cons_dict[constraint]) != 1:
                        cons_details = self.cons_dict[constraint]
                        value = self.condition_function_result(cons_details, var_value)
                    else:
                        if self.cons_dict[constraint][0].find("max") != -1:
                            constraint_formula = self.cons_dict[constraint][0]
                            value = self.max_function_result(constraint_formula, var_value)
                        elif self.cons_dict[constraint][0].find("min") != -1:
                            constraint_formula = self.cons_dict[constraint][0]
                            value = self.min_function_result(constraint_formula, var_value)

                        else:
                            constraint_formula = self.cons_dict[constraint][0]
                            formula = self.prepare_formula(constraint_formula, var_value)
                            value += self.RVN(formula)
                agent["cons_value"] = str(value)
                agent["prev_cons_value"] = str(value)
        return agents_param

    def prepare_formula(self, constraint_formula, var_value):
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

    def RVN(self, formula_ready):
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

    def share_constraint_2(self, agent, prev_var_value):
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
            actual_cons = self.calculate_constraint_agent(agent2, prev_var_value)
            delta = float(actual_cons["cons_value"]) - float(agent["prev_cons_value"])
            try:
                if delta > 0:
                    for cons in agent["constraint"]:
                        must_be_added = None
                        current_formula = self.cons_dict[cons][0]
                        # if there is a min or max function in the constraint formula
                        if current_formula.find("max") != -1:
                            s = current_formula.find("max")
                            end = current_formula.find(")")
                            considered_formula = current_formula[s:end + 1]
                            if considered_formula.find(neighbor) != -1:
                                must_be_added = "+ {}".format(neighbor)

                            current_formula = current_formula[:s] + '0' + current_formula[end + 1:]
                        if current_formula.find("min") != -1:
                            s = current_formula.find("min")
                            end = current_formula.find(")")
                            considered_formula = current_formula[s:end + 1]
                            if considered_formula.find(neighbor) != -1:
                                must_be_added = "+ {} ".format(neighbor)
                            current_formula = current_formula[:s] + '0' + current_formula[end + 1:]

                        list_formula = current_formula.split()
                        for element in range(len(list_formula)):
                            if list_formula[element] == neighbor:
                                str_cons_to_send = str(list_formula[element])

                                if list_formula[element - 1] == "*":
                                    try:
                                        nbr = int(list_formula[element - 2])
                                    except:
                                        nbr = list_formula[element - 2]
                                    str_cons_to_send = str(nbr) + ' ' + str(list_formula[element - 1]) + ' ' + str(
                                        list_formula[element])
                                else:
                                    if element != 0:
                                        str_cons_to_send = str(list_formula[element - 1]) + " " + str_cons_to_send
                                try:
                                    cons_to_send[neighbor] = str_cons_to_send + " " + cons_to_send[neighbor]
                                except:
                                    cons_to_send[neighbor] = str_cons_to_send
                                if cons_to_send[neighbor] in prev_var_value.keys():
                                    cond = True
                                    cons_to_remp = cons_to_send[neighbor]
                                    cons_to_send[neighbor] = "+ " + cons_to_send[neighbor]

                    if must_be_added is not None:
                        try:
                            cons_to_send[neighbor] += ' ' + must_be_added
                        except:
                            cons_to_send[neighbor] = must_be_added

                    if cond:
                        self.cons_dict[agent["constraint"][0]][0] = self.cons_dict[agent["constraint"][0]][0].replace(
                            cons_to_remp, "0")
                        cond = False
                    else:
                        self.cons_dict[agent["constraint"][0]][0] = self.cons_dict[agent["constraint"][0]][0].replace(
                            neighbor, "0")
            except:
                pass

        return agent, cons_to_send
    def share_constraint_1(self, agent, prev_var_value):
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
            actual_cons = self.calculate_constraint_agent(agent2, prev_var_value)
            delta = float(actual_cons["cons_value"]) - float(agent["prev_cons_value"])
            try:
                if delta > float(agent["neighbors_LR"][neighbor]):
                    for cons in agent["constraint"]:
                        must_be_added = None
                        current_formula = self.cons_dict[cons][0]
                        # if there is a min or max function in the constraint formula
                        if current_formula.find("max") != -1:
                            s = current_formula.find("max")
                            end = current_formula.find(")")
                            considered_formula = current_formula[s:end+1]
                            if considered_formula.find(neighbor) != -1:
                                must_be_added = "+ {}".format(neighbor)

                            current_formula = current_formula[:s] + '0' + current_formula[end+1:]
                        if current_formula.find("min") != -1:
                            s = current_formula.find("min")
                            end = current_formula.find(")")
                            considered_formula = current_formula[s:end+1]
                            if considered_formula.find(neighbor) != -1:
                                must_be_added = "+ {} ".format(neighbor)
                            current_formula = current_formula[:s] + '0' + current_formula[end+1:]

                        list_formula = current_formula.split()
                        for element in range(len(list_formula)):
                            if list_formula[element] == neighbor:
                                str_cons_to_send = str(list_formula[element])

                                if list_formula[element - 1] == "*":
                                    try:
                                        nbr = int(list_formula[element - 2])
                                    except:
                                        nbr = list_formula[element - 2]
                                    str_cons_to_send = str(nbr) + ' ' + str(list_formula[element - 1]) + ' ' + str(
                                        list_formula[element])
                                else:
                                    if element != 0:
                                        str_cons_to_send = str(list_formula[element - 1]) + " " + str_cons_to_send
                                try:
                                    cons_to_send[neighbor] = str_cons_to_send + " " + cons_to_send[neighbor]
                                except:
                                    cons_to_send[neighbor] = str_cons_to_send
                                if cons_to_send[neighbor] in prev_var_value.keys():
                                    cond = True
                                    cons_to_remp = cons_to_send[neighbor]
                                    cons_to_send[neighbor] = "+ " + cons_to_send[neighbor]

                    if must_be_added is not None:
                        try:
                            cons_to_send[neighbor] += ' ' + must_be_added
                        except:
                            cons_to_send[neighbor] = must_be_added


                    if cond:
                        self.cons_dict[agent["constraint"][0]][0] = self.cons_dict[agent["constraint"][0]][0].replace(
                            cons_to_remp, "0")
                        cond = False
                    else:
                        self.cons_dict[agent["constraint"][0]][0] = self.cons_dict[agent["constraint"][0]][0].replace(
                            neighbor, "0")
            except:
                pass

        return agent, cons_to_send

    def update_cons(self, cons_to_send, agents_param):
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

    def get_var_value(self, agents_param):
        '''
        Get the values of each variable, anytime
        :param agents_param: all the agents with their parameters
        :return: var_value: values of each variable. type : dict
        '''
        var_value = {}

        for agent in agents_param.values():
            var_value[agent["variable"]] = int(agent["value"])
        return var_value

    def calculate_constraint_agent(self, agent, var_value):
        '''
        Compute the value of the constraint for each variable
        :param agents_param: all the agents with their parameters. type : dict
        :param cons_dict: formula of all the constraints. type : dict
        :param variables: all the variables with the self.domain they take their values from. type : dict
        :return: agents_param. All the agents with their parameters and their constraints value. type : dict
        '''

        if len(agent["constraint"]) != 0:
            value = 0
            for i in range(len(agent["constraint"])):
                constraint = agent["constraint"][i]
                if len(self.cons_dict[constraint]) != 1:
                    cons_details = self.cons_dict[constraint]
                    value = self.condition_function_result(cons_details, var_value)
                else:
                    if self.cons_dict[constraint][0].find("max") != -1:
                        constraint_formula = self.cons_dict[constraint][0]
                        value = self.max_function_result(constraint_formula, var_value)
                    elif self.cons_dict[constraint][0].find("min") != -1:
                        constraint_formula = self.cons_dict[constraint][0]
                        value = self.min_function_result(constraint_formula, var_value)

                    else:
                        constraint_formula = self.cons_dict[constraint][0]
                        formula = self.prepare_formula(constraint_formula, var_value)
                        value += self.RVN(formula)
            agent["cons_value"] = str(value)
        return agent

    def compute_LR_min(self, agent):
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
        for new_value in self.domain["cost"]:
            var_values[agent["variable"]] = float(new_value)
            new_cons = float(self.calculate_constraint_agent(agent, var_values)["cons_value"])
            LR = old_cons - new_cons
            each_LR[new_value] = [LR]
        value_best_LR = self.max_dict(each_LR)
        assoc_LR = each_LR[value_best_LR][0]
        best_LR = [assoc_LR, value_best_LR]
        agent["current_LR"] = float(assoc_LR)
        agent["cons_value"] = cons_init
        return best_LR

    def compute_LR_max(self, agent):
        '''
        Try all the values with the constraint of a variable in order to find the best LR objective is max)
        :param: agent: an agent of the problem. type : dict
        :return: best_LR : the best possible local reduction in cost, with the value associated. type : list
        '''

        each_LR = {}
        var_values = {}
        cons_init = agent["cons_value"]
        for neighbor, neigh_val in agent["neighbors"].items():
            var_values[neighbor] = float(neigh_val)
        old_cons = float(agent["prev_cons_value"])
        for new_value in self.domain["cost"]:
            var_values[agent["variable"]] = float(new_value)
            new_cons = float(self.calculate_constraint_agent(agent, var_values)["cons_value"])
            LR = old_cons - new_cons
            each_LR[new_value] = [LR]
        value_best_LR = self.min_dict(each_LR)
        assoc_LR = each_LR[value_best_LR][0]
        best_LR = [assoc_LR, value_best_LR]
        agent["current_LR"] = float(assoc_LR)
        agent["cons_value"] = cons_init
        return best_LR

    def all_LR(self, agents_param, objective):
        '''
        Create an iterable with all the best LRs and the value associated, for all variables.
        :param agents_param: agents_param: all the agents with their parameters. type : dict
        :return: all_LR: all the LRs with their associated variable and value for this variable. type : dict
        '''
        all_LR = {}
        for agent in agents_param.values():
            current_var = agent["variable"]
            if objective == "min":
                current_best_LR = self.compute_LR_min(agent)
            else:
                current_best_LR = self.compute_LR_max(agent)
            all_LR[current_var] = current_best_LR

        return all_LR

    def collect_LR(self, agents_param, all_LR):
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

    def update_value(self, agents_param, all_LR, objective):
        '''
        Update the value of a variable chosen thanks to its LR.
        :param agents_param: all the agents with their parameters. type : dict
        :param all_LR: all the LRs with their associated variable and value for this variable. type : dict
        :return: agents_param: all the agents with their parameters, and the value updated. type : dict
        '''
        if objective == "min":
            key = self.max_dict_2(all_LR)
            if key is None:
                return agents_param
        else:
            key = self.min_dict_2(all_LR)
            if key is None:
                return agents_param
        for agent in agents_param.values():
            if agent["variable"] == key:
                agent["value"] = all_LR[key][1]


        return agents_param

    def max_dict(self, dictio):
        '''
        Compute the index associated to the max value in a dictionary of iterable.
        :param dictio: the iterable in which we want to have the index of the max value. type : dict
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

    def max_dict_2(self, dictio):
        '''
        Compute the index associated to the max value in a dictionary of iterable.
        :param dictio: the iterable in which we want to have the index of the max value. type : dict
        :return: key: the index of the maximum value. type : str
        '''
        values = []
        for i in dictio.values():
            values.append(float(i[0]))

        maximum = max(values)
        if maximum < 0:
            key = None
            return key
        for k, val in dictio.items():
            if maximum == float(val[0]):
                key = k

        return key

    def min_dict(selfself, dictio):
        """
        Compute the index associated to the min value in a dictionary of iterable.
        :param dictio: the iterable in which we want to have the index of the min value. type : dict
        :return: key: the index of the minimum value. type : str
        """
        values = []
        for i in dictio.values():
            values.append(float(i[0]))

        minimum = min(values)
        for k, val in dictio.items():
            if minimum == float(val[0]):
                key = k

        return key

    def min_dict_2(selfself, dictio):
        """
        Compute the index associated to the min value in a dictionary of iterable.
        :param dictio: the iterable in which we want to have the index of the min value. type : dict
        :return: key: the index of the minimum value. type : str
        """
        values = []
        for i in dictio.values():
            values.append(float(i[0]))

        minimum = min(values)
        if minimum > 0:
            key = None
            return key
        for k, val in dictio.items():
            if minimum == float(val[0]):
                key = k

        return key

    def cons_update(self, cons_to_transfer):
        for var, cons in cons_to_transfer.items():
            formula_list = cons.split()
            if "*" in formula_list:
                self.cons_dict[self.constraints[var][0]][0] = cons + " + " + self.cons_dict[self.constraints[var][0]][0]
            else:
                self.cons_dict[self.constraints[var][0]][0] += " " + cons

    def show_result(self, agents_param, file, algo, final_result, cost_init, height_cons,time_tot):
        '''
        how the results; with the value of each variable and the constraints cost for each variable
        :param agents_param: all the agents with the final parameters. type : dict
        :param file: the name of the file we want to study. type : str
        :param algo: the name of the algorithm that has been used. type : str
        :param final_result: all the costs, considering only the constraints given in the initialization part. type : dict
        :param cost_init: the initial cost, before solving the problem. type : float
        :param height_cons: len of each constraint in the initialisation. type : dict
        :return: None
        '''
        new_height = {}
        for cons, form in self.cons_dict.items():
            new_height[cons] = len(form[0].split())
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
                f.write("Initial cost : " + str(cost_init) + "\n")
                f.write("\n")
                f.write("Resolution time (s) : "+str(time_tot))
                f.write("\n")
                f.write("Constraints initial length :" + "          " + "Constraints new length :" + "\n")
                for cons in height_cons:
                    f.write("{} :{}".format(cons, height_cons[cons]) + "                                    ")
                    f.write("{} :{}".format(cons, new_height[cons]) + "\n")

    def result_final(self, var_value, constraint):
        """
        Compute the final result with only the constraits given in the initialization part
        :param cons_dict: formulas of all the constraints. type : dict
        :param var_value: all the values of the variables. type : dict
        :param constraint: constraint for each variable. type: dict
        :return: final_cost: all the costs, considering only the constraints given in the initialization part. type : dict
        """
        final_cost = {}
        for var, cons in constraint.items():
            if len(self.cons_dict[cons[0]]) != 1:
                cons_details = self.cons_dict[cons[0]]
                final_cost[var] = str(self.condition_function_result(cons_details, var_value))
            else:
                if self.cons_dict[cons[0]][0].find("max") != -1:
                    constraint_formula = self.cons_dict[cons[0]][0]
                    final_cost[var] = str(self.max_function_result(constraint_formula, var_value))
                elif self.cons_dict[cons[0]][0].find("min") != -1:
                    constraint_formula = self.cons_dict[cons[0]][0]
                    final_cost[var] = str(self.min_function_result(constraint_formula, var_value))

                else:
                    constraint_formula = self.cons_dict[cons[0]][0]
                    formula = self.prepare_formula(constraint_formula, var_value)
                    final_cost[var] = str(self.RVN(formula))

        return final_cost

    def draw_histo(self, histo, nbr_launch, file):
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
        plt.tick_params(axis='x', labelsize=7)
        plt.bar(values, y, width, color='b', label="GCA_MGM")

        plt.legend(loc='upper right')
        plt.savefig("Results/Histogram_{}_{}.pdf".format(nbr_launch, file.strip(".yaml")))
