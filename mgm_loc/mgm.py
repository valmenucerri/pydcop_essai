import handle_file as hf
import sys
import handle_problem as hp
file = hf.file_name(sys.argv)
domain, variables , constraints , cons_dict , cons_for_var , agents= hf.get_data(file)
time_limit = hf.time_limit(sys.argv)

agents_param = hp.config_agents(variables,agents,constraints)
agents_param = hp.init_agents(agents_param,domain)
var_value = hp.get_var_value(agents_param)
nbr_cycle = 0
while nbr_cycle < time_limit:
    value_mess = hp.send_values(agents_param)
    agents_param = hp.collect_values(agents_param,value_mess)
    all_LR = hp.all_LR(agents_param)
    agents_param = hp.collect_LR(agents_param,all_LR)
    agents_param = hp.update_value(agents_param,all_LR)
    var_value = hp.get_var_value(agents_param)
    agents_param = hp.calculate_constraint(agents_param,cons_dict,var_value)
    nbr_cycle += 1

hp.show_result(agents_param,file)
