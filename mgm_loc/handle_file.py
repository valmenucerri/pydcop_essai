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
        variables = get_variables(line_corrected,i)
        return domain, variables

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
    print(file_list)
    variables = {}
    continu = True
    for i in range(index,len(file_list),2):
        if file_list[i]=='':
            break
        variable_name = file_list[i].strip(':')
        variable_domain = file_list[i+1].split()[1]
        variables[variable_name.split()[0]] = variable_domain
    print(i)
    return variables

def get_constraints(file_list,first_index,variables):
    '''
    Get constraints for each variable.
    :param file_list: list with all the file's lines. type : list
    :param first_index: index of the last variable. type : int
    :return: var_constraints: all the contraints for each variable. type : dict
    :return: constraints
    '''
    var_constraints = {}
    constraints = {}
    words = ["types:","variables:","values:"]
    for j in variables:
        var_constraints[j] = []

    for i in range(index,len(file_list)):
        cons_name = file_list[i].strip(':')
        associated_var = file_list[i+2].split()[1]
        var_constraints[associated_var].append(cons_name.strip(''))






print(get_domain("graph_coloring.yaml"))




