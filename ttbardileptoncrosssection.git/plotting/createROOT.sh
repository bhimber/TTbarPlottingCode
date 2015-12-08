#SYSTEMATICs="mini,btag_up"
SYSTEMATICs="BJesUnc_down,BJesUnc_up,EtaIntercalibrationModel_down,EtaIntercalibrationModel_up,EtaIntercalibrationTotalStat_down,EtaIntercalibrationTotalStat_up,JesEffectiveDet1_down,JesEffectiveDet1_up,JesEffectiveDet2_down,JesEffectiveDet2_up,JesEffectiveDet3_down,JesEffectiveDet3_up,JesEffectiveMix1_down,JesEffectiveMix1_up,JesEffectiveMix2_down,JesEffectiveMix2_up,JesEffectiveMix3_down,JesEffectiveMix3_up,JesEffectiveMix4_down,JesEffectiveMix4_up,JesEffectiveModel1_down,JesEffectiveModel1_up,JesEffectiveModel2_down,JesEffectiveModel2_up,JesEffectiveModel3_down,JesEffectiveModel3_up,JesEffectiveModel4_down,JesEffectiveModel4_up,JesEffectiveStat1_down,JesEffectiveStat1_up,JesEffectiveStat2_down,JesEffectiveStat2_up,JesEffectiveStat3_down,JesEffectiveStat3_up,JesEffectiveStat4_down,JesEffectiveStat4_up,Pileup_OffsetMu_down,Pileup_OffsetMu_up,Pileup_OffsetNPV_down,Pileup_OffsetNPV_up,Pileup_Pt_down,Pileup_Pt_up,Pileup_Rho_down,Pileup_Rho_up,PunchThrough_down,PunchThrough_up,SinglePart_down,SinglePart_up,btag_down,btag_up,ctautag_down,ctautag_up,eer_down,eer_up,ees_down,ees_up,el_idSF_down,el_idSF_up,el_recSF_down,el_recSF_up,el_trigSF_down,el_trigSF_up,flavor_comp_down,flavor_comp_up,flavor_response_down,flavor_response_up,jeff,jer,jvf_down,jvf_up,mini,mistag_down,mistag_up,mu_idSF_down,mu_idSF_up,mu_recSF_down,mu_recSF_up,mu_trigSF_down,mu_trigSF_up,muid_res,mums_res,musc_down,musc_up,res_soft_down,res_soft_up,sc_soft_down,sc_soft_up"

for SYSTEMATIC in `echo ${SYSTEMATICs} | awk -v RS=, '{print}'`
do
    echo "SYSTEMATIC=${SYSTEMATIC}"
    python ttbardilep.py ./configfiles/ttbarelmu.json  0 ${SYSTEMATIC}
done

# do do:
# 1. add all the variations in SYSTEMATICs
# 2. change in ttbarelmu.json from mcfiles_test.txt to mcfiles.txt to run over all the files.
# 3. run by ./createROOT.sh