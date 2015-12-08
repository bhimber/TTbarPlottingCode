import ROOT
from array import array
from collections import namedtuple
from itertools import combinations

from DPlot import DPlot

lep_pt_plot = DPlot("lep_pt", "lepton p_{T} / MeV", "lep_pt",
        range(0, 200001, 20000),
        True) # include overflow


lep0_pt_plot = DPlot("lep0_pt", "leading lepton p_{T} / MeV", "lep_pt[0]",
        range(0, 200001, 20000),
        True) # include overflow


lep1_pt_plot = DPlot("lep1_pt", "subleading lepton p_{T} / MeV", "lep_pt[1]",
        range(0, 200001, 20000),
        True) # include overflow


lep_eta_plot = DPlot("lep_eta", "lepton #eta", "lep_eta",
        [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5],
        False) # no overflow

lep0_eta_plot = DPlot("lep0_eta", "leading lepton #eta", "lep_eta[0]",
        [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5],
        False) # no overflow

lep1_eta_plot = DPlot("lep1_eta", "subleading lepton #eta", "lep_eta[1]",
        [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5],
        False) # no overflow


lep_phi_plot = DPlot("lep_phi", "lepton #phi", "lep_phi",
        [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        False) # no overflow

lep0_phi_plot = DPlot("lep0_phi", "leading lepton #phi", "lep_phi[0]",
        [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        False) # no overflow

lep1_phi_plot = DPlot("lep1_phi", "subleading lepton #phi", "lep_phi[1]",
        [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        False) # no overflow


mll_plot = DPlot("mll", "m_{ll} / MeV", "mass",
        range(0, 500001, 25000),
        True) # overflow


lep_plots = [[lep_pt_plot], [lep_eta_plot], [lep_phi_plot],
             [lep0_pt_plot], [lep0_eta_plot], [lep0_phi_plot],
             [lep1_pt_plot], [lep1_eta_plot], [lep1_phi_plot],
             [mll_plot]
            ]


jet_n_plot = DPlot("jet_n", "jet multiplicity", "jet_n",
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        True) # include overflow


bjet_n_plot = DPlot("bjet_n", "b-jet multiplicity", "bjet_n",
        [0, 1, 2, 3, 4],
        True) # include overflow

jet_pt_plot = DPlot("jet_pt", "jet p_{T} / MeV", "jet_pt",
        range(0, 500001, 25000),
        True) # include overflow


jet0_pt_plot = DPlot("jet0_pt", "leading jet p_{T} / MeV", "jet_pt[0]",
        range(0, 500001, 25000),
        True) # include overflow


jet1_pt_plot = DPlot("jet1_pt", "subleading jet p_{T} / MeV", "jet_pt[1]",
        range(0, 500001, 25000),
        True) # include overflow


jet_eta_plot = DPlot("jet_eta", "jet #eta", "jet_eta",
        [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5],
        False) # no overflow

jet0_eta_plot = DPlot("jet0_eta", "leading jet #eta", "jet[0]_eta",
        [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5],
        False) # no overflow

jet1_eta_plot = DPlot("jet1_eta", "subleading jet #eta", "jet[1]_eta",
        [-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5],
        False) # no overflow


jet_phi_plot = DPlot("jet_phi", "jet #phi", "jet_phi",
        [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        False) # no overflow

jet0_phi_plot = DPlot("jet0_phi", "leading jet #phi", "jet[0]_phi",
        [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        False) # no overflow

jet1_phi_plot = DPlot("jet1_phi", "subleading jet #phi", "jet[1]_phi",
        [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        False) # no overflow


jet_plots = [[jet_n_plot], [bjet_n_plot],
             [jet_pt_plot], [jet_eta_plot], [jet_phi_plot],
             [jet0_pt_plot], [jet0_eta_plot], [jet0_phi_plot],
             [jet1_pt_plot], [jet1_eta_plot], [jet1_phi_plot]
             ]




ht_plot = DPlot("ht", "H_{T} / MeV", "ht",
        range(0, 1000001, 50000),
        True) # include overflow

met_et_plot = DPlot("met_et", "E_{T}^{miss} / MeV", "met_et",
        range(0, 250001, 10000),
        True) # include overflow

event_plots = [[met_et_plot], [ht_plot]]

plots = jet_plots + lep_plots + event_plots
