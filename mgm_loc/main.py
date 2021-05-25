import sys
import mgm
import mcs_mgm
import gca_mgm



if '__main__' ==__name__:
    if sys.argv[1] == "mgm":
        mgm.launch_prog()
    elif sys.argv[1] == "mcs_mgm":
        mcs_mgm.launch_prog()
    else:
        gca_mgm.launch_prog()


