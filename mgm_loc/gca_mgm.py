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
    var_value = hp.get_var_value(agents_param)
    nbr_cycle = 0
    prev_var_value = None

    while nbr_cycle < time_limit:
        value_mess = hp.send_values(agents_param)
        agents_param = hp.collect_values(agents_param, value_mess)  # collect values pf the neighbors
        cons_to_send = {}  # prepare the dictionary where the program will put the constraints that must be sent

        for agent, param in agents_param.items():  # Here's the new part, that makes the difference between MGM and MCS-MGM
            if param["current_LR"] is not None:
                new_agent, cons_to_transfer = hp.share_constraint_2(param, prev_var_value)
                agents_param[agent] = new_agent
                cons_to_send.update(cons_to_transfer)

        agents_param = hp.update_cons(cons_to_send, agents_param)  # collect the neighbors constraints update
        all_LR = hp.all_LR(agents_param)  # compute the LR for each variable
        agents_param = hp.collect_LR(agents_param, all_LR)
        prev_var_value = hp.get_var_value(agents_param)
        agents_param = hp.update_value(agents_param, all_LR)  # update only one value, depending on the LRs
        var_value = hp.get_var_value(agents_param)
        agents_param = hp.calculate_constraint(agents_param, cons_dict, var_value)  # Calculate the new constraints values
        nbr_cycle += 1

    hp.show_result(agents_param, file,algo)  # Create the file with the results written on it
