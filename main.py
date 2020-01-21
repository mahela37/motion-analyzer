f=open("sqdata.txt", "r")
contents =f.read().splitlines()
f.close()	

f=open("base.txt","r")
base =f.read().splitlines()
f.close()

f=open("single_2.txt", "r")
single_contents =f.read().splitlines()
f.close()

f=open("5squat.txt", "r")
squat5 =f.read().splitlines()
f.close()

f=open("walk.txt", "r")
walk =f.read().splitlines()
f.close()

f=open("j_5sq.txt", "r")
j_5sq =f.read().splitlines()
f.close()

f=open("run.txt", "r")
run =f.read().splitlines()
f.close()


import numpy as np
contents=np.array(contents,dtype=float)
single_contents=np.array(single_contents,dtype=float)
walk=np.array(walk,dtype=float)
squat5=np.array(squat5,dtype=float)
j_5sq=np.array(j_5sq,dtype=float)
run=np.array(run,dtype=float)
base=np.array(base,dtype=float)



from scipy import stats
from scipy import signal


contents=stats.zscore(contents)
single_contents=stats.zscore(single_contents)
walk=stats.zscore(walk)
squat5=stats.zscore(squat5)
j_5sq=stats.zscore(j_5sq)
run=stats.zscore(run)
base=stats.zscore(base)

"""
corr_out=signal.correlate(contents,squat5,'valid')
corr_walk=signal.correlate(contents,walk,'valid')
corr_j=signal.correlate(contents,j_5sq,'valid')
corr_run=signal.correlate(contents,run,'valid')


from numpy import trapz
area1=trapz(corr_out,dx=1)
area2=trapz(corr_walk,dx=1)
area3=trapz(corr_j,dx=1)
area4=trapz(run,dx=1)

import matplotlib.pyplot as plt
f, (ax1, ax2,ax3,ax4,ax5,ax6,ax7) = plt.subplots(7, 1,sharex=True)
ax1.plot(contents)
ax1.set_title('raw data')
ax2.plot(squat5)
ax2.set_title('squat5')
ax3.plot(corr_out)
ax3.set_title('cross correlation 5 squats. area: '+str(area1))
ax4.plot(walk)
ax4.set_title('walk')
ax5.plot(corr_walk)
ax5.set_title('cross correlation walk. area: '+str(area2))

ax6.plot(run)
ax6.set_title('run')
ax7.plot(corr_run)
ax7.set_title('cross correlation run. area: '+str(area4))
plt.show()
"""

def doplotting(sample):
	corr=signal.correlate(sample,base,'valid')

	from numpy import trapz
	area1=trapz(corr,dx=1)


	import matplotlib.pyplot as plt
	f, (ax1, ax2,ax3) = plt.subplots(3, 1,sharex=True)

	ax1.plot(base)
	ax1.set_title('base')

	ax2.plot(sample)
	ax2.set_title('sample')

	ax3.plot(corr)
	ax3.set_title('corr. area: '+str(area1))

	print(area1)
	plt.show()

doplotting(contents)
doplotting(single_contents)
doplotting(walk)
doplotting(j_5sq)
doplotting(squat5)
doplotting(run)
