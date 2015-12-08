from sys import argv, stdout
from DCut import mul_cut, combine_cuts, DCut

# allow cuts to be a cut string or a list of cuts
# doesn't attempt to find loops: be careful!
def resolve_cut(cutkey, cutdict):
    cut = cutdict[cutkey]

    if type(cut) is list:
        return combine_cuts(
                map(lambda c: resolve_cut(c, cutdict), cut)
            )
    else:
        return DCut(cut)


def main(myargv):

    # number of arguments + 1
    if len(myargv)!=4:
        print "Usage: python", myargv[0], "config_file    useoriginal tree "
        print "Usage: python", myargv[0], "ttbarelmu.json 1           mini"
        print "Usage: python", myargv[0], "ttbarelmu.json 1           btag_up"
        stdout.flush()
        exit(1)

    configfilename=myargv[1]
    useoriginal=bool(int(myargv[2]))
    treename=myargv[3]

    debug=True
    if debug:
        print "useoriginal",useoriginal
        print "configfilename",configfilename
        print "treename",treename

    # imports
    from itertools import product, combinations
    from glob import glob

    import TTbarDilepPlots
    from DUtils import make_hist, make_stack
    from DSample import DSample
    from DSampleDict import getprocess
    import json

    import ROOT
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(False)
    ROOT.TH1.SetDefaultSumw2(True)

    # initialize top data prep tool
    from os import environ
    rootcoredir = environ["ROOTCOREDIR"]
    if debug:
        print "rootcoredir",rootcoredir
    datapreppath = glob("%s/lib/*/libTopDataPreparation.so" % rootcoredir)
    ROOT.gSystem.Load(datapreppath[0])

    datapreptool = ROOT.SampleXsection()
    datapreptool.readFromFile(rootcoredir +
            "/data/TopDataPreparation/XSection-MC12-8TeV.data")
    datapreptool.readFromFile(rootcoredir +
            "/data/TopDataPreparation/XSection-MC12-8TeV-4gt.data")


    # open the config file
    dconfig = json.load(open(configfilename))



    # collect all infiles by dsid
    filesdict = {}
    datasetsfile = dconfig["datasetsfile"]
    for filename in open(datasetsfile):
        if filename.startswith("#"):
            continue

        filename = filename.rstrip().lstrip()

        print "opening file", filename; stdout.flush()
        f = ROOT.TFile.Open(filename)
        if not f:
            print "ERROR: unable to open input file %s. Exiting." % filename
            exit(-1)

        if useoriginal:
            treename=dconfig["tree_name"]
        else:
            # from the command line argument to loop over all systematic trees
            None
        tree = f.Get(treename)
        tree.GetEntry(0)

        # data dsid should be zero.
        dsid = tree.channelNumber
        if dsid > 200000:
            dsid = 0

        f.Close()

        if dsid in filesdict:
            filesdict[dsid].append(filename)
        else:
            filesdict[dsid] = [filename]

        continue

    # now loop over all files and make the sample for each dsid.
    bkg_samps = []
    data_samps = []
    sig_samps = []
    for dsid, fnames in filesdict.items():
        datasetname = fnames[0].split('/')[-2]

        print "looking at dataset:"
        print datasetname
        print "with dsid:", dsid

        title = fnames[0].replace('/', '_').replace('.', '_')
        chain = ROOT.TChain(dconfig["tree_name"])
        friend_chains = []
        if "friend_tree_names" in dconfig:
            for friend in dconfig["friend_tree_names"]:
                friend_chains.append(ROOT.TChain(friend))

        xsec = datapreptool.getXsection(dsid)
        nevt = 0.0

        for fname in fnames:
            print "looking in file", fname; stdout.flush()

            f = ROOT.TFile.Open(fname)
            if not f:
                print "ERROR: unable to open input file %s. Exiting." % fname
                exit(-1)

            hcutflow = f.Get(dconfig["cutflow"])

            nevt += hcutflow.GetBinContent(1)
            f.Close()

            chain.AddFile(fname)
            map(lambda c: c.AddFile(fname), friend_chains)
            continue

        # register the friend trees
        map(lambda c: chain.AddFriend(c), friend_chains)

        lab = getprocess(title)
        # TODO
        # unknown
        if lab in ["TTBAR", "SINGLETOP", "ZJETS", "DIBOSON", "OTHER"]:
            print "adding sample %s: %s" % (lab, title); stdout.flush()
            print "xsec: %s" % xsec; stdout.flush()
            print "nevt: %s" % nevt; stdout.flush()
            print "norm: %s" % (xsec/nevt); stdout.flush()
            bkg_samps.append(DSample(title, title, dsid, chain, xsec/nevt))
        elif lab == "DATA":
            print "adding sample %s: %s" % (lab, title); stdout.flush()
            print "xsec: %s" % xsec; stdout.flush()
            print "nevt: %s" % nevt; stdout.flush()
            data_samps.append(DSample(title, title, dsid, chain, 1))
        # TODO
        # this is really, really ugly.
        else:
            print "sample", title, "with label", lab, "will not be plotted."
            stdout.flush()

        continue


    weight = DCut(dconfig["weight"])
    for (outfname, cutname) in dconfig["runs"]:

        if useoriginal:
            None
        else:
            # overwrite the config file input a differen one for each treename
            # meaning a different one for each systematic uncertainty
            outfname="./output/"+cutname+"_"+treename+".root"
        
        cut = resolve_cut(cutname, dconfig["cuts"])
        mc_cut = mul_cut(cut, weight)

        # open the output file.
        fout = ROOT.TFile.Open(outfname, "recreate")

        if not fout or fout.IsZombie():
            print "cannot open outfile " + outfname + ". quitting"
            stdout.flush()
            exit(-1)

        fout.cd()

        print "storing histograms in", outfname
        stdout.flush()

        # TODO
        # get plot list from json file
        for plot in TTbarDilepPlots.plots:
            name = "_".join(map(lambda p: p.name, plot))

            print "making histograms for plot", name
            stdout.flush()

            if len(bkg_samps):
                bkg_hists = map(lambda s: make_hist(plot, s, mc_cut), bkg_samps)

                bkg_stack = make_stack("bkg_%s" % name, "bkg_%s" % name,
                        bkg_hists, groupfunc=ROOT.TH1.GetTitle)

                # fix the axis labels and save
                bkg_stack.Draw()
                bkg_stack.GetXaxis().SetTitle(bkg_hists[0].GetXaxis().GetTitle())
                bkg_stack.GetYaxis().SetTitle(bkg_hists[0].GetYaxis().GetTitle())
                bkg_stack.Write()

            if len(data_samps):
                data_hists = map(lambda s: make_hist(plot, s, cut), data_samps)
                data_stack = make_stack("data_%s" % name, "data_%s" % name,
                        data_hists, groupfunc=ROOT.TH1.GetTitle)

                # fix the axis labels and save
                data_stack.Draw()
                data_stack.GetXaxis().SetTitle(data_hists[0].GetXaxis().GetTitle())
                data_stack.GetYaxis().SetTitle(data_hists[0].GetYaxis().GetTitle())
                data_stack.Write()

            if len(sig_samps):
                sig_hists = map(lambda s: make_hist(plot, s, mc_cut), sig_samps)
                sig_stack = make_stack("sig_%s" % name, "sig_%s" % name,
                        sig_hists, groupfunc=ROOT.TH1.GetTitle)

                # fix the axis labels and save
                sig_stack.Draw()
                sig_stack.GetXaxis().SetTitle(sig_hists[0].GetXaxis().GetTitle())
                sig_stack.GetYaxis().SetTitle(sig_hists[0].GetYaxis().GetTitle())
                sig_stack.Write()

            continue

        fout.Close()
        continue

    return 0

if __name__ == '__main__':

    main(argv)
