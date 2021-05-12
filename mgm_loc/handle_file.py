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
    with open(file,'r') as f:
        objective = None
        for line in f:
            line = line.strip()
            if line[0] == "objective:":
                objective = line[1]
                break
    return objective
def get_domain(file):
    '''
    Get the domain of the values from the file
    :param file: the name of the file. type : str
    :return: domain: the domain caracteristics. type : dict
    '''
    with open(file,'r') as f:
        line = f.readlines()
        line_corrected = []
        for element in line:
            element = element.strip('\n')
            line_corrected.append(element)
        for i in range (len(line_corrected)):
            if line_corrected[i] == 'domains:':
                name = line_corrected[i+1].strip(':')

            if line_corrected[i] != '':
                line_stud = line_corrected[i].split()
                if line_stud[0]=="values:":
                    values = []
                    for j in range(1,len(line_stud)):
                        line_ad = handle_domain_values(line_stud[j])
                        values.append(line_ad)

                    break


        domain = {name.split()[0]: values}
        variables,constraints = get_variables(line_corrected,i)

        return domain, variables , constraints

def handle_domain_values(line):
    '''
    Delete undesirable characters from the domain values
    :param line: the line we want to correct. type : str
    :return: line_ad: the line corrected/ type : str
    '''
    line_ad = line.strip("[")
    line_ad = line_ad.strip("]")
    line_ad = line_ad.strip(",")
    return line_ad

def get_variables(file_list,first_index):
    '''
    get variables names and domains
    :param file_list: list with all the file's lines. type : list
    :param first_index: index of the first variable. type : int
    :return: variables : all of the variables, with their domains. type : dict
    '''
    index = first_index +3

    variables = {}
    continu = True
    for i in range(index,len(file_list),2):
        if file_list[i]=='':
            break
        variable_name = file_list[i].strip(':')
        variable_domain = file_list[i+1].split()[1]
        variables[variable_name.split()[0]] = variable_domain

    constraints = get_constraints(file_list, i,variables)
    return variables,constraints

def get_constraints(file_list,first_index,variables):
    '''
    Get constraints for each variable.
    :param variables: all the variables. type : dict
    :param file_list: list with all the file's lines. type : list
    :param first_index: index of the last variable. type : int
    :return: var_constraints: all the contraints for each variable. type : dict
    :return: constraints
    '''
    var_constraints = {}
    constraints = {}
    words = [["values:"],["variables:"],["type:"]]
    index = first_index + 2 #index of the first constraint
    for j in variables:   #create a dictionnary with all the variables
        var_constraints[j] = []

    for i in range(index,len(file_list)):
        line = file_list[i].split()
        if line not in words and len(line)==1:   #check if the line is only about one variable
            cons_name = line[0].strip(':')
            step_s = 1
            line_s = file_list[i+step_s].split()
            while line_s[0] != "variables:":
                step_s += 1
                line_s = file_list[i + step_s].split()

            if file_list[i+2].split()[0] == "variables:":
                line_var = file_list[i+2].split()
                if len(line_var)==2:
                    associated_var = [file_list[i+2].split()[1]]
                else:
                    step = 1
                    keys = [k for k in variables.keys()]
                    next_line = keys[0]
                    while next_line in keys:
                        next_line = file_list[i + 2 + step].split().strip('-')
                        associated_var.append(next_line)
                        step += 1
            else:
                associated_var = []
                for var in file_list[i+2].split():
                    if var in var_constraints.keys():
                        associated_var.append(var)

            for var in associated_var:
                var_constraints[var].append(cons_name.strip(''))

    return var_constraints





print(get_domain("graph_coloring_50.yaml"))




