import handle_file as hf
import handle_problem as hp
import sys


def launch_prog():
    
    """Launch the program
    :return: None"""

    algo = hf.get_algo(sys.argv)
    file = hf.file_name(sys.argv)
    domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(
        file)  # Initialize the parameters of the problem
    time_limit = hf.time_limit(sys.argv)

    agents_param = hp.config_agents(variables, agents, constraints)  # Initialize each agent
    agents_param = hp.init_agents(agents_param, domain)
    # agents_param = hp.init_agents_contr(agents_param, domain)
    var_value = hp.get_var_value(agents_param)
    hp.calculate_constraint_init(agents_param, cons_dict, var_value)
    cost_init = 0
    for agent in agents_param.values():
        cost_init += float(agent["cons_value"])
    nbr_cycle = 0
    while nbr_cycle < time_limit:
        value_mess = hp.send_values(agents_param)
        agents_param = hp.collect_values(agents_param, value_mess)  # collect values of the neighbors


        all_LR = hp.all_LR(agents_param)  # compute the LR for each variable
        agents_param = hp.collect_LR(agents_param, all_LR)
        agents_param = hp.update_value(agents_param, all_LR)  # update only one value, depending on the LRs
        var_value = hp.get_var_value(agents_param)
        agents_param = hp.calculate_constraint(agents_param, cons_dict,
                                               var_value)  # Calculate the new constraints values
        nbr_cycle += 1
    final_result = hp.result_final(cons_dict, var_value, constraints)
    hp.show_result(agents_param, file, algo, final_result, cost_init)
    cost = 0
    for val in final_result.values():
        cost += float(val)
    return cost , cost_init