import numpy as np
from matplotlib import pyplot as plt

fudgefact=1.0 # multiplication factor to fudge data to get extremes to match

def extreme_fit(fact, data):
    nmax=len(data)//fact
    #extremes = np.sort(data[np.argpartition(data, -1*nmax)[-1*nmax:]]) # max vals in the total array
    extremes = np.sort([np.max(x) for x in np.array_split(data,np.ceil(len(data)/365))])
    #extremes = np.log(extremes)
    ln=len(extremes)
    cump = (np.arange(ln)+1)/(ln+1)
    lcump = -np.log(-np.log(cump))
    return [extremes, lcump]

factor_extremes = 50 # take 1/factor_extremes th of the largest values for extreme value calculation


dataN = np.loadtxt("../data/Qdaily.txt")
dataS = np.loadtxt("./synthetic/Qdaily-1000x1.csv")*fudgefact

plt.figure(num=1, figsize=(14, 14), dpi=80)

ax3=plt.subplot(223)
plt.plot(np.arange(len(dataN))+1,dataN)

ax3=plt.subplot(224)
plt.plot(np.arange(len(dataN))+1,dataS[:len(dataN)])

ax1=plt.subplot(221)
ax1.set_yscale('log')
ax1.grid()
plt.boxplot([dataN, dataS])


ax2=plt.subplot(222)

handles=[]
data=extreme_fit(factor_extremes, dataN)
handle, = plt.plot(*data, 'o', label='obs')
handles.append(handle)


n=len(dataN)

for i in range(10):
    data=extreme_fit(factor_extremes, dataS[n*i:n*(i+1)])
    handle, =plt.plot(data[0], data[1], '-', label='syn %s' % (i+1))
    handles.append(handle)
plt.legend(handles=handles)


plt.show()
