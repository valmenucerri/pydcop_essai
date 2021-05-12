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


        domain = {name: values}
        return domain

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
    :param file_list:
    :param first_index:
    :return:
    '''
print(get_domain("graph_coloring.yaml"))




