import numpy as np

def removeInvalid(x,y,z,threshold,xheight):	
	#since a squat produces simiar motion in all 3 axes, we should get peaks on cross correlation around the same time.
	#remove datasets across x,y,z that do not occur around the same time.
	#threshold is how many samples far x can vary from y or z, to be considered in the "same time". current 1 increment=0.02 sec
	#due to accelerometer data sampling rate.
	#xheight is the input y values of the x list, which as used to plot the final points [x,y] for x dataset
	
	#not the most efficient, but it works for now. 
	#first compare x and y
	i=0;
	nx=[]
	hx=[]
	while(i<len(x)):
		j=0;
		while(j<len(y)):
			absol=abs(x[i]-y[j])
			if(absol<threshold):
				nx.append(x[i])
				hx.append(xheight[i])
				np.delete(y,j)
				break
				
			j=j+1
		i=i+1
	#get the remaining valid x entries. compare with z
	i=0;
	x=nx
	xheight=hx
	nx=[]
	hx=[]
	while(i<len(x)):
		j=0;
		while(j<len(z)):
			absol=abs(x[i]-z[j])
			if(absol<threshold):
				nx.append(x[i])
				hx.append(xheight[i])
				np.delete(z,j)
				break
				
			j=j+1
		i=i+1

	#send back whatever is remaining to be valid. this is the filtered [x,y] of dataset x
	return nx,hx

def parseCSV(filepath,convert):	
	#given a csv, return x,y,z coordinates parsed into individual lists.
	#filepath: path to the .csv 	convert:if 1, parses the file  in utf-16 which is used by the app output

	#read file contents
	if(convert):
		f=open(filepath, "r",encoding='utf-16')
	else:	#i must have manually converted it to ANSI already. 
		f=open(filepath, "r")
	contents =f.read().splitlines()
	f.close()

	#get rid of header
	del contents[0]
	del contents[0]
	del contents[0]
	del contents[0]
	del contents[0]

	#bin the data to x,y,z lists
	x=[]
	y=[]
	z=[]

	for item in contents:
		item=item.split("	")	#tab delimited
		x.append(item[1])
		y.append(item[2])
		z.append(item[3])
		
	#convert the lists from string to float
	x=np.array(x,dtype=float)
	y=np.array(y,dtype=float)
	z=np.array(z,dtype=float)

	return x,y,z

def analysis(samplefile,convert,server=0,fname="untitled"):
	#main chunk of the program
	#server flag is used to disable things that aren't necessary when running in the Flask server

	#1.Load the reference data sequence. Then load the data sequence we would like to identify
	base_x,base_y,base_z=parseCSV("base.csv",1)
	sq_x,sq_y,sq_z=parseCSV(samplefile,convert)

	#2.Do a z score normalization for both sets
	from scipy import stats
	from scipy import signal
	base_x=stats.zscore(base_x)
	base_y=stats.zscore(base_y)
	base_z=stats.zscore(base_z)
	sq_x=stats.zscore(sq_x)
	sq_y=stats.zscore(sq_y)
	sq_z=stats.zscore(sq_z)

	#3.Cross correlate the two signals
	corr_x=signal.correlate(sq_x,base_x,'same')
	corr_y=signal.correlate(sq_y,base_y,'same')
	corr_z=signal.correlate(sq_z,base_z,'same')

	#4.Find the peaks of the correlation curves. The distance, height,etc parameters were found by experimentation and nature of dataset
	from scipy.signal import find_peaks
	peaks_x=find_peaks(corr_x,distance=50,height=30,prominence=30,width=30)
	peaks_x_time=[1]*len(peaks_x[0])
	peaks_y=find_peaks(corr_y,distance=50,height=30,prominence=30,width=30)
	peaks_y_time=[1]*len(peaks_y[0])
	peaks_z=find_peaks(corr_z,distance=50,height=30,prominence=30,width=30)
	peaks_z_time=[1]*len(peaks_z[0])

	#5.Filter the data to remove any false readings 
	filtered,filtered_y=removeInvalid(peaks_x[0],peaks_y[0],peaks_z[0],50,peaks_x[1]['peak_heights'])
	if(server==0):
		print(peaks_x[0])
		print(peaks_y[0])
		print(peaks_z[0])

	#6.Time for fancy visuals!
	import matplotlib.pyplot as plt
	f, (ax1, ax2,ax3) = plt.subplots(3, 3,sharex=True)

	#Graph reference data
	ax1[0].plot(base_x)
	ax1[0].set_title('reference x')
	ax1[1].plot(base_y)
	ax1[1].set_title('reference y')
	ax1[2].plot(base_z)
	ax1[2].set_title('reference z')
	#Graph sample data
	ax2[0].plot(sq_x)
	ax2[0].set_title('sample x')
	ax2[1].plot(sq_y)
	ax2[1].set_title('sample y')
	ax2[2].plot(sq_z)
	ax2[2].set_title('sample z')
	#Graph correlation data
	ax3[0].plot(corr_x)
	ax3[0].set_title('correlation x ')
	ax3[1].plot(corr_y)
	ax3[1].set_title('correlation y ')
	ax3[2].plot(corr_z)
	ax3[2].set_title('correlation z ')
	#Show correlation peaks 
	ax3[0].scatter(peaks_x[0],peaks_x[1]['peak_heights'],c='red',edgecolors='red')
	ax3[1].scatter(peaks_y[0],peaks_y[1]['peak_heights'],c='red',edgecolors='red')
	ax3[2].scatter(peaks_z[0],peaks_z[1]['peak_heights'],c='red',edgecolors='red')
	#Show filtered data
	ax3[0].scatter(filtered,filtered_y,c='green',edgecolors='green')

	f.suptitle(fname+" Final Result: "+str(len(filtered)))
	if(server==0):
		plt.show()
	if(server):
		plt.savefig('static/results.png')

	#Return results to whoever called the function
	returnList=[]
	average=len(filtered)
	returnList.append(average)
	returnList.append(len(peaks_x[0]))
	returnList.append(len(peaks_y[0]))
	returnList.append(len(peaks_z[0]))
	return returnList


def runTests():
	print("Running Self-Test Module:")
	testEntries=[]
	
	entry=[1,"1",1]
	testEntries.append(entry)
	entry=[2,"2",1]
	testEntries.append(entry)
	entry=[3,"3",1]
	testEntries.append(entry)
	entry=[5,"5",1]
	testEntries.append(entry)
	entry=[6,"6",1]
	testEntries.append(entry)
	entry=[10,"10",1]
	testEntries.append(entry)
	entry=[0,"walk",0]
	testEntries.append(entry)

	numTests=len(testEntries)
	numPassed=0
	for test in testEntries:
		results=analysis("C:\\Users\\Mahela\\Downloads\\CSV\\"+test[1]+".csv",test[2],server=1)
		result=results[0]
		if(result==test[0]):
			print("Test "+test[1]+ " success")
			numPassed=numPassed+1
		else:
			print("Test "+test[1]+ " failed")
			print("x:%d y:%d z:%d guessed:%d EXPECTED:%d " %(results[1],results[2],results[3],results[0],test[0]))
	
	print("\n%d/%d Test cases passed. %f percent success rate." %(numPassed,numTests,float(numPassed)/float(numTests)*100))
if __name__ == "__main__":
	#run this code when .py file is directly launched, i.e. not imported as a library by Flask

	runTests()

	#analysis("5squat.csv",1)
	#filename="1"	
	#analysis("C:\\Users\\Mahela\\Downloads\\CSV\\"+filename+".csv",1)

	#analysis("run.csv",0)
	#analysis("0sq.csv",1)
