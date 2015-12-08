#include <iostream>
#include <vector>

#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TLorentzVector.h"
#include "TInterpreter.h"

using namespace std;

int main(int argc, char *argv[]) {
    if (argc != 3) {
        cout << "usage: " << argv[0] << " infile.root outfile.root" << endl;
        return 0;
    }

    TH1::SetDefaultSumw2();
    gInterpreter->GenerateDictionary("vector<float>", "vector");

    TFile *fin = new TFile(argv[1]);
    if (fin->IsZombie()) {
        cout << "failed to open infile " << argv[1] << endl;
        cout << "exiting." << endl;
        return -1;
    }

    TFile *fout = new TFile(argv[2], "create");
    if (fout->IsZombie()) {
        cout << "failed to open outfile " << argv[2] << endl;
        cout << "exiting." << endl;
        return -1;
    }

    TTree* t = dynamic_cast<TTree*> (fin->Get("mini"));

    float scaleFactor_ALLBTAG = 0;
    float mcWeight = 0;
    unsigned int flag_DL = 0;
    unsigned int channel_DL = 0;

    int mc_n = 0;
    vector<float>* mc_pt = 0;
    vector<float>* mc_eta = 0;
    vector<float>* mc_phi = 0;
    vector<float>* mc_m = 0;
    vector<float>* mc_pdgId = 0;
    vector<float>* mc_charge = 0;

    unsigned int lep_n = 0;
    float lep_pt[3];
    float lep_eta[3];
    float lep_phi[3];
    float lep_E[3];
    float lep_charge[3];
    unsigned int lep_type[3];

    t->SetBranchAddress("scaleFactor_ALLBTAG", &scaleFactor_ALLBTAG);
    t->SetBranchAddress("mcWeight", &mcWeight);
    t->SetBranchAddress("flag_DL", &flag_DL);
    t->SetBranchAddress("channel_DL", &channel_DL);

    t->SetBranchAddress("mc_n", &mc_n);
    t->SetBranchAddress("mc_pt", &mc_pt);
    t->SetBranchAddress("mc_eta", &mc_eta);
    t->SetBranchAddress("mc_phi", &mc_phi);
    t->SetBranchAddress("mc_m", &mc_m);
    t->SetBranchAddress("mc_pdgId", &mc_pdgId);
    t->SetBranchAddress("mc_charge", &mc_charge);

    t->SetBranchAddress("lep_n", &lep_n);
    t->SetBranchAddress("lep_pt", &lep_pt);
    t->SetBranchAddress("lep_eta", &lep_eta);
    t->SetBranchAddress("lep_phi", &lep_phi);
    t->SetBranchAddress("lep_E", &lep_E);
    t->SetBranchAddress("lep_charge", &lep_charge);
    t->SetBranchAddress("lep_type", &lep_type);


    fout->cd();

    // book histograms
    TH1D *h_el_reco_pt = new TH1D("h_el_reco_pt", "el_reco_pt;reco electron p_{T} / MeV;entries", 20, 0.0, 200000);
    TH1D *h_el_true_pt = new TH1D("h_el_true_pt", "el_true_pt;true electron p_{T} / MeV;entries", 20, 0.0, 200000);

    TH1D *h_mu_reco_pt = new TH1D("h_mu_reco_pt", "mu_reco_pt;reco muon p_{T} / MeV;entries", 20, 0.0, 200000);
    TH1D *h_mu_true_pt = new TH1D("h_mu_true_pt", "mu_true_pt;true muon p_{T} / MeV;entries", 20, 0.0, 200000);


    // variables used in the event loop
    float elCharge, muCharge;
    TLorentzVector tlvRecoEl, tlvRecoMu, tlvLL;
    TLorentzVector tlvTrueEl, tlvTrueMu, tlvTrueLL;

    // temporary loop variables
    TLorentzVector tlvTmpLep, tlvTmpTrueLep;


    unsigned int max = t->GetEntries();
    for (unsigned int i = 0; i < max; ++i) {
        t->GetEntry(i);

        if (i % 1000 == 0)
            cout << "processing event " << i << "." << endl;

        // APPLY CUTS
        // only keep emu events
        if (channel_DL != 3)
            continue;

        // MATCH TRUTH LEPTONS
        // reset the tlvs
        tlvRecoEl.SetPtEtaPhiE(0, 0, 0, 0);
        tlvRecoMu.SetPtEtaPhiE(0, 0, 0, 0);
        tlvLL.SetPtEtaPhiE(0, 0, 0, 0);
        tlvTrueEl.SetPtEtaPhiE(0, 0, 0, 0);
        tlvTrueMu.SetPtEtaPhiE(0, 0, 0, 0);
        tlvTrueLL.SetPtEtaPhiE(0, 0, 0, 0);

        tlvTmpLep.SetPtEtaPhiE(0, 0, 0, 0);
        tlvTmpTrueLep.SetPtEtaPhiE(0, 0, 0, 0);

        elCharge = 0;
        muCharge = 0;

        for (int iTrueLep = 0; iTrueLep < mc_n; iTrueLep++) {

            float pt = mc_pt->at(iTrueLep);
            float eta = mc_eta->at(iTrueLep);
            float abseta = fabs(eta);
            float phi = mc_phi->at(iTrueLep);
            float m = mc_m->at(iTrueLep);

            float charge = mc_charge->at(iTrueLep);
            int pid = mc_pdgId->at(iTrueLep);
            int abspid = abs(pid);

            // only keep muons and electrons
            // TODO
            // add eta cuts
            if (abspid == 11 &&
                    pt > 15000 &&
                    abseta < 2.47 && !(1.37 < abseta && abseta < 1.52)) {

                tlvTrueEl.SetPtEtaPhiM(pt, eta, phi, m);
                elCharge = charge;
            } else if (abspid == 13 &&
                    pt > 15000 &&
                    abseta < 2.5) {

                tlvTrueMu.SetPtEtaPhiM(pt, eta, phi, m);
                muCharge = charge;
            } else
                continue;
        }

        // check to make sure we have both an electron and muon
        if (!tlvTrueEl.Pt()) {
            cout << "no good true electron found." << endl;
            continue;
        } else if (!tlvTrueMu.Pt()) {
            cout << "no good true muon found." << endl;
            continue;
        }

        h_el_true_pt->Fill(tlvTrueEl.Pt(), mcWeight);
        h_mu_true_pt->Fill(tlvTrueMu.Pt(), mcWeight);

        // require full event selection.
        if (flag_DL != 1048575)
            continue;

        for (unsigned int iRecoLep = 0; iRecoLep < lep_n; iRecoLep++) {
            // 25 GeV reco pt cut
            if (lep_pt[iRecoLep] < 25000)
                continue;

            // electrons
            if (lep_type[iRecoLep] == 11 &&
                    lep_charge[iRecoLep]*elCharge > 0) {

                tlvRecoEl.SetPtEtaPhiE(lep_pt[iRecoLep],
                        lep_eta[iRecoLep],
                        lep_phi[iRecoLep],
                        lep_E[iRecoLep]);
            }
            
            // muons
            else if (lep_type[iRecoLep] == 13 &&
                    lep_charge[iRecoLep]*muCharge > 0) {

                tlvRecoMu.SetPtEtaPhiE(lep_pt[iRecoLep],
                        lep_eta[iRecoLep],
                        lep_phi[iRecoLep],
                        lep_E[iRecoLep]);
            }
        }

        // check to make sure we have both an electron and muon
        if (!tlvRecoEl.Pt()) {
            cout << "no good reco electron found." << endl;
            continue;
        } else if (!tlvRecoMu.Pt()) {
            cout << "no good reco muon found." << endl;
            continue;
        }

        h_el_reco_pt->Fill(tlvRecoEl.Pt(), mcWeight*scaleFactor_ALLBTAG);
        h_mu_reco_pt->Fill(tlvRecoMu.Pt(), mcWeight*scaleFactor_ALLBTAG);
    }

    TH1D *h_el_eff_pt = dynamic_cast<TH1D *>(h_el_true_pt->Clone("h_el_eff_pt"));
    h_el_eff_pt->GetXaxis()->SetTitle("electron p_{T} / MeV");
    h_el_eff_pt->GetYaxis()->SetTitle("efficiency");
    h_el_eff_pt->Divide(h_el_reco_pt, h_el_true_pt);

    TH1D *h_mu_eff_pt = dynamic_cast<TH1D *>(h_mu_true_pt->Clone("h_mu_eff_pt"));
    h_mu_eff_pt->GetXaxis()->SetTitle("muon p_{T} / MeV");
    h_mu_eff_pt->GetYaxis()->SetTitle("efficiency");
    h_mu_eff_pt->Divide(h_mu_reco_pt, h_mu_true_pt);

    h_el_true_pt->Write();
    h_el_reco_pt->Write();
    h_el_eff_pt->Write();

    h_mu_true_pt->Write();
    h_mu_reco_pt->Write();
    h_mu_eff_pt->Write();

    fout->Close();
    fin->Close();

    return 0;
}
