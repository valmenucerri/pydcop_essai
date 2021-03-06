import handle_file as hf
import sys
import handle_problem as hp


def launch_prog():
    """
    Launch the program
    :return: None
    """
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
    prev_var_value = None
    cons_to_send = {}
    while nbr_cycle < time_limit:
        value_mess = hp.send_values(agents_param)
        agents_param = hp.collect_values(agents_param, value_mess)  # collect values of the neighbors
        for agent in agents_param.values():
            cons_to_send[agent[
                "variable"]] = []  # prepare the dictionary where the program will put the constraints that must be sent

        for agent, param in agents_param.items():  # Here's the new part, that makes the difference between MGM and MCS-MGM
            if param["current_LR"] is not None:
                new_agent, cons_to_transfer = hp.share_constraint_2(param, prev_var_value)
                agents_param[agent] = new_agent
                for var, cons in cons_to_transfer.items():
                    for i in range(len(cons)):
                        cons_to_send[var].append(cons[i])

        agents_param = hp.update_cons(cons_to_send, agents_param)  # collect the neighbors constraints update
        all_LR = hp.all_LR(agents_param)  # compute the LR for each variable
        agents_param = hp.collect_LR(agents_param, all_LR)
        prev_var_value = hp.get_var_value(agents_param)
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
    return cost,cost_init