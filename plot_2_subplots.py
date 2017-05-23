import csv
from itertools import takewhile    
from collections import deque
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
import os
import matplotlib.lines as mlines
import time


save_time = time.strftime("%d_%m")
x = str(save_time)
CMD = "pscp pi@fhlrasptemp.desy.de:/home/pi/slowpi/data_" + x + ".csv C:\\Users\\cordinge\\Desktop\\IR_Monitor\\Pi_Slow_Control" #Putty Command to copy the data from Pi to Windows 

fig = plt.figure(figsize=(7,6.5)) #Create the Window
ax1 = fig.add_subplot(2, 1, 2) #Define that only one Graph that takes up alle the Window size is displayed
ax2 = ax1.twinx() #Second Y-axis added to the Graph
ax3 = fig.add_subplot(2,1,1)
ax4 = ax3.twinx()

fig.canvas.set_window_title('IR Chamber - Humidity and Temperature') #Winow Name
max_length = 200000 #Length of Arrays with len max_length    
small_length = 15 #Length
one_length = 1   #Length of 1 necessary for Alarm feature, most recent value displayed  

lasttime = deque(maxlen=one_length) #deque array instead of list due to better features
lasttemp = deque(maxlen=one_length)
lasthumid = deque(maxlen=one_length)

tentime = deque(maxlen=small_length)
tentemp = deque(maxlen=small_length)
tenhumid = deque(maxlen=small_length)

tentemp2 = deque(maxlen=small_length)
tenhumid2 = deque(maxlen=small_length)

tentemp3 = deque(maxlen=small_length)
tenhumid3 = deque(maxlen=small_length)

tentemp_avg = deque(maxlen=small_length)
tenhumid_avg = deque(maxlen=small_length)

t = deque(maxlen=max_length) # time object
y = deque(maxlen=max_length) # temperature
h = deque(maxlen=max_length) # humidity

y2 = deque(maxlen=max_length) # temperature2
h2 = deque(maxlen=max_length) # humidity2

y3 = deque(maxlen=max_length) # temperature3
h3 = deque(maxlen=max_length) # humidity3

temp_avg = deque(maxlen=max_length)
humid_avg = deque(maxlen=max_length)

patch1 = mlines.Line2D([], [], color='red', marker = 's', label='Sensor 1: Temp') #Legend patches
patch2 = mlines.Line2D([], [], color='red', marker = 'o', label='Sensor 2: Temp')
patch3 = mlines.Line2D([], [], color='green', marker = 's', label='Sensor 1: Humidity')
patch4 = mlines.Line2D([], [], color='green', marker = 'o', label='Sensor 2: Humidity')
patch5 = mlines.Line2D([], [], color='red', marker = '^', label='Sensor 3: Temp')
patch6 = mlines.Line2D([], [], color='green', marker = '^', label='Sensor 3: Humidity')
patch7 = mlines.Line2D([], [], color='blue', marker = 's', label='Average Temperature')
patch8 = mlines.Line2D([], [], color='blue', marker = 'o', label='Average Humidity')


os.system(CMD)

def read_file(): #function that reads the csv and appends values to the deque arrays
    with open('data_' + save_time + '.csv', newline='') as f_input: #opens the file , comma delimiter default setting
        csv_input = csv.reader(f_input)
            #header = next(csv_input)        
    
        if len(t):
                list(takewhile(lambda row: datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S') != t[-1], csv_input)) 
                
                '''
                This line ^^^ is crucial for memory efficiency. It compares all the data of the csv file that is opened every time the function is called with the already existing arrays in memory.
                It will start appending new values only. If this is not done, array size goes up to several hundred thousand over time. When the program is started the first time and this function
                is called the first time, nothing will happen as memory and arrays are empty at that point.
                '''
    
        for row in csv_input: #this for loop is executed x many times, x being the number of rows in the csv file
                
                t.append(datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S')) #csv header useful, easy to declare what row in csv is what value
                y.append(float(row[1]))
                h.append(float(row[4]))
                y2.append(float(row[2]))
                h2.append(float(row[4]))
                y3.append(float(row[3]))
                h3.append(float(row[6]))
                
                tentime.append(datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S'))
                tentemp.append(float(row[1]))
                tenhumid.append(float(row[4]))
                tentemp2.append(float(row[2]))
                tenhumid2.append(float(row[5]))
                tentemp3.append(float(row[3]))
                tenhumid3.append(float(row[6]))
                
                lasttime.append(datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S'))
                lasttemp.append(float(row[1]))
                lasthumid.append(float(row[4]))
                
                avg_temp = (float(row[1])+float(row[2])+float(row[3]))/3 #for each iteration of the function read_file, an average value of each csv element of temp and humid
                avg_humid = (float(row[4])+float(row[5])+float(row[6]))/3 #is calculated and appended to a deque array which is plotted
                
                tentemp_avg.append(float(avg_temp))           
                tenhumid_avg.append(float(avg_humid))
                
                temp_avg.append(float(avg_temp))
                humid_avg.append(float(avg_humid))
                
def Plot(): #plotting function
 
    

 avgtemp = ((sum(y)/len(y))+(sum(y2)/len(y2))+(sum(y3)/len(y3))/3) #for plt.title, displays avg values if no alarm is triggered
 avghumid = ((sum(h)/len(h))+(sum(h2)/len(h2))+(sum(h3)/len(h3))/3)
 
 last_time = list(lasttime)[-1] #necessary to convert deque element to something that can be recognised as a number or individual value
 last_temp = list(lasttemp)[-1]
 last_humid = list(lasthumid)[-1]
 last_temp2 = list(y2)[-1]
 last_humid2 = list(h2)[-1]
 last_temp3 = list(y3)[-1]
 last_humid3 = list(h3)[-1]

 ax1 = fig.add_subplot(2, 1, 2) #for some reason this is necessary for the plotting to look how it is supposed to look

 ax1.clear() #to avoid plotting over an existing plot, saves memory
 ax1.plot(t, y, 's-', color = 'r')
 ax1.plot(t, y2, 'o-', color = 'r')
 ax1.plot(t, y3, '^-', color = 'r')
 ax1.plot(t, temp_avg, 's-', color = 'b')
 plt.yticks([0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40])
 ax1.set_ylabel('TEMPERATURE in C')
 ax1.set_xlabel('TIME')
 ax1.yaxis.label.set_color('red')
 plt.xticks(rotation=20)
 ax1.grid()
 ax1.tick_params(axis='y', colors='red')
 

 ax2.clear()
 ax2.plot(t, h, 's-', color = 'g')
 ax2.plot(t, h2, 'o-', color = 'g')
 ax2.plot(t, h3, '^-', color = 'g')
 ax2.plot(t, humid_avg, 'o-', color = 'b')
 ax2.set_yticks([4,12,20,28,36,44,52,60,68,76,84,92,100])
 ax2.set_ylabel('HUMIDITY in %')
 ax2.yaxis.label.set_color('green')
 ax2.tick_params(axis='y', colors='green')
 
 ax3.clear()
 ax3.plot(tentime, tentemp, 's-', color = 'r')
 ax3.plot(tentime, tentemp2, 'o-', color = 'r')
 ax3.plot(tentime, tentemp3, '^-', color = 'r')
 ax3.plot(tentime, tentemp_avg, 's-', color = 'b')
 ax3.set_yticks([0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40])
 ax3.set_ylabel('TEMPERATURE in C')
 ax3.yaxis.label.set_color('red')
 avgtentemp = sum(tentemp)/len(tentemp)
 avgtenhumid = sum(tenhumid)/len(tenhumid)
 avgtentemp2 = sum(tentemp2)/len(tentemp2)
 avgtenhumid2 = sum(tenhumid2)/len(tenhumid2)
 avgtentemp3 = sum(tentemp3)/len(tentemp3)
 avgtenhumid3 = sum(tenhumid3)/len(tenhumid3)
 ax3.set_title('Last Fifteen Minutes: ' + 'Temperature: ' + "%.2f" % avgtentemp + '/' + "%.2f" % avgtentemp2 + '/' + "%.2f" % avgtentemp3 + '  ' + 'Humidity: '  + "%.2f" % avgtenhumid + '/' "%.2f" % avgtenhumid2 + '/' "%.2f" % avgtenhumid3)
 ax3.set_xlabel('TIME')
 ax3.grid()
 ax3.tick_params(axis='y', colors='red')

 ax4.clear()
 ax4.plot(tentime, tenhumid, 's-', color = 'g')
 ax4.plot(tentime, tenhumid2, 'o-', color = 'g')
 ax4.plot(tentime, tenhumid3, '^-', color = 'g')
 ax4.plot(tentime, tenhumid_avg, 'o-', color = 'b')
 ax4.set_yticks([0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50]) 
 ax4.set_ylabel('HUMIDITY in %')
 ax4.yaxis.label.set_color('green')
 ax4.tick_params(axis='y', colors='green')
 

 ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m' + ' - ' + '%H:%M:%S')) #this recognises that the timestamp to be plotted on x-axis has to be changed
 ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
 
 plt.title('Average Temperature ' +  "%.2f" % avgtemp + '   ' + 'Average Humidity ' + "%.2f" % avghumid)
 fig.tight_layout() #resizes the window appropriately, even if you change the windows size


 if last_temp >= 20 and last_humid >= 25: #alarms, writes to log.csv
     plt.title('WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ' + "%.2f" % last_temp + '/' + "%.2f" % last_temp2 + '/' + "%.2f" % last_temp3 + "   " + "%.2f" % last_humid + '/' + "%.2f" % last_humid2 + '/' + "%.2f" % last_humid3, color = 'r')
     print("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: " + "%.2f" % last_temp + ' / ' + "%.2f" % last_humid + '  ' + str(last_time))

     myrow = str("WARNING! BOTH TEMP AND HUMIDITY TOO HIGH: ") + str(last_time) + ', Sensor 1, Temp: ' + str(last_temp) + ', Sensor 2, Temp: ' + str(last_temp2) + ', Sensor 3, Temp: ' + str(last_temp3) + ', Sensor 1, Humidity: ' + str(last_humid) + ', Sensor 2, Humidity' + str(last_humid2) + ', Sensor 3, Humidity: ' + str(last_humid3) + '\n'
     fd = open('log.csv','a')
     fd.write(myrow)
     fd.close()


 elif last_temp >= 33:
    plt.title('WARNING! TEMPERATURE TOO HIGH: ' + "%.2f" % last_temp + '/' + "%.2f" % last_temp2 + '/' + "%.2f" % last_temp3, color = 'r')
    print("WARNING! TEMPERATURE TOO HIGH: " + "%.2f" % last_temp + '  ' + str(last_time))

    myrow = str("WARNING! TEMPERATURE TOO HIGH: ") + str(last_time) + ', Sensor 1: ' + str(last_temp) + ', Sensor 2: ' + str(last_temp2) + ', Sensor 3: ' + str(last_temp3) + '\n'
    fd = open('log.csv','a')
    fd.write(myrow)
    fd.close()

 elif last_humid >= 25:
    plt.title('WARNING! HUMIDITY TOO HIGH: ' + "%.2f" % last_humid + ' / ' + "%.2f" % last_humid2 + ' / ' + "%.2f" % last_humid3, color = 'r')
    print("WARNING! HUMIDITY TOO HIGH: " + str(last_humid) + '  ' + str(last_time))

    myrow = str("WARNING! HUMIDITY TOO HIGH: ") + str(last_time) + ', Sensor 1: ' + str(last_humid) + ', Sensor2 : ' + str(last_humid2) + ', Sensor 3: ' + str(last_humid3) + '\n'
    fd = open('log.csv','a')
    fd.write(myrow)
    fd.close()

 plt.legend(handles =[patch1, patch2, patch5, patch3, patch4, patch6, patch7, patch8], loc = (0.85,0.75)) #legend patches



def animate(i):
 read_file()
 Plot()
 os.system(CMD) #the csv is copied from the Rpi every x seconds

 #fig.savefig('C:/Users/cordinge/Desktop/RaspberryPi_Sensor-master/plot.png', bbox_inches='tight', dpi=80)
     
ani = animation.FuncAnimation(fig, animate, interval=5000) #the function animate is called every x seconds, the window (fig) is a parameter that is necessary

#plt.show()

