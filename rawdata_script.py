 
#TODO: add support for ADC histogram plotting.
#TODO: add support for determining ADC input level 

import corr,time,numpy,struct,sys,logging,pylab,matplotlib
import matplotlib.pyplot as plt
import cmath
import math
import numpy as np
import time
from scipy.fftpack import fft, ifft


bitstream = 'ramtestreg_2017-04-12_1129.bof'
katcp_port=7147

from SNAPsynth import LMX2581
fpga=LMX2581('rpi3-2')

time.sleep(0.1)

#fpga.progdev('fin_model_power_2017-05-10_1643.bof')
print fpga.listdev()

print fpga.listbof()

#fpga.from_gen_synth(synth_mhz=500,ref_signal=10)



#fpga.write_int('fft_a1_2',2)
fpga.write_int('fft_shift',2**11-1)
fpga.write_int('adc16_use_synth',0)
fpga.write_int('sync_gen2_sync',1)
#fpga.write_int('sync_gen1_sync_period_var',2**16-2)

#fpga.write_int('sync_gen1_sync_period_sel',1)
print fpga.est_brd_clk()
fpga.write_int('acc_len',6*10**5)
fpga.write_int('cnt_rst',1)
print fpga.read_int('acc_len')

Fs=250*10**6

acc_cnt=fpga.read_int('acc_cnt')
acc_cnt_loop=fpga.read_int('acc_cnt')
print fpga.read_int('acc_cnt')
fpga.write_int('cnt_rst',0)
time.sleep(5)
print time.time()
while (acc_cnt==acc_cnt_loop):
 acc_cnt_loop=fpga.read_int('acc_cnt')
 print fpga.read_int('acc_cnt')
 time.sleep(0.001)
print time.time()
  

print fpga.read_int('acc_cnt')
print time.time()




raw_data_hist1=struct.unpack('>2048b',fpga.snapshot_get('snapshot1',man_trig=True,man_valid=True)['data'])
raw_data_hist2=struct.unpack('>2048b',fpga.snapshot_get('snapshot2',man_trig=True,man_valid=True)['data'])
raw_data_hist3=struct.unpack('>2048b',fpga.snapshot_get('snapshot4',man_trig=True,man_valid=True)['data'])
raw_data_hist4=struct.unpack('>2048b',fpga.snapshot_get('snapshot5',man_trig=True,man_valid=True)['data'])
raw_data_hist5=struct.unpack('>2048b',fpga.snapshot_get('snapshot6',man_trig=True,man_valid=True)['data'])
raw_data_hist6=struct.unpack('>2048b',fpga.snapshot_get('snapshot7',man_trig=True,man_valid=True)['data'])



plt.subplot(6,1,1)
plt.plot(raw_data_hist1)
plt.xlabel('Frequency')
plt.ylabel('raw_data_hist1')

plt.subplot(6,1,2)
plt.plot(raw_data_hist2)
plt.xlabel('Frequency')
plt.ylabel('raw_data_hist2')

plt.subplot(6,1,3)
plt.plot(raw_data_hist3)
plt.xlabel('Frequency')
plt.ylabel('raw_data_hist3')


plt.subplot(6,1,4)
plt.plot(raw_data_hist4)
plt.xlabel('Frequency')
plt.ylabel('raw_data_hist4')


plt.subplot(6,1,5)
plt.plot(raw_data_hist5)
plt.xlabel('Frequency')
plt.ylabel('raw_data_hist5')


plt.subplot(6,1,6)
plt.plot(raw_data_hist6)
plt.xlabel('Frequency')
plt.ylabel('raw_data_hist6')

plt.show()






