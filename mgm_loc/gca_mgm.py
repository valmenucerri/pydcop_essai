import handle_file as hf
import sys
import handle_problem as hp
import time

def launch_prog(argv):
    """
    Launch the program
    :return: None
    """
    algo = hf.get_algo(argv)
    time_cycle = {} # Dict with the time for each cycle {cycle : time associated}
    file = hf.file_name(argv)
    objective = hf.get_objective(file)
    domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(
        file)
    obj = hp.HP(domain, variables, constraints, cons_dict, cons_for_var, agents)
    height_cons = {}
    for cons,form in cons_dict.items():
        height_cons[cons] = len(form[0].split())

    # Initialize the parameters of the problem
    obj.init_problem(argv)
    conti = True
    time_limit = hf.time_limit(argv)
    agents_param = obj.config_agents()  # Initialize each agent
    agents_param = obj.init_agents(agents_param)
    var_value = obj.get_var_value(agents_param)
    obj.calculate_constraint_init(agents_param, var_value)
    cost_init = 0
    termination = 0
    for agent in agents_param.values():
        cost_init += float(agent["cons_value"])
    nbr_cycle = prev_cost =  0
    prev_var_value = None
    cons_to_send = {}
    start = time.process_time()
    while nbr_cycle < time_limit and conti:
        start_cycle = time.process_time()
        value_mess = obj.send_values(agents_param)
        agents_param = obj.collect_values(agents_param, value_mess)  # collect values of the neighbors
        for agent in agents_param.values():
            cons_to_send[agent[
                "variable"]] = []  # prepare the dictionary where the program will put the constraints that must be sent

        for agent, param in agents_param.items():  # Here's the new part, that makes the difference between MGM and MCS-MGM
            if param["current_LR"] is not None:
                new_agent, cons_to_transfer = obj.share_constraint_2(param, prev_var_value)  # line 7/8/9
                print(cons_to_transfer)
                agents_param[agent] = new_agent
                for var, cons in cons_to_transfer.items():
                    formula_list = cons.split()
                    if "*" in formula_list:
                        cons_dict[constraints[var][0]][0] = cons + " + " + cons_dict[constraints[var][0]][0]
                    else:
                        cons_dict[constraints[var][0]][0] += " " + cons

        agents_param = obj.update_cons(cons_to_send, agents_param)  # collect the neighbors constraints update
        all_LR = obj.all_LR(agents_param,objective)  # compute the LR for each variable
        agents_param = obj.collect_LR(agents_param, all_LR)
        prev_var_value = obj.get_var_value(agents_param)
        agents_param = obj.update_value(agents_param, all_LR,objective) # update only one value, depending on the LRs
        var_value = obj.get_var_value(agents_param)
        agents_param = obj.calculate_constraint(agents_param,
                                               var_value)  # Calculate the new constraints values
        end_cycle = time.process_time()
        cycle_time = end_cycle - start_cycle
        time_cycle[nbr_cycle] = cycle_time
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
    obj.show_result(agents_param, file, algo, final_result, cost_init,height_cons,time_tot)
    cost = 0
    print(cons_dict)

    for val in final_result.values():
        cost += float(val)
    return cost,cost_init