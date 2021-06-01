def get_algo(command):
    '''
    Get the name of the algorithm that the user wants to use
    :param command: the command line. type : list
    :return: algo: the algorithm's name. type : str
    '''
    algo = command[1]
    return algo


def time_limit(command):
    '''
    Get the time limit chosen by the user.
    :param command: the command line. type : list
    :return: time_lim: number max of cycles. type : int
    '''
    for arg in range(len(command)):
        if command[arg] == "time":
            time_lim = int(command[arg + 1])
    return time_lim


def file_name(command):
    '''
    Get the name of the file from the command line
    :param command: the command line. type : list
    :return: file: the name of the file. type : str
    '''
    file = command[-1]
    return file


def get_objective(file):
    '''
    Get objective, min or max from the file
    :param file: name of the file. type : str
    :return: objective: objective min or max. type : str
    '''
    with open("Graph/{}".format(file), 'r') as f:
        objective = None
        for line in f:
            line = line.strip()
            if line[0] == "objective:":
                objective = line[1]
                break
    return objective


def get_data(file):
    '''
    Get all the data from the file
    :param file: the name of the file. type : str
    :return: domain: the domain characteristics. type : dict
    :return: variables: all the variables from the file with their domain. type : dict
    :return: constraints: the constraints fr each variable. type : dict
    :return: cons_dict: all the constraints with their values, and conditions to take those values. type : dict
    :return: cons_for_var: each constraint with the variables they imply on. type : dict
    :return: agents: all the agents used for the considered problem. type : list
    '''
    with open("Graph/{}".format(file), 'r') as f:
        line = f.readlines()
        line_corrected = []
        for element in line:
            element = element.strip('\n')
            line_corrected.append(element)
        for i in range(len(line_corrected)):
            if line_corrected[i] == 'domains:':
                name = line_corrected[i + 1].strip(':')

            if line_corrected[i] != '':
                line_stud = line_corrected[i].split()
                if line_stud[0] == "values:":
                    values = correct_values(line_corrected[i])

                    break

        domain = {name.split()[0]: values}
        variables, constraints, cons_dict, agents, cons_for_var = get_variables(line_corrected, i)

        return domain, variables, constraints, cons_dict, cons_for_var, agents


def correct_values(line):
    '''
    Delete undesirable characters from the domain values
    :param line: the line we want to correct. type : str
    :return: line_ad: the line corrected/ type : str
    '''
    line2 = line.split()
    del line2[0]
    line = " ".join(line2)
    line_ad = line.strip('[')
    line_ad = line_ad.strip(']')
    line_ad = line_ad.split(',')
    return line_ad


def get_last_ind(file_list, first_ind):
    """
    Get the last index of the line that describes a constraint function.
    :param file_list:
    :return:
    """
    forbidden = ["else:"]
    i = first_ind
    line = file_list[i].split()
    cond = True
    while cond:
        i += 1
        line = file_list[i].split()
        if len(line) == 1 and line[0] not in forbidden:
            cond = False

    return i


def get_variables(file_list, first_index):
    '''
    get variables names and domains
    :param file_list: list with all the file's lines. type : list
    :param first_index: index of the first variable. type : int
    :return: variables : all of the variables, with their domains. type : dict
    '''
    index = first_index + 3

    variables = {}
    continu = True
    for i in range(index, len(file_list), 2):
        if file_list[i] == '':
            break
        variable_name = file_list[i].strip(':')
        variable_domain = file_list[i + 1].split()[1]
        variables[variable_name.split()[0]] = variable_domain

    constraints, cons_dict, first_agent_index, cons_for_var = get_constraints(file_list, i, variables)
    agents = get_agent(file_list, first_agent_index, variables)
    return variables, constraints, cons_dict, agents, cons_for_var


def get_constraints(file_list, first_index, variables):
    '''
    Get constraints for each variable.
    :param variables: all the variables. type : dict
    :param file_list: list with all the file's lines. type : list
    :param first_index: index of the last variable. type : int
    :return: var_constraints: all the contraints for each variable. type : dict
    :return: constraints: all the constraints with their values and values conditions. type : dict
    '''
    var_constraints = {}
    constraints = {}
    constraints_for_var = {}
    words = [["values:"], ["variables:"], ["type:"],["function:"],["else:"]]
    index = first_index + 2  # index of the first constraint
    for j in variables:  # create a dictionnary with all the variables
        var_constraints[j] = []

    for i in range(index, len(file_list)):
        forbidden = ["variables:", "function:", "agents:"]
        line = file_list[i].split()  # each line of the file
        step_cv = 1

        if len(line) == 1 and line[0] == "agents:":
            break
        if line not in words and len(line) == 1:  # check if the line is only about one variable

            cons_name = line[0].strip(':')
            step_s = 1
            line_s = file_list[i + step_s].split()

            while line_s[0] not in forbidden:
                step_s += 1
                line_s = file_list[i + step_s].split()

            if line_s[0] == "variables:":  # check that we are looking to variables
                if len(line_s) == 2:  # word and variable's name are on the same line
                    associated_var = [file_list[i + step_s].split()[1]]
                else:  # variable's name under the constraints values
                    step = 1
                    keys = [k for k in variables.keys()]
                    next_line = file_list[i + step_s + step]
                    next_line = next_line.split()
                    associated_var = []
                    associated_var.append(next_line[1])
                    while len(
                            next_line) == 2:  # each variable is added, in case of multiple variables for one constraint
                        step += 1
                        associated_var.append(next_line[1])
                        next_line = file_list[i + step_s + step]
                        next_line = next_line.split()

            else:  # add variables even if they are not explicitly mentioned in the file
                associated_var = []
                for var in file_list[i + step_s].split():
                    if var in var_constraints.keys():
                        associated_var.append(var)

            for var in associated_var:  # add each constraint name for each variable
                var_constraints[var].append(cons_name.strip(''))

        try:
            line_cv = file_list[i + step_cv].split()
            if line_cv[0] == "values:":  # get the constraints values
                constraints[cons_name] = []
                while line_cv[0] not in forbidden:
                    try:

                        val = eval(line_cv[0].strip(':'))
                        line_copy = line_cv.copy()
                        del line_copy[0]
                        text = " ".join(line_copy)
                        constraints[cons_name].append((val, text))
                    except NameError:
                        pass
                    step_cv += 1
                    line_cv = file_list[i + step_cv].split()
            elif line_cv[0] == "function:" and len(line_cv) != 1:
                constraints[cons_name] = []
                nex_line = line_cv.copy()
                del nex_line[0]
                fun = " ".join(nex_line)
                constraints[cons_name].append(fun)
            elif line_cv[0] == "function:" and len(line_cv) == 1:
                first_ind = i + step_cv + 1
                last_ind = int(get_last_ind(file_list, first_ind))
                constraints[cons_name] = []
                for p in range(first_ind, last_ind):
                    constraints[cons_name].append(file_list[p])





        except IndexError:
            pass
    for k in constraints.keys():
        constraints_for_var[k] = []
    for v, c in var_constraints.items():
        for c2 in c:
            constraints_for_var[c2].append(v)
    return var_constraints, constraints, i, constraints_for_var


def get_agent(file_list, first_index, variables):
    '''
    Get agents name from the file
    :param variables: all the variables. type : dict
    :param file_list: list with all the file's lines. type : list
    :param first_index: index of the last variable. type : int
    :return: agents:  all the agents of the considered problem. type : list
    '''
    line = file_list[first_index].split()
    nbr_agents = len(variables)
    agents = []
    if len(line) != 1:
        agents = correct_values(file_list[first_index])
    else:
        step_a = 1
        line_a = file_list[first_index + step_a].split()
        while len(agents) != nbr_agents:
            if len(line_a) == 1:
                agents.append(line_a[0].strip(':'))
            step_a += 1
            line_a = file_list[first_index + step_a].split()

    return agents
