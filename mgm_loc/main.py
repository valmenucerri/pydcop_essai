import sys
import mgm
import mcs_mgm
import gca_mgm
import handle_file as hf
from handle_problem import draw_histo
file = hf.file_name(sys.argv)
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
    if sys.argv[1] == "mgm":
        final_cost = mgm.launch_prog()
    elif sys.argv[1] == "mcs_mgm":
        final_cost2 = mcs_mgm.launch_prog()
    elif sys.argv[1] == "all":
        for element in range(len(sys.argv)):
            if sys.argv[element] == "nbr_iter":
                nbr_launch = int(sys.argv[element + 1])
        histo = {"mgm": {}, "mcs_mgm": {}, "gca_mgm": {}}

        for rep in range(nbr_launch):
            final_cost,cost_init = mgm.launch_prog()
            try:
                histo["mgm"][final_cost][0] += 1
                histo["mgm"][final_cost][1].append(cost_init)

            except:
                histo["mgm"][final_cost] = [1,[cost_init]]

            final_cost2,cost_init2 = mcs_mgm.launch_prog()
            try:
                histo["mcs_mgm"][final_cost2][0] += 1
                histo["mcs_mgm"][final_cost2][1].append(cost_init2)
            except:
                histo["mcs_mgm"][final_cost2] = [1,[cost_init2]]

            final_cost3,cost_init3 = gca_mgm.launch_prog()
            try:
                histo["gca_mgm"][final_cost3][0] += 1
                histo["gca_mgm"][final_cost3][1].append(cost_init3)
            except:
                histo["gca_mgm"][final_cost3] = [1, [cost_init3]]
        histogram(histo, nbr_launch, file)
        draw_histo(histo,nbr_launch,file)
    else:
        final_cost = gca_mgm.launch_prog()
    print('\a')

