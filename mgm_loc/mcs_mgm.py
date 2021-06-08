

import handle_file as hf
import handle_problem as hp
import sys



def launch_prog():
    """
    Launch the program
    :return: None
    """
    algo = hf.get_algo(sys.argv)
    file = hf.file_name(sys.argv)
    domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(
        file)  # Initialize the parameters of the problem
    time_limit = hf.time_limit(sys.argv)# get the number max of cycles

    agents_param = hp.config_agents(variables, agents, constraints)  # Initialize each agent
    agents_param = hp.init_agents(agents_param, domain) # line 1
    var_value = hp.get_var_value(agents_param)
    hp.calculate_constraint_init(agents_param, cons_dict, var_value)
    cost_init = 0
    for agent in agents_param.values():
        cost_init += float(agent["cons_value"])
    nbr_cycle = 0
    prev_var_value = None
    cons_to_send = {}
    while nbr_cycle < time_limit:  # line 2
        value_mess = hp.send_values(agents_param)  # line 3
        agents_param = hp.collect_values(agents_param, value_mess)  # line 4
        for agent in agents_param.values():
            cons_to_send[agent[
                "variable"]] = []  # prepare the dictionary where the program will put the constraints that must be sent
        # Here's the new part, that makes the difference between MGM and MCS-MGM
        for agent, param in agents_param.items(): # line 5
            if param["current_LR"] is not None:
                new_agent, cons_to_transfer = hp.share_constraint_1(param, prev_var_value,cons_dict)  # line 7/8/9
                agents_param[agent] = new_agent
                for var, cons in cons_to_transfer.items():
                    formula_list = cons.split()
                    if "*" in formula_list:
                        cons_dict[constraints[var][0]][0] = cons +" + "+ cons_dict[constraints[var][0]][0]
                    else:
                        cons_dict[constraints[var][0]][0] += " "+cons

        #agents_param = hp.update_cons(cons_to_send, agents_param)  # line 10/11
        # compute the LR for each variable
        all_LR = hp.all_LR(agents_param)  # line 12/13
        agents_param = hp.collect_LR(agents_param, all_LR)  # line 14
        prev_var_value = hp.get_var_value(agents_param)
        agents_param = hp.update_value(agents_param, all_LR)  # line 15/16/17
        var_value = hp.get_var_value(agents_param)
        agents_param = hp.calculate_constraint(agents_param, cons_dict, var_value)
        nbr_cycle += 1

    final_result = hp.result_final(cons_dict, var_value, constraints)
    hp.show_result(agents_param, file, algo, final_result, cost_init)  # Create the file with the results written on it
    cost = 0
    for val in final_result.values():
        cost += float(val)
    return cost,cost_init

