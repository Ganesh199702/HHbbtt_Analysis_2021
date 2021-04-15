from ROOT import *
import math 
import time

###############################################################M1000##############################################################

bcount = 0
events_passing = 0
events_failing = 0
events_selected = 0

i_counter=0
delta_r=0
delta_r_least=0
i_least=0

events_passing_b = 0
events_failing_b = 0
events_selected_b = 0

tau_id = 4


#Histograms for efficiencies
file_bbtt = TFile("NanoAOD_M1000.root") #opening the root file
hist_bbtt_higgspt_pass = TH1F("Hist_higgspt_pass","Hist_higgspt_pass", 14, 100, 800)
#hist_bbtt_higgspt_fail = TH1F("Hist_Mhiggspt_fail","Hist_higgspt_fail", 14, 100, 800)
hist_bbtt_higgspt_total = TH1F("Hist_higgspt_total","Hist_higgspt_total",14, 100, 800)

hist_bbtt_higgspt_pass_b = TH1F("Hist_higgspt_pass_b","Hist_higgspt_pass_b", 14, 100, 800)
#hist_bbtt_higgspt_fail_b = TH1F("Hist_higgspt_fail_b","Hist_higgspt_fail_b", 14, 100, 800)
hist_bbtt_higgspt_total_b = TH1F("Hist_higgspt_total_b","Hist_higgspt_total_b",14, 100, 800)


###Setting the cutflow Histrograms###########
cutflow_1000 = TH1F("cutflow_M1000_standard","cutflow_M1000_standard",6,0,6);
cutflow_1000.GetXaxis().SetBinLabel(1,"Events_selected")
cutflow_1000.GetXaxis().SetBinLabel(2,"Triggers")
cutflow_1000.GetXaxis().SetBinLabel(3,"pt_cut")
cutflow_1000.GetXaxis().SetBinLabel(4,"eta_cut")
cutflow_1000.GetXaxis().SetBinLabel(5,"DecayMode_ID")
cutflow_1000.GetXaxis().SetBinLabel(6,"MVA_Tau_ID")
cutflow_1000.SetFillColor(38)
cutflow_1000.SetStats(0)
cutflow_1000.GetXaxis().SetTitle("Selections")
cutflow_1000.GetYaxis().SetTitle("Events")

cutflow_1000_b = TH1F("cutflow_M1000_boosted","cutflow_M1000_boosted",6,0,6);
cutflow_1000_b.GetXaxis().SetBinLabel(1,"Events_selected")
cutflow_1000_b.GetXaxis().SetBinLabel(2,"Triggers")
cutflow_1000_b.GetXaxis().SetBinLabel(3,"pt_cut")
cutflow_1000_b.GetXaxis().SetBinLabel(4,"eta_cut")
cutflow_1000_b.GetXaxis().SetBinLabel(5,"DecayMode_ID")
cutflow_1000_b.GetXaxis().SetBinLabel(6,"MVA_Tau_ID")
cutflow_1000_b.SetFillColor(66)
cutflow_1000_b.SetStats(0)
cutflow_1000_b.GetXaxis().SetTitle("Selections")
cutflow_1000_b.GetYaxis().SetTitle("Events")


Tau_v1=TLorentzVector(0.0,0.0,0.0,0.0)
#Tau_v2=TLorentzVector(0.0,0.0,0.0,0.0)
Higgs_v1=TLorentzVector(0.0,0.0,0.0,0.0)

tree_bbtt = file_bbtt.Get('Events')
nEntries = tree_bbtt.GetEntries()
print nEntries


#Events Loop
for x in range(nEntries):
	if (x%1000 == 0):
		print("events_processed=",x)
	tree_bbtt.GetEntry(x)
	for i in range(len(tree_bbtt.FatJet_btagDeepB)): # AK8 jet counter
		#print ("btag_score", tree_bbtt.Jet_btagDeepB[i])
		if (tree_bbtt.FatJet_btagDeepB[i] > 0.45):
			bcount = bcount + 1


	if(bcount==1 and tree_bbtt.nMuon ==1 and tree_bbtt.nTau==1):#Selecting events for semileptonic channel
		cutflow_1000.AddBinContent(1)
		events_selected=events_selected+1
		Tau_v1.SetPtEtaPhiM(tree_bbtt.Tau_pt[0],tree_bbtt.Tau_eta[0],tree_bbtt.Tau_phi[0],tree_bbtt.Tau_mass[0])


		####To find the Higgs closest to Tau system######
		for i in range(len(tree_bbtt.GenPart_pt)):
			if (tree_bbtt.GenPart_mass[i]==125.0):
				Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
				delta_r=Tau_v1.DeltaR(Higgs_v1)
				if (i_counter==0 or delta_r<delta_r_least):
					delta_r_least=delta_r
					i_least=i
					i_counter=i_counter+1

		#Filling the denominator histogram
		hist_bbtt_higgspt_total.Fill(tree_bbtt.GenPart_pt[i_least])
		i_counter=0
		i_least=0
		delta_r=0
		delta_r_least=0
		###The following set of if statements is simply to fill the cutflow histograms####
		if(tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1):
			cutflow_1000.AddBinContent(2)
			if(tree_bbtt.Tau_pt[0]>20):
				cutflow_1000.AddBinContent(3)
				if(abs(tree_bbtt.Tau_eta[0])<2.3):
					cutflow_1000.AddBinContent(4)
					if(tree_bbtt.Tau_idDecayModeNewDMs[0]==1):
						cutflow_1000.AddBinContent(5)
						if(tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id == tau_id):
							cutflow_1000.AddBinContent(6)

		#The Condition for triggers and the additional pt, eta and ID requirements#####
		if((tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1) and (tree_bbtt.Tau_pt[0]>20 and abs(tree_bbtt.Tau_eta[0])<2.3 and tree_bbtt.Tau_idDecayModeNewDMs[0]==1 and (tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id == tau_id))):
			#print ("bitwise_check",tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id, tree_bbtt.Tau_idDecayModeNewDMs[0])
			Tau_v1.SetPtEtaPhiM(tree_bbtt.Tau_pt[0],tree_bbtt.Tau_eta[0],tree_bbtt.Tau_phi[0],tree_bbtt.Tau_mass[0])

			for i in range(len(tree_bbtt.GenPart_pt)):
				if (tree_bbtt.GenPart_mass[i]==125.0):
					Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
					delta_r=Tau_v1.DeltaR(Higgs_v1)
					if (i_counter==0 or delta_r<delta_r_least):
						delta_r_least=delta_r
						i_least=i
						i_counter = i_counter+1

			hist_bbtt_higgspt_pass.Fill(tree_bbtt.GenPart_pt[i_least])#Filling the numerator Histogram
			events_passing = events_passing + 1
			i_counter=0
			i_least=0
			delta_r=0
			delta_r_least=0

	#######boosted####################boosted#############Repeat the procudure for boosted Taus#####################

	if(bcount==1 and tree_bbtt.nMuon ==1 and tree_bbtt.nboostedTau==1):
		cutflow_1000_b.AddBinContent(1)
		events_selected_b=events_selected_b+1
		Tau_v1.SetPtEtaPhiM(tree_bbtt.boostedTau_pt[0],tree_bbtt.boostedTau_eta[0],tree_bbtt.boostedTau_phi[0],tree_bbtt.boostedTau_mass[0])

		for i in range(len(tree_bbtt.GenPart_pt)):
			if (tree_bbtt.GenPart_mass[i]==125.0):
				Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
				delta_r=Tau_v1.DeltaR(Higgs_v1)
				if (i_counter==0 or delta_r<delta_r_least):
					delta_r_least=delta_r
					i_least=i
					i_counter=i_counter+1


		hist_bbtt_higgspt_total_b.Fill(tree_bbtt.GenPart_pt[i_least])
		i_counter=0
		i_least=0
		delta_r=0
		delta_r_least=0
		if(tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1):
			cutflow_1000_b.AddBinContent(2)
			if(tree_bbtt.boostedTau_pt[0]>20):
				cutflow_1000_b.AddBinContent(3)
				if(abs(tree_bbtt.boostedTau_eta[0])<2.3):
					cutflow_1000_b.AddBinContent(4)
					if(tree_bbtt.boostedTau_idDecayModeNewDMs[0]==1):
						cutflow_1000_b.AddBinContent(5)
						if(tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id == tau_id):
							cutflow_1000_b.AddBinContent(6)

		if((tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1) and (tree_bbtt.boostedTau_pt[0]>20 and abs(tree_bbtt.boostedTau_eta[0])<2.3 and tree_bbtt.boostedTau_idDecayModeNewDMs[0]==1 and (tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id == tau_id))):
			#print ("bitwise_check",tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id, tree_bbtt.boostedTau_idDecayModeNewDMs[0])
			Tau_v1.SetPtEtaPhiM(tree_bbtt.boostedTau_pt[0],tree_bbtt.boostedTau_eta[0],tree_bbtt.boostedTau_phi[0],tree_bbtt.boostedTau_mass[0])

			for i in range(len(tree_bbtt.GenPart_pt)):
				if (tree_bbtt.GenPart_mass[i]==125.0):
					Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
					delta_r=Tau_v1.DeltaR(Higgs_v1)
					if (i_counter==0 or delta_r<delta_r_least):
						delta_r_least=delta_r
						i_least=i
						i_counter = i_counter+1

			hist_bbtt_higgspt_pass_b.Fill(tree_bbtt.GenPart_pt[i_least])
			events_passing_b = events_passing_b + 1
			i_counter=0
			i_least=0
			delta_r=0
			delta_r_least=0

	bcount=0


hist_bbtt_higgspt_eff = TGraphAsymmErrors(hist_bbtt_higgspt_pass,hist_bbtt_higgspt_total,'e1000')
hist_bbtt_higgspt_eff_b = TGraphAsymmErrors(hist_bbtt_higgspt_pass_b,hist_bbtt_higgspt_total_b,'e1000_b')

hist_bbtt_higgspt_eff.SetLineColor(9)
hist_bbtt_higgspt_eff.SetMarkerStyle(20)
hist_bbtt_higgspt_eff.SetMarkerColor(9)
hist_bbtt_higgspt_eff.SetMarkerSize(1)
hist_bbtt_higgspt_eff.SetTitle("Efficiency Plot")
hist_bbtt_higgspt_eff.GetXaxis().SetTitle("Higgs p_{T}(GeV)")
hist_bbtt_higgspt_eff.GetYaxis().SetTitle("Efficiency")
hist_bbtt_higgspt_eff.GetYaxis().SetRangeUser(-0.05,1.1)

hist_bbtt_higgspt_eff_b.SetLineColor(2)
hist_bbtt_higgspt_eff_b.SetMarkerStyle(24)
hist_bbtt_higgspt_eff_b.SetMarkerColor(2)
hist_bbtt_higgspt_eff_b.SetMarkerSize(1)
hist_bbtt_higgspt_eff_b.SetTitle("Efficiency Plot")
hist_bbtt_higgspt_eff_b.GetXaxis().SetTitle("Higgs p_{T}(GeV)")
hist_bbtt_higgspt_eff_b.GetYaxis().SetTitle("Efficiency")
hist_bbtt_higgspt_eff_b.GetYaxis().SetRangeUser(-0.05,1.1)
#hist_bbtt_MET_eff.SetStats(0)
print ("M1000 non_b_taus",events_selected, events_passing, events_failing)
print ("M1000 b_taus",events_selected_b, events_passing_b, events_failing_b)





######################################################################################M2000####################################################################################################################


bcount = 0
events_passing = 0
events_failing = 0
events_selected = 0

i_counter=0
delta_r=0
delta_r_least=0
i_least=0

events_passing_b = 0
events_failing_b = 0
events_selected_b = 0

file_bbtt_2000 = TFile("NanoAOD_M2000.root") #opening the root file
hist_bbtt_higgspt_pass_2000 = TH1F("Hist_higgspt_pass_2000","Hist_higgspt_pass_2000", 11, 200, 1300)
hist_bbtt_higgspt_fail_2000 = TH1F("Hist_Mhiggspt_fail_2000","Hist_higgspt_fail_2000", 11, 200, 1300)
hist_bbtt_higgspt_total_2000 = TH1F("Hist_higgspt_total_2000","Hist_higgspt_total_2000",11, 200, 1300)

hist_bbtt_higgspt_pass_2000_b = TH1F("Hist_higgspt_pass_2000_b","Hist_higgspt_pass_2000_b", 11, 200, 1300)
hist_bbtt_higgspt_fail_2000_b = TH1F("Hist_higgspt_fail_2000_b","Hist_higgspt_2000_fail_b", 11, 200, 1300)
hist_bbtt_higgspt_total_2000_b = TH1F("Hist_higgspt_total_2000_b","Hist_higgspt_total_2000_b",11, 200, 1300)

cutflow_2000 = TH1F("cutflow_M2000_standard","cutflow_M2000_standard",6,0,6);
cutflow_2000.GetXaxis().SetBinLabel(1,"Events_selected")
cutflow_2000.GetXaxis().SetBinLabel(2,"Triggers")
cutflow_2000.GetXaxis().SetBinLabel(3,"pt_cut")
cutflow_2000.GetXaxis().SetBinLabel(4,"eta_cut")
cutflow_2000.GetXaxis().SetBinLabel(5,"DecayMode_ID")
cutflow_2000.GetXaxis().SetBinLabel(6,"MVA_Tau_ID")
cutflow_2000.SetFillColor(38)
cutflow_2000.SetStats(0)
cutflow_2000.GetXaxis().SetTitle("Selections")
cutflow_2000.GetYaxis().SetTitle("Events")

cutflow_2000_b = TH1F("cutflow_M2000_boosted","cutflow_M2000_boosted",6,0,6);
cutflow_2000_b.GetXaxis().SetBinLabel(1,"Events_selected")
cutflow_2000_b.GetXaxis().SetBinLabel(2,"Triggers")
cutflow_2000_b.GetXaxis().SetBinLabel(3,"pt_cut")
cutflow_2000_b.GetXaxis().SetBinLabel(4,"eta_cut")
cutflow_2000_b.GetXaxis().SetBinLabel(5,"DecayMode_ID")
cutflow_2000_b.GetXaxis().SetBinLabel(6,"MVA_Tau_ID")
cutflow_2000_b.SetFillColor(66)
cutflow_2000_b.SetStats(0)
cutflow_2000_b.GetXaxis().SetTitle("Selections")
cutflow_2000_b.GetYaxis().SetTitle("Events")

Tau_v1=TLorentzVector(0.0,0.0,0.0,0.0)
#Tau_v2=TLorentzVector(0.0,0.0,0.0,0.0)
Higgs_v1=TLorentzVector(0.0,0.0,0.0,0.0)

tree_bbtt = file_bbtt_2000.Get('Events')
nEntries = tree_bbtt.GetEntries()
print nEntries

for x in range(nEntries):
	if (x%1000 == 0):
		print("events_processed=",x)
	tree_bbtt.GetEntry(x)
	for i in range(len(tree_bbtt.FatJet_btagDeepB)):
		#print ("btag_score", tree_bbtt.Jet_btagDeepB[i])
		if (tree_bbtt.FatJet_btagDeepB[i] > 0.45):
			bcount = bcount + 1


	if(bcount==1 and tree_bbtt.nMuon ==1 and tree_bbtt.nTau==1):
		events_selected=events_selected+1
		cutflow_2000.AddBinContent(1)
		Tau_v1.SetPtEtaPhiM(tree_bbtt.Tau_pt[0],tree_bbtt.Tau_eta[0],tree_bbtt.Tau_phi[0],tree_bbtt.Tau_mass[0])

		for i in range(len(tree_bbtt.GenPart_pt)):
			if (tree_bbtt.GenPart_mass[i]==125.0):
				Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
				delta_r=Tau_v1.DeltaR(Higgs_v1)
				if (i_counter==0 or delta_r<delta_r_least):
					delta_r_least=delta_r
					i_least=i
					i_counter=i_counter+1


		hist_bbtt_higgspt_total_2000.Fill(tree_bbtt.GenPart_pt[i_least])
		i_counter=0
		i_least=0
		delta_r=0
		delta_r_least=0

		if(tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1):
			cutflow_2000.AddBinContent(2)
			if(tree_bbtt.Tau_pt[0]>20):
				cutflow_2000.AddBinContent(3)
				if(abs(tree_bbtt.Tau_eta[0])<2.3):
					cutflow_2000.AddBinContent(4)
					if(tree_bbtt.Tau_idDecayModeNewDMs[0]==1):
						cutflow_2000.AddBinContent(5)
						if(tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id == tau_id):
							cutflow_2000.AddBinContent(6)

		if((tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1) and (tree_bbtt.Tau_pt[0]>20 and abs(tree_bbtt.Tau_eta[0])<2.3 and tree_bbtt.Tau_idDecayModeNewDMs[0]==1 and (tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id == tau_id))):
			#print ("bitwise_check",tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id, tree_bbtt.Tau_idDecayModeNewDMs[0])
			Tau_v1.SetPtEtaPhiM(tree_bbtt.Tau_pt[0],tree_bbtt.Tau_eta[0],tree_bbtt.Tau_phi[0],tree_bbtt.Tau_mass[0])

			for i in range(len(tree_bbtt.GenPart_pt)):
				if (tree_bbtt.GenPart_mass[i]==125.0):
					Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
					delta_r=Tau_v1.DeltaR(Higgs_v1)
					if (i_counter==0 or delta_r<delta_r_least):
						delta_r_least=delta_r
						i_least=i
						i_counter = i_counter+1

			hist_bbtt_higgspt_pass_2000.Fill(tree_bbtt.GenPart_pt[i_least])
			events_passing = events_passing + 1
			i_counter=0
			i_least=0
			delta_r=0
			delta_r_least=0

	#######boosted#############

	if(bcount==1 and tree_bbtt.nMuon ==1 and tree_bbtt.nboostedTau==1):
		events_selected_b=events_selected_b+1
		cutflow_2000_b.AddBinContent(1)
		Tau_v1.SetPtEtaPhiM(tree_bbtt.boostedTau_pt[0],tree_bbtt.boostedTau_eta[0],tree_bbtt.boostedTau_phi[0],tree_bbtt.boostedTau_mass[0])

		for i in range(len(tree_bbtt.GenPart_pt)):
			if (tree_bbtt.GenPart_mass[i]==125.0):
				Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
				delta_r=Tau_v1.DeltaR(Higgs_v1)
				if (i_counter==0 or delta_r<delta_r_least):
					delta_r_least=delta_r
					i_least=i
					i_counter=i_counter+1


		hist_bbtt_higgspt_total_2000_b.Fill(tree_bbtt.GenPart_pt[i_least])
		i_counter=0
		i_least=0
		delta_r=0
		delta_r_least=0

		if(tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1):
			cutflow_2000_b.AddBinContent(2)
			if(tree_bbtt.boostedTau_pt[0]>20):
				cutflow_2000_b.AddBinContent(3)
				if(abs(tree_bbtt.boostedTau_eta[0])<2.3):
					cutflow_2000_b.AddBinContent(4)
					if(tree_bbtt.boostedTau_idDecayModeNewDMs[0]==1):
						cutflow_2000_b.AddBinContent(5)
						if(tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id == tau_id):
							cutflow_2000_b.AddBinContent(6)

		if((tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1) and (tree_bbtt.boostedTau_pt[0]>20 and abs(tree_bbtt.boostedTau_eta[0])<2.3 and tree_bbtt.boostedTau_idDecayModeNewDMs[0]==1 and (tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id == tau_id))):
			#print ("bitwise_check",tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id, tree_bbtt.boostedTau_idDecayModeNewDMs[0])
			Tau_v1.SetPtEtaPhiM(tree_bbtt.boostedTau_pt[0],tree_bbtt.boostedTau_eta[0],tree_bbtt.boostedTau_phi[0],tree_bbtt.boostedTau_mass[0])

			for i in range(len(tree_bbtt.GenPart_pt)):
				if (tree_bbtt.GenPart_mass[i]==125.0):
					Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
					delta_r=Tau_v1.DeltaR(Higgs_v1)
					if (i_counter==0 or delta_r<delta_r_least):
						delta_r_least=delta_r
						i_least=i
						i_counter = i_counter+1

			hist_bbtt_higgspt_pass_2000_b.Fill(tree_bbtt.GenPart_pt[i_least])
			events_passing_b = events_passing_b + 1
			i_counter=0
			i_least=0
			delta_r=0
			delta_r_least=0

	bcount=0


hist_bbtt_higgspt_eff_2000 = TGraphAsymmErrors(hist_bbtt_higgspt_pass_2000,hist_bbtt_higgspt_total_2000,'e2000')
hist_bbtt_higgspt_eff_2000_b = TGraphAsymmErrors(hist_bbtt_higgspt_pass_2000_b,hist_bbtt_higgspt_total_2000_b,'e2000_b')

hist_bbtt_higgspt_eff_2000.SetLineColor(8)
hist_bbtt_higgspt_eff_2000.SetMarkerStyle(21)
hist_bbtt_higgspt_eff_2000.SetMarkerColor(8)
hist_bbtt_higgspt_eff_2000.SetMarkerSize(1)
hist_bbtt_higgspt_eff_2000.SetTitle("Efficiency Plot")
hist_bbtt_higgspt_eff_2000.GetXaxis().SetTitle("Higgs p_{T}(GeV)")
hist_bbtt_higgspt_eff_2000.GetYaxis().SetTitle("Efficiency")
hist_bbtt_higgspt_eff_2000.GetYaxis().SetRangeUser(-0.05,1.1)

hist_bbtt_higgspt_eff_2000_b.SetLineColor(49)
hist_bbtt_higgspt_eff_2000_b.SetMarkerStyle(25)
hist_bbtt_higgspt_eff_2000_b.SetMarkerColor(49)
hist_bbtt_higgspt_eff_2000_b.SetMarkerSize(1)
hist_bbtt_higgspt_eff_2000_b.SetTitle("Efficiency Plot")
hist_bbtt_higgspt_eff_2000_b.GetXaxis().SetTitle("Higgs p_{T}(GeV)")
hist_bbtt_higgspt_eff_2000_b.GetYaxis().SetTitle("Efficiency")
hist_bbtt_higgspt_eff_2000_b.GetYaxis().SetRangeUser(-0.05,1.1)
#hist_bbtt_MET_eff.SetStats(0)
print ("M2000 non_b_taus",events_selected, events_passing, events_failing)
print ("M2000 b_taus",events_selected_b, events_passing_b, events_failing_b)




############################################################################################M4000###################################################################################################

bcount = 0
events_passing = 0
events_failing = 0
events_selected = 0

i_counter=0
delta_r=0
delta_r_least=0
i_least=0

events_passing_b = 0
events_failing_b = 0
events_selected_b = 0

file_bbtt_4000 = TFile("NanoAOD_M4000.root") #opening the root file
hist_bbtt_higgspt_pass_4000 = TH1F("Hist_higgspt_pass_4000","Hist_higgspt_pass_4000", 8, 400, 2200)
hist_bbtt_higgspt_fail_4000 = TH1F("Hist_Mhiggspt_fail_4000","Hist_higgspt_fail_4000", 8, 400, 2200)
hist_bbtt_higgspt_total_4000 = TH1F("Hist_higgspt_total_4000","Hist_higgspt_total_4000",8, 400, 2200)

hist_bbtt_higgspt_pass_4000_b = TH1F("Hist_higgspt_pass_4000_b","Hist_higgspt_pass_4000_b", 8, 400, 2200)
hist_bbtt_higgspt_fail_4000_b = TH1F("Hist_higgspt_fail_4000_b","Hist_higgspt_4000_fail_b", 8, 400, 2200)
hist_bbtt_higgspt_total_4000_b = TH1F("Hist_higgspt_total_4000_b","Hist_higgspt_total_4000_b",8, 400, 2200)

cutflow_4000 = TH1F("cutflow_M4000_standard","cutflow_M4000_standard",6,0,6);
cutflow_4000.GetXaxis().SetBinLabel(1,"Events_selected")
cutflow_4000.GetXaxis().SetBinLabel(2,"Triggers")
cutflow_4000.GetXaxis().SetBinLabel(3,"pt_cut")
cutflow_4000.GetXaxis().SetBinLabel(4,"eta_cut")
cutflow_4000.GetXaxis().SetBinLabel(5,"DecayMode_ID")
cutflow_4000.GetXaxis().SetBinLabel(6,"MVA_Tau_ID")
cutflow_4000.SetFillColor(38)
cutflow_4000.SetStats(0)
cutflow_4000.GetXaxis().SetTitle("Selections")
cutflow_4000.GetYaxis().SetTitle("Events")

cutflow_4000_b = TH1F("cutflow_M4000_boosted","cutflow_M4000_boosted",6,0,6);
cutflow_4000_b.GetXaxis().SetBinLabel(1,"Events_selected")
cutflow_4000_b.GetXaxis().SetBinLabel(2,"Triggers")
cutflow_4000_b.GetXaxis().SetBinLabel(3,"pt_cut")
cutflow_4000_b.GetXaxis().SetBinLabel(4,"eta_cut")
cutflow_4000_b.GetXaxis().SetBinLabel(5,"DecayMode_ID")
cutflow_4000_b.GetXaxis().SetBinLabel(6,"MVA_Tau_ID")
cutflow_4000_b.SetFillColor(66)
cutflow_4000_b.SetStats(0)
cutflow_4000_b.GetXaxis().SetTitle("Selections")
cutflow_4000_b.GetYaxis().SetTitle("Events")


Tau_v1=TLorentzVector(0.0,0.0,0.0,0.0)
#Tau_v2=TLorentzVector(0.0,0.0,0.0,0.0)
Higgs_v1=TLorentzVector(0.0,0.0,0.0,0.0)

tree_bbtt = file_bbtt_4000.Get('Events')
nEntries = tree_bbtt.GetEntries()
print nEntries

for x in range(nEntries):
	if (x%1000 == 0):
		print("events_processed=",x)
	tree_bbtt.GetEntry(x)
	for i in range(len(tree_bbtt.FatJet_btagDeepB)):
		#print ("btag_score", tree_bbtt.Jet_btagDeepB[i])
		if (tree_bbtt.FatJet_btagDeepB[i] > 0.45):
			bcount = bcount + 1



	if(bcount==1 and tree_bbtt.nMuon ==1 and tree_bbtt.nTau==1):
		events_selected=events_selected+1
		cutflow_4000.AddBinContent(1)
		Tau_v1.SetPtEtaPhiM(tree_bbtt.Tau_pt[0],tree_bbtt.Tau_eta[0],tree_bbtt.Tau_phi[0],tree_bbtt.Tau_mass[0])

		for i in range(len(tree_bbtt.GenPart_pt)):
			if (tree_bbtt.GenPart_mass[i]==125.0):
				Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
				delta_r=Tau_v1.DeltaR(Higgs_v1)
				if (i_counter==0 or delta_r<delta_r_least):
					delta_r_least=delta_r
					i_least=i
					i_counter=i_counter+1


		hist_bbtt_higgspt_total_4000.Fill(tree_bbtt.GenPart_pt[i_least])
		i_counter=0
		i_least=0
		delta_r=0
		delta_r_least=0

		if(tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1):
			cutflow_4000.AddBinContent(2)
			if(tree_bbtt.Tau_pt[0]>20):
				cutflow_4000.AddBinContent(3)
				if(abs(tree_bbtt.Tau_eta[0])<2.3):
					cutflow_4000.AddBinContent(4)
					if(tree_bbtt.Tau_idDecayModeNewDMs[0]==1):
						cutflow_4000.AddBinContent(5)
						if(tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id == tau_id):
							cutflow_4000.AddBinContent(6)

		if((tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1) and (tree_bbtt.Tau_pt[0]>20 and abs(tree_bbtt.Tau_eta[0])<2.3 and tree_bbtt.Tau_idDecayModeNewDMs[0]==1 and (tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id == tau_id))):
			#print ("bitwise_check",tree_bbtt.Tau_idMVAoldDM2017v1[0] & tau_id, tree_bbtt.Tau_idDecayModeNewDMs[0])
			Tau_v1.SetPtEtaPhiM(tree_bbtt.Tau_pt[0],tree_bbtt.Tau_eta[0],tree_bbtt.Tau_phi[0],tree_bbtt.Tau_mass[0])

			for i in range(len(tree_bbtt.GenPart_pt)):
				if (tree_bbtt.GenPart_mass[i]==125.0):
					Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
					delta_r=Tau_v1.DeltaR(Higgs_v1)
					if (i_counter==0 or delta_r<delta_r_least):
						delta_r_least=delta_r
						i_least=i
						i_counter = i_counter+1

			hist_bbtt_higgspt_pass_4000.Fill(tree_bbtt.GenPart_pt[i_least])
			events_passing = events_passing + 1
			i_counter=0
			i_least=0
			delta_r=0
			delta_r_least=0

	#######boosted#############

	if(bcount==1 and tree_bbtt.nMuon ==1 and tree_bbtt.nboostedTau==1):
		events_selected_b=events_selected_b+1
		cutflow_4000_b.AddBinContent(1)
		Tau_v1.SetPtEtaPhiM(tree_bbtt.boostedTau_pt[0],tree_bbtt.boostedTau_eta[0],tree_bbtt.boostedTau_phi[0],tree_bbtt.boostedTau_mass[0])

		for i in range(len(tree_bbtt.GenPart_pt)):
			if (tree_bbtt.GenPart_mass[i]==125.0):
				Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
				delta_r=Tau_v1.DeltaR(Higgs_v1)
				if (i_counter==0 or delta_r<delta_r_least):
					delta_r_least=delta_r
					i_least=i
					i_counter=i_counter+1


		hist_bbtt_higgspt_total_4000_b.Fill(tree_bbtt.GenPart_pt[i_least])
		i_counter=0
		i_least=0
		delta_r=0
		delta_r_least=0

		if(tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1):
			cutflow_4000_b.AddBinContent(2)
			if(tree_bbtt.boostedTau_pt[0]>20):
				cutflow_4000_b.AddBinContent(3)
				if(abs(tree_bbtt.boostedTau_eta[0])<2.3):
					cutflow_4000_b.AddBinContent(4)
					if(tree_bbtt.boostedTau_idDecayModeNewDMs[0]==1):
						cutflow_4000_b.AddBinContent(5)
						if(tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id == tau_id):
							cutflow_4000_b.AddBinContent(6)


		if((tree_bbtt.HLT_PFMETNoMu90_PFMHTNoMu90_IDTight==1 or tree_bbtt.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight==1 or tree_bbtt.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight==1 or tree_bbtt.HLT_PFMET110_PFMHT110_IDTight==1 or tree_bbtt.HLT_PFMET120_PFMHT120_IDTight==1 or  tree_bbtt.HLT_PFMET170_NoiseCleaned==1 or tree_bbtt.HLT_PFMET170_HBHECleaned==1 or tree_bbtt.HLT_PFMET170_HBHE_BeamHaloCleaned==1) and (tree_bbtt.boostedTau_pt[0]>20 and abs(tree_bbtt.boostedTau_eta[0])<2.3 and tree_bbtt.boostedTau_idDecayModeNewDMs[0]==1 and (tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id == tau_id))):
			#print ("bitwise_check",tree_bbtt.boostedTau_idMVAoldDM2017v1[0] & tau_id, tree_bbtt.boostedTau_idDecayModeNewDMs[0])
			Tau_v1.SetPtEtaPhiM(tree_bbtt.boostedTau_pt[0],tree_bbtt.boostedTau_eta[0],tree_bbtt.boostedTau_phi[0],tree_bbtt.boostedTau_mass[0])

			for i in range(len(tree_bbtt.GenPart_pt)):
				if (tree_bbtt.GenPart_mass[i]==125.0):
					Higgs_v1.SetPtEtaPhiM(tree_bbtt.GenPart_pt[i],tree_bbtt.GenPart_eta[i],tree_bbtt.GenPart_phi[i],tree_bbtt.GenPart_mass[i])
					delta_r=Tau_v1.DeltaR(Higgs_v1)
					if (i_counter==0 or delta_r<delta_r_least):
						delta_r_least=delta_r
						i_least=i
						i_counter = i_counter+1

			hist_bbtt_higgspt_pass_4000_b.Fill(tree_bbtt.GenPart_pt[i_least])
			events_passing_b = events_passing_b + 1
			i_counter=0
			i_least=0
			delta_r=0
			delta_r_least=0

	bcount=0


hist_bbtt_higgspt_eff_4000 = TGraphAsymmErrors(hist_bbtt_higgspt_pass_4000,hist_bbtt_higgspt_total_4000,'e4000')
hist_bbtt_higgspt_eff_4000_b = TGraphAsymmErrors(hist_bbtt_higgspt_pass_4000_b,hist_bbtt_higgspt_total_4000_b,'e4000_b')

hist_bbtt_higgspt_eff_4000.SetLineColor(1)
hist_bbtt_higgspt_eff_4000.SetMarkerStyle(22)
hist_bbtt_higgspt_eff_4000.SetMarkerColor(1)
hist_bbtt_higgspt_eff_4000.SetMarkerSize(1)
hist_bbtt_higgspt_eff_4000.SetTitle("Efficiency Plot")
hist_bbtt_higgspt_eff_4000.GetXaxis().SetTitle("Higgs p_{T}(GeV)")
hist_bbtt_higgspt_eff_4000.GetYaxis().SetTitle("Efficiency")
hist_bbtt_higgspt_eff_4000.GetYaxis().SetRangeUser(-0.05,1.1)

hist_bbtt_higgspt_eff_4000_b.SetLineColor(42)
hist_bbtt_higgspt_eff_4000_b.SetMarkerStyle(26)
hist_bbtt_higgspt_eff_4000_b.SetMarkerColor(42)
hist_bbtt_higgspt_eff_4000_b.SetMarkerSize(1)
hist_bbtt_higgspt_eff_4000_b.SetTitle("Efficiency Plot")
hist_bbtt_higgspt_eff_4000_b.GetXaxis().SetTitle("Higgs p_{T}(GeV)")
hist_bbtt_higgspt_eff_4000_b.GetYaxis().SetTitle("Efficiency")
hist_bbtt_higgspt_eff_4000_b.GetYaxis().SetRangeUser(-0.05,1.1)
#hist_bbtt_MET_eff.SetStats(0)
print ("M4000 non_b_taus",events_selected, events_passing, events_failing)
print ("M4000 b_taus",events_selected_b, events_passing_b, events_failing_b)




#######################################################################################Plotting######################################################################################################

print("GetBinContent_M1000",cutflow_1000.GetBinContent(6))
print("GetBinContent_M1000_boosted",cutflow_1000_b.GetBinContent(6))

legend = TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
legend.SetHeader("#tau_{#mu,e}-#tau_{h} channels","C")
legend.SetFillStyle(1001)
legend.AddEntry(hist_bbtt_higgspt_eff,"M1000 non-boosted tau","ep")
legend.AddEntry(hist_bbtt_higgspt_eff_b,"M1000 boosted tau","ep")

legend2 = TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
legend2.SetHeader("#tau_{#mu,e}-#tau_{h} channels","C")
legend2.SetFillStyle(1001)
legend2.AddEntry(hist_bbtt_higgspt_eff_2000,"M2000 non-boosted tau","ep")
legend2.AddEntry(hist_bbtt_higgspt_eff_2000_b,"M2000 boosted tau","ep")
#legend.AddEntry(hist_bbtt_higgspt_eff_2000,"M2000 non-boosted tau","ep")
#legend.AddEntry(hist_bbtt_higgspt_eff_2000_b,"M2000 boosted tau","ep")
#legend.AddEntry(hist_bbtt_higgspt_eff_4000,"M4000 non-boosted tau","ep")
#legend.AddEntry(hist_bbtt_higgspt_eff_4000_b,"M4000 boosted tau","ep")

legend3 = TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
legend3.SetHeader("#tau_{#mu,e}-#tau_{h} channels","C")
legend3.SetFillStyle(1001)
legend3.AddEntry(hist_bbtt_higgspt_eff_4000,"M4000 non-boosted tau","ep")
legend3.AddEntry(hist_bbtt_higgspt_eff_4000_b,"M4000 boosted tau","ep")

legend4 = TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
legend4.SetHeader("#tau_{#mu,e}-#tau_{h} channels","C")
legend4.SetFillStyle(1001)
legend4.AddEntry(hist_bbtt_higgspt_eff,"M1000 non-boosted tau","ep")
legend4.AddEntry(hist_bbtt_higgspt_eff_2000,"M2000 non-boosted tau","ep")
legend4.AddEntry(hist_bbtt_higgspt_eff_4000,"M4000 non-boosted tau","ep")

legend5 = TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
legend5.SetHeader("#tau_{#mu,e}-#tau_{h} channels","C")
legend5.SetFillStyle(1001)
legend5.AddEntry(hist_bbtt_higgspt_eff_b,"M1000 boosted tau","ep")
legend5.AddEntry(hist_bbtt_higgspt_eff_2000_b,"M2000 boosted tau","ep")
legend5.AddEntry(hist_bbtt_higgspt_eff_4000_b,"M4000 boosted tau","ep")

legend6 = TLegend(0.1289398,0.6281513,0.5100287,0.8802521)
legend6.SetHeader("#tau_{#mu,e}-#tau_{h} channels","C")
legend6.SetFillStyle(1001)
legend6.AddEntry(hist_bbtt_higgspt_eff,"M1000 non-boosted tau","ep")
legend6.AddEntry(hist_bbtt_higgspt_eff_b,"M1000 boosted tau","ep")
legend6.AddEntry(hist_bbtt_higgspt_eff_2000,"M2000 non-boosted tau","ep")
legend6.AddEntry(hist_bbtt_higgspt_eff_2000_b,"M2000 boosted tau","ep")
legend6.AddEntry(hist_bbtt_higgspt_eff_4000,"M4000 non-boosted tau","ep")
legend6.AddEntry(hist_bbtt_higgspt_eff_4000_b,"M4000 boosted tau","ep")



can1 = TCanvas("canvas1", "efficiency")
#can1.cd()
can1.SetGrid()
#can1 = TCanvas("canvas", "Trigger Efficiency")
hist_bbtt_higgspt_eff.Draw("ap")
hist_bbtt_higgspt_eff_b.Draw("same p")
#hist_bbtt_higgspt_eff_2000.Draw("ap")
#hist_bbtt_higgspt_eff_2000_b.Draw("same p")
#hist_bbtt_higgspt_eff_4000.Draw("ap")
#hist_bbtt_higgspt_eff_4000_b.Draw("same p")
#can1 = TCanvas("canvas", "Trigger Efficiency")
#hist_bbtt_higgspt_eff.Draw("same p")
#hist_bbtt_higgspt_eff_b.Draw("same p")
#hist_bbtt_higgspt_eff_2000.Draw("same p")
#hist_bbtt_higgspt_eff_2000_b.Draw("same p")

#l.Draw("same")	
legend.Draw("same")
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can2 = TCanvas("canvas2", "efficiency")
#can2.cd()
can2.SetGrid()
hist_bbtt_higgspt_eff_2000.Draw("ap")
hist_bbtt_higgspt_eff_2000_b.Draw("same p")
legend2.Draw("same")
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can3 = TCanvas("canvas3", "efficiency")
#can2.cd()
can3.SetGrid()
hist_bbtt_higgspt_eff_4000.Draw("ap")
hist_bbtt_higgspt_eff_4000_b.Draw("same p")
legend3.Draw("same")
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can4 = TCanvas("canvas4", "efficiency")
#can2.cd()
can4.SetGrid()
hist_bbtt_higgspt_eff_4000.Draw("ap")
hist_bbtt_higgspt_eff_2000.Draw("same p")
hist_bbtt_higgspt_eff.Draw("same p")
legend4.Draw("same")
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can5 = TCanvas("canvas5", "efficiency")
#can2.cd()
can5.SetGrid()
hist_bbtt_higgspt_eff_4000_b.Draw("ap")
hist_bbtt_higgspt_eff_2000_b.Draw("same p")
hist_bbtt_higgspt_eff_b.Draw("same p")
legend5.Draw("same")
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can6 = TCanvas("canvas6", "efficiency")
#can2.cd()
can6.SetGrid()
hist_bbtt_higgspt_eff_4000.Draw("ap")
hist_bbtt_higgspt_eff_4000_b.Draw("same p")
hist_bbtt_higgspt_eff_2000.Draw("same p")
hist_bbtt_higgspt_eff_2000_b.Draw("same p")
hist_bbtt_higgspt_eff.Draw("same p")
hist_bbtt_higgspt_eff_b.Draw("same p")
legend6.Draw("same")
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can7= TCanvas("canvas7", "cutflow_1000")
can7.SetGrid()
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cutflow_1000.Draw()
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")


can8=TCanvas("canvas8", "cutflow_1000_b")
can8.SetGrid()
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cutflow_1000_b.Draw()
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")
#cmsLatex.DrawLatex(0.1+0.09,0.92,"Preliminary")

can9= TCanvas("canvas9", "cutflow_2000")
can9.SetGrid()
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cutflow_2000.Draw()
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can10= TCanvas("canvas10", "cutflow_2000_b")
can10.SetGrid()
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cutflow_2000_b.Draw()
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can11 = TCanvas("canvas11", "cutflow_4000")
can11.SetGrid()
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cutflow_4000.Draw()
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")

can12 = TCanvas("canvas12", "cutflow_4000_b")
can12.SetGrid()
cmsLatex = TLatex()
cmsLatex.SetTextSize(0.035)
cmsLatex.SetNDC(True)
cmsLatex.SetTextFont(61)
cmsLatex.SetTextAlign(11)
cmsLatex.SetTextFont(20)
cutflow_4000_b.Draw()
cmsLatex.DrawLatex(0.1,0.92,"CMS Preliminary")









time.sleep(1000)


	
can1.SaveAs("Trigger_Efficiency4000_With_Error.pdf")
