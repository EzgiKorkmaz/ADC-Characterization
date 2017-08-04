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


print fpga.listdev()

print fpga.listbof()



fpga.write_int('fft_shift',2**11-1)
fpga.write_int('adc16_use_synth',0)
fpga.write_int('sync_gen2_sync',1)
fpga.write_int('sync_gen1_sync_period_var',2**16-2)
fpga.write_int('sync_gen1_sync_period_sel',1)


print fpga.est_brd_clk()

fpga.write_int('cnt_rst',1)
print fpga.read_int('acc_len')



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

### Parameter Setting ###

j=cmath.sqrt(-1)
fpga.write_int('acc_len',2*10**5)
Fs=250*10**6

length_acc=2000

a=np.arange(1024)
a=a[28:233]
slice_length=len(a)


### Define Arrays ###

autocor_fft3out2_mean=np.arange(length_acc,dtype=np.float64)
autocor_fft3out2_sliced=np.arange(slice_length,dtype=np.float64)
auto_div_cross=np.zeros(1024,dtype=np.float64)
t_auto=np.arange(length_acc,dtype=np.float64)
division_auto=np.zeros(length_acc,dtype=np.float64)
autocor_fft3out2_8=np.zeros(1024,dtype=np.float64)
autocor_fft3out2_sum_8=np.zeros(1024,dtype=np.float64)
autocor_fft3out28_sliced=np.arange(slice_length,dtype=np.float64)
autocor_fft3out28_sum=np.arange(slice_length,dtype=np.float64)

cor_fft3out1_fft3out2_sum_re=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_mean_re=np.arange(length_acc,dtype=np.float64)
cor_fft3out1_fft3out2_mean_im=np.arange(length_acc,dtype=np.float64)

t=np.arange(length_acc,dtype=np.float64)

cor_fft3out1_fft3out2_mean=np.arange(length_acc,dtype=np.float64)

cor_fft3out1_fft3out2_re=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_im=np.zeros(1024,dtype=np.float64)

cor_fft3out1_fft3out2_sum=np.arange(slice_length,dtype=np.float64)
cor_fft3out1_fft3out2=np.arange(slice_length,dtype=np.float64)
division=np.zeros(length_acc,dtype=np.float64)
cor_fft3out1_fft3out2_sliced_re=np.arange(slice_length,dtype=np.float64)
cor_fft3out1_fft3out2_sliced_im=np.arange(slice_length,dtype=np.float64)

cor_fft3out1_fft3out2_re=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_im=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_mag=np.arange(slice_length,dtype=np.float64)
cor_fft3out1_fft3out2_mag_sliced=np.arange(slice_length,dtype=np.float64)
cor_fft3out1_fft3out2_sum=np.arange(slice_length,dtype=np.float64)

cor_fft3out1_fft3out2_sum_1=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_mag_1=np.zeros(1024,dtype=np.float64)

cor_fft3out1_fft3out2_re=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_im=np.zeros(1024,dtype=np.float64)

cor_fft3out1_fft3out2_mag_momentary=np.zeros(1024,dtype=np.float64)

cor_fft3out1_fft3out2_sum_re_sq=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_sum_im_sq=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_mag_momentary_1=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_mag_1=np.zeros(1024,dtype=np.float64)
cor_fft3out1_fft3out2_mean_mag=np.arange(length_acc,dtype=np.float64)


autocor_fft3out2_sum_1_sq=np.zeros(1024,dtype=np.float64)
autocor_fft3out2_sum_8_sq=np.zeros(1024,dtype=np.float64)
multi_mean_auto=np.zeros(1024,dtype=np.float64)
corr_phase=np.zeros(1024,dtype=np.float64)


### First value of Sum Autocorrelation ###

autocor_fft3out2=struct.unpack('>1024q',fpga.read('Correlator_fft2_out1_Memory2_SharedBRAM3_wideband',8192,0))
autocor_fft3out2_sliced=autocor_fft3out2[28:233]
autocor_fft3out2_sum=autocor_fft3out2_sliced

### First value of Sum Crosscorrelation ###

cor_fft3out1_fft3out2_re=np.array(struct.unpack('>1024q',fpga.read('Correlator_fft3_out1_Memory1_SharedBRAM1_wideband',8192,0)),dtype=np.float64)
cor_fft3out1_fft3out2_im=np.array(struct.unpack('>1024q',fpga.read('Correlator_fft3_out1_Memory1_SharedBRAM2_wideband',8192,0)),dtype=np.float64)
autocor_fft3out2_1=struct.unpack('>1024q',fpga.read('Correlator_fft3_out1_Memory1_SharedBRAM3_wideband',8192,0))
autocor_fft3out2_8=struct.unpack('>1024q',fpga.read('Correlator_fft3_out1_Memory1_SharedBRAM4_wideband',8192,0))

cor_fft3out1_fft3out2_sum_re=cor_fft3out1_fft3out2_re
cor_fft3out1_fft3out2_sum_im=cor_fft3out1_fft3out2_im


autocor_fft3out2_sum_1=autocor_fft3out2_1
autocor_fft3out2_sum_8=autocor_fft3out2_8

### Open Files ###

cross_sum_re=open('cross_sum_re.txt','w')
cross_sum_im=open('cross_sum_im.txt','w')

auto_sum_1=open('auto_sum_1.txt','w')
auto_sum_8=open('auto_sum_8.txt','w')

mean_div_acclen_cross=open('mean_div_acclen_cross.txt','w')
mean_div_acclen_auto=open('mean_div_acclen_auto.txt','w')

auto_cross_ratio=open('auto_cross_ratio.txt','w')
phase_cross=open('phase_cross.txt','w')

cross_sum_mag=open('cross_sum_mag.txt','w')
auto_mean_6=open('auto_mean_6.txt','w')

cross_mean=open('cross_mean.txt','w')

### For Loop Start ###


for m in range (1,length_acc):
 
 print 'Loop value:' ,m

 acc_cnt=fpga.read_int('acc_cnt')
 acc_cnt_loop=fpga.read_int('acc_cnt')
 print fpga.read_int('acc_cnt')

 while (acc_cnt==acc_cnt_loop):
  acc_cnt_loop=fpga.read_int('acc_cnt')
  print fpga.read_int('acc_cnt')
  time.sleep(0.001)
 print time.time()
 

 cor_fft3out1_fft3out2_re=np.array(struct.unpack('>1024q',fpga.read('Correlator_fft3_out1_Memory1_SharedBRAM1_wideband',8192,0)),dtype=np.float64)
 cor_fft3out1_fft3out2_im=np.array(struct.unpack('>1024q',fpga.read('Correlator_fft3_out1_Memory1_SharedBRAM2_wideband',8192,0)),dtype=np.float64)
 print fpga.read_int('acc_cnt')
 

 autocor_fft3out2_1=struct.unpack('>1024q',fpga.read('Correlator_fft3_out1_Memory1_SharedBRAM3_wideband',8192,0))
 autocor_fft3out2_8=struct.unpack('>1024q',fpga.read('Correlator_fft3_out1_Memory1_SharedBRAM4_wideband',8192,0))
 

### Concatenate crosscorrelation ###

 cor_fft3out1_fft3out2_sum_re_pre=cor_fft3out1_fft3out2_sum_re   # [m-1]th value of the summation of sum of the real part of the cross
 cor_fft3out1_fft3out2_sum_im_pre=cor_fft3out1_fft3out2_sum_im   # [m-1]th value of the summation of sum of the imaginary part of the cross

 cor_fft3out1_fft3out2_sum_re_con=np.concatenate([cor_fft3out1_fft3out2_sum_re_pre,cor_fft3out1_fft3out2_sum_re])
 cor_fft3out1_fft3out2_sum_im_con=np.concatenate([cor_fft3out1_fft3out2_sum_im_pre,cor_fft3out1_fft3out2_sum_im])
 
 print cor_fft3out1_fft3out2_sum_re_con

 np.savetxt('cross_sum_re' , cor_fft3out1_fft3out2_sum_re_con)
 np.savetxt('cross_sum_im' , cor_fft3out1_fft3out2_sum_re_con)


### Sum the real and imginary part of Cross and take the magnitude ###


 cor_fft3out1_fft3out2_sum_re=np.add(cor_fft3out1_fft3out2_sum_re,cor_fft3out1_fft3out2_re) 
 cor_fft3out1_fft3out2_sum_im=np.add(cor_fft3out1_fft3out2_sum_im,cor_fft3out1_fft3out2_im)

 cor_fft3out1_fft3out2_sum_re_con=np.concatenate([cor_fft3out1_fft3out2_sum_re_pre,cor_fft3out1_fft3out2_sum_re])
 cor_fft3out1_fft3out2_sum_im_con=np.concatenate([cor_fft3out1_fft3out2_sum_im_pre,cor_fft3out1_fft3out2_sum_im])

 complex_val = cor_fft3out1_fft3out2_sum_re + 1j*cor_fft3out1_fft3out2_sum_im
 cor_fft3out1_fft3out2_mag = np.abs(complex_val)
 
 cor_fft3out1_fft3out2_mag_momentary=cor_fft3out1_fft3out2_mag[28:233]
 cor_fft3out1_fft3out2_mean_mag[m]=np.mean(cor_fft3out1_fft3out2_mag_momentary)

 t[m]=m*1*10**5
 division[m]=float(cor_fft3out1_fft3out2_mean_mag[m])/float(t[m])


### Concatenate the Autocorrelation ###

 
 autocor_fft3out2_sum_1_pre=autocor_fft3out2_sum_1   # [m-1]th value of the summation for autocorrelation
 autocor_fft3out2_sum_8_pre=autocor_fft3out2_sum_8   # [m-1]th value of the summation for autocorrelation
 autocor_fft3out2_sum_1=np.add(autocor_fft3out2_1,autocor_fft3out2_sum_1)
 autocor_fft3out2_sum_8=np.add(autocor_fft3out2_8,autocor_fft3out2_sum_8)
 
 autocor_fft3out2_sum_1_con=np.concatenate([autocor_fft3out2_sum_1_pre,autocor_fft3out2_sum_1])
 autocor_fft3out2_sum_8_con=np.concatenate([autocor_fft3out2_sum_8_pre,autocor_fft3out2_sum_8])

 np.savetxt('auto_sum_1' , autocor_fft3out2_sum_1_con)
 np.savetxt('auto_sum_8' , autocor_fft3out2_sum_8_con)


 ### Slice the autocorrelation,add and take the mean ### 



 autocor_fft3out2_1_sliced=autocor_fft3out2_1[28:233]
 autocor_fft3out2_sum=np.add(autocor_fft3out2_sliced,autocor_fft3out2_sum)
 autocor_fft3out2_mean[m]=np.mean(autocor_fft3out2_sum)
 t_auto[m]=m*1.*10**5
 division_auto[m]=autocor_fft3out2_mean[m]/float(t_auto[m])



cor_fft3out1_fft3out2_sliced_re=cor_fft3out1_fft3out2_sum_re[28:233]
cor_fft3out1_fft3out2_sliced_im=cor_fft3out1_fft3out2_sum_im[28:233]



### Magnitude of Summation Crosscorrelation ###

complex_val = cor_fft3out1_fft3out2_sum_re + 1j*cor_fft3out1_fft3out2_sum_im 
cor_fft3out1_fft3out2_mag = np.abs(complex_val)



### Phase of the Crosscorrelation ###

corr_phase=numpy.arctan2(cor_fft3out1_fft3out2_sum_re,cor_fft3out1_fft3out2_sum_im)

### Multiplicative Mean of Autocorretlation ###

autocor_fft3out2_sum_1_sq=np.sqrt(autocor_fft3out2_sum_1)
autocor_fft3out2_sum_8_sq=np.sqrt(autocor_fft3out2_sum_8)
multi_mean_auto=np.multiply(autocor_fft3out2_sum_1_sq,autocor_fft3out2_sum_8_sq)


### Autocorrelation / Crosscorrelation ###

for m in range (1,1024):

 auto_div_cross[m]=float(multi_mean_auto[m])/float(cor_fft3out1_fft3out2_mag[m])



### Save Text ###

np.savetxt('mean_div_acclen_cross' , division)
np.savetxt('mean_div_acclen_auto' , division_auto)
np.savetxt('auto_cross_ratio' , auto_div_cross)
np.savetxt('phase_cross' , corr_phase)
np.savetxt('cross_sum_mag' , cor_fft3out1_fft3out2_mag)
np.savetxt('auto_mean_6' , autocor_fft3out2_mean)
np.savetxt('cross_mean' , cor_fft3out1_fft3out2_mean_mag)


### Frequency Axis ###

cor_fft3out1_fft3out2_len=len(cor_fft3out1_fft3out2_mag)
print cor_fft3out1_fft3out2_len
cor_fft3out1_fft3out2_freq=np.linspace(0,Fs,cor_fft3out1_fft3out2_len)

cor_fft3out1_fft3out2_freq_sliced=cor_fft3out1_fft3out2_freq[28:233]
cor_fft3out1_fft3out2_freq_sliced_len=len(cor_fft3out1_fft3out2_freq_sliced)
print cor_fft3out1_fft3out2_freq_sliced_len

autocor_fft3out2_len=len(autocor_fft3out2)
autocor_fft3out2_freq=np.linspace(0,Fs,autocor_fft3out2_len)





### Seperation of first values ###

auto_div_cross_1=auto_div_cross[3:1024]
autocor_fft3out2_freq_1=autocor_fft3out2_freq[3:1024]

print auto_div_cross_1[152]
print auto_div_cross_1[151]
print auto_div_cross_1[150]

division=division[2:]
division_auto=division_auto[2:]

t_1=t[2:]
t_auto=t_auto[2:]

print autocor_fft3out2_sum_1[367]
print autocor_fft3out2_sum_1[368]
print autocor_fft3out2_sum_1[369]
print autocor_fft3out2_sum_1[370]
print autocor_fft3out2_sum_1[371]






plt.subplot(3,3,1)
plt.plot(t_1,division)
plt.ylabel('Mean of Crosscorrelation divided by Accumulation length')
plt.xlabel('Accumulation Length')
plt.title('Mean of Crosscorrelation/Accumulation length vs Accumulation length')


plt.subplot(3,3,2)
plt.plot(t_auto,division_auto)
plt.ylabel('Mean of Autocorrelation divided by Accumulation length')
plt.xlabel('Accumulation Length')
plt.title('Mean of Autocorrelation/Accumulation length vs Accumulation length')

plt.subplot(3,3,3)
plt.semilogy(cor_fft3out1_fft3out2_freq,cor_fft3out1_fft3out2_mag)
plt.ylabel('Crosscorrelation of Input8 & Input9')
plt.xlabel('Frequency(Hz)')
plt.title('Crosscorrelation of Input8 & Input9 vs Frequency')

plt.subplot(3,3,4)
plt.semilogy(autocor_fft3out2_freq,autocor_fft3out2_sum_1)
plt.ylabel('Autocorrelation of Input9')
plt.xlabel('Frequency(Hz)')
plt.title('Autocorrelation of Input9 vs Frequency')


plt.subplot(3,3,5)
plt.semilogy(autocor_fft3out2_freq,autocor_fft3out2_sum_8)
plt.ylabel('Autocorrelation of Input8')
plt.xlabel('Frequency(Hz)')
plt.title('Autocorrelation of Input8 vs Frequency')

plt.subplot(3,3,6)
plt.semilogy(autocor_fft3out2_freq_1,auto_div_cross_1)
plt.ylabel('Autocorrelation/Crosscorrelation')
plt.xlabel('Frequency(Hz)')
plt.title('Autocorrelation/Crosscorrelation vs Frequency')


plt.subplot(3,3,7)
plt.plot(t,cor_fft3out1_fft3out2_mean)
plt.ylabel('Mean of Crosscorrelation')
plt.xlabel('Frequency(Hz)')
plt.title('Mean of Crosscorrelation vs Frequency')


plt.subplot(3,3,8)
plt.plot(cor_fft3out1_fft3out2_freq,corr_phase)
plt.xlabel('Frequency(Hz)')
plt.ylabel('Phase of Crosscorrelation')
plt.title('Phase of Crosscorrelation vs Frequency')

plt.subplot(3,3,9)
plt.plot(autocor_fft3out2_freq[3:],cor_fft3out1_fft3out2_sum_re[3:])
plt.plot(autocor_fft3out2_freq[3:],cor_fft3out1_fft3out2_sum_im[3:])
plt.ylabel('Crosscorrelation Real and Imaginary Parts')
plt.xlabel('Frequency(Hz)')
plt.title('Crosscorrelation Real and Imaginary Parts vs Frequency')


plt.show()

















