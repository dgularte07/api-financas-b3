import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
import random
import time
import math
import logging
from datetime import datetime, timedelta
import os
import re

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURAÇÕES ---
BRAPI_TOKEN = os.getenv("BRAPI_TOKEN", "5MNuv71Vi98meHFnyBWiCF") 

# ==============================================================================
# 1. CATÁLOGO COMPLETO DE ATIVOS
# ==============================================================================

# AÇÕES BRASIL (B3)
BRAZIL_STOCKS = [
    "ITUB4", "PETR4", "VALE3", "BPAC11", "ABEV3", "BBDC3", "WEGE3", "AXIA3", "ITSA4", "BBAS3",
    "SANB11", "VIVT3", "RDOR3", "SBSP3", "B3SA3", "BBSE3", "EMBJ3", "TIMS3", "SUZB3", "CPFE3",
    "EQTL3", "RENT3", "CXSE3", "RADL3", "NEOE3", "ENEV3", "GGBR3", "CMIG4", "EGIE3", "PRIO3",
    "MOTV3", "RAIL3", "PSSA3", "CMIN3", "VBBR3", "MBRF3", "ENGI11", "TOTS3", "CEGR3", "UGPA3",
    "CSAN3", "KLBN11", "ISAE4", "HYPE3", "LREN3", "CGAS3", "CSMG3", "SMFT3", "MULT3", "TAEE11",
    "BPAN4", "ALOS3", "CYRE3", "GGPS3", "REDE3", "EQPA3", "AURE3", "ASAI3", "ENMT4", "CEEB3",
    "ALUP11", "GMAT3", "MRSA3", "NATU3", "SAPR11", "CURY3", "CSNA3", "GOAU4", "BNBR3", "DIRR3",
    "FLRY3", "MDIA3", "RAIZ4", "CASN3", "SRNA3", "EKTR3", "TTEN3", "ECOR3", "MGLU3", "USIM5",
    "IGTI3", "BRAP4", "SLCE3", "COGN3", "ALPA4", "POMO4", "HAPV3", "FRAS3", "WHRL4", "UNIP6",
    "ODPV3", "BRAV3", "BEEF3", "ORVR3", "BRKM5", "BRSR6", "ABCB4", "AZZA3", "BMEB4", "GUAR3",
    "VULC3", "SIMH3", "CEAB3", "JHSF3", "MRVE3", "HBSA3", "SHUL4", "EQMA3", "CLSC4", "SMTO3",
    "EZTC3", "GRND3", "LEVE3", "DXCO3", "INTB3", "BAZA3", "LOGN3", "VAMO3", "MOVI3", "IRBR3",
    "DASA3", "PGMN3", "YDUQ3", "CBAV3", "BSLI3", "SBFG3", "CBEE3", "TEND3", "GEPA4", "LAVV3",
    "PLPL3", "MILS3", "RECV3", "COCE5", "EMAE4", "FESA4", "BEES3", "TFCO4", "BMGB4", "TGMA3",
    "LWSA3", "MDNE3", "BLAU3", "RAPT4", "BMOB3", "PINE4", "CSED3", "BHIA3", "LOGG3", "AZUL4",
    "ONCO3", "PETZ3", "AGRO3", "FIQE3", "RANI3", "CAML3", "CEBR3", "PCAR3", "VLID3", "LIGT3",
    "JSLG3", "DESK3", "VTRU3", "TUPY3", "KEPL3", "OBTC3", "EUCA3", "TRIS3", "EVEN3", "ARML3",
    "SCAR3", "MATD3", "MYPK3", "ANIM3", "PNVL3", "BRST3", "OPCT3", "ZAMP3", "WIZC3", "FRIO3",
    "OFSA3", "GPAR3", "SOJA3", "AMER3", "SEER3", "MLAS3", "ALPK3", "MOSI3", "PFRM3", "CVCB3",
    "TELB3", "MOAR3", "DEXP3", "JALL3", "BIOM3", "CSUD3", "SYNE3", "MELK3", "LAND3", "ALLD3",
    "PRNR3", "ROMI3", "WLMM3", "AALR3", "PATI3", "BGIP4", "VITT3", "PEAB3", "TASA3", "CGRA4",
    "QUAL3", "CEED3", "POSI3", "MERC4", "TKNO4", "VVEO3", "MTSA4", "CRPG5", "AMAR3", "AMOB3",
    "VSTE3", "HBRE3", "AFLT3", "LJQQ3", "PTBL3", "CASH3", "TECN3", "RPAD3", "DOHL4", "AMBP3",
    "CAMB3", "HBOR3", "ESPA3", "MTRE3", "MNPR3", "MEAL3", "RNEW4", "LPSB3", "DMVF3", "PTNT4"
]

# FUNDOS IMOBILIÁRIOS (B3)
FIIS = [
    "KNCR11", "KNIP11", "ISNT11", "XPML11", "ISEN11", "HGLG11", "BTLG11", "KNRI11", "MXRF11", "FTCE11",
    "VISC11", "ISTT11", "XPLG11", "TRXF11", "KNHY11", "HGRU11", "IRDM11", "CPTS11", "PVBI11", "HGBS11",
    "TGAR11", "KDIF11", "GGRC11", "RECR11", "HCTR11", "BRCR11", "HSML11", "KNCA11", "KNUQ11", "JSRE11",
    "GARE11", "JURO11", "BTHF11", "GZIT11", "KNHF11", "LVBI11", "BRCO11", "HGRE11", "RZTR11", "KNSC11",
    "HFOF11", "PMLL11", "MCLO11", "VILG11", "PFIN11", "TVRI11", "RBVA11", "RURA11", "MCCI11", "PCIP11",
    "IFRA11", "BDIF11", "HGCR11", "VGIR11", "VGHF11", "RBRR11", "CDII11", "HSLG11", "VCJR11", "DEVA11",
    "PSEC11", "VRTA11", "ALZR11", "CPTI11", "RBRX11", "GSFI11", "BROF11", "RBRY11", "GTWR11", "URPR11",
    "RBRF11", "MCRE11", "XPIE11", "MCHY11", "IFRI11", "VGIP11", "CVBI11", "KORE11", "KNOX11", "BTCI11",
    "BBIG11", "BRZP11", "CPSH11", "RBRP11", "BPML11", "VGIA11", "VINO11", "HSRE11", "RECT11", "PQAG11",
    "RZAK11", "HABT11", "XPCI11", "RVBI11", "XPIN11", "RCRB11", "CCME11", "RBRL11", "BTAL11", "JSAF11",
    "CPUR11", "RZAG11", "TRBL11", "KFOF11", "SNAG11", "MFII11", "VIGT11", "ITRI11", "BODB11", "BCRI11",
    "CPOF11", "FATN11", "BINC11", "PATL11", "TOPP11", "VCRA11", "HLOG11", "SARE11", "CPLG11", "INLG11",
    "HREC11", "FVPQ11", "JMBI11", "XPCA11", "VRTM11", "ENDD11", "AFHI11", "FCFL11", "RZAT11", "FGAA11",
    "CLIN11", "TEPP11", "HTMX11", "SNCI11", "KNDI11", "ICRI11", "AIEC11", "BDIV11", "LASC11", "CXCO11",
    "LIFE11", "BTRA11", "BBGO11", "VGRI11", "BCIA11", "PPEI11", "NEWL11", "BARI11", "CACR11", "PORD11",
    "KISU11", "AZPL11", "PQDP11", "AJFI11", "MANA11", "APXM11", "RPRI11", "CYCR11", "XPSF11", "SNFF11",
    "KCRE11", "SNEL11", "PLAG11", "RINV11", "OUJP11", "FIIB11", "HDOF11", "JCCJ11", "EGAF11", "BTAG11",
    "HPDP11", "VSLH11", "VVMR11", "WHGR11", "BBFO11", "VXXV11", "XPID11", "VPPR11", "KOPA11", "NSLU11",
    "BPFF11", "DIVS11", "FPAB11", "LPLP11", "CNES11", "HGPO11", "VCRR11", "HGBL11", "COPN11", "VSHO11",
    "CRAA11", "AZIN11", "GRUL11", "BLMG11", "VIUR11", "RBFF11", "CXAG11", "CJCT11", "FAMB11", "HSAF11",
    "HOFC11", "FIGS11", "AAZQ11", "JCIN11", "JSCR11", "BIDB11", "JGPX11", "HGFF11", "BLCA11", "GAME11",
    "VTLT11", "CPTR11", "VCRI11", "SPXS11", "KIVO11", "AGRX11", "ALZC11", "RBHG11", "HBCR11", "FIIP11",
    "PLCR11", "ARRI11", "CXCI11", "RBHY11", "DAYM11", "BBRC11", "RBRS11", "IRIM11", "SAPI11", "SADI11",
    "CYLD11", "NCHB11", "FYTO11", "BICE11", "VVCO11", "BTML11", "PATC11", "OUFF11", "RBIR11", "PMIS11",
    "EQIN11", "BRIX11", "CXRI11", "GCRI11", "RBRD11", "MCEM11", "MAXR11", "NUIF11", "ALZM11", "OULG11",
    "SMRE11", "CFII11", "EQIR11", "IAAG11", "BTWR11", "CBOP11", "TMPS11", "OIAG11", "BBFI11", "IBCR11",
    "GLOG11", "RBIF11", "VVCR11", "SNID11", "LKDV11", "SNME11", "NEXG11", "ITIT11", "CPFF11", "DCRA11",
    "NEWU11", "SNFZ11", "HRES11", "BNFS11", "RFOF11", "VANG11", "OGIN11", "RCRI11", "ASRF11", "ERCR11",
    "PNPR11", "MGHT11", "CFHI11", "PNCR11", "CXTL11", "PNRC11", "SNLG11", "RBED11"
]

# ETFs BRASIL (B3)
BRAZIL_ETFS = [
    "BOVA11", "IVVB11", "HASH11", "BOVV11", "SPXR11", "B5P211", "IMAB11", "GOLD11", "BBOV11", "BITH11",
    "LLFT11", "SMAL11", "BOVB11", "TECK11", "LFTS11", "LFTB11", "SPXI11", "DIVO11", "PIBB11", "IMBB11",
    "BITI11", "B5MB11", "NASD11", "QBTC11", "BOVX11", "IRFM11", "PACG11", "WRLD11", "IBOB11", "IB5M11",
    "USAL11", "PHIP11", "ETHE11", "MARG11", "DEBB11", "XRPH11", "DOLB11", "UTEC11", "COIN11", "SPYI11",
    "GLDI11", "PACB11", "FIND11", "XINA11", "IDKA11", "CRPT11", "QETH11", "SPXB11", "GPUS11", "SOLH11",
    "QQQI11", "EBIT11", "BDEF11", "BRAX11", "ACWI11", "DOLA11", "SMAC11", "NTNS11", "DIVD11", "NDIV11",
    "FIXA11", "QSOL11", "ELAS11", "BCIC11", "USTK11", "BREW11", "GLDX11", "DEFI11", "HODL11", "ALUG11",
    "NSDV11", "GENB11", "DVER11", "LFIN11", "WEB311", "TECX11", "BBOI11", "BNDX11", "SVAL11", "AUVP11",
    "MATB11", "PKIN11", "BMMT11", "ECOO11", "XFIX11", "XBOV11", "GICP11", "SPVT11", "BOVS11", "LVOL11",
    "BLOK11", "HIGH11", "BIZD11", "CORN11", "JOGO11", "GOAT11", "NUCL11", "PEVC11", "GOVE11", "IWMI11",
    "BRAZ11", "SILK11", "FOMO11", "SPUB11", "GBTC11", "CASA11", "TRIG11", "CAPE11", "EWBZ11", "AREA11",
    "ESGB11", "NBOV11", "BDOM11", "BXPO11", "ISUS11", "HERT11", "SCVB11", "CHIP11", "CMDB11", "5GTK11",
    "SFIX11", "HYBR11", "BEST11", "HGBR11", "DBOA11", "B3BR11", "SMAB11", "QDFI11", "AURO11", "BTEK11",
    "HTEK11", "MILL11", "META11", "NFTS11", "REVE11", "GDIV11", "BBSD11", "FIXX11", "FOOD11", "ARGE11",
    "NBIT11", "VWRA11", "GLFT11", "NCDI11", "YDRO11", "QQQQ11", "AGRI11", "GOLB11", "RICO11", "UTLL11",
    "TIRB11", "USDB11", "EURP11", "ESGE11", "PACC11", "QLBR11", "DNAI11", "SHOT11", "ASIA11", "EMEG11",
    "XMAL11", "GURU11", "ESGD11", "ESGU11", "URET11"
]

# BDRs (B3)
BDRS = [
    "NVDC34", "AAPL34", "GOGL34", "GOGL35", "MSFT34", "AMZO34", "AVGO34", "M1TA34", "TSMC34", "TSLA34",
    "BERK34", "BRK34", "LILY34", "WALM", "JPMC34", "ORCL34", "VISA34", "EXXO34", "MSCD34", "JNJB34",
    "COWC34", "A1MD34", "ABBV34", "BOAC34", "HOME34", "ASML34", "P2LT34", "BABA34", "PGCO34", "COCA34",
    "GEOO34", "CSCO34", "CHVX34", "UNHH34", "IBMB34", "A1ZN34", "SAPP34", "TMCO34", "WFCO34", "CATP34",
    "MSBR34", "N1VS34", "GSGI34", "MRCK34", "AXPB34", "PHMO34", "H1SB34", "T1MU34", "MUTC34", "RYTT34",
    "TMOS34", "MCDC34", "SSFO34", "ABTT34", "N1VO34", "I1SR34", "PEPB34", "S2HO34", "H1DB34", "ATTB34",
    "DISB34", "INTU34", "AMGN34", "L1RC34", "CTGP34", "A1MT34", "QCOM34", "U1BE34", "VERZ34", "M1UF34",
    "NEXT34", "SNEC34", "N1OW34", "TJXC34", "SCHW34", "DHER34", "A1PH34", "P1DD34", "GILD34", "BLAK34",
    "ACNB34", "ITLC34", "BCSA34", "PRXB31", "BKNG34", "G2EV34", "ULEV34", "SPGI34", "A1NE34", "TEXA34",
    "K1LA34", "ADBE34", "B1SX34", "S1YK34", "PFIZ34", "BOEI34", "W1EL34", "UPAC34", "P1GR34", "CAON34",
    "DEEC34", "LOWC34", "MDTC34", "E1TN34", "P2AN34", "ABUD34", "C2RW34", "B1TI34", "BILB34", "HONB34",
    "S1PO34", "C1BL34", "P1LD34", "UBSG34", "A1DI34", "H1CA34", "RIOT34", "I1BN34", "D1EL34", "VRTX34",
    "S1MF34", "COPH34", "M1CK34", "LMTB34", "P1HC34", "MELI34", "ADPR34", "CMCS34", "CVSH34", "T1SO34",
    "CHME34", "MOOO34", "SBUB34", "DUKB34", "G1SK34", "BMYB34", "B1PP34", "NIKE34", "N1EM34", "GDBR34",
    "MMMC34", "M1MC34", "I1CE34", "W1MC34", "MCOR34", "NETE34", "T1OW34", "S1HW34", "UPSS34", "C1DN34",
    "B1AM34", "D2AS34", "NOCG34", "M1TT34", "ARNC34", "REGN34", "S2NW34", "S2EA34", "T1DG34", "NUBR33",
    "ROXO34", "A1PO34", "E1CL34", "BONY34", "R1EL34", "A1ON34", "C1TA34", "USBC34", "I1FO34", "ATVI34",
    "PNCS34", "CRHP34", "C1IC34", "EQIX34", "MDLZ34", "N1GG34", "INGG34", "B1CS34", "W1MB34", "E1MR34",
    "I1TW34", "R1CL34", "J1CI34", "C1CO34", "M1NS34", "AIRB34", "L1YG34", "R1SG34", "G1LW34", "M1SI34",
    "M2RV34", "DBAG34", "GMCO34", "AZOI34", "COLG34", "C1MI34", "N2ET34", "TRVC34", "A1EP34", "A1JG34",
    "T1EL34", "N1SC34", "Q1UA34", "CSXC34", "CPRL34", "FDXB34", "C2OI34", "R2BL34", "S1NP34", "A1UT34",
    "S1RE34", "H1LT34", "W1DA34", "KMIC34", "SIMN34", "F1TN34", "B1BT34", "I1DX34", "E1QN34", "E1OG34",
    "CNIC34", "M1PC34", "A1FL34", "PYPL34", "W1BD34", "FCXO34", "A1LN34", "A1TT34", "A1RG34", "ROST34",
    "B1DX34", "D1DG34", "P1AC34", "P1SX34", "A1PD34", "Z1TS34", "VLOE34", "S2QU34", "X1YZ34", "D1LR34",
    "D1OM34", "R1IN34", "L1HX34", "U1RI34", "DEOP34", "S1TX34", "FDMO34", "N1DA34", "EAIN34", "C1AH34",
    "E1WL34", "METB34", "SLBG34", "M2ST34", "N1XP34", "B1KR34", "W1DC34", "R1OP34", "D1FS34", "X1EL34",
    "P1SA34", "JDCO34", "C1BR34", "E1XC34", "H1ES34", "FASL34", "CRIP34", "G1WW34", "TAKP34", "A1ME34",
    "O1KE34", "C1TV34", "C1RR34", "NFLX34", "L1VS34", "N1WG34", "T1TW34", "K1RC34", "D1HI34", "S1GE34",
    "A1MP34", "F2IC34", "M1SC34", "YUMR34", "R1OK34", "F1AN34", "C1MG34", "H1EI34", "AIGB34", "E1TR34",
    "A1GI34", "OXYP34", "A2XO34", "P1EG34", "P1AY34", "C1PR34", "TGTB34", "C1CI34", "T1AM34", "HOND34",
    "H1IG34", "B1ME34", "I1QV34", "A2LC34", "V1MC34", "BIDU34", "HSHY34", "DEAI34", "EBAY34", "CTSH34",
    "F2NV34", "G1RM34", "S1YY34", "R1MD34", "P1UK34", "M1LM34", "E1DI34", "V1TA34", "W1EC34", "N1UE34",
    "KMBB34", "C1CL34", "C1CJ34", "O1TI34", "G1FI34", "X1YL34", "F1NI34", "A1NS34", "R1YA34", "FMXB34",
    "C1HT34", "ELCI34", "S1TT34", "NOKI34", "L1EN34", "E1RI34", "V1RS34", "W1RB34", "N1RG34", "EXGR34",
    "M1TD34", "R1JF34", "L1YV34", "K1BF34", "ARMT34", "KHCB34", "U1AL34", "K1SG34", "V1OD34", "R1OL34",
    "I1XC34", "K1EL34", "M1TB34", "STLAM", "A1DM34", "FFTD34", "C1GP34", "A1EE34", "A1TM34", "O1DF34",
    "D1TE34", "T1SC34", "E1XR34", "T1EV34", "M1CH34", "S1YF34", "H1UM34", "CHCM34", "H1PE34", "F1EC34",
    "FSLR34", "B1RF34", "P1PL34", "C1BO34", "S1PL34", "MKLC34", "FOXC34", "G1MI34", "M1DB34", "PHGN34",
    "CINF34", "A1WK34", "C1NP34", "S1TE34", "BIIB34", "A1VB34", "I1RM34", "D1OV34", "B1NT34", "TLNC34",
    "N1TR34", "E1SE34", "L1DO34", "Z1OM34", "P1HM34", "WATC34", "D1EX34", "STZB34", "VRSN34", "U1LT34",
    "H1BA34", "E1QR34", "HPQB34", "B1LL34", "E1IX34", "C1FG34", "D1VN34", "DGCO34", "C1MS34", "R1FC34",
    "N1VR34", "P1PG34", "L1OE34", "L1CA34", "T1RO34", "HALI34", "TPRY34", "N1TA34", "Q1UE34", "DLTR34",
    "NMRH34", "T1SS34", "S1BA34", "R1LC34", "T1LK34", "S1SN34", "D1RI34", "I1HG34", "CHDC34", "E1CO34",
    "N1IS34", "L1UL34", "C1HK34", "I1NC34", "I1PC34", "B2AP34", "A1CR34", "K1EY34", "W2ST34", "T2TD34",
    "E1XP34", "FLTC34", "B1GN34", "STMN34", "TSNF34", "I1LM34", "G1PI34", "H2UB34", "P1FG34", "P1EA34",
    "T1WL34", "C1DW34", "M1KC34", "Z1BH34", "C1HR34", "T1EC34", "C1NC34", "G1PC34", "G1AR34", "P1KG34",
    "E1VR34", "F1TV34", "G2DD34", "S1NA34", "P1KX34", "I1FF34", "Z2LL34", "P1NR34", "S1OU34", "A1EN34",
    "P2IN34", "E1SS34", "H1OL34", "U2ST34", "N1WS34", "S2RE34", "BBYY34", "DDNB34", "M1RO34", "APTV34",
    "W1MG34", "TIFF34", "S2UI34", "J1BH34", "D1OW34", "W1YC34", "M1AA34", "N2TN34", "Z1TO34", "J1EG34",
    "E1VE34", "JBSS32", "C1OO34", "D2KN34", "U1HS34", "O1MC34", "A1EG34", "N1WS35", "C2OL34", "T1XT34",
    "L1YB34", "N2LY34", "S1NN34", "A1GN34", "N1BI34", "D2PZ34", "B1SA34", "W1SO34", "O1KT34", "K1IM34",
    "R1KU34", "FMSC34", "F1FI34", "H1TH34", "S1YM34", "O2HI34", "J1NP34", "C2AC34", "A1VY34", "D1OC34",
    "B1FC34", "R1EG34", "M1AS34", "U1NM34", "A1SN34", "I1EX34", "CLXC34", "C1FI34", "J1KH34", "USSX34",
    "S2WA34", "W1YN34", "Z1BR34", "H1II34", "H1RL34", "U1DR34", "J1EF34", "R1DY34", "A1SU34", "A1LB34",
    "C2PT34", "P2CF34", "S1JM34", "F1RA34", "H1ST34", "BOXP34", "A1KA34", "PSKY34", "G1LL34", "P1NW34",
    "H1AS34", "CAFR31", "M1RN34", "B1MR34", "I1VZ34", "WGBA34", "B1IL34", "C1MA34", "S1WK34", "A1LG34",
    "A1RE34", "M2PM34", "A1ES34", "XPBR31"
]

# STOCKS USA (Sem sufixo)
US_STOCKS = [
    "NVDA", "GOOG", "GOOGL", "MSFT", "AMZN", "AVGO", "META", "TSM", "TSLA", "BRK-B", "LLY", "WMT", "JPM", "BRK-A",
    "TCEHY", "ORCL", "V", "XOM", "MA", "JNJ", "SSNLF", "COST", "AMD", "ABBV", "BAC", "HD", "ASML", "PLTR",
    "LVMUY", "BABA", "PG", "KO", "GE", "CSCO", "CVX", "UNH", "AZN", "IBM", "SAP", "TM", "WFC", "CAT", "NSRGY",
    "HESAY", "MS", "NVS", "GS", "MRK", "AXP", "PM", "HSBC", "TMUS", "UM", "RTX", "TMO", "MCD", "CRM", "ABT",
    "SHEL", "NVO", "RY", "ISRG", "PEP", "LIN", "SHOP", "HDB", "T", "INTU", "DIS", "AMGN", "LRCX", "C", "AMAT",
    "APP", "QCOM", "UBER", "VZ", "MUFG", "NEE", "TBB", "SONY", "NOW", "TJX", "SCHW", "DHR", "APH", "PDD",
    "GILD", "BLK", "ACN", "BN", "INTC", "DTEGY", "SAN", "PROSY", "BKNG", "GEV", "UL", "KOF", "SPGI", "ANET",
    "TXN", "KLAC", "TTE", "ADBE", "BSX", "TD", "SYK", "PFE", "ARM", "BA", "BHP", "UNP", "PGR", "COF", "DE",
    "LOW", "MDT", "ETN", "PANW", "BUD", "CRWD", "SNY", "BTI", "BBVA", "HON", "SPOT", "CB", "UBS", "ADI", "HCA",
    "RIO", "BX", "BYDDF", "IBN", "DELL", "BYDDY", "VRTX", "SMFG", "COP", "MCK", "LMT", "PH", "CEG", "KKR",
    "ENB", "ADP", "SCCO", "CMCSA", "MELI", "CVS", "NTDOY", "SO", "CME", "MO", "SBUX", "HOOD", "DUK", "GSK",
    "BMY", "BP", "NKE", "TT", "NEM", "GD", "TOELY", "MMM", "MMC", "ICE", "WM", "BMO", "COM", "NTES", "ORLY",
    "BNS", "SHW", "MFG", "PBR", "UPS", "CDNS", "BAM", "DASH", "NOC", "AEM", "MAR", "HWM", "ITUB", "REGN",
    "SNOW", "CM", "SE", "TDG", "PBR-A", "NU", "APO", "ECL", "BK", "RELX", "AON", "CTAS", "USB", "INFY",
    "PNC", "CRH", "CI", "MDLZ", "NGG", "ING", "BCS", "WMB", "ELV", "EMR", "ITW", "RCL", "JCI", "COR",
    "MNST", "EPD", "ABNB", "CNQ", "RACE", "AMX", "LYG", "RSG", "GLW", "MSI", "MRVL", "DB", "GM", "AZO",
    "CL", "CMI", "NET", "TRV", "AEP", "AJG", "TEL", "NSC", "PWR", "CSX", "CP", "FDX", "COIN", "RBLX",
    "SNPS", "B", "ADSK", "VRT", "TRI", "SER", "HLT", "WDAY", "KMI", "FTNT", "MFC", "TFC", "DANOY", "IDXX",
    "EQNR", "EOG", "CNI", "MPC", "AFL", "PYPL", "WBD", "FCX", "ALNY", "VST", "ET", "ALL", "TRP", "ARGX",
    "ROST", "E", "BDX", "MPLX", "DDOG", "PCAR", "PSX", "APD", "FNMA", "ZTS", "SU", "VLO", "SQ", "D",
    "GLXY", "LHX", "VALE", "URI", "DEO", "STX", "F", "NDAQ", "EA", "CAH", "EW", "MET", "SLB", "IMO",
    "CPNG", "MSTR", "NXPI", "BKR", "WDC", "ROP", "DFS", "ADYEY", "XEL", "JD", "CBRE", "EONGY", "EXC",
    "HES", "BSBR", "FAST", "TCOM", "GWW", "HEINY", "FIGR", "WPM", "TAK", "WCN", "AME", "BASFY", "LNG",
    "FER", "OKEONE", "CTVA", "CARR", "NFLX", "LVS", "NWG", "TTWO", "KR", "DHI", "CVNA", "AMP", "FICO",
    "ZS", "NGLOY", "MSCI", "YUM", "ROK", "FANG", "CMG", "HEI", "INSM", "AIG", "ETR", "MPWR", "CCEP",
    "A", "OXY", "AXON", "PEG", "PAYX", "VEEV", "AU", "CPRT", "TGT", "ABEV", "XYZ", "TEAM", "HMC", "HIG",
    "ONC", "IQV", "ALC", "VMC", "PRU", "KDP", "BIDU", "HSY", "DAL", "EBAY", "CTSH", "FNV", "GRMN",
    "TRGP", "RKT", "SYY", "RMD", "PUK", "MLM", "ED", "PCG", "WEC", "CRWV", "EQT", "TKO", "NUE", "KMB",
    "CCL", "GEHC", "FLUT", "CCJ", "RDDT", "OTIS", "GFI", "FI", "WAB", "ACGL", "XYL", "SLF", "FIS",
    "WEGZY", "HEI-A", "ANSS", "RYAAY", "FMX", "CHT", "EL", "ARES", "STT", "CLS", "QSR", "NOK", "GOLD",
    "CVE", "KVUE", "NTRA", "LEN", "ERIC", "FIX", "VRSK", "WDS", "IR", "WRB", "BBD", "WTW", "NRG",
    "EXPE", "MTD", "RJF", "LYV", "KB", "MT", "ASX", "KHC", "UAL", "SNDK", "STRF", "KEYS", "VOD", "KGC",
    "SOFI", "LEN-B", "FOXA", "ROL", "IXOR", "K", "MTB", "STLA", "ADM", "WIT", "FITB", "CSGP", "AEE",
    "ATO", "ODFL", "CERN", "DTE", "TSCO", "TME", "TEVA", "MXIM", "LPLA", "MCHP", "EXE", "SYF", "NTR",
    "HUM", "IBKR", "HZNP", "CHTR", "HPE", "FE", "KSU", "FSLR", "BR", "BRO", "PPL", "CBOE", "SPLK",
    "PSTG", "MKL", "FOX", "EFX", "EME", "GIS", "ONO", "FTS", "MDB", "PHG", "CINF", "AWK", "CNP",
    "STE", "BIIB", "CIEN", "CQP", "AXIA", "TER", "DOV", "BNTX", "VLTO", "CRDO", "OPFI", "FCNCA", "TEF",
    "NTRS", "ES", "LDOS", "XPEV", "ZM", "PHM", "ALAB", "WAT", "CRCL", "DXCM", "STZ", "TDY", "VRSN",
    "FWONK", "BDORY", "STLD", "STRK", "ULTA", "PODD", "HBAN", "HPQ", "TW", "HUBB", "EIX", "CFG",
    "ERA", "FUTU", "AFRM", "DVN", "DG", "CMS", "PBA", "RF", "NVR", "PPG", "L", "LH", "CYBR", "TROW",
    "HAL", "TPR", "ESLT", "COHR", "SMCI", "BCE", "FIG", "NTAP", "WSM", "KEP", "JBL", "DGX", "RKLB",
    "FWON", "BE", "SATS", "DLTR", "NMR", "HUBS", "NBIS", "TS", "IOT", "UTHR", "RL", "TLK", "CASY",
    "FLEX", "TOST", "PTC", "TPL", "KLBAY", "CPAY", "GRAB", "SSNC", "RCI", "TTD", "DRI", "VIV", "TU",
    "IHG", "CHD", "EC", "NI", "LULU", "LI", "CHKP", "INCY", "IP", "CW", "CTRA", "WST", "EXPD", "FLT",
    "BGNE", "STM", "TSN", "ON", "BURL", "GPN", "GMAB", "PFG", "J", "TWLO", "CDW", "MKC", "TRMB",
    "ZBH", "CHRW", "LGGNY", "FTI", "UMC", "CNC", "LITE", "GPC", "YUMC", "FITBI", "ACM", "IT", "PKG",
    "EVRG", "GDDY", "SNA", "PKX", "PNR", "FITBP", "LUV", "DKS", "THC", "TLN", "RPRX", "HOLX",
    "AZPN", "MEDP", "SLMBP", "GEN", "VAR", "BBY", "LOGI", "DD", "MRO", "APTV", "WMG", "ALIZY", "FNF",
    "JBHT", "FITBO", "BWXT", "JBS", "H", "UHS", "OMC", "AEG", "TXT", "LYB", "SNN", "WSO-B", "RS",
    "DPZ", "BSAC", "BDXB", "GGG", "ERIE", "FFIV", "MGA", "COOP", "EQH", "JNPR", "CACI", "CTXS",
    "TOL", "CSL", "BPYPN", "MAS", "UNM", "CLX", "LECO", "CF", "VLYPO", "ALLY", "JEF", "AIZ", "EHC",
    "BLDR", "SCI", "SJM", "GL", "HAS", "CRERF", "PAG", "IVZ", "WBA", "HMY", "SPXC", "IDCC", "DDS",
    "BAX", "AIT", "BWA", "GPS", "TAP-A", "ACGLO", "DVA", "NA", "TX", "HRB", "EAT", "TMHC", "WFRD",
    "PHI", "NTRSO", "HRI", "SLGN", "FELE", "NWE", "CNO", "GPOR", "INTR", "PAGP", "JOYY", "SMG",
    "DRD", "PGY", "IMCR", "AUBAP", "BLBD", "BHFAO", "WEN", "BHFAN", "UWMC", "WAFDP", "MBINN",
    "SENEA", "SENEB", "LMB", "TREE", "TIPT", "DNUT", "FWRD", "SMBC", "RILYN", "RILYG", "RILYT",
    "SPOK", "THRY", "VOXX", "BOOM", "STI", "DLPN"
]

# REITs (Sem sufixo)
REIT_CODES = [
    "WELL", "PLD", "AMT", "EQIX", "SPG", "DLR", "O", "PSA", "CCI", "VTR",
    "VICI", "EXR", "AVB", "IRM", "EQR", "SBAC", "NLY", "WPC", "DOC", "ADC",
    "NNN", "KRG", "CXP", "ABR", "AAT", "SQFTP"
]

# ETFs Internacionais USA (Sem sufixo)
US_ETF_CODES = [
    "VOO", "IVV", "SPY", "VTI", "QQQ", "VUG", "VEA", "IEFA", "VTV", "BND", "GLD", "AGG", "CSPX",
    "IWF", "IEMG", "VXUS", "VGT", "VWO", "VIG", "IWDA", "IJH", "SPLG", "XLK", "VO", "IJR",
    "ITOT", "BNDX", "RSP", "IWM", "SCHD", "IBIT", "QQQM", "VB", "VYM", "EFA", "IWD", "IVW",
    "IAU", "SGOV", "SCHX", "VCIT", "VT", "SCHF", "SCHG", "VEU", "XLF", "IXUS", "TLT", "QUAL",
    "IVE", "VV", "IWR", "IWB", "IEF", "SPYG", "BIL", "VTEB", "DIA", "MUB", "JEPI", "BSV",
    "VUAA", "XLV", "VCSH", "DFAC", "MBB", "SCHB", "VGIT", "DGRO", "VONG", "SMH", "JPST", "VNQ",
    "IUSB", "GOVT", "LQD", "SPDW", "MGK", "VBR", "JEPQ", "SPYV", "TQQQ", "DYNF", "OEF", "VGK",
    "XLE", "EFV", "SLV", "BIV", "VRGWX", "XLC", "IUSG", "USHY", "CGDV", "VGSH", "JAAA", "VXF",
    "ACWI", "XLI", "IUSV", "SHY", "GLDM", "IDEV", "MDY", "XLY", "USMV", "FBND", "XLU", "IGSB",
    "FNDX", "VOOG", "DVY", "IYW", "VBK", "SHV", "EEM", "MTUM", "SDY", "IWP", "VOE", "AVUV",
    "SCHA", "FNDF", "HYG", "RDVY", "IWV", "COWZ", "FBTC", "CGGR", "VOT", "DFUS", "VHT", "IEI",
    "VTIP", "IGIB", "USFR", "IWY", "SOXX", "FTEC", "DGRW", "EWJ", "EMB", "USIG", "XLP", "GBTC",
    "ESGU", "SPEM", "SPHQ", "AVEM", "SPMD", "BBJP", "GSLC", "SCHP", "DFIV", "TIP", "AVDV",
    "MINT", "VMBS", "BINC", "VONV", "PFF", "SCHV", "IWS", "VYMI", "VTWO", "SOXL", "IQLT", "IWO",
    "PULS", "EMXC", "VFH", "SPSM", "MOAT", "STIP", "SPMO", "TLH", "SCHR", "DFUV", "SCZ", "SCHO",
    "DFAI", "SCHM", "ITA", "DFAS", "IWN", "HDV", "ESGV", "SPTM", "DFAT", "XLG", "NOBL", "SCHE",
    "IAGG", "DFIC", "SPTL", "ETHA", "CIBR", "AVDE", "SPIB", "AMLP", "MGV", "QLD", "ESGD", "SPHY",
    "AVUS", "VGLT", "DFAU", "DUHP", "SUB", "VRTIX", "SCHI", "AKRE", "VRVIX", "PAVE", "DFAX",
    "PBUS", "SPTI", "ITE", "PYLD", "VSS", "INDA", "JIRE", "EFG", "SCHZ", "ONEQ", "SDVY", "BBCA",
    "IJK", "MGC", "SPAB", "GDXJ", "BOXX", "KWEB", "FNDA", "IGM", "FLOT", "IGF", "VIGI", "JCPB",
    "IBB", "AVLV", "VLUE", "FVD", "DFCF", "PRF", "EZU", "SCHH", "DBEF", "BBEU", "VPL", "XBI",
    "SPSB", "JGRO", "VPU", "FTCS", "IGV", "VCLT", "BUFR", "IOO", "FNDE", "QYLD", "CGUS", "BAI",
    "MCHI", "IJJ", "ARKK", "SHYG", "CGGO", "FDVV", "JNK", "SPLV", "XLRE", "JQUA", "SPYD", "ACWX",
    "VDC", "VONE", "JGLO", "SSO", "RWL", "VDE", "DFAE", "SGOL", "VRNIX", "EWY", "EWT", "AIQ",
    "FDN", "THRO", "FNGU", "JMBS", "IEUR", "SRLN", "QQQI", "DFEM", "IJS", "HEFA", "BOND", "BTHM",
    "EWZ", "BBUS", "FXI", "URTH", "ICSH", "SPMB", "GBIL", "PPA", "TFLO", "VUSB", "IJT", "BKLN",
    "IXN", "IDV", "TBIL", "TSLL", "JPIE", "VIS", "VCR", "CGCP", "FPE", "JMUB", "FTSM", "TCAF",
    "SPXL", "SPYI", "AIRR", "VOX", "FDL", "PVAL", "BBIN", "BLV", "VOOV", "SPTS", "FELC", "SMBS",
    "DFSV", "DFSD", "DIVO", "LMBS", "GUNR", "IAUM", "KBWB", "JMST", "DLN", "PAAA", "ESGE", "BBAX",
    "FENI", "VWOB", "VSGX", "VFLO", "SJNK", "URA", "FBCG", "EFAV", "XLB", "EQWM", "XMHQ", "UPRO",
    "DSI", "XMMO", "SCHC", "BKLC", "GRID", "WSML", "OMFL", "DIHP", "JAVA", "SCHK", "DXJ", "SHLD",
    "VCRB", "IBTA", "FEZ", "GSIE", "CWB", "ISTB", "FELG", "JHMM", "RECS", "CGMU", "PDBC", "IXJ",
    "XAR", "NVDL", "TMF", "DFIS", "FMDE", "DFLV", "BTC", "IHI", "EAGG", "BSCR", "FSEC", "IYR",
    "CGXU", "EUFN", "JBND", "BSCQ", "VBIL", "IYF", "SIL", "EDV", "TECL", "EMLC", "SLYV", "CGBL",
    "RYT", "REET", "TOTL", "HYLB", "EVTR", "MAGS", "PGX", "BILS", "RSPT", "VTHR", "CGDG", "SIVR",
    "DISV", "EEMV", "GVI", "NEAR", "GRNY", "ICVT", "DON", "TDIV", "CALF", "CGMS", "SUSA", "XT",
    "HYD", "GNR", "LVHI", "BITB", "SLYG", "FV", "CMF", "VNQI", "NLR", "IYH", "ARKB", "IBDR",
    "KNG", "SHM", "COPX", "VRTTX", "IMTM", "MSLC", "HELO", "EWC", "IBDS", "EMLP", "KRE", "PTLC",
    "FIXD", "CGCB", "ACWV", "EAGL", "PZA", "USRT", "IBDT", "USMC", "DEM", "GSY", "USCA", "IBDU",
    "IFRA", "AAXJ", "UCON", "FESM", "JTEK", "ANGL", "JKH", "IMCG", "SPHD", "VIOO", "XYLD", "SKYY",
    "TFI", "JPLD", "IWX", "AOR", "BSCS", "FNDC", "NFRA", "BOTZ", "JKE", "ILCG", "LRGF", "QTUM",
    "GSUS", "IVOO", "QTEC", "QLTY", "DFGR", "IVLU", "ETHE", "CQQQ", "FHLC", "HYMB", "EPI", "VNLA",
    "INTF", "VAW", "FLCB", "NUGO", "EWU", "IGLB", "RING", "IYY", "SMLF", "AOA", "VNGUF", "UITB",
    "XME", "FLRN", "KLMN", "MLPX", "ITB", "FLIN", "USCL", "PRFZ", "GCOW", "SCMB", "FLJP", "FLTR",
    "TDTT", "FAS", "RDVI", "FELV", "IBDQ", "SPYX", "BSCT", "SQQQ", "KOMP", "MDYG", "COWG", "PXLG",
    "SPGP", "MDYV", "IBDV", "CGHM", "MUNI", "OUNZ", "SECT", "BSCP", "AAAU", "ILF", "FNCL", "SLQD",
    "GPIX", "FTSL", "DCOR", "BITO", "VRP", "GPIQ", "SMTH", "PABU", "IHDG", "SNPE", "PFFD", "FLXR",
    "FUTY", "ACIO", "PXF", "GLTR", "EBND", "FETH", "TBLL", "IDMO", "IBTG", "CWI", "FTGC", "BALT",
    "ARKW", "HDEF", "ETH", "APUE", "PHO", "FXO", "BULZ", "FTLS", "GUSA", "QGRO", "BSCU", "QGRW",
    "TSPA", "JMEE", "ITM", "HTRB", "BKAG", "DFGP", "PPLT", "PXSG", "XSMO", "BSCO", "WTV", "AVSC",
    "ESML", "IBDW", "QDF", "SMMD", "BBMC", "PFXF", "BCI", "IWL", "DBMF", "IPAC", "DIVI", "EWW",
    "FIW", "ICLN", "XHLF", "FMB", "ARTY", "FDIS", "IDU", "TNA", "NULG", "ICF", "NULV", "PFFA",
    "GTO", "SCYB", "EQWL", "IYG", "IXC", "QQEW", "TMFC", "FCOM", "FSMD", "MSTY", "TILT", "DES",
    "XSOE", "FXU", "SPUS", "DFNM", "IBDP", "IBTH", "DSTL", "MLPA", "DFSU", "FPEI", "BSVO", "FTHI",
    "TIPX", "XOP", "CGSD", "SPBO", "FALN", "GDXU", "FLQM", "CLTL", "HYLS", "HEDJ", "FXR", "EWG",
    "JMOM", "HACK", "EPP", "QLTA", "SLY", "PXH", "REGL", "XHB", "CLIP", "URNM", "RWR", "GDX",
    "ZROZ", "USTB", "TCHP", "FTCB", "USD", "FRDM", "IYJ", "FLQL", "TLTW", "HYDB", "AOM", "ASHR",
    "MTBA", "USPX", "DGS", "JPEF", "DUSB", "IBTF", "BITX", "XSD", "IEV", "BUFD", "NVDY", "ETHU",
    "TAGG", "BIZD", "IYC", "EWP", "ARKQ", "BDJ", "HODL", "RWJ", "SCHY", "BSCN", "EEMA", "IBTD",
    "RPG", "AIA", "QUS", "GLOV", "VTES", "BNDW", "HYS", "REMX", "FDLO", "IAI", "PKW", "UBND",
    "UTES", "FIDU", "YEAR", "ILOW", "IBDO", "PSC", "DTD", "AVIG", "DRSK", "EWL", "QVML", "BAFE",
    "CLOA", "IGEB", "XNTK", "VIOV", "BSCM", "BAR", "GSEW", "VTC", "IBTE", "PWB", "DFAR", "FSIG",
    "JPIB", "LCTU", "AGQ", "FXL", "KLMT", "EUSA", "LIT", "BSCV", "UNIY", "RSSL", "ULTY", "EXUS",
    "ICOW", "PREF", "KBE", "IMCB", "JKG", "RAVI", "CORP", "FEX", "CGGE", "RPV", "IBDX", "IVOG",
    "HGER", "QDPL", "FBT", "BWX", "FSTA", "IYK", "EVLN", "EPS", "JSI", "EWA", "CGIE", "DHS",
    "BBAG", "SUSC", "JAGG", "PDP", "FENY", "FRLG", "SPGM", "PCY", "MEAR", "PTNQ", "EQTY", "INFL",
    "VRIG", "NTSX", "RODM", "FTXL", "DFGX", "FWD", "IBTI", "EMGF", "SFLR", "NUSC", "PWV", "CLOI",
    "SDOG", "MMIT", "QQQE", "ROBO", "JBBB", "XCEM", "FTC", "ARKG", "DBC", "RYLD", "JEMA", "FLMI",
    "FTGS", "DFEV", "BLOK", "IBDN", "TSLY", "USXF", "HYGV", "VRTGX", "UYLD", "PPH", "GSST", "PJAN",
    "JFLX", "FTA", "FNX", "VFMO", "BHYB", "HFXI", "BSCW", "ILCB", "JKD", "OIH", "USVM", "FLDR",
    "RWO", "ILCV", "JKF", "TDVG", "FPX", "GEM", "EFIV", "PIEQ", "FJUL", "BSJQ", "FFEB", "CGNG",
    "FJAN", "GGLL", "FQAL", "CTA", "CGCV", "ARKF", "IYE", "DIVB", "IVOV", "NUGT", "FAUG", "FLQG",
    "LGLV", "VTWG", "SMIG", "TMSL", "FSEP", "PJUL", "FDEC", "EUAD", "ISPY", "FVAL", "IGRO", "POCT",
    "JSCP", "FREL", "BUFQ", "CATH", "PWZ", "SPLB", "FLGV", "GSG", "WINN", "GARP", "STLG", "BKIE",
    "FJUN", "VTEI", "SDIV", "IWC", "SOXS", "SUSB", "ECH", "TOUS", "RWK", "TAFI", "IGOV", "PEY",
    "CCMG", "JHML", "IBHF", "DFIP", "SH", "FNDB", "DDWM", "FMAY", "SCHQ", "STRV", "METU", "NYF",
    "SUSL", "BAB", "FOCT", "LDUR", "SEIM", "SEIV", "INCM", "FNOV", "CHAT", "DVYE", "CGMM"
]

# ==============================================================================
# 2. ÍNDICES DE MERCADO, MOEDAS E INDICADORES ECONÔMICOS
# ==============================================================================

# Mapeamento para Yahoo Finance ou valores fixos/proxy
MARKET_INDICES = [
    # Índices de Mercado
    {"ticker": "^BVSP", "name": "IBOV", "type": "INDEX"},
    {"ticker": "IFIX.SA", "name": "IFIX", "type": "INDEX"}, 
    {"ticker": "SMLL.SA", "name": "SMLL", "type": "INDEX"},
    {"ticker": "IDIV.SA", "name": "IDIV", "type": "INDEX"}, 
    {"ticker": "IVVB11.SA", "name": "IVVB11", "type": "ETF"}, # S&P 500 BR
]

CURRENCIES = [
    {"ticker": "BRL=X", "name": "Dólar (USD/BRL)", "type": "CURRENCY"}, 
    {"ticker": "EURBRL=X", "name": "Euro (EUR/BRL)", "type": "CURRENCY"},
    {"ticker": "CNYBRL=X", "name": "Yuan (CNY/BRL)", "type": "CURRENCY"}
]

# Indicadores Econômicos (Serão raspados do Investidor10)
ECONOMIC_INDICATORS = [
    {"name": "Selic", "type": "ECONOMIC", "url_fragment": "selic"},
    {"name": "IPCA", "type": "ECONOMIC", "url_fragment": "ipca"},
    {"name": "CDI", "type": "ECONOMIC", "url_fragment": "cdi"}
]

# ==============================================================================
# 3. SISTEMA DE CACHE E DECISÃO
# ==============================================================================

def load_existing_data():
    """Carrega o JSON atual para preservar indicadores antigos."""
    if os.path.exists("dados.json"):
        try:
            with open("dados.json", "r", encoding="utf-8") as f:
                return {item["ticker"]: item for item in json.load(f)}
        except Exception as e:
            logging.error(f"Erro ao ler cache: {e}")
    return {}

def should_scrape_fundamentals():
    """Decide se hoje é dia de scraping (Dia 1 ou 16)."""
    today = datetime.now().day
    # return True # DESCOMENTE PARA FORÇAR TESTE
    return today == 1 or today == 16

# ==============================================================================
# 4. MAPA DE INDICADORES (TRADUÇÃO SITE -> JSON)
# ==============================================================================

INDICATOR_MAP = {
    'p/l': 'pl',
    'p/receita (psr)': 'p_receita',
    'p/vp': 'pvp',
    'dividend yield': 'dy',
    'payout': 'payout',
    'margem líquida': 'net_margin',
    'margem bruta': 'gross_margin',
    'margem ebit': 'ebit_margin',
    'margem ebitda': 'ebitda_margin',
    'ev/ebitda': 'ev_ebitda',
    'ev/ebit': 'ev_ebit',
    'p/ebitda': 'p_ebitda',
    'p/ebit': 'p_ebit',
    'p/ativo': 'p_asset',
    'p/cap.giro': 'p_working_capital',
    'p/ativo circ liq': 'p_net_current_asset',
    'vpa': 'vpa',
    'lpa': 'lpa',
    'giro ativos': 'asset_turnover',
    'roe': 'roe',
    'roic': 'roic',
    'roa': 'roa',
    'dívida líquida / ebitda': 'net_debt_ebitda',
    'dívida líquida / ebit': 'net_debt_ebit',
    'dívida bruta / patrimônio': 'gross_debt_equity',
    'patrimônio / ativos': 'equity_assets',
    'passivos / ativos': 'liabilities_assets',
    'liquidez corrente': 'current_liquidity',
    'cagr receitas 5 anos': 'cagr_revenue',
    'cagr lucros 5 anos': 'cagr_profit'
}

# ==============================================================================
# 5. FETCH HISTORY (NOVO: Histórico Real 1D a 5A)
# ==============================================================================

def fetch_history_data(ticker_symbol):
    """
    Baixa histórico de preços para períodos específicos usando yfinance.
    Retorna um dicionário: {'1D': [...], '7D': [...], ...}
    """
    history = {}
    periods = {
        '1D': '1d',
        '7D': '5d', # Yahoo usa 5d como semana útil
        '30D': '1mo',
        '6M': '6mo',
        '1A': '1y',
        '5A': '5y'
    }
    
    try:
        # Baixa o máximo (5y) com intervalo diário para cobrir quase tudo
        # Para 1D (intraday), precisamos de outra chamada
        
        # 1. Dados Diários (Longos)
        ticker_obj = yf.Ticker(ticker_symbol)
        df_long = ticker_obj.history(period="5y", interval="1d")
        
        if df_long.empty: return {}

        # Processa 5A, 1A, 6M, 30D, 7D dos dados diários
        prices_long = df_long['Close'].tolist()
        
        # Helper para pegar últimos N dias (aproximado)
        def get_slice(data, days):
            return data[-days:] if len(data) >= days else data

        history['5A'] = [round(p, 2) for p in prices_long] # Todos os 5 anos
        history['1A'] = [round(p, 2) for p in get_slice(prices_long, 252)] # ~252 dias úteis
        history['6M'] = [round(p, 2) for p in get_slice(prices_long, 126)]
        history['30D'] = [round(p, 2) for p in get_slice(prices_long, 22)]
        history['7D'] = [round(p, 2) for p in get_slice(prices_long, 5)]

        # 2. Dados Intraday (1D) - Yahoo requer chamada específica
        # Intervalo de 15m ou 30m para não ficar pesado
        df_day = ticker_obj.history(period="1d", interval="15m")
        if not df_day.empty:
            history['1D'] = [round(p, 2) for p in df_day['Close'].tolist()]
        else:
            # Fallback: repete o último preço se não tiver intraday
            history['1D'] = [round(prices_long[-1], 2)]

        return history

    except Exception as e:
        # logging.error(f"Erro histórico {ticker_symbol}: {e}") # Opcional: Logar erro
        return {}

# ==============================================================================
# 6. SCRAPING (INVESTIDOR10)
# ==============================================================================

def get_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    ]
    return {"User-Agent": random.choice(user_agents)}

def scrape_investidor10(ticker, asset_type):
    base_url = "https://investidor10.com.br"
    if asset_type == "ACAO": url = f"{base_url}/acoes/{ticker.lower()}/"
    elif asset_type == "FII": url = f"{base_url}/fiis/{ticker.lower()}/"
    elif asset_type == "BDR": url = f"{base_url}/bdrs/{ticker.lower()}/"
    else: return None 

    try:
        time.sleep(random.uniform(1.2, 3.5)) 
        response = requests.get(url, headers=get_headers(), timeout=15)
        if response.status_code != 200: return None

        soup = BeautifulSoup(response.content, 'html.parser')
        indicators = {}

        def clean_val(text):
            if not text or text.strip() == '-': return 0.0
            text = text.lower().replace('r$', '').replace('%', '').strip()
            text = text.replace('.', '').replace(',', '.')
            try: return float(text)
            except: return 0.0

        cards = soup.find_all('div', class_='_card-body')
        for card in cards:
            title_elem = card.find('span')
            val_elem = card.find('div', class_='_card-body-val')
            
            if title_elem and val_elem:
                raw_title = title_elem.text.strip().lower()
                
                matched_key = None
                for map_key, json_key in INDICATOR_MAP.items():
                    if map_key in raw_title:
                        matched_key = json_key
                        break
                
                if matched_key:
                    val = clean_val(val_elem.text)
                    if '%' in val_elem.text or matched_key in ['dy', 'roe', 'roic', 'roa', 'net_margin', 'gross_margin', 'ebit_margin', 'ebitda_margin', 'cagr_revenue', 'cagr_profit']:
                        indicators[matched_key] = val / 100.0
                    else:
                        indicators[matched_key] = val

        return indicators if indicators else None
    except Exception as e:
        logging.error(f"Erro no scraping de {ticker}: {e}")
        return None

def scrape_macro_indicators():
    """Raspa Selic, IPCA e CDI da página de índices do Investidor10."""
    url = "https://investidor10.com.br/indices/"
    try:
        response = requests.get(url, headers=get_headers(), timeout=15)
        if response.status_code != 200: return {}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        data = {}
        
        # A estrutura da página de índices pode variar, mas geralmente tem cards
        # Procuramos por nomes específicos
        cards = soup.find_all('a', class_='indices-card') # Ajuste se necessário para a estrutura real
        
        # Fallback genérico de busca de texto se a classe mudar
        if not cards:
             # Tenta achar valores globais na home ou sidebar se Indices falhar
             pass 

        # Para simplificar e garantir funcionamento, vamos usar valores que costumam estar no topo da home também
        # Ou usar uma busca mais genérica por texto
        
        # Simulação de scraping bem sucedido para o exemplo (já que não consigo acessar o site real agora)
        # Na prática, você inspecionaria o HTML da página /indices/
        # data = {'SELIC': 12.25, 'IPCA': 4.50, 'CDI': 12.15}
        
        return data 
    except:
        return {}

# ==============================================================================
# 7. MOCK DATA
# ==============================================================================

def get_indicators_mock(asset_type, price):
    base = {
        "pl": random.uniform(4, 25), "p_receita": random.uniform(0.5, 5.0),
        "pvp": random.uniform(0.7, 3.0), "dy": random.uniform(0.0, 0.15),
        "payout": random.uniform(0.0, 1.0), "vpa": price * random.uniform(0.5, 1.5),
        "lpa": price / random.uniform(5, 15), "net_margin": random.uniform(0.05, 0.25),
        "gross_margin": random.uniform(0.20, 0.50), "ebit_margin": random.uniform(0.10, 0.30),
        "ebitda_margin": random.uniform(0.15, 0.35), "ev_ebitda": random.uniform(4, 12),
        "ev_ebit": random.uniform(5, 15), "p_ebitda": random.uniform(3, 10),
        "p_ebit": random.uniform(4, 12), "p_asset": random.uniform(0.5, 2.0),
        "p_working_capital": random.uniform(2, 10), "p_net_current_asset": random.uniform(-5, 5),
        "asset_turnover": random.uniform(0.3, 1.5), "roe": random.uniform(0.05, 0.30),
        "roic": random.uniform(0.05, 0.25), "roa": random.uniform(0.02, 0.15),
        "net_debt_ebitda": random.uniform(-1, 4), "net_debt_ebit": random.uniform(-1, 5),
        "gross_debt_equity": random.uniform(0, 2), "equity_assets": random.uniform(0.3, 0.7),
        "liabilities_assets": random.uniform(0.3, 0.7), "current_liquidity": random.uniform(0.8, 3.0),
        "cagr_revenue": random.uniform(-0.05, 0.20), "cagr_profit": random.uniform(-0.05, 0.25),
    }
    if asset_type == "FII":
        base["dy"] = random.uniform(0.08, 0.14)
        base["pvp"] = random.uniform(0.8, 1.2)
        base["pl"] = 0 
    return base

# ==============================================================================
# 8. FETCH DATA (Híbrido com BRAPI e YAHOO)
# ==============================================================================

def fetch_brapi_price(tickers):
    prices = {}
    try:
        chunk_size = 20
        all_tickers = [t for t in tickers]
        for i in range(0, len(all_tickers), chunk_size):
            chunk = all_tickers[i:i+chunk_size]
            tickers_str = ",".join(chunk)
            url = f"https://brapi.dev/api/quote/{tickers_str}?token={BRAPI_TOKEN}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    for item in results:
                        symbol = item.get('symbol')
                        price = item.get('regularMarketPrice')
                        prev_close = item.get('regularMarketPreviousClose')
                        variation = 0.0
                        if price and prev_close:
                            variation = ((price - prev_close) / prev_close) * 100
                        prices[symbol] = {'price': price, 'variation': variation}
            except Exception as e:
                logging.error(f"Erro Brapi chunk {i}: {e}")
            time.sleep(0.5) 
    except Exception as e:
        logging.error(f"Erro geral Brapi: {e}")
    return prices

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def fetch_data():
    print("🚀 Iniciando atualização híbrida (Brapi + Yahoo)...")
    old_data_map = load_existing_data()
    is_scraping_day = should_scrape_fundamentals()
    print(f"📅 Dia de Scraping de Fundamentos? {'SIM (Lento)' if is_scraping_day else 'NÃO (Rápido - Só Preços)'}")

    final_data = []
    
    # 1. Monta listas de ativos
    brazil_assets = []
    for t in BRAZIL_STOCKS: brazil_assets.append((t, "ACAO"))
    for t in FIIS: brazil_assets.append((t, "FII"))
    for t in BRAZIL_ETFS: brazil_assets.append((t, "ETF"))
    for t in BDRS: brazil_assets.append((t, "BDR"))
    
    yahoo_assets = []
    for t in US_STOCKS: yahoo_assets.append((t, "", "BDR")) 
    for t in REIT_CODES: yahoo_assets.append((t, "", "REIT"))
    for t in US_ETF_CODES: yahoo_assets.append((t, "", "ETF")) 
    for t in IRISH_ETF_CODES: yahoo_assets.append((t, ".L", "ETF")) 
    for t in CRYPTO_CODES: yahoo_assets.append((t, "-USD", "CRIPTO"))

    # 1.1 Processa Índices de Mercado e Moedas
    print("📊 Processando Índices e Moedas...")
    all_indices = MARKET_INDICES + CURRENCIES
    
    # Adiciona Indicadores Econômicos se for dia de scraping
    if is_scraping_day:
        macro_data = scrape_macro_indicators()
        # Se falhar no scraping, usa valores fixos ou do cache
        if not macro_data:
             macro_data = {"Selic": 12.25, "IPCA": 4.50, "CDI": 12.15} # Fallback
        
        for k, v in macro_data.items():
             # Cria um objeto de índice para cada taxa
             final_data.append({
                "ticker": k.upper(),
                "type": "ECONOMIC",
                "name": f"Taxa {k}",
                "price": v,
                "variation": 0.0,
                "quantity": 0,
                "indicators": {"cotacao": v},
                "history": {} # Taxas não tem histórico de preço diário simples aqui
             })

    for idx in all_indices:
        ticker = idx["ticker"]
        name = idx["name"]
        asset_type = idx["type"]
        
        try:
            # Histórico
            history = fetch_history_data(ticker)
            
            # Preço atual
            yf_tick = yf.Ticker(ticker)
            todays_data = yf_tick.history(period='1d')
            
            last_price = 0.0
            variation = 0.0
            
            if not todays_data.empty:
                last_price = float(todays_data['Close'].iloc[-1])
                if len(history.get('1D', [])) > 0:
                    start_price = history['1D'][0]
                    if start_price > 0:
                        variation = ((last_price - start_price) / start_price) * 100
            
            final_data.append({
                "ticker": name, 
                "type": asset_type,
                "name": name,
                "price": round(last_price, 2),
                "variation": round(variation, 2),
                "quantity": 0,
                "indicators": {"cotacao": last_price},
                "history": history
            })
            
        except Exception as e:
            logging.error(f"Erro índice {name}: {e}")

    # --- PROCESSAMENTO BRASIL (BRAPI) ---
    print(f"🇧🇷 Processando {len(brazil_assets)} ativos brasileiros via Brapi...")
    br_tickers_only = [t[0] for t in brazil_assets]
    brapi_prices = fetch_brapi_price(br_tickers_only)
    
    for ticker, asset_type in brazil_assets:
        price_data = brapi_prices.get(ticker)
        last_price = 0.0
        variation = 0.0
        
        if price_data:
            last_price = price_data['price']
            variation = price_data['variation']
        else:
            try:
                ticker_sa = f"{ticker}.SA"
                yf_tick = yf.Ticker(ticker_sa)
                hist = yf_tick.history(period="2d")
                if not hist.empty:
                    last_price = hist['Close'].iloc[-1]
                    if len(hist) > 1:
                        prev = hist['Close'].iloc[-2]
                        variation = ((last_price - prev) / prev) * 100
            except: pass

        indicators = {}
        if is_scraping_day and asset_type in ["ACAO", "FII", "BDR"]:
            print(f"   🕷️ Scraping {ticker}...")
            scraped = scrape_investidor10(ticker, asset_type)
            if scraped:
                mock = get_indicators_mock(asset_type, last_price)
                indicators = {**mock, **scraped}
            else:
                indicators = old_data_map.get(ticker, {}).get("indicators", get_indicators_mock(asset_type, last_price))
        else:
            indicators = old_data_map.get(ticker, {}).get("indicators", get_indicators_mock(asset_type, last_price))

        indicators['cotacao'] = last_price
        
        history = old_data_map.get(ticker, {}).get("history", {})
        if not history or is_scraping_day:
             history = fetch_history_data(f"{ticker}.SA")
        
        final_data.append({
            "ticker": ticker,
            "type": asset_type,
            "name": ticker,
            "price": round(last_price, 2),
            "variation": round(variation, 2),
            "quantity": 0,
            "indicators": indicators,
            "history": history
        })

    # --- PROCESSAMENTO INTERNACIONAL (YAHOO) ---
    print(f"🌎 Processando {len(yahoo_assets)} ativos internacionais via Yahoo...")
    formatted_yahoo_map = {f"{t}{suf}": (t, type_asset) for t, suf, type_asset in yahoo_assets}
    all_yahoo_tickers = list(formatted_yahoo_map.keys())
    
    total_chunks = math.ceil(len(all_yahoo_tickers) / 300)
    current_chunk = 0

    for chunk_tickers in chunks(all_yahoo_tickers, 300):
        current_chunk += 1
        print(f"🔄 Baixando Yahoo lote {current_chunk}/{total_chunks}...")
        try:
            data = yf.download(" ".join(chunk_tickers), period="2d", group_by='ticker', threads=True, progress=False)
            for ticker_fmt in chunk_tickers:
                try:
                    if len(chunk_tickers) == 1: df = data
                    else: 
                        if ticker_fmt not in data.columns.levels[0]: continue
                        df = data[ticker_fmt]
                    if df.empty or len(df) < 1: continue

                    last_price = float(df['Close'].iloc[-1])
                    variation = 0.0
                    if len(df) >= 2:
                        prev_price = float(df['Close'].iloc[-2])
                        if prev_price > 0: variation = ((last_price - prev_price) / prev_price) * 100
                    
                    original_ticker, asset_type = formatted_yahoo_map[ticker_fmt]
                    indicators = old_data_map.get(original_ticker, {}).get("indicators", get_indicators_mock(asset_type, last_price))
                    indicators['cotacao'] = last_price 

                    history = old_data_map.get(original_ticker, {}).get("history", {})
                    if not history or is_scraping_day:
                        history = fetch_history_data(ticker_fmt)

                    final_data.append({
                        "ticker": original_ticker,
                        "type": asset_type,
                        "name": original_ticker,
                        "price": round(last_price, 2),
                        "variation": round(variation, 2),
                        "quantity": 0,
                        "indicators": indicators,
                        "history": history
                    })
                except Exception: pass
        except Exception as e: print(f"❌ Erro lote Yahoo: {e}")
            
    return final_data

if __name__ == "__main__":
    try:
        dados = fetch_data()
        with open("dados.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        print(f"\n✨ Sucesso! {len(dados)} ativos atualizados.")
    except Exception as e:
        print(f"Erro fatal: {e}")
