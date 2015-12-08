 # calculates differential cross sections from an input file with a
# data stack, e.g. "data_lep0_pt"; a background stack, e.g.
# "bkg_lep0_pt"; and another file with the relevant efficiency
# histograms, e.g. "lep0_pt_eff".

# these should be set in the appropriate .json file.

def main():                                                                                    
    from sys import argv
    import json

    dconfig = json.load(open(argv[1]))    

    import ROOT

    # the files containing the spectra (datafile) and efficiency are parsed by PyROOT 
    # histograms (efffile)
    datafile = ROOT.TFile(dconfig["data_file"])
    efffile = ROOT.TFile(dconfig["eff_file"])

    # the file we will write to
    outfile = ROOT.TFile(dconfig["out_file"], "create")

    # luminosity in 1/pb
    lumi = dconfig["lumi"]

    for run_name, rundict in dconfig["xsec_runs"].iteritems():
        print " run_name", " rundict", run_name,rundict
        
        data_hist_list = list(datafile.Get(rundict["data_stack"]).GetHists())
        print "data_hist_list",  data_hist_list 
        sm_hist_list = list(datafile.Get(rundict["sm_stack"]).GetHists())
        print "sm_hist_list", sm_hist_list
        if len(data_hist_list) < 1 or len(sm_hist_list) < 2:
            print "oops: we don't have enough inputs from the datafile for run", run_name
            continue

        eff_hist = efffile.Get(rundict["eff_hist"])

        # sum all non-ttbar histograms into a bkg hist.
        # ttbar should always be the last histogram.
       
        bkg_hist = sm_hist_list[0].Clone()
        print "sm_hist_list[0]",sm_hist_list[0]
        for h in sm_hist_list[1:-1]:
         print "background hist list,h", h
         bkg_hist.Add(h)

        # scale the bkgs by the luminosity
        bkg_hist.Scale(lumi)

        # TODO
        # for debugging
        print "bkg bin content 3:", bkg_hist.GetBinContent(3)
        print "ttbar bin content 3:", sm_hist_list[-1].GetBinContent(3)*lumi

        # sum over all data histograms.
        data_hist = data_hist_list[0].Clone()
        for h in data_hist_list[1:]:
            data_hist.Add(h)

        print "data bin content 3:", data_hist.GetBinContent(3)

        # check to make sure the binning is ~consistent
        if eff_hist.GetNbinsX() != data_hist.GetNbinsX():
            print "oops: we have a different number of bins for the efficiency and data histograms for run", run_name
            continue


        # calculate the differential cross section
        xsec_hist = data_hist.Clone()


        # TODO:
        # we are getting negative cross sections.
        # this is probably a problem with the background subtraction.
        # let's try printing out some information to get a hint of
        # what's going on...

        # subtract the backgrounds from the data
        xsec_hist.Add(bkg_hist, -1)

        xsec_hist.Scale(1.0/lumi)
        xsec_hist.Divide(eff_hist)
        xsec_hist.SetName(run_name + "_diff_xsec")
        xsec_hist.SetTitle(run_name + "_diff_xsec")

        # TODO
        # set correct formatting for histogram: axis labels, etc.

        xsec_hist.Write()

        continue


# run main()
if __name__ == "__main__":
    main()
