#TODO: add support for ADC histogram plotting.
#TODO: add support for determining ADC input level 

import corr,time,numpy,struct,sys,logging,pylab,matplotlib
import matplotlib.pyplot as plt
import cmath
import math
import numpy as np
import time
from scipy.fftpack import fft, ifft


#bitstream = 'ramtestreg_2017-04-12_1129.bof'
katcp_port=7147

from SNAPsynth import LMX2581
fpga=LMX2581('rpi3-2')

time.sleep(0.1)

#fpga.progdev('fin_model_power_2017-05-10_1643.bof')
print fpga.listdev()

print fpga.listbof()

#fpga.from_gen_synth(synth_mhz=500,ref_signal=10)



print fpga.read_int('acc_cnt')
print time.time()


fpga.write_int('acc_len',6*10**5)

fpga.write_int('cnt_rst',1)


fpga.write_int('adc16_use_synth',0)
fpga.write_int('sync_gen2_sync',1)
fpga.write_int('sync_gen1_sync_period_var',2**20-2)
fpga.write_int('sync_gen1_sync_period_sel',1)


histogram_x=np.linspace(-127,127,256)
print len(histogram_x)

length_acc=100


raw_data_hist1_1=np.zeros(512)
raw_data_hist1_2=np.zeros(512)
raw_data_hist1_3=np.zeros(512)
raw_data_hist1_4=np.zeros(512)

raw_data_hist2_1=np.zeros(512)
raw_data_hist2_2=np.zeros(512)
raw_data_hist2_3=np.zeros(512)
raw_data_hist2_4=np.zeros(512)

raw_data_hist3_1=np.zeros(512)
raw_data_hist3_2=np.zeros(512)
raw_data_hist3_3=np.zeros(512)
raw_data_hist3_4=np.zeros(512)

raw_data_hist4_1=np.zeros(512)
raw_data_hist4_2=np.zeros(512)
raw_data_hist4_3=np.zeros(512)
raw_data_hist4_4=np.zeros(512)

raw_data_hist5_1=np.zeros(512)
raw_data_hist5_2=np.zeros(512)
raw_data_hist5_3=np.zeros(512)
raw_data_hist5_4=np.zeros(512)

raw_data_hist6_1=np.zeros(512)
raw_data_hist6_2=np.zeros(512)
raw_data_hist6_3=np.zeros(512)
raw_data_hist6_4=np.zeros(512)

raw_data_hist1_1_con=np.zeros(512*length_acc)
raw_data_hist1_2_con=np.zeros(512*length_acc)
raw_data_hist1_3_con=np.zeros(512*length_acc)
raw_data_hist1_4_con=np.zeros(512*length_acc)

raw_data_hist2_1_con=np.zeros(512*length_acc)
raw_data_hist2_2_con=np.zeros(512*length_acc)
raw_data_hist2_3_con=np.zeros(512*length_acc)
raw_data_hist2_4_con=np.zeros(512*length_acc)

raw_data_hist3_1_con=np.zeros(512*length_acc)
raw_data_hist3_2_con=np.zeros(512*length_acc)
raw_data_hist3_3_con=np.zeros(512*length_acc)
raw_data_hist3_4_con=np.zeros(512*length_acc)

raw_data_hist4_1_con=np.zeros(512*length_acc)
raw_data_hist4_2_con=np.zeros(512*length_acc)
raw_data_hist4_3_con=np.zeros(512*length_acc)
raw_data_hist4_4_con=np.zeros(512*length_acc)

raw_data_hist5_1_con=np.zeros(512*length_acc)
raw_data_hist5_2_con=np.zeros(512*length_acc)
raw_data_hist5_3_con=np.zeros(512*length_acc)
raw_data_hist5_4_con=np.zeros(512*length_acc)

raw_data_hist6_1_con=np.zeros(512*length_acc)
raw_data_hist6_2_con=np.zeros(512*length_acc)
raw_data_hist6_3_con=np.zeros(512*length_acc)
raw_data_hist6_4_con=np.zeros(512*length_acc)

raw_data_hist1=struct.unpack('>2048b',fpga.snapshot_get('snapshot1',man_trig=True,man_valid=True)['data'])
raw_data_hist2=struct.unpack('>2048b',fpga.snapshot_get('snapshot2',man_trig=True,man_valid=True)['data'])
raw_data_hist3=struct.unpack('>2048b',fpga.snapshot_get('snapshot4',man_trig=True,man_valid=True)['data'])
raw_data_hist4=struct.unpack('>2048b',fpga.snapshot_get('snapshot5',man_trig=True,man_valid=True)['data'])
raw_data_hist5=struct.unpack('>2048b',fpga.snapshot_get('snapshot6',man_trig=True,man_valid=True)['data'])
raw_data_hist6=struct.unpack('>2048b',fpga.snapshot_get('snapshot7',man_trig=True,man_valid=True)['data'])


for n in range (1,512):

 raw_data_hist1_1[n]=raw_data_hist1[4*n-3]
 raw_data_hist1_2[n]=raw_data_hist1[4*n-2]
 raw_data_hist1_3[n]=raw_data_hist1[4*n-1]
 raw_data_hist1_4[n]=raw_data_hist1[4*n]

 raw_data_hist2_1[n]=raw_data_hist2[4*n-3]
 raw_data_hist2_2[n]=raw_data_hist2[4*n-2]
 raw_data_hist2_3[n]=raw_data_hist2[4*n-1]
 raw_data_hist2_4[n]=raw_data_hist2[4*n]
 

 raw_data_hist3_1[n]=raw_data_hist3[4*n-3]
 raw_data_hist3_2[n]=raw_data_hist3[4*n-2]
 raw_data_hist3_3[n]=raw_data_hist3[4*n-1]
 raw_data_hist3_4[n]=raw_data_hist3[4*n]


 raw_data_hist4_1[n]=raw_data_hist4[4*n-3]
 raw_data_hist4_2[n]=raw_data_hist4[4*n-2]
 raw_data_hist4_3[n]=raw_data_hist4[4*n-1]
 raw_data_hist4_4[n]=raw_data_hist4[4*n]

 raw_data_hist5_1[n]=raw_data_hist5[4*n-3]
 raw_data_hist5_2[n]=raw_data_hist5[4*n-2]
 raw_data_hist5_3[n]=raw_data_hist5[4*n-1]
 raw_data_hist5_4[n]=raw_data_hist5[4*n]

 raw_data_hist6_1[n]=raw_data_hist6[4*n-3]
 raw_data_hist6_2[n]=raw_data_hist6[4*n-2]
 raw_data_hist6_3[n]=raw_data_hist6[4*n-1]
 raw_data_hist6_4[n]=raw_data_hist6[4*n]

raw_data_hist1_1_sum=raw_data_hist1_1
raw_data_hist1_2_sum=raw_data_hist1_2
raw_data_hist1_3_sum=raw_data_hist1_3
raw_data_hist1_4_sum=raw_data_hist1_4

raw_data_hist2_1_sum=raw_data_hist2_1
raw_data_hist2_2_sum=raw_data_hist2_2
raw_data_hist2_3_sum=raw_data_hist2_3
raw_data_hist2_4_sum=raw_data_hist2_4

raw_data_hist3_1_sum=raw_data_hist3_1
raw_data_hist3_2_sum=raw_data_hist3_2
raw_data_hist3_3_sum=raw_data_hist3_3
raw_data_hist3_4_sum=raw_data_hist3_4

raw_data_hist4_1_sum=raw_data_hist4_1
raw_data_hist4_2_sum=raw_data_hist4_2
raw_data_hist4_3_sum=raw_data_hist4_3
raw_data_hist4_4_sum=raw_data_hist4_4

raw_data_hist5_1_sum=raw_data_hist5_1
raw_data_hist5_2_sum=raw_data_hist5_2
raw_data_hist5_3_sum=raw_data_hist5_3
raw_data_hist5_4_sum=raw_data_hist5_4

raw_data_hist6_1_sum=raw_data_hist6_1
raw_data_hist6_2_sum=raw_data_hist6_2
raw_data_hist6_3_sum=raw_data_hist6_3
raw_data_hist6_4_sum=raw_data_hist6_4

#####################################


raw_data_hist1_1_con=raw_data_hist1_1
raw_data_hist1_2_con=raw_data_hist1_2
raw_data_hist1_3_con=raw_data_hist1_3
raw_data_hist1_4_con=raw_data_hist1_4

raw_data_hist1_1_con=raw_data_hist1_1
raw_data_hist1_2_con=raw_data_hist1_2
raw_data_hist1_3_con=raw_data_hist1_3
raw_data_hist1_4_con=raw_data_hist1_4

raw_data_hist2_1_con=raw_data_hist2_1
raw_data_hist2_2_con=raw_data_hist2_2
raw_data_hist2_3_con=raw_data_hist2_3
raw_data_hist2_4_con=raw_data_hist2_4

raw_data_hist3_1_con=raw_data_hist3_1
raw_data_hist3_2_con=raw_data_hist3_2
raw_data_hist3_3_con=raw_data_hist3_3
raw_data_hist3_4_con=raw_data_hist3_4

raw_data_hist4_1_con=raw_data_hist4_1
raw_data_hist4_2_con=raw_data_hist4_2
raw_data_hist4_3_con=raw_data_hist4_3
raw_data_hist4_4_con=raw_data_hist4_4



for m in range (1,length_acc):

 raw_data_hist1=struct.unpack('>2048b',fpga.snapshot_get('snapshot1',man_trig=True,man_valid=True)['data'])
 raw_data_hist2=struct.unpack('>2048b',fpga.snapshot_get('snapshot2',man_trig=True,man_valid=True)['data'])
 raw_data_hist3=struct.unpack('>2048b',fpga.snapshot_get('snapshot4',man_trig=True,man_valid=True)['data'])
 raw_data_hist4=struct.unpack('>2048b',fpga.snapshot_get('snapshot5',man_trig=True,man_valid=True)['data'])
 raw_data_hist5=struct.unpack('>2048b',fpga.snapshot_get('snapshot6',man_trig=True,man_valid=True)['data'])
 raw_data_hist6=struct.unpack('>2048b',fpga.snapshot_get('snapshot7',man_trig=True,man_valid=True)['data'])


 for n in range (1,512):

  raw_data_hist1_1[n]=raw_data_hist1[4*n-3]
  raw_data_hist1_2[n]=raw_data_hist1[4*n-2]
  raw_data_hist1_3[n]=raw_data_hist1[4*n-1]
  raw_data_hist1_4[n]=raw_data_hist1[4*n]

  raw_data_hist2_1[n]=raw_data_hist2[4*n-3]
  raw_data_hist2_2[n]=raw_data_hist2[4*n-2]
  raw_data_hist2_3[n]=raw_data_hist2[4*n-1]
  raw_data_hist2_4[n]=raw_data_hist2[4*n]
 

  raw_data_hist3_1[n]=raw_data_hist3[4*n-3]
  raw_data_hist3_2[n]=raw_data_hist3[4*n-2]
  raw_data_hist3_3[n]=raw_data_hist3[4*n-1]
  raw_data_hist3_4[n]=raw_data_hist3[4*n]


  raw_data_hist4_1[n]=raw_data_hist4[4*n-3]
  raw_data_hist4_2[n]=raw_data_hist4[4*n-2]
  raw_data_hist4_3[n]=raw_data_hist4[4*n-1]
  raw_data_hist4_4[n]=raw_data_hist4[4*n]

  raw_data_hist5_1[n]=raw_data_hist5[4*n-3]
  raw_data_hist5_2[n]=raw_data_hist5[4*n-2]
  raw_data_hist5_3[n]=raw_data_hist5[4*n-1]
  raw_data_hist5_4[n]=raw_data_hist5[4*n]

  raw_data_hist6_1[n]=raw_data_hist6[4*n-3]
  raw_data_hist6_2[n]=raw_data_hist6[4*n-2]
  raw_data_hist6_3[n]=raw_data_hist6[4*n-1]
  raw_data_hist6_4[n]=raw_data_hist6[4*n]




 raw_data_hist1_1_sum=np.add(raw_data_hist1_1,raw_data_hist1_1_sum)
 raw_data_hist1_2_sum=np.add(raw_data_hist1_2,raw_data_hist1_2_sum)
 raw_data_hist1_3_sum=np.add(raw_data_hist1_3,raw_data_hist1_3_sum)
 raw_data_hist1_4_sum=np.add(raw_data_hist1_4,raw_data_hist1_4_sum)

 raw_data_hist2_1_sum=np.add(raw_data_hist2_1,raw_data_hist2_1_sum)
 raw_data_hist2_2_sum=np.add(raw_data_hist2_2,raw_data_hist2_2_sum)
 raw_data_hist2_3_sum=np.add(raw_data_hist2_3,raw_data_hist2_3_sum)
 raw_data_hist2_4_sum=np.add(raw_data_hist2_4,raw_data_hist2_4_sum)

 raw_data_hist3_1_sum=np.add(raw_data_hist3_1,raw_data_hist3_1_sum)
 raw_data_hist3_2_sum=np.add(raw_data_hist3_2,raw_data_hist3_2_sum)
 raw_data_hist3_3_sum=np.add(raw_data_hist3_3,raw_data_hist3_3_sum)
 raw_data_hist3_4_sum=np.add(raw_data_hist3_4,raw_data_hist3_4_sum)

 raw_data_hist4_1_sum=np.add(raw_data_hist4_1,raw_data_hist4_1_sum)
 raw_data_hist4_2_sum=np.add(raw_data_hist4_2,raw_data_hist4_2_sum)
 raw_data_hist4_3_sum=np.add(raw_data_hist4_3,raw_data_hist4_3_sum)
 raw_data_hist4_4_sum=np.add(raw_data_hist4_4,raw_data_hist4_4_sum)

 raw_data_hist5_1_sum=np.add(raw_data_hist5_1,raw_data_hist5_1_sum)
 raw_data_hist5_2_sum=np.add(raw_data_hist5_2,raw_data_hist5_2_sum)
 raw_data_hist5_3_sum=np.add(raw_data_hist5_3,raw_data_hist5_3_sum)
 raw_data_hist5_4_sum=np.add(raw_data_hist5_4,raw_data_hist5_4_sum)

 raw_data_hist6_1_sum=np.add(raw_data_hist6_1,raw_data_hist6_1_sum)
 raw_data_hist6_2_sum=np.add(raw_data_hist6_2,raw_data_hist6_2_sum)
 raw_data_hist6_3_sum=np.add(raw_data_hist6_3,raw_data_hist6_3_sum)
 raw_data_hist6_4_sum=np.add(raw_data_hist6_4,raw_data_hist6_4_sum)
 

 raw_data_hist1_1_con=np.concatenate([raw_data_hist1_1_con,raw_data_hist1_1])
 raw_data_hist1_2_con=np.concatenate([raw_data_hist1_2_con,raw_data_hist1_2])
 raw_data_hist1_3_con=np.concatenate([raw_data_hist1_3_con,raw_data_hist1_3])
 raw_data_hist1_4_con=np.concatenate([raw_data_hist1_4_con,raw_data_hist1_4])

 raw_data_hist2_1_con=np.concatenate([raw_data_hist2_1_con,raw_data_hist2_1])
 raw_data_hist2_2_con=np.concatenate([raw_data_hist2_2_con,raw_data_hist2_2])
 raw_data_hist2_3_con=np.concatenate([raw_data_hist2_3_con,raw_data_hist2_3])
 raw_data_hist2_4_con=np.concatenate([raw_data_hist2_4_con,raw_data_hist2_4])

 raw_data_hist3_1_con=np.concatenate([raw_data_hist3_1_con,raw_data_hist3_1])
 raw_data_hist3_2_con=np.concatenate([raw_data_hist3_2_con,raw_data_hist3_2])
 raw_data_hist3_3_con=np.concatenate([raw_data_hist3_3_con,raw_data_hist3_3])
 raw_data_hist3_4_con=np.concatenate([raw_data_hist3_4_con,raw_data_hist3_4])

 raw_data_hist4_1_con=np.concatenate([raw_data_hist4_1_con,raw_data_hist4_1])
 raw_data_hist4_2_con=np.concatenate([raw_data_hist4_2_con,raw_data_hist4_2])
 raw_data_hist4_3_con=np.concatenate([raw_data_hist4_3_con,raw_data_hist4_3])
 raw_data_hist4_4_con=np.concatenate([raw_data_hist4_4_con,raw_data_hist4_4])

 raw_data_hist5_1_con=np.concatenate([raw_data_hist5_1_con,raw_data_hist5_1])
 raw_data_hist5_2_con=np.concatenate([raw_data_hist5_2_con,raw_data_hist5_2])
 raw_data_hist5_3_con=np.concatenate([raw_data_hist5_3_con,raw_data_hist5_3])
 raw_data_hist5_4_con=np.concatenate([raw_data_hist5_4_con,raw_data_hist5_4])

 raw_data_hist6_1_con=np.concatenate([raw_data_hist6_1_con,raw_data_hist6_1])
 raw_data_hist6_2_con=np.concatenate([raw_data_hist6_2_con,raw_data_hist6_2])
 raw_data_hist6_3_con=np.concatenate([raw_data_hist6_3_con,raw_data_hist6_3])
 raw_data_hist6_4_con=np.concatenate([raw_data_hist6_4_con,raw_data_hist6_4])
 print m

print fpga.est_brd_clk()
print fpga.read_int('acc_len')

Fs=200*10**6

raw_data_hist1_1_sum_mean=np.mean(raw_data_hist1_1_con)
raw_data_hist1_2_sum_mean=np.mean(raw_data_hist1_2_con)
raw_data_hist1_3_sum_mean=np.mean(raw_data_hist1_3_con)
raw_data_hist1_4_sum_mean=np.mean(raw_data_hist1_4_con)

raw_data_hist2_1_sum_mean=np.mean(raw_data_hist2_1_con)
raw_data_hist2_2_sum_mean=np.mean(raw_data_hist2_2_con)
raw_data_hist2_3_sum_mean=np.mean(raw_data_hist2_3_con)
raw_data_hist2_4_sum_mean=np.mean(raw_data_hist2_4_con)


raw_data_hist3_1_sum_mean=np.mean(raw_data_hist3_1_con)
raw_data_hist3_2_sum_mean=np.mean(raw_data_hist3_2_con)
raw_data_hist3_3_sum_mean=np.mean(raw_data_hist3_3_con)
raw_data_hist3_4_sum_mean=np.mean(raw_data_hist3_4_con)

raw_data_hist4_1_sum_mean=np.mean(raw_data_hist4_1_con)
raw_data_hist4_2_sum_mean=np.mean(raw_data_hist4_2_con)
raw_data_hist4_3_sum_mean=np.mean(raw_data_hist4_3_con)
raw_data_hist4_4_sum_mean=np.mean(raw_data_hist4_4_con)

raw_data_hist5_1_sum_mean=np.mean(raw_data_hist5_1_con)
raw_data_hist5_2_sum_mean=np.mean(raw_data_hist5_2_con)
raw_data_hist5_3_sum_mean=np.mean(raw_data_hist5_3_con)
raw_data_hist5_4_sum_mean=np.mean(raw_data_hist5_4_con)

raw_data_hist6_1_sum_mean=np.mean(raw_data_hist6_1_con)
raw_data_hist6_2_sum_mean=np.mean(raw_data_hist6_2_con)
raw_data_hist6_3_sum_mean=np.mean(raw_data_hist6_3_con)
raw_data_hist6_4_sum_mean=np.mean(raw_data_hist6_4_con)

raw_data_hist1_1_sum_deviation=np.std(raw_data_hist1_1_con)
raw_data_hist1_2_sum_deviation=np.std(raw_data_hist1_2_con)
raw_data_hist1_3_sum_deviation=np.std(raw_data_hist1_3_con)
raw_data_hist1_4_sum_deviation=np.std(raw_data_hist1_4_con)

raw_data_hist2_1_sum_deviation=np.std(raw_data_hist2_1_con)
raw_data_hist2_2_sum_deviation=np.std(raw_data_hist2_2_con)
raw_data_hist2_3_sum_deviation=np.std(raw_data_hist2_3_con)
raw_data_hist2_4_sum_deviation=np.std(raw_data_hist2_4_con)

raw_data_hist3_1_sum_deviation=np.std(raw_data_hist3_1_con)
raw_data_hist3_2_sum_deviation=np.std(raw_data_hist3_2_con)
raw_data_hist3_3_sum_deviation=np.std(raw_data_hist3_3_con)
raw_data_hist3_4_sum_deviation=np.std(raw_data_hist3_4_con)

raw_data_hist4_1_sum_deviation=np.std(raw_data_hist4_1_con)
raw_data_hist4_2_sum_deviation=np.std(raw_data_hist4_2_con)
raw_data_hist4_3_sum_deviation=np.std(raw_data_hist4_3_con)
raw_data_hist4_4_sum_deviation=np.std(raw_data_hist4_4_con)

raw_data_hist5_1_sum_deviation=np.std(raw_data_hist5_1_con)
raw_data_hist5_2_sum_deviation=np.std(raw_data_hist5_2_con)
raw_data_hist5_3_sum_deviation=np.std(raw_data_hist5_3_con)
raw_data_hist5_4_sum_deviation=np.std(raw_data_hist5_4_con)

raw_data_hist6_1_sum_deviation=np.std(raw_data_hist6_1_con)
raw_data_hist6_2_sum_deviation=np.std(raw_data_hist6_2_con)
raw_data_hist6_3_sum_deviation=np.std(raw_data_hist6_3_con)
raw_data_hist6_4_sum_deviation=np.std(raw_data_hist6_4_con)

print '---------------------------------'
print '---------------------------------'
print '---------------------------------'

print 'raw_data_hist1_1_sum_mean' ,raw_data_hist1_1_sum_mean
print 'raw_data_hist1_2_sum_mean' ,raw_data_hist1_2_sum_mean
print 'raw_data_hist1_3_sum_mean' ,raw_data_hist1_3_sum_mean
print 'raw_data_hist1_4_sum_mean' ,raw_data_hist1_4_sum_mean

print '---------------------------------'

print 'raw_data_hist2_1_sum_mean' ,raw_data_hist2_1_sum_mean
print 'raw_data_hist2_2_sum_mean' ,raw_data_hist2_2_sum_mean
print 'raw_data_hist2_3_sum_mean' ,raw_data_hist2_3_sum_mean
print 'raw_data_hist2_4_sum_mean' ,raw_data_hist2_4_sum_mean

print '---------------------------------'

print 'raw_data_hist3_1_sum_mean' ,raw_data_hist3_1_sum_mean
print 'raw_data_hist3_2_sum_mean' ,raw_data_hist3_2_sum_mean
print 'raw_data_hist3_3_sum_mean' ,raw_data_hist3_3_sum_mean
print 'raw_data_hist3_4_sum_mean' ,raw_data_hist3_4_sum_mean

print '---------------------------------'

print 'raw_data_hist4_1_sum_mean' ,raw_data_hist4_1_sum_mean
print 'raw_data_hist4_2_sum_mean' ,raw_data_hist4_2_sum_mean
print 'raw_data_hist4_3_sum_mean' ,raw_data_hist4_3_sum_mean
print 'raw_data_hist4_4_sum_mean' ,raw_data_hist4_4_sum_mean

print '---------------------------------'


print 'raw_data_hist5_1_sum_mean' ,raw_data_hist5_1_sum_mean
print 'raw_data_hist5_2_sum_mean' ,raw_data_hist5_2_sum_mean
print 'raw_data_hist5_3_sum_mean' ,raw_data_hist5_3_sum_mean
print 'raw_data_hist5_4_sum_mean' ,raw_data_hist5_4_sum_mean

print '---------------------------------'

print 'raw_data_hist6_1_sum_mean' ,raw_data_hist6_1_sum_mean
print 'raw_data_hist6_2_sum_mean' ,raw_data_hist6_2_sum_mean
print 'raw_data_hist6_3_sum_mean' ,raw_data_hist6_3_sum_mean
print 'raw_data_hist6_4_sum_mean' ,raw_data_hist6_4_sum_mean

print '---------------------------------'

print 'raw_data_hist1_1_sum_deviation' ,raw_data_hist1_1_sum_deviation
print 'raw_data_hist1_2_sum_deviation' ,raw_data_hist1_2_sum_deviation
print 'raw_data_hist1_3_sum_deviation' ,raw_data_hist1_3_sum_deviation
print 'raw_data_hist1_4_sum_deviation' ,raw_data_hist1_4_sum_deviation

print '---------------------------------'

print 'raw_data_hist2_1_sum_deviation' ,raw_data_hist2_1_sum_deviation
print 'raw_data_hist2_2_sum_deviation' ,raw_data_hist2_2_sum_deviation
print 'raw_data_hist2_3_sum_deviation' ,raw_data_hist2_3_sum_deviation
print 'raw_data_hist2_4_sum_deviation' ,raw_data_hist2_4_sum_deviation

print '---------------------------------'

print 'raw_data_hist3_1_sum_deviation' ,raw_data_hist3_1_sum_deviation
print 'raw_data_hist3_2_sum_deviation' ,raw_data_hist3_2_sum_deviation
print 'raw_data_hist3_3_sum_deviation' ,raw_data_hist3_3_sum_deviation
print 'raw_data_hist3_4_sum_deviation' ,raw_data_hist3_4_sum_deviation

print '---------------------------------'

print 'raw_data_hist4_1_sum_deviation' ,raw_data_hist4_1_sum_deviation
print 'raw_data_hist4_2_sum_deviation' ,raw_data_hist4_2_sum_deviation
print 'raw_data_hist4_3_sum_deviation' ,raw_data_hist4_3_sum_deviation
print 'raw_data_hist4_4_sum_deviation' ,raw_data_hist4_4_sum_deviation

print '---------------------------------'

print 'raw_data_hist5_1_sum_deviation' ,raw_data_hist5_1_sum_deviation
print 'raw_data_hist5_2_sum_deviation' ,raw_data_hist5_2_sum_deviation
print 'raw_data_hist5_3_sum_deviation' ,raw_data_hist5_3_sum_deviation
print 'raw_data_hist5_4_sum_deviation' ,raw_data_hist5_4_sum_deviation

print '---------------------------------'

print 'raw_data_hist6_1_sum_deviation' ,raw_data_hist6_1_sum_deviation
print 'raw_data_hist6_2_sum_deviation' ,raw_data_hist6_2_sum_deviation
print 'raw_data_hist6_3_sum_deviation' ,raw_data_hist6_3_sum_deviation
print 'raw_data_hist6_4_sum_deviation' ,raw_data_hist6_4_sum_deviation

print '---------------------------------'
print '---------------------------------'
print '---------------------------------'
print '---------------------------------'

print len(raw_data_hist1_1_sum)


np.savetxt('raw_data_hist3_1_con_file',raw_data_hist3_1_con,newline='\n', delimiter='', header='raw_data_hist3_1_con')
np.savetxt('raw_data_hist3_2_con_file',raw_data_hist3_2_con,newline='\n', delimiter='', header='raw_data_hist3_2_con')
np.savetxt('raw_data_hist3_3_con_file',raw_data_hist3_3_con,newline='\n', delimiter='', header='raw_data_hist3_3_con')
np.savetxt('raw_data_hist3_4_con_file',raw_data_hist3_4_con,newline='\n', delimiter='', header='raw_data_hist3_4_con')

np.savetxt('raw_data_hist4_1_con_file',raw_data_hist4_1_con,newline='\n', delimiter='', header='raw_data_hist4_1_con')
np.savetxt('raw_data_hist4_2_con_file',raw_data_hist4_2_con,newline='\n', delimiter='', header='raw_data_hist4_2_con')
np.savetxt('raw_data_hist4_3_con_file',raw_data_hist4_3_con,newline='\n', delimiter='', header='raw_data_hist4_3_con')
np.savetxt('raw_data_hist4_4_con_file',raw_data_hist4_4_con,newline='\n', delimiter='', header='raw_data_hist4_4_con')

np.savetxt('raw_data_hist5_1_con_file',raw_data_hist5_1_con,newline='\n', delimiter='', header='raw_data_hist5_1_con')
np.savetxt('raw_data_hist5_2_con_file',raw_data_hist5_2_con,newline='\n', delimiter='', header='raw_data_hist5_2_con')
np.savetxt('raw_data_hist5_3_con_file',raw_data_hist5_3_con,newline='\n', delimiter='', header='raw_data_hist5_3_con')
np.savetxt('raw_data_hist5_4_con_file',raw_data_hist5_4_con,newline='\n', delimiter='', header='raw_data_hist5_4_con')



plt.figure(1)

plt.subplot(6,4,1)
plt.hist(raw_data_hist1_1_con, bins=histogram_x)
plt.ylabel('raw_data_hist1_1_sum')
plt.subplot(6,4,2)
plt.hist(raw_data_hist1_2_con, bins=histogram_x)
plt.ylabel('raw_data_hist1_2_sum')
plt.subplot(6,4,3)
plt.hist(raw_data_hist1_3_con, bins=histogram_x)
plt.ylabel('raw_data_hist1_3_sum')
plt.subplot(6,4,4)
plt.hist(raw_data_hist1_4_con, bins=histogram_x)
plt.ylabel('raw_data_hist1_4_sum')

plt.subplot(6,4,5)
plt.hist(raw_data_hist2_1_con, bins=histogram_x)
plt.ylabel('raw_data_hist2_1_sum')
plt.subplot(6,4,6)
plt.hist(raw_data_hist2_2_con, bins=histogram_x)
plt.ylabel('raw_data_hist2_2_sum')
plt.subplot(6,4,7)
plt.hist(raw_data_hist2_3_con, bins=histogram_x)
plt.ylabel('raw_data_hist2_3_sum')
plt.subplot(6,4,8)
plt.hist(raw_data_hist2_4_con, bins=histogram_x)
plt.ylabel('raw_data_hist2_4_sum')

plt.subplot(6,4,9)
plt.hist(raw_data_hist3_1_con, bins=histogram_x)
plt.ylabel('raw_data_hist3_1_sum')
plt.subplot(6,4,10)
plt.hist(raw_data_hist3_2_con, bins=histogram_x)
plt.ylabel('raw_data_hist3_2_sum')
plt.subplot(6,4,11)
plt.hist(raw_data_hist3_3_con, bins=histogram_x)
plt.ylabel('raw_data_hist3_3_sum')
plt.subplot(6,4,12)
plt.hist(raw_data_hist3_4_con, bins=histogram_x)
plt.ylabel('raw_data_hist3_4_sum')

plt.subplot(6,4,13)
plt.hist(raw_data_hist4_1_con, bins=histogram_x)
plt.ylabel('raw_data_hist4_1_sum')
plt.subplot(6,4,14)
plt.hist(raw_data_hist4_2_con, bins=histogram_x)
plt.ylabel('raw_data_hist4_2_sum')
plt.subplot(6,4,15)
plt.hist(raw_data_hist4_3_con, bins=histogram_x)
plt.ylabel('raw_data_hist4_3_sum')
plt.subplot(6,4,16)
plt.hist(raw_data_hist4_4_con, bins=histogram_x)
plt.ylabel('raw_data_hist4_4_sum')


plt.subplot(6,4,17)
plt.hist(raw_data_hist5_1_con, bins=histogram_x)
plt.ylabel('raw_data_hist5_1_sum')
plt.subplot(6,4,18)
plt.hist(raw_data_hist5_2_con, bins=histogram_x)
plt.ylabel('raw_data_hist5_2_sum')
plt.subplot(6,4,19)
plt.hist(raw_data_hist5_3_con, bins=histogram_x)
plt.ylabel('raw_data_hist5_3_sum')
plt.subplot(6,4,20)
plt.hist(raw_data_hist5_4_con, bins=histogram_x)
plt.ylabel('raw_data_hist5_4_sum')


plt.subplot(6,4,21)
plt.hist(raw_data_hist6_1_con, bins=histogram_x)
plt.ylabel('raw_data_hist6_1_sum')
plt.subplot(6,4,22)
plt.hist(raw_data_hist6_2_con, bins=histogram_x)
plt.ylabel('raw_data_hist6_2_sum')
plt.subplot(6,4,23)
plt.hist(raw_data_hist6_3_con, bins=histogram_x)
plt.ylabel('raw_data_hist6_3_sum')
plt.subplot(6,4,24)
plt.hist(raw_data_hist6_4_con, bins=histogram_x)
plt.ylabel('raw_data_hist6_4_sum')

plt.show()








