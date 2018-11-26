#coding: utf-8
import numpy as np
import cmath as cm
import matplotlib.pyplot as plt
import wave
import struct
import warnings
import time
warnings.filterwarnings('ignore')

file = "test.wav"
span = 15000
dt = 0.01          # サンプリング間隔
fq1, fq2 = 5, 40    # 周波数
fc, fc2 = 25, 75            # カットオフ周波数

def plot(locate, f, a, b, lab): #plot
    plt.subplot(locate)
    plt.plot(f, label=lab)
    plt.xlabel(a, fontsize=20)
    plt.ylabel(b, fontsize=20)
    plt.grid()
    
def out_wav(name, outd): # wav file output
    outf = name
    wave_file = wave.open(outf, 'w')
    wave_file.setnchannels(ch)
    wave_file.setsampwidth(width)
    wave_file.setnframes(fn)
    wave_file.setframerate(fr)
    wave_file.writeframes(outd)
    wave_file.close()

def dft(data):
    res = []
    N = len(data)
    for k in range(N):
        w = cm.exp(-1j * 2 * cm.pi * k / float(N))
        X_k = 0
        for n in range(N):
            X_k += data[n] * (w ** n)
        res.append(abs(X_k))
    return res

def ifft_data(F, locate, wav): # ifft + plot + output
    f = np.fft.ifft(F)
    outd = [int(x) for x in f]
    outd = struct.pack("h" * len(outd), *outd)
    Amp = np.abs(F)
    plot(locate, f, "time", "signal", "f(n)") # 時間信号（元）
    plot(locate+1, Amp, "freq.", "amp.", "|F(k)|")# 周波数信号(元)
    out_wav(wav, outd)
    
# グラフ
plt.figure()
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10
leg = plt.legend(loc=1, fontsize=25)
# leg.get_frame().set_alpha(1)
    
# read
wave_file = wave.open(file, "rb")
ch = wave_file.getnchannels()
width = wave_file.getsampwidth()
fr = wave_file.getframerate()
fn = wave_file.getnframes()
f = wave_file.readframes(wave_file.getnframes())
wave_file.close()
f = np.frombuffer(f, dtype = "int16")
F = np.fft.fft(f)
N = len(F)            # サンプル数
t = np.arange(0, N*dt, dt) # 時間軸
freq = np.linspace(0, 1.0/dt, N) # 周波数軸

# filter
F2 = F.copy()
F3 = F.copy()
F4 = F.copy()

F2[(freq < fc)] = 0 # high
F3[(freq > fc2)] = 0 #low
F4[(freq < fc/2)] = 0 #band
F4[(fc2/2 < freq)] = 0

ifft_data(F, 421, "original.wav")
ifft_data(F2, 423, "high.wav")
ifft_data(F3, 425, "low.wav")
ifft_data(F4, 427, "band.wav")

#描画
# leg.get_frame().set_alpha(1)
plt.show()



#時間測る
start = time.time()
np.fft.fft(f[10000:11024])
end = time.time()
t1 = end - start
print("1024fft", t1)
start = time.time()
dft(f[10000:11024])
end = time.time()
t2 = end - start
print("1024dft", t2)
print("1024 fft - dft", t2 - t1) #1024

start = time.time()
np.fft.fft(f[10000:12048])
end = time.time()
t1 = end - start
print("2048fft", t1)
start = time.time()
dft(f[10000:12048])
end = time.time()
t2 = end - start
print("2048dft", t2)
print("2048 fft - dft", t2 - t1) #2048

start = time.time()
np.fft.fft(f[10000:14096])
end = time.time()
t1 = end - start
print("4096fft", t1)
start = time.time()
dft(f[10000:14096])
end = time.time()
t2 = end - start
print("4096dft", t2)
print("4096 fft - dft", t2 - t1) #4096

# 1024fft 0.00017452239990234375
# 1024dft 2.41331148147583
# 1024 fft - dft 2.4131369590759277
# 2048fft 0.0002422332763671875
# 2048dft 9.947956800460815
# 2048 fft - dft 9.947714567184448
# 4096fft 0.0004248619079589844
# 4096dft 39.19393801689148
# 4096 fft - dft 39.19351315498352

