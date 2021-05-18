import handle_file as hf
import sys
import random as r
file = hf.file_name(sys.argv)
domain, variables , constraints , cons_dict , cons_for_var , agents= hf.get_data(file)


def config_agents(variables,agents):
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
        actual_agent["value"] = None
        actual_agent["neighbors"] = []
        agents_param[agents[ag]] = actual_agent
        for var2 in all_var:
            if var2 != actual_agent["variable"]:
                actual_agent["neighbors"].append(var2)

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
        agent["value"]= random_val
    return agents_param

