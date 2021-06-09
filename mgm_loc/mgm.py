import handle_file as hf
import handle_problem as hp



def launch_prog(argv):
    """Launch the program
    :return: None"""

    algo = hf.get_algo(argv)
    file = hf.file_name(argv)
    domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(
        file)
    obj = hp.HP(domain, variables, constraints, cons_dict, cons_for_var, agents)

    # Initialize the parameters of the problem
    obj.init_problem(argv)
    time_limit = hf.time_limit(argv)

    agents_param = obj.config_agents()  # Initialize each agent
    agents_param = obj.init_agents(agents_param)
    # agents_param = obj.init_agents_contr(agents_param, domain)
    var_value = obj.get_var_value(agents_param)
    obj.calculate_constraint_init(agents_param, var_value)
    cost_init = 0
    for agent in agents_param.values():
        cost_init += float(agent["cons_value"])
    nbr_cycle = 0
    while nbr_cycle < time_limit:
        value_mess = obj.send_values(agents_param)
        agents_param = obj.collect_values(agents_param, value_mess)  # collect values of the neighbors

        all_LR = obj.all_LR(agents_param)  # compute the LR for each variable
        agents_param = obj.collect_LR(agents_param, all_LR)
        agents_param = obj.update_value(agents_param, all_LR)  # update only one value, depending on the LRs
        var_value = obj.get_var_value(agents_param)
        agents_param = obj.calculate_constraint(agents_param,
                                               var_value)  # Calculate the new constraints values
        nbr_cycle += 1
    final_result = obj.result_final(var_value, constraints)
    obj.show_result(agents_param, file, algo, final_result, cost_init)
    cost = 0
    for val in final_result.values():
        cost += float(val)
    return cost, cost_init
