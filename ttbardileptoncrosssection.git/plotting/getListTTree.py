#!/usr/bin/python
from ROOT import *

filename="/nfs/atlas/ugul04/TTbarDilepXSec20150317/user.ugul.117050.e1728_s1581_s1586_r3658_r3549_p1575.TTbarDilepXSec20150320_ML_7F.root.22325534/user.ugul.5151411._000002.ML_7F.root"
file=TFile(filename,"READ")
tree=file.Get("mini")
systematics=""
for i,key in enumerate(file.GetListOfKeys()):
    if i==0:
        prefix=""
    else:
        prefix=","
    if key.GetClassName()=="TTree":
        systematics+=prefix+key.GetName()
# 
print "SYSTEMATICs=\""+systematics+"\""
