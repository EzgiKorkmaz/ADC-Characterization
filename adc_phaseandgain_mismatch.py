# Measure phase and gain mismatch for multicore ADC.




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



length_acc=5
count_time=50


input_160mhz_ph = [115.2, -129.6, -14.4, 115.2, -129.6, 115.2 ]


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




phase_31_32_calib_array = np.zeros(count_time)
phase_31_33_calib_array = np.zeros(count_time)
phase_31_34_calib_array = np.zeros(count_time)
phase_32_33_calib_array = np.zeros(count_time)
phase_32_34_calib_array = np.zeros(count_time)
phase_33_34_calib_array = np.zeros(count_time)

phase_31_32_bin  = np.zeros(count_time)
phase_31_33_bin  = np.zeros(count_time)
phase_31_34_bin  = np.zeros(count_time)
phase_32_33_bin  = np.zeros(count_time)
phase_32_34_bin  = np.zeros(count_time)
phase_33_34_bin  = np.zeros(count_time)


corr_31_32_abs_bin =  np.zeros(count_time)
corr_31_33_abs_bin =  np.zeros(count_time)
corr_31_34_abs_bin =  np.zeros(count_time)
corr_32_33_abs_bin =  np.zeros(count_time)
corr_32_34_abs_bin =  np.zeros(count_time)
corr_33_34_abs_bin =  np.zeros(count_time)



corr_41_42_abs_bin =  np.zeros(count_time)
corr_41_43_abs_bin =  np.zeros(count_time)
corr_41_44_abs_bin =  np.zeros(count_time)
corr_42_43_abs_bin =  np.zeros(count_time)
corr_42_44_abs_bin =  np.zeros(count_time)
corr_43_44_abs_bin =  np.zeros(count_time)



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
for k in range (1,count_time):


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

 raw_data_hist1 = struct.unpack('>2048b',fpga.snapshot_get('snapshot1',man_trig=True,man_valid=True)['data'])
 raw_data_hist2 = struct.unpack('>2048b',fpga.snapshot_get('snapshot2',man_trig=True,man_valid=True)['data'])
 raw_data_hist3 = struct.unpack('>2048b',fpga.snapshot_get('snapshot4',man_trig=True,man_valid=True)['data'])
 raw_data_hist4 = struct.unpack('>2048b',fpga.snapshot_get('snapshot5',man_trig=True,man_valid=True)['data'])
 raw_data_hist5 = struct.unpack('>2048b',fpga.snapshot_get('snapshot6',man_trig=True,man_valid=True)['data'])
 raw_data_hist6 = struct.unpack('>2048b',fpga.snapshot_get('snapshot7',man_trig=True,man_valid=True)['data'])

#struct.unpack('>2048b',fpga.snapshot_get('snapshot4',man_trig=True,man_valid=True)['data'])


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

  raw_data_hist1 = struct.unpack('>2048b',fpga.snapshot_get('snapshot1',man_trig=True,man_valid=True)['data'])
  raw_data_hist2 = struct.unpack('>2048b',fpga.snapshot_get('snapshot2',man_trig=True,man_valid=True)['data'])
  raw_data_hist3 = struct.unpack('>2048b',fpga.snapshot_get('snapshot4',man_trig=True,man_valid=True)['data'])
  raw_data_hist4 = struct.unpack('>2048b',fpga.snapshot_get('snapshot5',man_trig=True,man_valid=True)['data'])
  raw_data_hist5 = struct.unpack('>2048b',fpga.snapshot_get('snapshot6',man_trig=True,man_valid=True)['data'])
  raw_data_hist6 = struct.unpack('>2048b',fpga.snapshot_get('snapshot7',man_trig=True,man_valid=True)['data'])


  #struct.unpack('>2048b',fpga.snapshot_get('snapshot4',man_trig=True,man_valid=True)['data'])

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

 Fs=125*10**6

 print len(raw_data_hist3_1_con)

 raw_data_hist3_1_fft = np.fft.rfft(raw_data_hist3_1_con, n=2048)
 raw_data_hist3_2_fft = np.fft.rfft(raw_data_hist3_2_con, n=2048)
 raw_data_hist3_3_fft = np.fft.rfft(raw_data_hist3_3_con, n=2048)
 raw_data_hist3_4_fft = np.fft.rfft(raw_data_hist3_4_con, n=2048)




 raw_data_hist4_1_fft = np.fft.rfft(raw_data_hist4_1_con, n=2048)
 raw_data_hist4_2_fft = np.fft.rfft(raw_data_hist4_2_con, n=2048)
 raw_data_hist4_3_fft = np.fft.rfft(raw_data_hist4_3_con, n=2048)
 raw_data_hist4_4_fft = np.fft.rfft(raw_data_hist4_4_con, n=2048)




 corr_31_32 = np.multiply(np.conj(raw_data_hist3_1_fft) , raw_data_hist3_2_fft)
 corr_31_33 = np.multiply(np.conj(raw_data_hist3_1_fft) , raw_data_hist3_3_fft)
 corr_31_34 = np.multiply(np.conj(raw_data_hist3_1_fft) , raw_data_hist3_4_fft)
 corr_32_33 = np.multiply(np.conj(raw_data_hist3_2_fft) , raw_data_hist3_3_fft)
 corr_32_34 = np.multiply(np.conj(raw_data_hist3_2_fft) , raw_data_hist3_4_fft)
 corr_33_34 = np.multiply(np.conj(raw_data_hist3_3_fft) , raw_data_hist3_4_fft)


 auto_31 = np.multiply(np.conj(raw_data_hist3_1_fft) , raw_data_hist3_1_fft)
 auto_32 = np.multiply(np.conj(raw_data_hist3_2_fft) , raw_data_hist3_2_fft)
 auto_33 = np.multiply(np.conj(raw_data_hist3_3_fft) , raw_data_hist3_3_fft)
 auto_34 = np.multiply(np.conj(raw_data_hist3_4_fft) , raw_data_hist3_4_fft)

 NFFT = 1024

 corr_31_32_abs=np.abs(corr_31_32)
 corr_31_33_abs=np.abs(corr_31_33)
 corr_31_34_abs=np.abs(corr_31_34)
 corr_32_33_abs=np.abs(corr_32_33)
 corr_32_34_abs=np.abs(corr_32_34)
 corr_33_34_abs=np.abs(corr_33_34)
 


 corr_31_32_abs_bin[k]= corr_31_32_abs[574]
 corr_31_33_abs_bin[k]= corr_31_33_abs[574]
 corr_31_34_abs_bin[k]= corr_31_34_abs[574]
 corr_32_33_abs_bin[k]= corr_32_33_abs[574]
 corr_32_34_abs_bin[k]= corr_32_34_abs[574]
 corr_33_34_abs_bin[k]= corr_33_34_abs[574]






 phase_31_32 = np.angle( corr_31_32 ,deg=True )
 phase_31_33 = np.angle( corr_31_33 ,deg=True)
 phase_31_34 = np.angle( corr_31_34 ,deg=True)
 phase_32_33 = np.angle( corr_32_33 ,deg=True)
 phase_32_34 = np.angle( corr_32_34 ,deg=True)
 phase_33_34 = np.angle( corr_33_34 ,deg=True)

 auto_31_abs = np.abs(auto_31)
 auto_32_abs = np.abs(auto_32)
 auto_33_abs = np.abs(auto_33)
 auto_34_abs = np.abs(auto_34)

 corr_41_42 = np.multiply(np.conj(raw_data_hist4_1_fft) , raw_data_hist4_2_fft)
 corr_41_43 = np.multiply(np.conj(raw_data_hist4_1_fft) , raw_data_hist4_3_fft)
 corr_41_44 = np.multiply(np.conj(raw_data_hist4_1_fft) , raw_data_hist4_4_fft)
 corr_42_43 = np.multiply(np.conj(raw_data_hist4_2_fft) , raw_data_hist4_3_fft)
 corr_42_44 = np.multiply(np.conj(raw_data_hist4_2_fft) , raw_data_hist4_4_fft)
 corr_43_44 = np.multiply(np.conj(raw_data_hist4_3_fft) , raw_data_hist4_4_fft)

 auto_41 = np.multiply(np.conj(raw_data_hist4_1_fft) , raw_data_hist4_1_fft)
 auto_42 = np.multiply(np.conj(raw_data_hist4_2_fft) , raw_data_hist4_2_fft)
 auto_43 = np.multiply(np.conj(raw_data_hist4_3_fft) , raw_data_hist4_3_fft)
 auto_44 = np.multiply(np.conj(raw_data_hist4_4_fft) , raw_data_hist4_4_fft)

 auto_41_abs = np.abs(auto_41)
 auto_42_abs = np.abs(auto_42)
 auto_43_abs = np.abs(auto_43)
 auto_44_abs = np.abs(auto_44)


 corr_41_42_abs=np.abs(corr_41_42)
 corr_41_43_abs=np.abs(corr_41_43)
 corr_41_44_abs=np.abs(corr_41_44)
 corr_42_43_abs=np.abs(corr_42_43)
 corr_42_44_abs=np.abs(corr_42_44)
 corr_43_44_abs=np.abs(corr_43_44)


 corr_41_42_abs_bin[k]= corr_41_42_abs[574]
 corr_41_43_abs_bin[k]= corr_41_43_abs[574]
 corr_41_44_abs_bin[k]= corr_41_44_abs[574]
 corr_42_43_abs_bin[k]= corr_42_43_abs[574]
 corr_42_44_abs_bin[k]= corr_42_44_abs[574]
 corr_43_44_abs_bin[k]= corr_43_44_abs[574]






 phase_41_42 = np.angle( corr_41_42 ,deg=True )
 phase_41_43 = np.angle( corr_41_43 ,deg=True)
 phase_41_44 = np.angle( corr_41_44 ,deg=True)
 phase_42_43 = np.angle( corr_42_43 ,deg=True)
 phase_42_44 = np.angle( corr_42_44 ,deg=True)
 phase_43_44 = np.angle( corr_43_44 ,deg=True)


 mean_phase_41_42 = np.mean( phase_41_42 )
 mean_phase_41_43 = np.mean( phase_41_43 )
 mean_phase_41_44 = np.mean( phase_41_44 )
 mean_phase_42_43 = np.mean( phase_42_43 )
 mean_phase_42_44 = np.mean( phase_42_44 )
 mean_phase_43_44 = np.mean( phase_43_44 )



 std_phase_41_42 = np.std( phase_41_42 )
 std_phase_41_43 = np.std( phase_41_43 )
 std_phase_41_44 = np.std( phase_41_44 )
 std_phase_42_43 = np.std( phase_42_43 )
 std_phase_42_44 = np.std( phase_42_44 )
 std_phase_43_44 = np.std( phase_43_44 )


 corr_31_32_div_auto = np.zeros(len(raw_data_hist3_1_fft) , dtype=np.float128)
 corr_31_33_div_auto = np.zeros(len(raw_data_hist3_1_fft) , dtype=np.float128)
 corr_31_34_div_auto = np.zeros(len(raw_data_hist3_1_fft) , dtype=np.float128)
 corr_32_33_div_auto = np.zeros(len(raw_data_hist3_1_fft) , dtype=np.float128)
 corr_32_34_div_auto = np.zeros(len(raw_data_hist3_1_fft) , dtype=np.float128)
 corr_33_34_div_auto = np.zeros(len(raw_data_hist3_1_fft) , dtype=np.float128)
 corr_31_32_div_auto1= np.zeros(len(raw_data_hist3_1_fft) , dtype=np.float128)
 corr_31_32_div_auto2= np.zeros(len(raw_data_hist3_1_fft) , dtype=np.float128)


 auto_31_32 = np.multiply(auto_31_abs, auto_31_abs)
 auto_31_32 = np.sqrt(auto_31_32)
 corr_31_32_div_auto = np.divide(corr_31_32_abs, auto_31_abs , dtype=np.float128)

 auto_31_33 = np.multiply(auto_33_abs, auto_33_abs)
 auto_31_33 = np.sqrt(auto_31_33)
 corr_31_33_div_auto = np.divide(corr_31_33_abs, auto_31_abs , dtype=np.float128)

 auto_31_34 = np.multiply(auto_31_abs, auto_34_abs)
 auto_31_34 = np.sqrt(auto_31_34)
 corr_31_34_div_auto = np.divide(corr_31_34_abs, auto_31_abs , dtype=np.float128)

 auto_32_33 = np.multiply(auto_32_abs, auto_33_abs)
 auto_32_33 = np.sqrt(auto_32_33) 
 corr_32_33_div_auto = np.divide(corr_32_33_abs, auto_32_abs , dtype=np.float128)

 auto_32_34 = np.multiply(auto_32_abs, auto_34_abs)
 auto_32_34 = np.sqrt(auto_32_34)
 corr_32_34_div_auto = np.divide(corr_32_34_abs, auto_32_abs , dtype=np.float128)

 auto_33_34 = np.multiply(auto_33_abs, auto_34_abs)
 auto_33_34 = np.sqrt(auto_33_34)
 corr_33_34_div_auto = np.divide(corr_33_34_abs, auto_33_abs , dtype=np.float128)

 mean_corr_41_42 = np.mean(corr_41_42_abs)
 mean_corr_41_43 = np.mean(corr_41_43_abs)
 mean_corr_41_44 = np.mean(corr_41_44_abs)
 mean_corr_42_43 = np.mean(corr_42_43_abs)
 mean_corr_42_44 = np.mean(corr_42_44_abs)
 mean_corr_43_44 = np.mean(corr_43_44_abs)

 mean_auto_41 = np.mean(auto_41_abs)
 mean_auto_42 = np.mean(auto_42_abs)
 mean_auto_43 = np.mean(auto_43_abs)
 mean_auto_44 = np.mean(auto_44_abs)

 corr_div_auto_41_42 = mean_corr_41_42/(math.sqrt(mean_auto_41*mean_auto_42))
 corr_div_auto_41_43 = mean_corr_41_43/(math.sqrt(mean_auto_41*mean_auto_43))
 corr_div_auto_41_44 = mean_corr_41_44/(math.sqrt(mean_auto_41*mean_auto_44))
 corr_div_auto_42_43 = mean_corr_42_43/(math.sqrt(mean_auto_42*mean_auto_43))
 corr_div_auto_42_44 = mean_corr_42_44/(math.sqrt(mean_auto_42*mean_auto_44))
 corr_div_auto_43_44 = mean_corr_43_44/(math.sqrt(mean_auto_43*mean_auto_44))


#Printing Section #


 print '-------------------------------'
 print '-------------------------------'
 print '-------------------------------'
 print 'phase_41_42[736,737,738,739] :' , phase_41_42[572] ,' ', phase_41_42[573] ,' ',phase_41_42[574],' ',phase_41_42[575],' ',phase_41_42[576]
 print 'phase_41_43[736,737,738,739] :' , phase_41_43[572] ,' ', phase_41_43[573] ,' ',phase_41_43[574],' ',phase_41_43[575],' ',phase_41_43[576]
 print 'phase_41_44[736,737,738,739] :' , phase_41_44[572] ,' ', phase_41_44[573] ,' ',phase_41_44[574],' ',phase_41_44[575],' ',phase_41_44[576]
 print 'phase_42_43[736,737,738,739] :' , phase_42_43[572] ,' ', phase_42_43[573] ,' ',phase_42_43[574],' ',phase_42_43[575],' ',phase_42_43[576]
 print 'phase_42_44[736,737,738,739] :' , phase_42_44[572] ,' ', phase_42_44[573] ,' ',phase_42_44[574],' ',phase_42_44[575],' ',phase_42_44[576]
 print 'phase_43_44[736,737,738,739] :' , phase_43_44[572] ,' ', phase_43_44[573] ,' ',phase_43_44[574],' ',phase_43_44[575],' ',phase_43_44[576]
 print '-------------------------------'
 print '-------------------------------'
 print '-------------------------------'
 print '-------------------------------'
 print 'phase_31_32[736,737,738,739] :' , phase_31_32[572] ,' ', phase_31_32[573] ,' ',phase_31_32[574],' ',phase_31_32[575],' ',phase_31_32[576]
 print 'phase_31_33[736,737,738,739] :' , phase_31_33[572] ,' ', phase_31_33[573] ,' ',phase_31_33[574],' ',phase_31_33[575],' ',phase_31_33[576]
 print 'phase_31_34[736,737,738,739] :' , phase_31_34[572] ,' ', phase_31_34[573] ,' ',phase_31_34[574],' ',phase_31_34[575],' ',phase_31_34[576]
 print 'phase_32_33[736,737,738,739] :' , phase_32_33[572] ,' ', phase_32_33[573] ,' ',phase_32_33[574],' ',phase_32_33[575],' ',phase_32_33[576]
 print 'phase_32_34[736,737,738,739] :' , phase_32_34[572] ,' ', phase_32_34[573] ,' ',phase_32_34[574],' ',phase_32_34[575],' ',phase_32_34[576]
 print 'phase_33_34[736,737,738,739] :' , phase_33_34[572] ,' ', phase_33_34[573] ,' ',phase_33_34[574],' ',phase_33_34[575],' ',phase_33_34[576]
 print '-------------------------------'
 print '-------------------------------'
 print '-------------------------------'
 print '-------------------------------'
 print 'count_time:' ,  k
 print '-------------------------------'
 print '-------------------------------'
 print '-------------------------------'
 
 phase_31_32_bin[k] = phase_31_32[574]
 phase_31_33_bin[k] = phase_31_33[574]
 phase_31_34_bin[k] = phase_31_34[574]
 phase_32_33_bin[k] = phase_32_33[574]
 phase_32_34_bin[k] = phase_32_34[574]
 phase_33_34_bin[k] = phase_33_34[574]
 

phase_31_32_bin = phase_31_32_bin[1:]
phase_31_33_bin = phase_31_33_bin[1:]
phase_31_34_bin = phase_31_34_bin[1:]
phase_32_33_bin = phase_32_33_bin[1:]
phase_32_34_bin = phase_32_34_bin[1:]
phase_33_34_bin = phase_33_34_bin[1:]



corr_41_42_abs_bin = corr_41_42_abs[1:]
corr_41_43_abs_bin = corr_41_43_abs[1:]
corr_41_44_abs_bin = corr_41_44_abs[1:]
corr_42_43_abs_bin = corr_42_43_abs[1:]
corr_42_44_abs_bin = corr_42_44_abs[1:]
corr_43_44_abs_bin = corr_43_44_abs[1:]

corr_31_32_abs_bin = corr_31_32_abs_bin[1:]
corr_31_33_abs_bin = corr_31_33_abs_bin[1:]
corr_31_34_abs_bin = corr_31_34_abs_bin[1:]
corr_32_33_abs_bin = corr_32_33_abs_bin[1:]
corr_32_34_abs_bin = corr_32_34_abs_bin[1:]
corr_33_34_abs_bin = corr_33_34_abs_bin[1:]

phase_31_32_calib = phase_31_32_bin - 115.2
phase_31_33_calib = phase_31_33_bin + 129.6
phase_31_34_calib = phase_31_34_bin + 14.4
phase_32_33_calib = phase_32_33_bin - 115.2
phase_32_34_calib = phase_32_34_bin + 129.6
phase_33_34_calib = phase_33_34_bin - 115.2



phase_31_32_calib_abs = np.abs(phase_31_32_calib)
phase_31_33_calib_abs = np.abs(phase_31_33_calib)
phase_31_34_calib_abs = np.abs(phase_31_34_calib)
phase_32_33_calib_abs = np.abs(phase_32_33_calib)
phase_32_34_calib_abs = np.abs(phase_32_34_calib)
phase_33_34_calib_abs = np.abs(phase_33_34_calib)


phase_31_32_calib_mean = np.mean(phase_31_32_calib_abs)
phase_31_33_calib_mean = np.mean(phase_31_33_calib_abs)
phase_31_34_calib_mean = np.mean(phase_31_34_calib_abs)
phase_32_33_calib_mean = np.mean(phase_32_33_calib_abs)
phase_32_34_calib_mean = np.mean(phase_32_34_calib_abs)
phase_33_34_calib_mean = np.mean(phase_33_34_calib_abs)


phase_31_32_calib_std = np.std(phase_31_32_calib_abs)
phase_31_33_calib_std = np.std(phase_31_33_calib_abs)
phase_31_34_calib_std = np.std(phase_31_34_calib_abs)
phase_32_33_calib_std = np.std(phase_32_33_calib_abs)
phase_32_34_calib_std = np.std(phase_32_34_calib_abs)
phase_33_34_calib_std = np.std(phase_33_34_calib_abs)


corr_31_32_abs_bin_mean = np.mean(corr_31_32_abs_bin)
corr_31_33_abs_bin_mean = np.mean(corr_31_33_abs_bin)
corr_31_34_abs_bin_mean = np.mean(corr_31_34_abs_bin)
corr_32_33_abs_bin_mean = np.mean(corr_32_33_abs_bin)
corr_32_34_abs_bin_mean = np.mean(corr_32_34_abs_bin)
corr_33_34_abs_bin_mean = np.mean(corr_33_34_abs_bin)

corr_31_32_abs_bin_std = np.std(corr_31_32_abs_bin)
corr_31_33_abs_bin_std = np.std(corr_31_33_abs_bin)
corr_31_34_abs_bin_std = np.std(corr_31_34_abs_bin)
corr_32_33_abs_bin_std = np.std(corr_32_33_abs_bin)
corr_32_34_abs_bin_std = np.std(corr_32_34_abs_bin)
corr_33_34_abs_bin_std = np.std(corr_33_34_abs_bin)



print 'phase_31_32_calib: ', phase_31_32_calib
print 'phase_31_32_bin: ', phase_31_32_bin
print '-------------------------------'
print '-------------------------------'
print 'phase_31_33_calib: ', phase_31_33_calib
print 'phase_31_33_bin: ', phase_31_33_bin
print '-------------------------------'
print '-------------------------------'
print 'phase_31_32_calib_std: ', phase_31_32_calib_std
print 'phase_31_33_calib_std: ', phase_31_33_calib_std
print 'phase_31_34_calib_std: ', phase_31_34_calib_std
print 'phase_32_33_calib_std: ', phase_32_33_calib_std
print 'phase_32_34_calib_std: ', phase_32_34_calib_std
print 'phase_33_34_calib_std: ', phase_33_34_calib_std
print '-------------------------------'
print '-------------------------------'
print 'phase_31_32_calib_mean: ', phase_31_32_calib_mean
print 'phase_31_33_calib_mean: ', phase_31_33_calib_mean
print 'phase_31_34_calib_mean: ', phase_31_34_calib_mean
print 'phase_32_33_calib_mean: ', phase_32_33_calib_mean
print 'phase_32_34_calib_mean: ', phase_32_34_calib_mean
print 'phase_33_34_calib_mean: ', phase_33_34_calib_mean
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print 'corr_31_32_abs_bin: ', corr_31_32_abs_bin
print 'corr_31_33_abs_bin: ', corr_31_33_abs_bin
print 'corr_31_34_abs_bin: ', corr_31_34_abs_bin
print 'corr_32_33_abs_bin: ', corr_32_33_abs_bin
print 'corr_32_34_abs_bin: ', corr_32_34_abs_bin
print 'corr_33_34_abs_bin: ', corr_33_34_abs_bin
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print 'corr_31_32_abs_bin_mean: ', corr_31_32_abs_bin_mean
print 'corr_31_33_abs_bin_mean: ', corr_31_33_abs_bin_mean
print 'corr_31_34_abs_bin_mean: ', corr_31_34_abs_bin_mean
print 'corr_32_33_abs_bin_mean: ', corr_32_33_abs_bin_mean
print 'corr_32_34_abs_bin_mean: ', corr_32_34_abs_bin_mean
print 'corr_33_34_abs_bin_mean: ', corr_33_34_abs_bin_mean
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print 'corr_31_32_abs_bin_std: ', corr_31_32_abs_bin_std
print 'corr_31_33_abs_bin_std: ', corr_31_33_abs_bin_std
print 'corr_31_34_abs_bin_std: ', corr_31_34_abs_bin_std
print 'corr_32_33_abs_bin_std: ', corr_32_33_abs_bin_std
print 'corr_32_34_abs_bin_std: ', corr_32_34_abs_bin_std
print 'corr_33_34_abs_bin_std: ', corr_33_34_abs_bin_std
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'
print '-------------------------------'


print len(raw_data_hist1_1_sum)

freqs = np.linspace(0,Fs,NFFT)
freqs2 = np.linspace(0,Fs/2, len(raw_data_hist3_1_fft))
time_in = np.linspace(1,count_time,count_time)

print corr_31_33_abs
print corr_31_34_abs


plt.figure(1)

plt.subplot(6,4,1)
plt.semilogy(freqs2, corr_31_32_abs)
plt.ylabel('corr_31_32_abs')

plt.subplot(6,4,2)
plt.semilogy(freqs2, auto_31)
plt.ylabel('auto_31')

plt.subplot(6,4,3)
plt.semilogy(freqs2, corr_41_42_abs)
plt.ylabel('corr_41_42_abs')

plt.subplot(6,4,4)
plt.semilogy(freqs2, auto_41)
plt.ylabel('auto_41')

plt.subplot(6,4,5)
plt.semilogy(freqs2, corr_31_33_abs)
plt.ylabel('corr_31_33_abs')

plt.subplot(6,4,6)
plt.semilogy(freqs2, auto_32)
plt.ylabel('auto_32')

plt.subplot(6,4,7)
plt.semilogy(freqs2, corr_41_43_abs)
plt.ylabel('corr_41_43_abs')

plt.subplot(6,4,8)
plt.semilogy(freqs2, auto_42)
plt.ylabel('auto_42')

plt.subplot(6,4,9)
plt.semilogy(freqs2, corr_31_34_abs)
plt.ylabel('corr_31_34_abs')

plt.subplot(6,4,10)
plt.semilogy(freqs2, auto_33)
plt.ylabel('auto_33')

plt.subplot(6,4,11)
plt.semilogy(freqs2, corr_41_44_abs)
plt.ylabel('corr_41_44_abs')

plt.subplot(6,4,12)
plt.semilogy(freqs2, auto_43)
plt.ylabel('auto_43')

plt.subplot(6,4,13)
plt.semilogy(freqs2, corr_32_33_abs)
plt.ylabel('corr_32_33_abs')

plt.subplot(6,4,14)
plt.semilogy(freqs2, auto_34)
plt.ylabel('auto_34')

plt.subplot(6,4,15)
plt.semilogy(freqs2, corr_42_43_abs)
plt.ylabel('corr_42_43_abs')

plt.subplot(6,4,16)
plt.semilogy(freqs2, auto_44)
plt.ylabel('auto_44')

plt.subplot(6,4,17)
plt.semilogy(freqs2, corr_32_34_abs)
plt.ylabel('corr_32_34_abs')

plt.subplot(6,4,19)
plt.semilogy(freqs2, corr_42_44_abs)
plt.ylabel('corr_42_44_abs')

plt.subplot(6,4,21)
plt.semilogy(freqs2, corr_33_34_abs)
plt.ylabel('corr_32_34_abs')

plt.subplot(6,4,23)
plt.semilogy(freqs2, corr_43_44_abs)


plt.figure(2)

plt.subplot(6,1,1)
plt.plot( phase_41_42)
plt.ylabel('phase_41_42')

plt.subplot(6,1,2)
plt.plot( phase_41_43)
plt.ylabel('phase_41_43')

plt.subplot(6,1,3)
plt.plot( phase_41_44)
plt.ylabel('phase_41_44')

plt.subplot(6,1,4)
plt.plot( phase_42_43)
plt.ylabel('phase_42_43')

plt.subplot(6,1,5)
plt.plot( phase_42_44)
plt.ylabel('phase_42_44')

plt.subplot(6,1,6)
plt.plot( phase_43_44)
plt.ylabel('phase_43_44')


plt.figure(3)

plt.subplot(3,2,1)
plt.plot( phase_31_32_calib)
plt.ylabel('phase_31_32_calib[deg]')
plt.xlabel('Number of process loops')

plt.subplot(3,2,2)
plt.plot( phase_31_33_calib)
plt.ylabel('phase_31_33_calib[deg]')
plt.xlabel('Number of process loops')


plt.subplot(3,2,3)
plt.plot(phase_31_34_calib)
plt.ylabel('phase_31_34_calib[deg]')
plt.xlabel('Number of process loops')


plt.subplot(3,2,4)
plt.plot( phase_32_33_calib)
plt.ylabel('phase_32_33_calib[deg]')
plt.xlabel('Number of process loops')


plt.subplot(3,2,5)
plt.plot( phase_32_34_calib)
plt.ylabel('phase_32_34_calib[deg]')
plt.xlabel('Number of process loops')


plt.subplot(3,2,6)
plt.plot( phase_33_34_calib)
plt.ylabel('phase_33_34_calib[deg]')
plt.xlabel('Number of process loops')



plt.figure(4)

plt.subplot(3,2,1)
plt.plot( corr_31_32_abs_bin)
plt.ylabel('Crosscorrelation of $Core_1$ & $Core_2$ for the $F_c$ Bin')
plt.xlabel('Number of process loops')

plt.subplot(3,2,2)
plt.plot( corr_31_33_abs_bin)
plt.ylabel('Crosscorrelation of $Core_1$ & $Core_3$ for the $F_c$ Bin')
plt.xlabel('Number of process loops')


plt.subplot(3,2,3)
plt.plot(corr_31_34_abs_bin)
plt.ylabel('Crosscorrelation of $Core_1$ & $Core_4$ for the $F_c$ Bin')
plt.xlabel('Number of process loops')


plt.subplot(3,2,4)
plt.plot( corr_32_33_abs_bin)
plt.ylabel('Crosscorrelation of $Core_2$ & $Core_3$ for the $F_c$ Bin')
plt.xlabel('Number of process loops')


plt.subplot(3,2,5)
plt.plot( corr_32_34_abs_bin)
plt.ylabel('Crosscorrelation of $Core_2$ & $Core_4$ for the $F_c$ Bin')
plt.xlabel('Number of process loops')


plt.subplot(3,2,6)
plt.plot( corr_33_34_abs_bin)
plt.ylabel('Crosscorrelation of $Core_3$ & $Core_4$ for the $F_c$ Bin')
plt.xlabel('Number of process loops')


plt.show()



