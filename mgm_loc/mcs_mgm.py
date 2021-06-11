

import handle_file as hf
import handle_problem as hp
import time



def launch_prog(argv):
    """
    Launch the program
    :return: None
    """
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
    time_limit = hf.time_limit(argv)# get the number max of cycles

    agents_param = obj.config_agents()  # Initialize each agent
    agents_param = obj.init_agents(agents_param) # line 1
    var_value = obj.get_var_value(agents_param)
    obj.calculate_constraint_init(agents_param, var_value)
    cost_init = 0
    for agent in agents_param.values():
        cost_init += float(agent["cons_value"])
    nbr_cycle = 0
    prev_var_value = None
    cons_to_send = {}
    conti = True
    termination = 0
    prev_cost = 0
    start = time.process_time()
    while nbr_cycle < time_limit:# and conti:  # line 2
        start_cycle = time.process_time()
        value_mess = obj.send_values(agents_param)  # line 3
        agents_param = obj.collect_values(agents_param, value_mess)  # line 4
        for agent in agents_param.values():
            cons_to_send[agent[
                "variable"]] = []  # prepare the dictionary where the program will put the constraints that must be sent
        # Here's the new part, that makes the difference between MGM and MCS-MGM
        conditionnal_cons = {}
        for agent, param in agents_param.items():
            # line 5
            if param["current_LR"] is not None:
                new_agent, cons_to_transfer,cons_transferred = obj.share_constraint_1(param, prev_var_value)  # line 7/8/9
                agents_param[agent] = new_agent
                obj.cons_update(cons_to_transfer)# !!!!!!! regarder cette fonction !!!!!!!

                if cons_transferred is not None:
                    try:
                        conditionnal_cons[cons_transferred[0]].append(cons_transferred[1])
                    except:
                        conditionnal_cons[cons_transferred[0]] = [cons_transferred[1]]
        if len(conditionnal_cons) != 0:
            agents_param = obj.update_cons(conditionnal_cons,agents_param)# line 10/11

        # compute the LR for each variable
        all_LR = obj.all_LR(agents_param,objective)  # line 12/13
        agents_param = obj.collect_LR(agents_param, all_LR)  # line 14
        prev_var_value = obj.get_var_value(agents_param)
        agents_param = obj.update_value(agents_param, all_LR,objective)  # line 15/16/17
        var_value = obj.get_var_value(agents_param)
        agents_param = obj.calculate_constraint(agents_param,var_value)
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



    final_result = obj.result_final(var_value, constraints)
    end = time.process_time()
    time_tot = end - start
    print(agents_param)
    obj.show_result(agents_param, file, algo, final_result, cost_init,height_cons,time_tot)  # Create the file with the results written on it
    cost = 0
    for val in final_result.values():
        cost += float(val)
    print("time :",time_tot)

    return cost,cost_init

