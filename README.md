# Pattern injection test with emulator board
Document and code to generate comaprator digi and CLCT+LCT information for patten injection test

## Generate txt file with CSC L1 trigger emulator

  - step1: checkout cmssw and CSC L1 trigger emulator. 
  ```
cmsrel CMSSW_12_5_0_pre4
cd CMSSW_12_5_0_pre4/src
cmsenv
git cms-addpkg L1Trigger/CSCTriggerPrimitives
  ```
  - step2: apply the changes to CSC L1 trigger emulator and compile cmssw. 
  ```
git clone https://github.com/tahuang1991/InjectCSCPatterns.git
cp InjectCSCPatterns/CSCTriggerPrimitives/src/* L1Trigger/CSCTriggerPrimitives/src/
cp InjectCSCPatterns/CSCTriggerPrimitives/interface/*  L1Trigger/CSCTriggerPrimitives/interface
scram b -j 9
  ```
  - step3: run CSC L1 trigger emulation to get txt file. Replace the inputFiles with sample you want to process and set maxEvents to the number of events you need
  ```
  cd L1Trigger/CSCTriggerPrimitives/test
  rm ComparatorDigi_CLCT_ME*.txt
  cmsRun runCSCTriggerPrimitiveProducer_cfg.py mc=True run3=True inputFiles="file:/eos/user/t/tahuang/RelValSamples/CMSSW_12_4_0_pre3/27a95851-6358-485b-b15b-619f3404d795.root" maxEvents=10 saveEdmOutput=False l1=True runME11ILT=True runCCLUTOTMB=True
  ```

  
The output files generated from CSC L1 trigger emulator include:
  - ComparatorDigi_CLCT_ME11.txt for ME11 chamber type, with CCLUT and GEMCSC algorithm on
  - ComparatorDigi_CLCT_ME21.txt for ME21 chamber type, with CCLUT on
  - ComparatorDigi_CLCT_ME3141.txt for ME3141 chamber type, with CCLUT on

Everytime you run above program, the it would append the new printouts to the exist output files. Make sure that old files are removed 

## Txt file from CSC L1 trigger emulator conventions

start with "CSCChamber with Comparatordigi:" + detector information
>```
>CSCChamber with Comparatordigi: (end,station,ring,chamber) = 1, 2, 1, 7  
>```

Comparator digi part: ranked by BX and layer
>```
>Comparatordigi BX 7 Layer 1 halfstrip 67 
>Comparatordigi BX 7 Layer 2 halfstrip 67
>Comparatordigi BX 7 Layer 4 halfstrip 67
>Comparatordigi BX 7 Layer 5 halfstrip 67
>Comparatordigi BX 8 Layer 0 halfstrip 67
>Comparatordigi BX 8 Layer 3 halfstrip 67
>```

CLCT part: CLCTs in this chamber, up to two CLCTs per BX, ranked by BX
>```
>CSC CLCT #1: Valid = 1 BX = 7 Run-2 Pattern = 10 Run-3 Pattern = 4 Quality = 6 Comp Code 4095 Bend = 1  
>Slope = 0 CFEB = 2 Strip = 2 KeyHalfStrip = 66 KeyQuartStrip = 132 KeyEighthStrip = 265
>```

LCT part: LCTs in this chamber, up to two LCTs per BX,  ranked by BX
>```
>CSC LCT #1: Valid = 1 BX = 8 Run-2 Pattern = 10 Run-3 Pattern = 4 Quality = 3 Bend = 1 Slope = 0   
>KeyHalfStrip = 66 KeyQuartStrip = 132 KeyEighthStrip = 265 KeyWireGroup = 104 Type (SIM) = 1 MPC Link = 0
>```


## Generate txt file with GEMCode


