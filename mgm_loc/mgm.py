import handle_file as hf
import handle_problem as hp
ligne = "main.py mgm time 5  graph_exemple_5.yaml"
command = ligne.split()
algo = hf.get_algo(command)

file = hf.file_name(command)
domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(file)
time_limit = hf.time_limit(command)

agents_param = hp.config_agents(variables, agents, constraints)
agents_param = hp.init_agents(agents_param, domain)
#agents_param = hp.init_agents_contr(agents_param, domain)
print(agents_param)
var_value = hp.get_var_value(agents_param)
cost_init = 0
hp.calculate_constraint(agents_param, cons_dict, var_value)
for agent in agents_param.values():
    cost_init += float(agent["cons_value"])
nbr_cycle = 0
print("initialization : ",agents_param,"\n")
while nbr_cycle < time_limit:
    value_mess = hp.send_values(agents_param)
    agents_param = hp.collect_values(agents_param, value_mess)

    all_LR = hp.all_LR(agents_param)
    agents_param = hp.collect_LR(agents_param, all_LR)
    agents_param = hp.update_value(agents_param, all_LR)
    var_value = hp.get_var_value(agents_param)
    agents_param = hp.calculate_constraint(agents_param, cons_dict, var_value)
    print("cycle{} : ".format(nbr_cycle),agents_param,"\n")
    nbr_cycle += 1
final_result = hp.result_final(cons_dict, var_value, constraints)
hp.show_result(agents_param, file, algo, final_result, cost_init)

"""def launch_prog():
    
    Launch the program
    :return: None
    
    algo = hf.get_algo(sys.argv)

    file = hf.file_name(sys.argv)
    domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(file)
    time_limit = hf.time_limit(sys.argv)

    agents_param = hp.config_agents(variables, agents, constraints)
    #agents_param = hp.init_agents(agents_param, domain)
    agents_param = hp.init_agents_contr(agents_param, domain)
    var_value = hp.get_var_value(agents_param)
    cost_init = 0
    hp.calculate_constraint(agents_param,cons_dict,var_value)
    for agent in agents_param.values():
        cost_init += float(agent["cons_value"])
    nbr_cycle = 0
    while nbr_cycle < time_limit:
        value_mess = hp.send_values(agents_param)
        agents_param = hp.collect_values(agents_param, value_mess)

        all_LR = hp.all_LR(agents_param)
        agents_param = hp.collect_LR(agents_param, all_LR)
        agents_param = hp.update_value(agents_param, all_LR)
        var_value = hp.get_var_value(agents_param)
        agents_param = hp.calculate_constraint(agents_param, cons_dict, var_value)
        nbr_cycle += 1
    final_result=hp.result_final(cons_dict,var_value,constraints)
    print(agents_param)
    hp.show_result(agents_param, file, algo,final_result,cost_init)"""
