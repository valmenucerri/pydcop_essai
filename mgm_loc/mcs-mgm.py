import handle_file as hf
import sys
file = hf.file_name(sys.argv)
domain, variables , constraints , cons_dict , cons_for_var , agents= hf.get_data(file)


def config_agents(variables,agents):
    agents_param = {}
    all_var = []
    for var in variables.keys():
        all_var.append(var)
    for ag in range(len(agents)):
        actual_agent = {}
        actual_agent["variable"] = all_var[ag]
        actual_agent["value"] = None
        actual_agent["neighbors"] = None
        agents_param[agents[ag]] = actual_agent


    return agents_param


print(config_agents(variables,agents))