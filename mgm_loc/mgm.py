import handle_file as hf
import handle_problem as hp
import time


def launch_prog(argv):
    """Launch the program
    :return: None"""

    global start_cycle
    algo = hf.get_algo(argv)
    time_cycle = {}
    file = hf.file_name(argv)
    objective = hf.get_objective(file)
    domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(
        file)
    obj = hp.HP(domain, variables, constraints, cons_dict, cons_for_var, agents)
    height_cons = {}
    for cons, form in cons_dict.items():
        height_cons[cons] = len(form[0].split())

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
    nbr_cycle = prev_cost = 0
    conti = True
    termination = 0
    start = time.process_time()
    while nbr_cycle < time_limit:# and conti:
        start_cycle = time.process_time()
        value_mess = obj.send_values(agents_param)
        agents_param = obj.collect_values(agents_param, value_mess)  # collect values of the neighbors

        all_LR = obj.all_LR(agents_param,objective)  # compute the LR for each variable
        agents_param = obj.collect_LR(agents_param, all_LR)
        agents_param= obj.update_value(agents_param, all_LR,objective) # update only one value, depending on the LRs
        var_value = obj.get_var_value(agents_param)
        agents_param = obj.calculate_constraint(agents_param,
                                               var_value)  # Calculate the new constraints values
        final_result = obj.result_final(var_value, constraints)
        cost = 0
        for val in final_result.values():
            cost += float(val)
        if prev_cost == cost:
            termination += 1
        else:
            termination = 0
        if termination == 6:
            conti = False
        nbr_cycle += 1
        prev_cost = cost
        print(nbr_cycle)

    final_result = obj.result_final(var_value, constraints)
    end = time.process_time()
    time_tot = end - start
    end_cycle = time.process_time()
    cycle_time = end_cycle - start_cycle
    time_cycle[nbr_cycle] = cycle_time
    obj.show_result(agents_param, file, algo, final_result, cost_init,height_cons,time_tot)
    cost = 0
    for val in final_result.values():
        cost += float(val)
    return cost, cost_init
