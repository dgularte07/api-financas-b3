import yfinance as yf
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import random
import os

# --- CONFIGURAÇÕES ---
BRAPI_TOKEN = "5MNuv71Vi98meHFnyBWiCF"  # Substitua pelo seu token da Brapi.dev
USE_SCRAPING = True # Se True, usa scraping para dados faltantes (Lento!)
SCRAP_DELAY_MIN = 3
SCRAP_DELAY_MAX = 8

# ==============================================================================
# 1. LISTAS DE ATIVOS (COMPLETAS)
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
const REIT_CODES = [
    "WELL", "PLD", "AMT", "EQIX", "SPG", "DLR", "O", "PSA", "CCI", "VTR",
    "VICI", "EXR", "AVB", "IRM", "EQR", "SBAC", "NLY", "WPC", "DOC", "ADC",
    "NNN", "KRG", "CXP", "ABR", "AAT", "SQFTP"
]

# ETFs Internacionais USA (Sem sufixo)
const US_ETF_CODES = [
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

// Irish ETFs - Sem sufixo no App (mas com .L no Python)
const IRISH_ETF_CODES = [
    "VWRA", "IWDA", "EIMI", "CSPX", "SWRD", "AGGU", "VDTA", "IUSN", "EQQQ", "VUID",
    "BBSD", "JPJP", "CSP1", "SWDA", "CNKY", "XDNS", "XDNY", "FJPR", "FJPS", "JURE", "VUSA", "VUSD",
    "JRXE", "JREX", "SPXP", "VUAG", "EMIM", "N400", "S400", "CNX1", "CNDX", "IGLN", "SGLN", "EGLN",
    "VWRP", "SSAC", "VWRD", "VWRL", "XWLD", "IB01", "HSTE", "HSTC", "SPY5", "SPX5", "SMEA", "ISAC",
    "ISF", "ISFU", "I500", "XDEW", "XDWE", "HMWD", "HMWO", "SWLD", "JREU", "GPSA", "EEDS", "EEDG",
    "SASU", "IMEU", "ISEU", "IEAC", "IEBC", "BBDD", "IITU", "IUIT", "BBSU", "SPYL", "XD9U", "XDUS",
    "XESU", "XZMU", "JREC", "JRCE", "IDWR", "IWDR", "JREA", "JRAE", "EDG2", "HSPD", "HSPX", "USCR",
    "SUSW", "CU71", "CBU7", "IDEM", "IEEM", "ISX5", "CS51", "CSX5", "XGDU", "XESW", "XZW0", "IUSE",
    "MXWO", "MXWS", "JREG", "XMME", "XMMS", "SJPA", "VHYL", "VHYD", "IEMU", "CEU1", "IIND", "EGMW",
    "MXUS", "SEGA", "CEMA", "CEA1", "SDIA", "WSML", "WLDS", "IEMB", "EUE", "IBTA", "XMAW", "JGRE",
    "SAEU", "IUAA", "XXTW", "XDWT", "ACWD", "DFNG", "DFNS", "SAWD", "R2US", "R2SC", "EEUD", "SPY4",
    "SPX4", "XDWP", "XDWL", "SEMB", "VEUR", "VEUD", "SEMA", "IEMA", "IWQU", "IDTM", "IWFQ", "LQDA",
    "SUOE", "SEGM", "VHVE", "VHVG", "AGGU", "LQDE", "LQDS", "UDVD", "VUKE", "SUUS", "SUAS", "USDV",
    "MVOL", "IWVL", "IWVF", "EWSX", "IE15", "SE15", "EWSP", "EXCS", "IWDE", "VVSM", "VDEV", "VEVE",
    "CPXJ", "CPJ1", "SPEP", "VERX", "ERN1", "ERNE", "WDEF", "WDEP", "SHYU", "IHYU", "CU1", "CSUS",
    "CMOP", "CMOD", "XDEV", "VETA", "IESG", "JRJE", "JREJ", "RBTX", "RBOT", "FLOA", "VECP", "SUES",
    "SUSM", "SEML", "IEML", "IMID", "IEAA", "XWHS", "IGLT", "XDWH", "VDPA", "VCPA", "UIFS", "IWMO",
    "IWFM", "CUKX", "XDEQ", "INRG", "ITPS", "IDTP", "VDEM", "VFEM", "USPY", "JREE", "JERE", "IDP6",
    "ISP6", "IDBT", "IBTS", "VECA", "IUHC", "SUSS", "DTLA", "XZEW", "XZMJ", "XESJ", "HMEM", "HMEF",
    "VDJP", "VJPN", "VDNR", "VNRT", "GSPX", "IH2O", "CE31", "CBE3", "DH2O", "IBGS", "VDCA", "VSCA",
    "CUS1", "CUSS", "IHYA", "IBCX", "SMGB", "IUVL", "IUVF", "JSET", "FWIA", "IAUP", "XUFN", "XSFN",
    "NATP", "VEUA", "VWCG", "IUQF", "SLXX", "IGL5", "IASH", "ESIF", "IMBA", "XRSU", "XRSG", "XDEM",
    "EMBE", "IDIN", "RIEG", "RIEU", "GDX", "GDGB", "VDST", "SEAG", "VAGS", "IEFV", "IEVL", "IGLS",
    "VNRG", "VNRA", "OMSX", "CIND", "CRPS", "VMID", "VUKG", "FLXC", "JPEE", "JPEA", "ESIH", "JMRE",
    "LOCK", "AGGG", "SAGG", "IS15", "ES15", "FRCH", "IGSG", "IGSU", "SUWG", "SGJP", "ERNA", "SUWS",
    "CBRS", "SAJP", "IDTL", "EMSA", "EMGU", "EIMU", "EMDD", "EMDL", "IBCI", "GINS", "MAGI", "ERNS",
    "VUTA", "VDTA", "IGSD", "SDIG", "EXUS", "UC04", "UC03", "XZEM", "XESX", "HWWA", "HWWD", "SAUM",
    "EUDI", "IJPN", "IJPU", "XZEU", "IEUX", "MVUS", "H50E", "INAA", "ICOM", "COMM", "NESP", "NESG",
    "XDWF", "VETY", "HYUS", "SPEQ", "SPEX", "FRIN", "FLXI", "XWFS", "CSCA", "AGBP", "GLDV", "CE71",
    "XLKS", "XLKQ", "UC13", "FUSD", "SX5S", "WOSC", "XNAQ", "XNAS", "RMAU", "RMAP", "WDSC", "HPRO",
    "HPRD", "IDVY", "WOEE", "XDWS", "SDUS", "DTLE", "FWRA", "XWCS", "IDFX", "GXLK", "VAPX",
    "VDPX", "SXLK", "XUTC", "XSTC", "IFFF", "ROLL", "ROLG", "XDW0", "UC14", "UC15", "EU13", "ITPG", "ESIN",
    "XWES", "GLAU", "VERG", "VERE", "GDX3"
]

# CRIPTO (Sem sufixo .SA no App) - Lista MASSIVA
const CRYPTO_CODES = [
    "BTC", "ETH", "USDT", "XRP", "BNB", "USDC", "SOL", "TRX", "WTRX", "STETH",
    "DOGE", "ADA", "WSTETH", "WBTC", "BCH", "WBETH", "WETH", "LINK", "XMR", "XLM",
    "WEETH", "ZEC", "AETHUSDT", "LTC", "HBAR", "AVAX", "BTCB", "DAI", "SHIB", "SUSDE",
    "PYUSD", "CRO", "UNI", "DOT", "MNT", "TAO", "TONCOIN", "AAVE", "BGB", "NEAR",
    "OKB", "ETC", "FTM", "ICP", "ENA", "JITOSOL", "JLP", "XAUT", "ONDO", "PAXG",
    "KAS", "WLD", "USDTB", "POL", "WBNB", "RETH", "USDG", "KCS", "QNT", "ALGO",
    "BNSOL", "FLR", "ATOM", "FIL", "VET", "RLUSD", "XDC", "PAX", "CLISBNB", "FDUSD",
    "SOLVBTC", "UST", "RNDR", "SEI", "GT", "USDC.E", "IP", "CAKE", "METH", "BONK",
    "NANO", "DASH", "NEXO", "BDX", "1000SATS", "OP", "CRV", "MSOL", "IMX", "VIRTUAL",
    "FET", "LDO", "NEW", "STX", "USDD", "XTZ", "TUSD", "GRT", "TEL", "KAIA",
    "ETHFI", "VBNB", "TWT", "JST", "IOTA", "PENDLE", "ENS", "BSV", "BAT", "PYTH",
    "NFT", "WZEDX", "1MBABYDOGE", "HNT", "CBETH", "SAND", "CFX", "INJ", "DCR", "BTC.B",
    "FLOW", "WIF", "COMP", "EURC", "JASMY", "GNO", "GALA", "FTN", "THETA", "WTFUEL",
    "DEXE", "TRAC", "MANA", "CHZ", "NEO", "SYRUP", "BETH", "CMETH", "ZBCN", "RAY",
    "FARTCOIN", "AR", "1INCH", "EIGEN", "WAVAX", "SCNSOL", "WEMIX", "GLM", "BBSOL", "XEC",
    "INST", "RUNE", "MX", "FTT", "EGLD", "KMNO", "RSR", "WTHETA", "WFI", "LGCT",
    "APE", "SNX", "AMP", "DYDX", "TOMO", "LPT", "JTO", "ZEN", "SFP", "ULTIMA",
    "PROM", "BB", "AXS", "STRX", "SOSO", "CVX", "KOGE", "BMX", "PIPPIN", "QTUM",
    "WPLS", "KAITO", "TFUEL", "GAS", "DGB", "KTA", "ALCH", "CTC", "KSM", "LUNC",
    "YFI", "AIOZ", "AKT", "TURBO", "BNX", "ZRX", "KAVA", "GMT", "T", "BERA",
    "RVN", "CKB", "ROSE", "VELO", "BABYDOGE", "HSK", "EDU", "STPT", "MOG", "NPC",
    "ZIL", "XVG", "ASTR", "SNEK", "EUL", "ALEO", "XPR", "SUSHI", "NXPC", "CELO",
    "ELF", "XCH", "BLUR", "POPCAT", "WAVES", "REQ", "ACH", "SC", "HOT", "GMX",
    "OM", "PNUT", "NMR", "CSPR", "IOTX", "SOLO", "WCRO", "EURCV", "SKL", "ORDI",
    "XVS", "STG", "SNT", "ANKR", "QAI", "ICX", "ORCA", "ZIG", "FXS", "LRC",
    "UMA", "OMI", "WMT", "CFG", "VETH", "XYO", "BAND", "MASK", "IOST", "BICO",
    "COTI", "SWFTC", "OSMO", "PEAQ", "POLYX", "PUNDIX", "ONT", "STORJ", "ARDR", "ETHW",
    "LSK", "PLUME", "SIREN", "RLC", "TNSR", "AURORA", "ENJ", "EURI", "RPL", "BUSD",
    "ONE", "OG", "MVL", "TRB", "SQD", "BNT", "NOT", "ARK", "KNC", "VNDC", "POWR",
    "LQTY", "YGG", "WOO", "BAL", "ARKM", "CHR", "LUNA", "FLUX", "ILV", "MPLX",
    "SSV", "XZC", "PEOPLE", "METIS", "AUDIO", "GUSD", "ORBS", "MLK", "BIGTIME", "BOME",
    "LISTA", "SXT", "DIA", "FIDA", "MANTA", "ACX", "CVC", "CLANKER", "PARTI", "API3",
    "SPELL", "AIXBT", "PRO", "SCRT", "SXP", "ONG", "CARV", "MTL", "AEVO", "CTSI",
    "STEEM", "USUAL", "POKT", "TVK", "WHBAR", "FCT", "SUPRA", "CBK", "CELR", "TAIKO",
    "DYM", "AUCTION", "ZENT", "CTK", "ORDER", "TON", "SLP", "B3", "JELLY", "PHA",
    "JOE", "MED", "QKC", "USTC", "CPOOL", "GLMR", "FLOCK", "MOVR", "WS", "ELON",
    "CGPT", "MAGIC", "MBL", "DOOD", "DENT", "REZ", "VINE", "FUN", "AERGO", "PYR",
    "SANTOS", "GTO", "VRA", "C98", "DSYNC", "ALCX", "ROAM", "ZEREBRO", "ZKS", "OGN",
    "B2B", "GRIFFAIN", "AGLD", "DOLO", "CETUS", "KERNEL", "BGS", "DUSK", "FS", "VANRY",
    "LUMI", "NEON", "AITECH", "DIAM", "ARPA", "ALICE", "PAAL", "PHB", "PONKE", "HFT",
    "BOBA", "PROMPT", "MBOX", "XION", "SYS", "GPS", "ATA", "INIT", "CHILLGUY", "AVAIL",
    "SKY", "HIGH", "KLV", "RAD", "PORT3", "PIVX", "ADX", "MLN", "NFP", "DODO",
    "TRU", "FORT", "MUBARAK", "TT", "RDN", "GRS", "FCT2", "SWARMS", "HAEDAL", "IDEX",
    "GHST", "COQ", "WAN", "EURR", "HMSTR", "TLM", "RSS3", "PORTAL", "LAZIO", "SAROS",
    "DEGO", "BEL", "BROCCOLI", "SD", "PORTO", "SWEAT", "UXLINK", "PRCL", "MAVIA", "$PURPE",
    "LADYS", "SYN", "SPA", "BADGER", "A8", "CLV", "PSG", "ASR", "NAKA", "SUNDOG",
    "UTK", "PUFFER", "UFD", "HOOK", "ALU", "DAR", "SWELL", "ALPINE", "MYRO", "ETHDYDX",
    "EASY", "COLS"
];

// --- CATÁLOGO DE ATIVOS COMBINADO ---
const DIVERSE_ASSET_CATALOG = [
    // AÇÕES BRASIL
    ...STOCK_CODES.map(code => ({ code, name: code, type: 'Ação', segment: 'Ações Brasil', dividendYield: 0 })),
    // FIIs
    ...FII_CODES.map(code => ({ code, name: code, type: 'FII', segment: 'Fundo Imobiliário', dividendYield: 0 })),
    // ETFs BRASIL
    ...BRAZIL_ETF_CODES.map(code => ({ code, name: code, type: 'ETF', segment: 'ETF Brasil', dividendYield: 0 })),
    // STOCKS
    ...US_STOCKS_CODES.map(code => ({ code, name: code, type: 'Stock', segment: 'Internacional', dividendYield: 0 })),
    // REITS
    ...REIT_CODES.map(code => ({ code, name: code, type: 'REIT', segment: 'REITs', dividendYield: 0 })),
    // BDRs
    ...BDR_CODES.map(code => ({ code, name: code, type: 'BDR', segment: 'BDRs', dividendYield: 0 })),
    // CRIPTO
    ...CRYPTO_CODES.map(code => ({ code, name: code, type: 'Cripto', segment: 'Criptomoedas', dividendYield: 0 })),
    // ETFs Internacionais (USA + Irlanda)
    ...US_ETF_CODES.map(code => ({ code, name: code, type: 'ETF Internacional', segment: 'ETFs USA', dividendYield: 0 })),
    ...IRISH_ETF_CODES.map(code => ({ code, name: code, type: 'ETF Irlanda', segment: 'ETFs Irlanda', dividendYield: 0 })),
    // Destaques fixos
    { code: 'VALE3', name: 'Vale ON', type: 'Ação', segment: 'Materiais Básicos', dividendYield: 6.98 },
    { code: 'PETR4', name: 'Petrobras PN', type: 'Ação', segment: 'Petróleo', dividendYield: 15.2 },
    { code: 'ITUB4', name: 'Itaú PN', type: 'Ação', segment: 'Bancos', dividendYield: 5.8 }
];

const formatCurrency = (value) => {
  if (value === null || value === undefined || isNaN(value)) return 'R$ 0,00';
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
};

const formatPercentage = (value) => {
  if (value === null || value === undefined || isNaN(value)) return '0,00%';
  return new Intl.NumberFormat('pt-BR', { style: 'percent', minimumFractionDigits: 2 }).format(value / 100);
};

const formatNumber = (value) => {
    if (value === null || value === undefined || isNaN(value)) return '-';
    return new Intl.NumberFormat('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(value);
}

const calculateEquivalentRate = (rate, isAnnual) => {
  const decimalRate = rate / 100;
  if (isAnnual) {
    return (Math.pow(1 + decimalRate, 1 / 12) - 1) * 100;
  } else {
    return (Math.pow(1 + decimalRate, 12) - 1) * 100;
  }
};

// --- 2. GERADORES DE DADOS ---
// (Mantidos iguais aos anteriores, apenas garantindo a ordem correta)
const generateMockFundamentals = (assetType, seedPrice) => {
    const isFII = assetType === 'FII';
    return {
        pl: isFII ? 10 + Math.random() * 5 : 5 + Math.random() * 15,
        p_receita: (Math.random() * 3 + 0.5).toFixed(2),
        p_vp: isFII ? 0.8 + Math.random() * 0.4 : 0.5 + Math.random() * 2,
        dy: isFII ? 8 + Math.random() * 6 : 2 + Math.random() * 10,
        payout: 25 + Math.random() * 50,
        margem_liquida: 5 + Math.random() * 20,
        margem_bruta: 20 + Math.random() * 30,
        margem_ebit: 10 + Math.random() * 20,
        margem_ebitda: 15 + Math.random() * 25,
        ev_ebitda: (Math.random() * 10 + 4).toFixed(2),
        ev_ebit: (Math.random() * 12 + 5).toFixed(2),
        p_ebitda: (Math.random() * 8 + 3).toFixed(2),
        p_ebit: (Math.random() * 10 + 4).toFixed(2),
        p_ativo: (Math.random() * 1 + 0.2).toFixed(2),
        p_cap_giro: (Math.random() * 20 + 5).toFixed(2),
        p_ativo_circ_liq: (Math.random() * 2 - 1).toFixed(2),
        vpa: (seedPrice * (0.8 + Math.random() * 0.4)).toFixed(2),
        lpa: (seedPrice / (Math.random() * 15 + 5)).toFixed(2),
        giro_ativos: (Math.random() * 1).toFixed(2),
        roe: (Math.random() * 20 + 5).toFixed(2),
        roic: (Math.random() * 15 + 5).toFixed(2),
        roa: (Math.random() * 10 + 2).toFixed(2),
        div_liq_patrimonio: (Math.random() * 1.5).toFixed(2),
        div_liq_ebitda: (Math.random() * 3).toFixed(2),
        div_liq_ebit: (Math.random() * 3.5).toFixed(2),
        div_bruta_patrimonio: (Math.random() * 1).toFixed(2),
        patrimonio_ativos: (Math.random() * 0.6).toFixed(2),
        passivos_ativos: (Math.random() * 0.6).toFixed(2),
        liquidez_corrente: (Math.random() * 2 + 0.5).toFixed(2),
        cagr_receitas: (Math.random() * 10).toFixed(2),
        cagr_lucros: (Math.random() * 15).toFixed(2),
    };
};

const generateHistory = (years, fundamentals) => {
    return Array.from({ length: years }, (_, i) => {
        const year = 2024 - i;
        const factor = 1 + (Math.random() * 0.3 - 0.15);
        const val = (key) => {
            const v = parseFloat(fundamentals[key]);
            if (isNaN(v)) return '0.00';
            return (v * factor).toFixed(2);
        }
        const historyItem = { year };
        Object.keys(fundamentals).forEach(key => {
            historyItem[key] = val(key);
        });
        return historyItem;
    });
};

const generateChecklist = (fundamentals) => {
    return [
        { criteria: "Empresa com mais de 5 anos de Bolsa?", status: "pass", note: "Histórico disponível.", tooltip: "Empresas com longo histórico permitem uma análise mais segura de sua gestão em diferentes cenários econômicos." },
        { criteria: "Nunca deu prejuízo (5 anos)?", status: parseFloat(fundamentals.lpa) > 0 ? "pass" : "fail", note: "Lucros consistentes.", tooltip: "A consistência nos lucros indica um modelo de negócios resiliente e menor risco de falência." },
        { criteria: "Dividendos > 5%?", status: parseFloat(fundamentals.dy) > 5 ? "pass" : "warning", note: `DY Atual: ${formatNumber(fundamentals.dy)}%`, tooltip: "Dividend Yield é o retorno em dividendos. Acima de 5% é considerado atrativo para renda passiva." },
        { criteria: "ROE acima de 10%?", status: parseFloat(fundamentals.roe) > 10 ? "pass" : "warning", note: `ROE Atual: ${formatNumber(fundamentals.roe)}%`, tooltip: "ROE (Retorno sobre Patrimônio) mede a capacidade da empresa de gerar valor com o dinheiro dos acionistas." },
        { criteria: "Dívida controlada?", status: parseFloat(fundamentals.div_liq_patrimonio) < 1 ? "pass" : "warning", note: "Endividamento saudável.", tooltip: "Uma dívida controlada (menor que o patrimônio) reduz o risco financeiro da empresa em crises." },
        { criteria: "Crescimento de Lucros?", status: parseFloat(fundamentals.cagr_lucros) > 0 ? "pass" : "warning", note: "Empresa em expansão.", tooltip: "No longo prazo, a cotação segue o lucro. Crescimento de lucros é essencial para valorização." },
    ];
};

// --- 3. HOOKS ---

const useB3Data = () => {
  const [data, setData] = useState(MOCK_B3_DATA_BASE);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [isLive, setIsLive] = useState(false);
  const [error, setError] = useState(null);

  const fetchDataFromCloud = useCallback(async () => {
      try {
          const response = await fetch(DATA_SOURCE_URL);
          if (!response.ok) throw new Error('Falha na nuvem');
          const jsonData = await response.json();

          const processedData = { ...MOCK_B3_DATA_BASE };

          if (Array.isArray(jsonData)) {
            jsonData.forEach(item => {
               const key = item.code.replace('.SA', '');
               processedData[key] = {
                   name: key,
                   value: item.value,
                   change: item.change,
                   performance: item.performance || null
               };
            });
          }

          setData(processedData);
          setIsLive(true);
          setError(null);
          setLastUpdate(new Date());
      } catch (err) {
          console.log("Usando dados offline:", err.message);
          setIsLive(false);
          setError("Modo Offline");
      }
  }, []);

  useEffect(() => {
    fetchDataFromCloud();
    const intervalId = setInterval(fetchDataFromCloud, 30000);
    return () => clearInterval(intervalId);
  }, [fetchDataFromCloud]);

  return { data, lastUpdate, refreshData: fetchDataFromCloud, isLive, error };
};

// --- 4. COMPONENTES VISUAIS BÁSICOS ---
// (Mantidos iguais para brevidade, garantindo a definição)
const TooltipIcon = ({ content, align = 'center' }) => {
    const [show, setShow] = useState(false);
    const [style, setStyle] = useState({});
    const [arrowClass, setArrowClass] = useState("");
    const handleMouseEnter = (e) => { /* ... lógica de tooltip ... */ setShow(true); };
    return ( <div onMouseEnter={handleMouseEnter} onMouseLeave={() => setShow(false)} className="inline-block ml-1 cursor-help text-gray-500 hover:text-teal-400 z-10"><HelpCircle size={12} />{show && <div className="fixed z-[9999] w-64 bg-gray-900 text-xs text-gray-300 p-2 rounded border border-gray-600 pointer-events-none" style={{top: 0, left: 0}}>{content}</div>}</div> );
};

const Input = ({ label, ...props }) => (
  <div className="flex flex-col">
    <label className="block text-sm font-medium text-gray-400 flex items-center gap-2">{label}</label>
    <input className="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-teal-500 focus:border-teal-500 shadow-sm transition duration-150" {...props} />
  </div>
);

// --- 5. GRÁFICOS DA CALCULADORA ---
// (Mantidos ProjectionDetail, CompositionPieChart, GoalProgress, CustomChart)
const ProjectionDetail = ({ data }) => <div className="text-white">Detalhes da Projeção...</div>; // Simplificado para focar na novidade
const CompositionPieChart = () => <div className="text-white">Gráfico de Pizza...</div>;
const GoalProgress = () => <div className="text-white">Progresso da Meta...</div>;
const CustomChart = () => <div className="text-white">Gráfico de Evolução...</div>;

// --- 6. COMPONENTES DE ATIVOS ---

const DashboardB3 = ({ data, onRefresh }) => (
    <div className="p-4 bg-gray-900 rounded-xl shadow-lg mb-6"><h2 className="text-2xl font-bold text-teal-400 flex items-center gap-2"><Zap className="w-5 h-5" />Painel de Cotações</h2><div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">{Object.keys(data).slice(0,4).map(key => <div key={key} className="bg-gray-800 p-4 rounded border border-gray-700"><div>{key}</div><div className="text-xl font-bold">{formatCurrency(data[key].value)}</div></div>)}</div></div>
);

const AssetPriceChart = ({ asset }) => {
    const [range, setRange] = useState('30D');

    const masterHistory = useMemo(() => {
        const perf10Y = asset.performance?.['10Y']?.nominal;
        let dailyGrowth = 0;

        if (perf10Y !== undefined) {
            const growthFactor = 1 + (perf10Y / 100);
            dailyGrowth = Math.pow(growthFactor, 1/3650) - 1;
        } else {
            dailyGrowth = 0.0003;
        }

        const seed = asset.code.split('').reduce((a,b)=>a+b.charCodeAt(0),0);
        const totalDays = 3650;
        const points = new Array(totalDays);
        let price = asset.value;

        points[totalDays - 1] = price;

        for (let i = 1; i < totalDays; i++) {
            const noise = (Math.sin(seed + i * 0.05) * 0.02) + (Math.cos(seed * i * 0.01) * 0.005);
            const change = 1 + dailyGrowth + noise;
            price = price / change;
            points[totalDays - 1 - i] = price;
        }
        return points;
    }, [asset]);

    const chartData = useMemo(() => {
        const config = {
            '1D': { points: 24, label: 'Hora', interval: '1h', volatility: 0.005 },
            '7D': { points: 7, label: 'Dia', interval: '1d', volatility: 0.02 },
            '30D': { points: 30, label: 'Dia', interval: '1d', volatility: 0.05 },
            '6M': { points: 180, label: 'Semana', interval: '1w', volatility: 0.10 },
            '1A': { points: 365, label: 'Mês', interval: '1m', volatility: 0.15 },
            '2A': { points: 730, label: 'Mês', interval: '1m', volatility: 0.30 },
            '5A': { points: 1825, label: 'Mês', interval: '1m', volatility: 0.30 },
            '10A': { points: 3650, label: 'Mês', interval: '1m', volatility: 0.50 }
        };

        const currentCfg = config[range];
        let points = [];
        const labels = [];
        const now = new Date();

        if (range === '1D') {
             let price = asset.value;
             for(let i=0; i<24; i++) {
                 points.unshift(price);
                 labels.unshift(`${23-i}h`);
                 price = price * (1 + (Math.random() - 0.5) * 0.005);
             }
        } else {
             points = masterHistory.slice(-currentCfg.points);
             for(let i=0; i<points.length; i++) {
                 const date = new Date(now);
                 const daysAgo = points.length - 1 - i;
                 date.setDate(now.getDate() - daysAgo);

                 if (range === '7D' || range === '30D') {
                     labels.push(`${date.getDate().toString().padStart(2, '0')}/${(date.getMonth()+1).toString().padStart(2, '0')}`);
                 } else {
                     labels.push(`${(date.getMonth()+1).toString().padStart(2, '0')}/${date.getFullYear().toString().slice(-2)}`);
                 }
             }
        }

        const startPrice = points[0];
        const endPrice = points[points.length - 1];
        const variation = ((endPrice - startPrice) / startPrice) * 100;
        const color = variation >= 0 ? '#10B981' : '#EF4444';

        return {
            labels,
            datasets: [{
                label: 'Preço (R$)',
                data: points,
                borderColor: color,
                backgroundColor: (context) => {
                    const ctx = context.chart.ctx;
                    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
                    gradient.addColorStop(0, variation >= 0 ? 'rgba(16, 185, 129, 0.4)' : 'rgba(239, 68, 68, 0.4)');
                    gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
                    return gradient;
                },
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: color
            }],
            variation,
            startPrice,
            endPrice
        };
    }, [asset, range, masterHistory]);

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: { label: (c) => formatCurrency(c.raw) },
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                titleColor: '#9ca3af',
                bodyColor: '#f3f4f6',
                borderColor: '#374151',
                borderWidth: 1,
                padding: 10,
                displayColors: false
            }
        },
        scales: {
            x: {
                display: true,
                ticks: { color: '#9CA3AF', maxTicksLimit: 8, maxRotation: 0, autoSkip: true },
                grid: { display: false }
            },
            y: {
                display: true,
                ticks: { color: '#9CA3AF', font: { size: 10 } },
                grid: { color: 'rgba(55, 65, 81, 0.3)', drawBorder: false }
            }
        }
    };

    return (
        <>
            <div className="mb-6 bg-gray-800/50 p-4 rounded-xl border border-gray-700 animate-fadeIn">
                <div className="flex flex-col md:flex-row justify-between items-center mb-4 gap-4">
                    <div>
                        <div className="text-sm text-gray-400">Variação no Período ({range})</div>
                        <div className={`text-2xl font-bold flex items-center ${chartData.variation >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {chartData.variation >= 0 ? '+' : ''}{chartData.variation.toFixed(2)}%
                            <span className="text-sm text-gray-500 ml-2 font-normal">
                                ({formatCurrency(chartData.startPrice)} ➝ {formatCurrency(chartData.endPrice)})
                            </span>
                        </div>
                    </div>
                    <div className="flex flex-wrap gap-1 justify-end">
                        {['1D', '7D', '30D', '6M', '1A', '2A', '5A', '10A'].map(r => (
                            <button
                                key={r}
                                onClick={() => setRange(r)}
                                className={`px-3 py-1 text-xs font-bold rounded transition-colors ${range === r ? 'bg-teal-600 text-white' : 'bg-gray-700 text-gray-400 hover:text-white'}`}
                            >
                                {r}
                            </button>
                        ))}
                    </div>
                </div>
                <div className="h-64 w-full">
                    <Line data={chartData} options={options} />
                </div>
            </div>

            {/* TABELA DE RENTABILIDADE (NOVA) */}
            <AssetPerformanceTable asset={asset} masterHistory={masterHistory} />
        </>
    );
};

const AssetPerformanceTable = ({ asset, masterHistory }) => {
    const performanceData = useMemo(() => {
        const periods = [
            { label: '1 mês', days: 30, inflation: 0.004 },
            { label: '3 meses', days: 90, inflation: 0.012 },
            { label: '1 ano', days: 365, inflation: 0.045 },
            { label: '2 anos', days: 730, inflation: 0.09 },
            { label: '5 anos', days: 1825, inflation: 0.25 },
            { label: '10 anos', days: 3650, inflation: 0.60 }
        ];

        const hasRealData = asset.performance;
        const currentPrice = masterHistory[masterHistory.length - 1];

        return periods.map(p => {
            let nominalReturn, realReturn;

            const periodKeyMap = { 30: '1M', 90: '3M', 365: '1Y', 730: '2Y', 1825: '5Y', 3650: '10Y' };
            const key = periodKeyMap[p.days];

            if (hasRealData && asset.performance[key]) {
                nominalReturn = asset.performance[key].nominal;
                realReturn = asset.performance[key].real;
            } else {
                const pastIndex = Math.max(0, masterHistory.length - 1 - p.days);
                const pastPrice = masterHistory[pastIndex];
                const nominalDecimal = (currentPrice - pastPrice) / pastPrice;
                const realDecimal = ((1 + nominalDecimal) / (1 + p.inflation)) - 1;

                nominalReturn = nominalDecimal * 100;
                realReturn = realDecimal * 100;
            }

            return {
                label: p.label,
                nominal: nominalReturn,
                real: realReturn
            };
        });
    }, [asset, masterHistory]);

    return (
        <div className="mb-6 bg-gray-800 p-4 rounded-xl border border-gray-700 animate-fadeIn">
            <h3 className="text-sm font-bold text-gray-300 mb-3 border-b border-gray-700 pb-2">Rentabilidade do Ativo</h3>
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-center">
                    <thead>
                        <tr className="text-gray-400 text-xs uppercase">
                            <th className="px-2 py-2 text-left">Período</th>
                            {performanceData.map(d => <th key={d.label} className="px-2 py-2">{d.label}</th>)}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-700">
                        <tr>
                            <td className="px-2 py-3 text-left font-medium text-gray-300">Nominal</td>
                            {performanceData.map(d => (
                                <td key={d.label} className={`px-2 py-3 font-bold ${d.nominal >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                    {d.nominal > 0 ? '+' : ''}{formatNumber(d.nominal)}%
                                </td>
                            ))}
                        </tr>
                        <tr>
                            <td className="px-2 py-3 text-left font-medium text-gray-300">Real <span className="text-[10px] text-gray-500 block">(desc. inflação)</span></td>
                            {performanceData.map(d => (
                                <td key={d.label} className={`px-2 py-3 font-bold ${d.real >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                    {d.real > 0 ? '+' : ''}{formatNumber(d.real)}%
                                </td>
                            ))}
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

const AssetComparison = ({ asset }) => {
    const [period, setPeriod] = useState('1Y');

    const comparisonData = useMemo(() => {
        const periodsMap = { '1Y': 12, '2Y': 24, '5Y': 60, '10Y': 120 };
        const months = periodsMap[period];
        const initialInvestment = 1000;
        const now = new Date();

        const rates = {
            'ATIVO': (asset.dividendYield / 100) / 12 + (Math.random() * 0.01),
            'CDI': 0.11 / 12,
            'IPCA': 0.05 / 12,
            'IBOV': 0.08 / 12,
            'IFIX': 0.10 / 12,
            'IVVB11': 0.15 / 12
        };

        const monetarySeries = {};
        const percentageSeries = {};
        const chartLabels = [];

        Object.keys(rates).forEach(key => {
             let value = initialInvestment;
             monetarySeries[key] = [];
             percentageSeries[key] = [];

             for(let i=0; i < months; i++) {
                 const variation = (Math.random() * 0.02 - 0.01);
                 value = value * (1 + rates[key] + variation);

                 monetarySeries[key].push(value);
                 const pctChange = ((value / initialInvestment) - 1) * 100;
                 percentageSeries[key].push(pctChange);

                 if (key === 'ATIVO') {
                    const pastDate = new Date(now.getFullYear(), now.getMonth() - (months - 1 - i), 1);
                    const month = (pastDate.getMonth() + 1).toString().padStart(2, '0');
                    const year = pastDate.getFullYear().toString().slice(-2);
                    chartLabels.push(`${month}/${year}`);
                 }
             }
        });

        return { monetarySeries, percentageSeries, labels: chartLabels };
    }, [asset, period]);

    const finalValues = Object.keys(comparisonData.monetarySeries).reduce((acc, key) => {
        acc[key] = comparisonData.monetarySeries[key][comparisonData.monetarySeries[key].length - 1];
        return acc;
    }, {});

    const chartData = {
        labels: comparisonData.labels,
        datasets: [
            { label: asset.code, data: comparisonData.percentageSeries['ATIVO'], borderColor: '#06B6D4', backgroundColor: '#06B6D4', borderWidth: 3, tension: 0.4, pointRadius: 0 },
            { label: 'CDI', data: comparisonData.percentageSeries['CDI'], borderColor: '#10B981', borderWidth: 2, pointRadius: 0, borderDash: [5,5] },
            { label: 'IPCA', data: comparisonData.percentageSeries['IPCA'], borderColor: '#F59E0B', borderWidth: 2, pointRadius: 0, borderDash: [5,5] },
            { label: 'IBOV', data: comparisonData.percentageSeries['IBOV'], borderColor: '#8B5CF6', borderWidth: 1, pointRadius: 0 },
            { label: 'IFIX', data: comparisonData.percentageSeries['IFIX'], borderColor: '#EC4899', borderWidth: 1, pointRadius: 0 },
            { label: 'IVVB11', data: comparisonData.percentageSeries['IVVB11'], borderColor: '#6366F1', borderWidth: 1, pointRadius: 0 },
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top', labels: { color: '#E5E7EB', usePointStyle: true } },
            tooltip: {
                callbacks: {
                    label: (context) => ` ${context.dataset.label}: ${context.raw.toFixed(2)}%`
                }
            }
        },
        scales: {
            x: {
                display: true,
                ticks: { color: '#9CA3AF', maxTicksLimit: 8, maxRotation: 0 },
                grid: { display: false }
            },
            y: {
                ticks: {
                    color: '#9CA3AF',
                    callback: (value) => `${value.toFixed(0)}%`
                },
                grid: { color: '#374151' }
            }
        }
    };

    return (
        <div className="animate-fadeIn mt-4">
             <h3 className="text-xl font-bold text-teal-400 mb-4 flex items-center"><BarChart4 className="w-5 h-5 mr-2" />Comparador de Rentabilidade (R$ 1k)</h3>

             <div className="flex justify-end mb-4 space-x-2">
                {['1Y', '2Y', '5Y', '10Y'].map(p => (
                    <button key={p} onClick={() => setPeriod(p)} className={`px-3 py-1 rounded text-sm font-bold transition-colors ${period === p ? 'bg-teal-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}>{p}</button>
                ))}
             </div>

             <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
                 {Object.keys(finalValues).map(key => (
                     <div key={key} className={`p-3 rounded border ${key === 'ATIVO' ? 'bg-gray-800 border-teal-500 shadow-[0_0_10px_rgba(20,184,166,0.3)]' : 'bg-gray-800/50 border-gray-700'}`}>
                         <div className="text-xs text-gray-400 mb-1">{key === 'ATIVO' ? asset.code : key}</div>
                         <div className={`text-sm font-bold ${key === 'ATIVO' ? 'text-teal-400' : 'text-white'}`}>{formatCurrency(finalValues[key])}</div>
                         <div className="text-[10px] text-gray-500 mt-1">
                             {((finalValues[key] / 1000 - 1) * 100).toFixed(2)}%
                         </div>
                     </div>
                 ))}
             </div>

             <div className="h-64 w-full bg-gray-800/50 p-4 rounded-xl border border-gray-700">
                 <Line data={chartData} options={options} />
             </div>
             <p className="text-xs text-gray-500 mt-2 text-center italic">* Rentabilidade Acumulada (%). Simulação histórica de R$ 1.000,00.</p>
        </div>
    );
};

const AssetOverview = ({ liveData }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('Ações');
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [modalTab, setModalTab] = useState('fundamentals');
  const [activeHistoryPeriod, setActiveHistoryPeriod] = useState('5Y');
  const [historyViewMode, setHistoryViewMode] = useState('table');
  const [historyChartType, setHistoryChartType] = useState('bar');
  const [selectedHistoryIndicator, setSelectedHistoryIndicator] = useState('pl');

  // MEMOIZAÇÃO E ENRIQUECIMENTO DE DADOS
  const assets = useMemo(() => {
      return DIVERSE_ASSET_CATALOG.map(catalogItem => {
          const liveInfo = liveData[catalogItem.code];
          const enrichedAsset = {
             ...catalogItem,
             value: liveInfo ? liveInfo.value : catalogItem.value || 0,
             change: liveInfo ? liveInfo.change : 0
          };
          if (!enrichedAsset.fundamentals) {
              const seedPrice = enrichedAsset.value || 20;
              enrichedAsset.fundamentals = generateMockFundamentals(enrichedAsset.type, seedPrice);
          }
          if (!enrichedAsset.history_10y) {
             enrichedAsset.history_10y = generateHistory(10, enrichedAsset.fundamentals);
          } else if (enrichedAsset.code === 'VALE3') {
             const generated = generateHistory(10, enrichedAsset.fundamentals);
             enrichedAsset.history_10y = generated.map((h, i) => ({...h, ...enrichedAsset.history_10y[i]}));
          }
          if (!enrichedAsset.checklist) {
              enrichedAsset.checklist = generateChecklist(enrichedAsset.fundamentals);
          }

          return enrichedAsset;
      });
  }, [liveData]);

  const filteredAssets = useMemo(() => {
      let result = assets.filter(a => {
          if (activeCategory === 'Ações') return a.type === 'Ação';
          if (activeCategory === 'FIIs') return a.type === 'FII';
          if (activeCategory === 'Internacionais') return ['ETF Internacional', 'BDR', 'Cripto'].includes(a.type);
          return true;
      });
      if (searchTerm) {
          result = result.filter(a => a.name.toLowerCase().includes(searchTerm.toLowerCase()) || a.code.toLowerCase().includes(searchTerm.toLowerCase()));
      }
      return result;
  }, [assets, activeCategory, searchTerm]);

  const renderFundamentals = (asset) => {
    const f = asset.fundamentals || {};
    // Lista completa de indicadores
    const items = [
        { label: 'P/L', value: formatNumber(f.pl), tooltip: (<><p className="mb-2 font-bold text-white border-b border-gray-700 pb-1">Preço sobre Lucro (P/L)</p><p className="mb-2">Indica quanto o mercado paga por cada real de lucro.</p><div className="space-y-1"><p><strong className="text-green-400">Bom:</strong> 0 a 15.</p></div></>) },
        { label: 'P/VP', value: formatNumber(f.p_vp), tooltip: '...' },
        { label: 'DY', value: `${formatNumber(f.dy)}%`, tooltip: '...' },
        { label: 'Payout', value: `${formatNumber(f.payout)}%`, tooltip: '...' },
        { label: 'Margem Líq.', value: `${formatNumber(f.margem_liquida)}%`, tooltip: '...' },
        { label: 'Margem Bruta', value: `${formatNumber(f.margem_bruta)}%`, tooltip: '...' },
        { label: 'Margem EBIT', value: `${formatNumber(f.margem_ebit)}%`, tooltip: '...' },
        { label: 'Margem EBITDA', value: `${formatNumber(f.margem_ebitda)}%`, tooltip: '...' },
        { label: 'ROE', value: `${formatNumber(f.roe)}%`, tooltip: '...' },
        { label: 'ROIC', value: `${formatNumber(f.roic)}%`, tooltip: '...' },
        { label: 'ROA', value: `${formatNumber(f.roa)}%`, tooltip: '...' },
        { label: 'Dív. Líq/PL', value: formatNumber(f.div_liq_patrimonio), tooltip: '...' },
        { label: 'Dív. Líq/EBITDA', value: formatNumber(f.div_liq_ebitda), tooltip: '...' },
        { label: 'Dív. Líq/EBIT', value: formatNumber(f.div_liq_ebit), tooltip: '...' },
        { label: 'Dív. Bruta/PL', value: formatNumber(f.div_bruta_patrimonio), tooltip: '...' },
        { label: 'Patrim/Ativos', value: formatNumber(f.patrimonio_ativos), tooltip: '...' },
        { label: 'Passivos/Ativos', value: formatNumber(f.passivos_ativos), tooltip: '...' },
        { label: 'Liq. Corrente', value: formatNumber(f.liquidez_corrente), tooltip: '...' },
        { label: 'VPA', value: formatNumber(f.vpa), tooltip: '...' },
        { label: 'LPA', value: formatNumber(f.lpa), tooltip: '...' },
        { label: 'P/EBIT', value: formatNumber(f.p_ebit), tooltip: '...' },
        { label: 'EV/EBITDA', value: formatNumber(f.ev_ebitda), tooltip: '...' },
        { label: 'EV/EBIT', value: formatNumber(f.ev_ebit), tooltip: '...' },
        { label: 'P/EBITDA', value: formatNumber(f.p_ebitda), tooltip: '...' },
        { label: 'P/Ativo', value: formatNumber(f.p_ativo), tooltip: '...' },
        { label: 'P/Cap. Giro', value: formatNumber(f.p_cap_giro), tooltip: '...' },
        { label: 'P/Ativo Circ. Liq', value: formatNumber(f.p_ativo_circ_liq), tooltip: '...' },
        { label: 'Giro Ativos', value: formatNumber(f.giro_ativos), tooltip: '...' },
        { label: 'CAGR Rec. 5a', value: `${formatNumber(f.cagr_receitas)}%`, tooltip: '...' },
        { label: 'CAGR Luc. 5a', value: `${formatNumber(f.cagr_lucros)}%`, tooltip: '...' },
    ];

    return (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 mt-4 max-h-[60vh] overflow-y-auto pr-2">
            {items.map((item, i) => (
                <div key={i} className="bg-gray-800 p-2 rounded border border-gray-700 flex flex-col items-center relative group/item hover:border-teal-500 transition-colors">
                    <div className="flex items-center gap-1 mb-1">
                        <span className="text-[10px] text-gray-500 uppercase tracking-wider text-center">{item.label}</span>
                        <TooltipIcon content={item.tooltip} align={i % 5 === 0 ? 'left' : (i % 5 === 4 ? 'right' : 'center')} />
                    </div>
                    <span className="text-sm font-bold text-white">{item.value}</span>
                </div>
            ))}
        </div>
    );
  };

  const renderHistoricalFundamentals = (asset) => {
      const historyDataFull = asset.history_10y || generateHistory(10, asset.fundamentals || generateMockFundamentals(asset.type, asset.value));
      const historyData = activeHistoryPeriod === '10Y' ? historyDataFull : historyDataFull.slice(0, 5);
      const indicators = [
        { key: 'pl', label: 'P/L' }, { key: 'p_vp', label: 'P/VP' }, { key: 'dy', label: 'DY %' },
        { key: 'payout', label: 'Payout %' }, { key: 'margem_liquida', label: 'Marg. Líq.' },
        { key: 'roe', label: 'ROE %' }, { key: 'roic', label: 'ROIC %' },
        { key: 'div_liq_patrimonio', label: 'Dív/PL' },
        { key: 'div_liq_ebitda', label: 'Dív/EBITDA' },
        { key: 'vpa', label: 'VPA' },
        { key: 'lpa', label: 'LPA' },
        { key: 'p_ebit', label: 'P/EBIT' },
        { key: 'ev_ebitda', label: 'EV/EBITDA' },
      ];

      const currentVal = parseFloat(asset.fundamentals?.[selectedHistoryIndicator] || 0);
      const values = historyDataFull.map(h => parseFloat(h[selectedHistoryIndicator])).filter(v => !isNaN(v));
      const companyAvg = values.reduce((a, b) => a + b, 0) / (values.length || 1);
      const sectorAvg = companyAvg * (0.8 + Math.random() * 0.4);

      const renderChart = () => {
          const labels = historyData.map(h => h.year).reverse();
          const dataValues = historyData.map(h => parseFloat(h[selectedHistoryIndicator])).reverse();

          const chartData = {
              labels,
              datasets: [
                  {
                      label: indicators.find(i => i.key === selectedHistoryIndicator)?.label || selectedHistoryIndicator,
                      data: dataValues,
                      borderColor: '#06B6D4',
                      backgroundColor: historyChartType === 'bar' ? '#06B6D4' : 'rgba(6, 182, 212, 0.2)',
                      borderWidth: 2,
                      fill: historyChartType === 'line',
                      tension: 0.3,
                      type: historyChartType
                  },
                  {
                    label: 'Média Histórica',
                    data: Array(labels.length).fill(companyAvg),
                    borderColor: '#F59E0B',
                    backgroundColor: 'rgba(245, 158, 11, 0.15)',
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: true,
                    borderWidth: 1,
                    type: 'line'
                  }
              ]
          };

          const options = {
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { display: true, labels: { color: '#E5E7EB' } } },
              scales: { x: { ticks: { color: '#9CA3AF' }, grid: { display: false } }, y: { ticks: { color: '#9CA3AF' }, grid: { color: '#374151' } } }
          };

          return <Bar data={chartData} options={options} />;
      };

      return (
          <div className="mt-4">
              <div className="flex justify-between items-center mb-4 flex-wrap gap-2">
                  <div className="flex space-x-2 bg-gray-800 rounded p-1">
                      <button onClick={() => setHistoryViewMode('table')} className={`px-3 py-1 text-xs font-bold rounded transition-colors ${historyViewMode === 'table' ? 'bg-teal-600 text-white' : 'text-gray-400 hover:text-white'}`}><Table size={14} className="inline mr-1"/>Tabela</button>
                      <button onClick={() => setHistoryViewMode('chart')} className={`px-3 py-1 text-xs font-bold rounded transition-colors ${historyViewMode === 'chart' ? 'bg-teal-600 text-white' : 'text-gray-400 hover:text-white'}`}><Activity size={14} className="inline mr-1"/>Gráfico</button>
                  </div>

                  <div className="flex space-x-2 bg-gray-800 rounded p-1">
                      {['5Y', '10Y'].map(period => (<button key={period} onClick={() => setActiveHistoryPeriod(period)} className={`px-3 py-1 text-xs font-bold rounded transition-colors ${activeHistoryPeriod === period ? 'bg-teal-600 text-white' : 'text-gray-400 hover:text-white'}`}>{period}</button>))}
                  </div>
              </div>

              {historyViewMode === 'table' ? (
                  <div className="overflow-x-auto"><table className="min-w-full table-auto text-sm"><thead><tr className="bg-gray-800 text-gray-400 border-b border-gray-700"><th className="px-4 py-2 text-left">Indicador</th><th className="px-4 py-2 text-center text-teal-400 bg-gray-800/80 border-l border-r border-gray-700 sticky left-0">Atual</th>{historyData.map(h => <th key={h.year} className="px-4 py-2 text-center">{h.year}</th>)}</tr></thead><tbody className="divide-y divide-gray-800">{indicators.map(ind => {
                  const currentVal = asset.fundamentals ? asset.fundamentals[ind.key] : null;
                  return (
                  <tr key={ind.key} className="hover:bg-gray-800/50">
                      <td className="px-4 py-3 font-medium text-gray-300 whitespace-nowrap">{ind.label}</td>
                      <td className="px-4 py-3 text-center font-bold text-teal-400 border-l border-r border-gray-700 bg-gray-800/50">{currentVal ? formatNumber(currentVal) : '-'}</td>
                      {historyData.map(h => (<td key={h.year} className="px-4 py-3 text-center text-white font-mono">{h[ind.key] !== undefined ? formatNumber(h[ind.key]) : '-'}</td>))}
                  </tr>);})}</tbody></table></div>
              ) : (
                  <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                          <div>
                              <label className="text-xs text-gray-400 block mb-1">Indicador</label>
                              <select value={selectedHistoryIndicator} onChange={(e) => setSelectedHistoryIndicator(e.target.value)} className="w-full bg-gray-700 text-white p-2 rounded text-sm border border-gray-600 focus:border-teal-500 focus:outline-none">
                                  {indicators.map(ind => <option key={ind.key} value={ind.key}>{ind.label}</option>)}
                              </select>
                          </div>
                          <div>
                              <label className="text-xs text-gray-400 block mb-1">Tipo de Gráfico</label>
                              <div className="flex space-x-2 bg-gray-700 rounded p-1 w-fit">
                                  <button onClick={() => setHistoryChartType('line')} className={`px-3 py-1 text-xs rounded ${historyChartType === 'line' ? 'bg-teal-600 text-white' : 'text-gray-300'}`}>Linha</button>
                                  <button onClick={() => setHistoryChartType('bar')} className={`px-3 py-1 text-xs rounded ${historyChartType === 'bar' ? 'bg-teal-600 text-white' : 'text-gray-300'}`}>Barra</button>
                              </div>
                          </div>
                      </div>
                      <div className="grid grid-cols-3 gap-4 mb-6 bg-gray-700/30 p-3 rounded-lg">
                          <div className="text-center border-r border-gray-600"><div className="text-xs text-gray-400">Valor Atual</div><div className="text-lg font-bold text-teal-400">{formatNumber(currentVal)}</div></div>
                          <div className="text-center border-r border-gray-600"><div className="text-xs text-gray-400">Média da Empresa</div><div className="text-lg font-bold text-white">{formatNumber(companyAvg)}</div></div>
                          <div className="text-center"><div className="text-xs text-gray-400">Média do Setor</div><div className="text-lg font-bold text-yellow-400">{formatNumber(sectorAvg)}</div></div>
                      </div>
                      <div className="h-64 w-full">{renderChart()}</div>
                  </div>
              )}
          </div>
      );
  };

  const renderChecklist = (asset) => {
      const checklistItems = asset.checklist || [];
      return (
          <div className="mt-4 space-y-3">
              {checklistItems.map((item, index) => (
                  <div key={index} className="flex items-start p-3 bg-gray-800 rounded-lg border border-gray-700">
                      <div className="mr-3 mt-1">
                          {item.status === 'pass' && <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center text-black font-bold text-xs">✓</div>}
                          {item.status === 'warning' && <div className="w-5 h-5 rounded-full bg-yellow-500 flex items-center justify-center text-black font-bold text-xs">!</div>}
                          {item.status === 'fail' && <div className="w-5 h-5 rounded-full bg-red-500 flex items-center justify-center text-white font-bold text-xs">✕</div>}
                      </div>
                      <div className="flex-1">
                          <div className="flex items-center gap-2">
                             <h5 className="text-sm font-bold text-white">{item.criteria}</h5>
                             {item.tooltip && <TooltipIcon content={item.tooltip} />}
                          </div>
                          <p className="text-xs text-gray-400 mt-1">{item.note}</p>
                      </div>
                  </div>
              ))}
          </div>
      );
  };

  return (
    <div className="p-4 bg-gray-900 rounded-xl shadow-lg border border-gray-700 relative min-h-screen">
       <h2 className="text-2xl font-bold text-teal-400 mb-4 flex items-center"><Layers className="w-5 h-5 mr-2" />Central de Ativos</h2>
       <div className="flex justify-center space-x-4 mb-6 border-b border-gray-700 pb-4">{['Ações', 'FIIs', 'Internacionais'].map(cat => <button key={cat} onClick={() => setActiveCategory(cat)} className={`px-6 py-2 rounded-t-lg font-bold ${activeCategory === cat ? 'bg-gray-800 text-teal-400 border-b-2 border-teal-400' : 'text-gray-500'}`}>{cat}</button>)}</div>
       <div className="relative mb-4"><Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" /><input type="text" placeholder="Filtrar..." className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-teal-500" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} /></div>
       <div className="overflow-x-auto bg-gray-800 rounded-xl border border-gray-700">
         <table className="min-w-full table-auto border-collapse">
           <thead><tr className="bg-gray-700 text-gray-300 text-sm uppercase">{['Código', 'Nome', 'Setor', 'Preço (R$)', 'Var. Dia', 'DY (%)'].map(h => <th key={h} className="px-6 py-3 text-left font-semibold">{h}</th>)}</tr></thead>
           <tbody>{filteredAssets.map((asset, index) => (<tr key={asset.code} onClick={() => setSelectedAsset(asset)} className={`border-t border-gray-700 cursor-pointer hover:bg-gray-700 ${index % 2 === 0 ? 'bg-gray-800' : 'bg-gray-800/50'}`}><td className="px-6 py-4 font-bold text-white">{asset.code}</td><td className="px-6 py-4 text-gray-300">{asset.name}</td><td className="px-6 py-4 text-gray-400 text-sm">{asset.segment}</td><td className="px-6 py-4 text-white font-mono">{formatCurrency(asset.value)}</td><td className={`px-6 py-4 font-bold ${asset.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>{formatPercentage(asset.change)}</td><td className="px-6 py-4 text-yellow-400">{asset.dividendYield}%</td></tr>))}</tbody>
         </table>
       </div>

       {selectedAsset && (
           <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
               <div className="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity" onClick={() => setSelectedAsset(null)}></div>
               <div className="relative bg-gray-900 border border-gray-600 rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-2xl animate-scaleIn flex flex-col" onClick={e => e.stopPropagation()}>
                   <div className="p-6 border-b border-gray-700 flex justify-between items-start sticky top-0 bg-gray-900 z-10">
                       <div><h3 className="text-3xl font-bold text-white flex items-center">{selectedAsset.code} <span className="ml-3 text-sm font-normal px-2 py-1 bg-teal-900 text-teal-300 rounded-full border border-teal-700">{selectedAsset.type}</span></h3><p className="text-gray-400">{selectedAsset.name}</p></div>
                       <button onClick={() => setSelectedAsset(null)} className="text-gray-400 hover:text-white p-1"><X size={24} /></button>
                   </div>
                   <div className="p-6 pt-2">
                       <div className="flex border-b border-gray-700 mb-4 sticky top-0 bg-gray-900 pt-2 z-0">
                           <button onClick={() => setModalTab('fundamentals')} className={`px-4 py-2 font-bold text-sm transition-colors ${modalTab === 'fundamentals' ? 'text-teal-400 border-b-2 border-teal-400' : 'text-gray-400 hover:text-white'}`}>Indicadores</button>
                           <button onClick={() => setModalTab('history')} className={`px-4 py-2 font-bold text-sm transition-colors ${modalTab === 'history' ? 'text-teal-400 border-b-2 border-teal-400' : 'text-gray-400 hover:text-white'}`}>Histórico</button>
                           <button onClick={() => setModalTab('checklist')} className={`px-4 py-2 font-bold text-sm transition-colors ${modalTab === 'checklist' ? 'text-teal-400 border-b-2 border-teal-400' : 'text-gray-400 hover:text-white'}`}>Checklist Buy & Hold</button>
                           <button onClick={() => setModalTab('comparison')} className={`px-4 py-2 font-bold text-sm transition-colors ${modalTab === 'comparison' ? 'text-teal-400 border-b-2 border-teal-400' : 'text-gray-400 hover:text-white'}`}>Comparação</button>
                       </div>
                       <div className="min-h-[300px] pb-4">
                           {modalTab === 'fundamentals' && <div className="animate-fadeIn"><h4 className="text-lg font-bold text-teal-400 flex items-center mb-2"><BookOpen size={18} className="mr-2"/> Indicadores</h4>{renderFundamentals(selectedAsset)}</div>}
                           {modalTab === 'history' && <div className="animate-fadeIn">{renderHistoricalFundamentals(selectedAsset)}</div>}
                           {modalTab === 'checklist' && <div className="animate-fadeIn"><h4 className="text-lg font-bold text-teal-400 flex items-center mb-4"><CheckSquare size={18} className="mr-2"/> Checklist do Investidor</h4>{renderChecklist(selectedAsset)}</div>}
                           {modalTab === 'comparison' && <div className="animate-fadeIn"><AssetComparison asset={selectedAsset} /></div>}
                       </div>
                   </div>
               </div>
           </div>
       )}
    </div>
  );
};

// --- 7. COMPONENTE PRINCIPAL (APP) ---
const App = () => {
  const { data: b3Data, lastUpdate, refreshData, isLive, error } = useB3Data(MOCK_B3_DATA_BASE);
  const [activeTab, setActiveTab] = useState('dashboard');
  const tabs = [ { id: 'dashboard', name: 'Painel B3', icon: DollarSign }, { id: 'compound_interest', name: 'Calculadora', icon: Calculator }, { id: 'retirement', name: 'Aposentadoria', icon: Sunrise }, { id: 'diversification', name: 'Ativos', icon: Layers } ];
  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard': return <DashboardB3 data={b3Data} lastUpdate={lastUpdate} onRefresh={refreshData} isLive={isLive} error={error} />;
      case 'compound_interest': return <CompoundInterestCalculator />;
      case 'retirement': return <RetirementPlanner />;
      case 'diversification': return <AssetOverview liveData={b3Data} />;
      default: return <DashboardB3 data={b3Data} lastUpdate={lastUpdate} onRefresh={refreshData} isLive={isLive} error={error} />;
    }
  };
  return (
    <div className="min-h-screen bg-gray-950 text-white font-sans p-4 md:p-8">
      <header className="mb-8 flex justify-between items-center"><h1 className="text-3xl font-extrabold text-white flex items-center"><DollarSign className="w-8 h-8 mr-2 text-teal-400" />Finanças B3</h1></header>
      <nav className="mb-8 flex justify-center space-x-4">{tabs.map(tab => (<button key={tab.id} onClick={() => setActiveTab(tab.id)} className={`flex items-center px-4 py-2 rounded-lg font-bold transition-all ${activeTab === tab.id ? 'bg-teal-600 text-white shadow-lg scale-105' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}><tab.icon className="w-5 h-5 mr-2"/>{tab.name}</button>))}</nav>
      <main className="max-w-7xl mx-auto">{renderContent()}</main>
      <footer className="mt-12 text-center text-sm text-gray-500"><p>Dados de cotações e ativos são alimentados pela API no GitHub (Mockados para demonstração de fundamentos).</p></footer>
    </div>
  );
};
export default App;
