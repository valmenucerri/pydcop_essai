import sys
import mgm
import mcs_mgm
import gca_mgm
import handle_file as hf
import handle_problem as hp





def histogram(histo,nbr_launch,file):
    """
    Create a file with all the results on multiple problems
    :param histo:
    :return:
    """
    with open("Results/Histogram_{}_{}.txt".format(nbr_launch,file.strip(".yaml")),'w') as f:
        f.write("mgm results :"+"\n")
        for  val,occur in histo["mgm"].items():
            f.write("value "+str(val)+" : "+str(occur[0])+"     "+"Initial costs : "+str(occur[1]).strip("["+"]")+"\n")
        f.write("\n")
        f.write("mcs_mgm results :" + "\n")
        for val, occur in histo["mcs_mgm"].items():
            f.write("value " + str(val) + " : " + str(occur[0])+"     "+"Initial costs : "+str(occur[1]).strip("["+"]")+"\n")
        f.write("\n")
        f.write("gca_mgm results :" + "\n")
        for val, occur in histo["gca_mgm"].items():
            f.write("value " + str(val) + " : " + str(occur[0])+"     "+"Initial costs : "+str(occur[1]).strip("["+"]")+"\n")


if '__main__' ==__name__:
    argv = sys.argv
    file = hf.file_name(argv)
    domain, variables, constraints, cons_dict, cons_for_var, agents = hf.get_data(
        file)
    obj = hp.HP(domain, variables, constraints, cons_dict, cons_for_var, agents)

    if argv[1] == "mgm":
        final_cost = mgm.launch_prog(argv)
    elif argv[1] == "mcs_mgm":
        final_cost2 = mcs_mgm.launch_prog(argv)
    elif argv[1] == "all":
        for element in range(len(sys.argv)):
            if sys.argv[element] == "nbr_iter":
                nbr_launch = int(sys.argv[element + 1])
        histo = {"mgm": {}, "mcs_mgm": {}, "gca_mgm": {}}

        for rep in range(nbr_launch):
            final_cost,cost_init = mgm.launch_prog(argv)
            try:
                histo["mgm"][final_cost][0] += 1
                histo["mgm"][final_cost][1].append(cost_init)

            except:
                histo["mgm"][final_cost] = [1,[cost_init]]

            final_cost2,cost_init2 = mcs_mgm.launch_prog(argv)
            try:
                histo["mcs_mgm"][final_cost2][0] += 1
                histo["mcs_mgm"][final_cost2][1].append(cost_init2)
            except:
                histo["mcs_mgm"][final_cost2] = [1,[cost_init2]]

            final_cost3,cost_init3 = gca_mgm.launch_prog(argv)
            try:
                histo["gca_mgm"][final_cost3][0] += 1
                histo["gca_mgm"][final_cost3][1].append(cost_init3)
            except:
                histo["gca_mgm"][final_cost3] = [1, [cost_init3]]
        histogram(histo, nbr_launch, file)
        obj.draw_histo(histo,nbr_launch,file)
        print("\a")
    else:
        final_cost = gca_mgm.launch_prog(argv)

