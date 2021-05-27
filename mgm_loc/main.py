import sys
import mgm
import mcs_mgm
import gca_mgm
import handle_file as hf
file = hf.file_name(sys.argv)
def histogram(histo,nbr_launch,file):
    """
    Create a file with all the results on multiple problems
    :param histo:
    :return:
    """
    with open("Results/Histogram_{}_{}.yaml".format(nbr_launch,file)) as f:
        f.write("mgm results :"+"\n")
        for  val,occur in histo["mgm"].items():
            f.write("value "+str(val)+" : "+"occur"+"\n")
        f.write("mcs_mgm results :" + "\n")
        for val, occur in histo["mcs_mgm"].items():
            f.write("value " + str(val) + " : " + "occur" + "\n")
        f.write("gca_mgm results :" + "\n")
        for val, occur in histo["gca_mgm"].items():
            f.write("value " + str(val) + " : " + "occur" + "\n")


if '__main__' ==__name__:
    for element in range(len(sys.argv)):
        if sys.argv[element] == "nbr_iter":
            nbr_launch = int(sys.argv[element + 1])

    histo = {"mgm": {},"mcs_mgm" : {},"gca_mgm" : {}}
    for rep in range (nbr_launch):
        if sys.argv[1] == "mgm":
            final_cost = mgm.launch_prog()
            try:
                histo["mgm"][final_cost] += 1
            except:
                histo["mgm"][final_cost] = 1
        elif sys.argv[1] == "mcs_mgm":
            final_cost2 = mcs_mgm.launch_prog()
            try:
                histo["mcs_mgm"][final_cost] += 1
            except:
                histo["mcs_mgm"][final_cost] = 1
        else:
            final_cost = gca_mgm.launch_prog()
            try:
                histo["gca_mgm"][final_cost] += 1
            except:
                histo["gca_mgm"][final_cost] = 1
    histogram(histo,nbr_launch,file)

