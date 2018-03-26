import matplotlib

backend = "Qt5Agg"
try:
    matplotlib.use(backend)
except BaseException:
    print("Backend %s is not available. Using default %s." %
          (backend, matplotlib.get_backend()))

import numpy as np
from matplotlib import pyplot as plt



def extreme_fit(fact, data):
    nmax=len(data)//fact
    #extremes = np.sort(data[np.argpartition(data, -1*nmax)[-1*nmax:]]) # max vals in the total array
    extremes = np.sort([np.max(x) for x in np.array_split(data,np.ceil(len(data)/365))]) # max values from each year. 
    #extremes = np.log(extremes)
    ln=len(extremes)
    cump = (np.arange(ln)+1)/(ln+1)
    lcump = -np.log(-np.log(cump))
    return [extremes, lcump]

def time_series_plots(plt, loc1, loc2, Nsamples, dataN, dataS):
    # time series plot of observed data
    n=len(dataN)
    
    tsylim = max(np.max(dataN),np.max(dataS[0:Nsamples*n])) # get a common y limit for all time series plots. 
    tsylim = tsylim * 1.05 # keep some room on top    
    
    ax3=plt.subplot(loc1)
    plt.plot(np.arange(n)+1,dataN)
    plt.ylim(ymax=tsylim) # set y limit
    plt.xlabel('Time (days)')
    plt.ylabel(r'Flow (m$^3/$s)') 
    plt.title('Observed')

    # time series plots of synthetic data
    ax3=plt.subplot(loc2)

    handles=[]
    for i in range(Nsamples):
        handle, = plt.plot(np.arange(n)+1,dataS[n*i:n*(i+1)], label="syn %s" % (i+1))
        handles.append(handle)
    plt.legend(handles=handles)
    plt.ylim(ymax=tsylim) # set y limit
    plt.xlabel('Time (days)')
    plt.ylabel(r'Flow (m$^3/$s)')    
    plt.title('Synthetic')


def box_plots(plt,  loc, Nsamples, dataN, dataS):
    # boxplots of observed and synthetic data
    
    n=len(dataN)
    
    ax1=plt.subplot(loc)
    ax1.set_yscale('log')
    ax1.grid()
    data = [dataN]
    lab  = ['Obs'] 

    for i in range(Nsamples):
        data.append(dataS[n*i:n*(i+1)])
        lab.append('syn %s' % (i+1))
    data.append(dataS)
    lab.append('syn-all')
    plt.boxplot(data, labels=lab)
    
    plt.xlabel('Samples')
    plt.ylabel(r'Flow (m$^3/$s)')    
    plt.title('Statistics')    
    
def extreme_plot(plt, loc, factor_extremes, Nsamples, dataN, dataS):
    # extreme value plots
    ax2=plt.subplot(loc)

    n=len(dataN)

    handles=[]
    datasets = []
    datasets.append(extreme_fit(factor_extremes, dataN))
    handle, = plt.plot(*(datasets[-1]), 'o', label='obs')
    handles.append(handle)

    for i in range(Nsamples):
        datasets.append(extreme_fit(factor_extremes, dataS[n*i:n*(i+1)]))
        handle, =plt.plot(*(datasets[-1]), '-', label='syn %s' % (i+1))
        handles.append(handle)
    handle, = plt.plot(*extreme_fit(factor_extremes, dataS), '.', label='syn-all')
    handles.append(handle)
    
    minx = min(x[0][0]  for x in datasets)
    maxx = max(x[0][-1] for x in datasets)
    miny = min(x[1][0]  for x in datasets)
    maxy = max(x[1][-1] for x in datasets)    
    plt.xlim(minx*.95,maxx*1.05)
    plt.ylim(miny*.95,maxy*1.05)
    plt.legend(handles=handles)
    
    plt.xlabel(r'Flow (m$^3/$s)')  
    plt.ylabel(r'$-ln[-ln[P(X\leq x)]]$')
    plt.title('Extreme values')     


matplotlib.rcParams.update({'font.size': 16})

fudgefact=1.0 # multiplication factor to fudge data to get extremes to match
factor_extremes = 50 # take 1/factor_extremes th of the largest values for extreme value calculation
Nsamples = 5 # number of realisations to be used for extreme plots and boxplots
Nts = 2 # number of synthetic time series to be plot 

dataN = np.loadtxt("../data/Qdaily.txt")
dataS = np.loadtxt("./synthetic/Qdaily-1000x1.csv")*fudgefact

plt.figure(num=1, figsize=(14, 14), dpi=80)
time_series_plots(plt, 223, 224,  Nts, dataN, dataS)
box_plots(plt,  221, Nsamples, dataN, dataS)
extreme_plot(plt, 222, factor_extremes, Nsamples, dataN, dataS)
plt.tight_layout()
plt.show()
