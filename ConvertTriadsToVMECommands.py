##########################################################################
adr = 0x2A # ADR_CCB_CFG  CCB Configuration

wr_data = 0x0039   # 0x39   = b'0000'0000'0011'1001 Disable External CCB
  					       # bit 00: 1 = Ignore Received CCB Backplane Inputs
  					       # bit 01: 1 = Disable transmitted CCB backplane outputs
  					       # bit 02: 1 = Enable internal L1A emulator
  					       # bit 03: 1 = Enable ALCT+CLCT status to CCB front panel
  					       # bit 04: 1 = Enable ALCT status GTL outputs (req [03]=1)
  					       # bit 05: 1 = Enable CLCT status GTL outputs (req [03]=1)

print('W {0:03x} {1:04x} Turn off CCB backplane inputs'.format(adr, wr_data))

##########################################################################
adr = 0x2C # ADR_CCB_TRIG   CCB Trigger Control

wr_data = 0x0004   # 0x04   = b'0000'0100 
  					       # bit 02: 1 = Request CCB L1a on sequencer trigger

print('W {0:03x} {1:04x} Enable sequencer trigger'.format(adr, wr_data))



# parameters
mxtbins = 32
mxly    = 6 # maximum number of layers in CSC
mxdsabs = 40 # maximum number of distrip per chamber with 5 CFEBs
#mxdsabs = 56 # maximum number of distrip per chamber with 7 CFEBs

# initialize triads with zeroes
itriad = []

for itbin in range(mxtbins):
  itriad.append([])
  for idistrip in range(mxdsabs):
    itriad[itbin].append([])
    for layer in range(mxly):
      itriad[itbin][idistrip].append(0)

#print itriad

# read file with triads
with open("SimulateCSCPatterns/PatternExamples/CLCTPattern_nLayers6_00.txt") as file:
  for line in file:
    itbin = int(line[0:2])
    layer = int(line[3:4])
#    print itbin, layer,
    idistrip = 0
    for i in range(5, len(line)-1):
      if line[i:i+1] is not "|":
        itriad[itbin][idistrip][layer] = int(line[i:i+1])
#        print itriad[itbin][idistrip][layer],
        idistrip = idistrip + 1
#    print 

#print itriad

# Initialize pattern RAM
pat_ram = []
for itbin in range(mxtbins):
  pat_ram.append([])
  for layer in range(0,mxly,2):
    pat_ram[itbin].append([])
    iram=layer/2
    for idistrip in range(mxdsabs):
      icfeblp =idistrip // 8
      idslocal=idistrip %  8
      if idslocal==0: pat_ram[itbin][iram].append(0)

# Pack triads into pattern RAM
wr_data=0
for layer in range(0,mxly,2):
  iram=layer/2
  for itbin in range(mxtbins):
    for idistrip in range(mxdsabs):
      icfeblp =idistrip // 8
      idslocal=idistrip %  8
#      print idistrip, icfeblp, idslocal
      if idslocal==0: wr_data=0
      
      ibit=itriad[itbin][idistrip][layer]
      wr_data=wr_data | (ibit << idslocal)
      
      ibit=itriad[itbin][idistrip][layer+1]
      wr_data=wr_data | (ibit << (idslocal+8))
      
      pat_ram[itbin][iram][icfeblp] = wr_data
#      print itbin, iram, format(wr_data, '#06X')

#print pat_ram

# Write muon data to Injector
for icfeblp in range(5):
  for iram in range(3):
    for itbin in range(12):
      wr_data_mem = pat_ram[itbin][iram][icfeblp]    # RAM data to write at this cfeb and tbin
      wr_data_lsb = (wr_data_mem >>  0) & 0x0FFFF    # RAM write data [15:0] go to ADR 0x46
      wr_data_msb = (wr_data_mem >> 16) & 0x3        # RAM write data [17:16] go to ADR 0x100
      wadr        = itbin
      
      ##########################################################################
      adr = 0x42 # ADR_CFEB_INJ  CFEB Injector Control

      wr_data = 0x7C1F                           # 0111110000011111 <-- Zero CFEB select
      febsel  = (1 << icfeblp)                   # Select CFEB
      wr_data = wr_data | (febsel << 5) | 0x7C00 # Set febsel, enable injectors
      
      print('W {0:03x} {1:04x} Select CFEB {2}'.format(adr, wr_data, icfeblp))
      
      ##########################################################################
      adr = 0x44 # ADR_CFEB_INJ_ADR  CFEB Injector RAM Address

      ren     = 0
      wen     = 0
      wr_data = wen | (ren << 3) | (wadr << 6) # Set RAM Address + No write
      
      print('W {0:03x} {1:04x} Set RAM Address for tbin {2} + No write'.format(adr, wr_data, itbin))
      
      ##########################################################################
      adr = 0x46 # ADR_CFEB_INJ_WDATA  CFEB Injector Write Data lsb = 16 bits

      wr_data = wr_data_lsb
      
      if wr_data_mem != 0:
        print('W {0:03x} {1:04x} Store RAM Data lsb [15:0] <-- NONZERO'.format(adr, wr_data))
      else:
        print('W {0:03x} {1:04x} Store RAM Data lsb [15:0]'.format(adr, wr_data))
      
      ##########################################################################
      adr = 0x100 # ADR_L1A_LOOKBACK  CFEB Injector Write Data msb = 2 addtional bits

      wr_data = (wr_data_msb << 11)
      
      if wr_data_mem != 0:
        print('W {0:03x} {1:04x} Store RAM Data msb [17:16] <-- NONZERO'.format(adr, wr_data))
      else:
        print('W {0:03x} {1:04x} Store RAM Data msb [17:16]'.format(adr, wr_data))
      
      ##########################################################################
      adr = 0x44 # ADR_CFEB_INJ_ADR  CFEB Injector RAM Address + Assert write
      
      ren     = 0
      wen     = (1 << iram)
      wr_data = wen | (ren << 3) | (wadr << 6) # Set RAM Address + Assert write
      
      print('W {0:03x} {1:04x} Set RAM Address for tbin {2} + Assert write RAM {3}'.format(adr, wr_data, itbin, iram))

##########################################################################
adr = 0x42 # ADR_CFEB_INJ  CFEB Injector Control

wr_data = 0xFC1F                           # 1111110000011111 <-- Start pattern injector

print('W {0:03x} {1:04x} Start pattern injector'.format(adr, wr_data))

