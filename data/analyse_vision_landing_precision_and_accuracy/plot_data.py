import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
from pathlib import Path

class plot_data():
    
    def __init__(self):

        self.data = []

        #Target waypoints above acceptence region
        self.errors_above_acc = 0

        #self.read_data('test2.txt')
        #self.read_data('real_test_landing_board_two/vision_landing_precision_and_accuracy.txt')
        self.read_data('vision_landing_precision_and_accuracy.txt')
        
        #Landing station 
        self.landing_station = np.array([item[0] for item in self.data])
       
        #Landing station one
        self.aruco_x_one = []
        self.aruco_y_one = [] 
        self.setpoint_x_one = []
        self.setpoint_y_one = [] 
        self.g_x_one = [] 
        self.g_y_one = []

        self.target_error_one = []
        self.pose_estimation_error_one = []

        #Landing station two
        self.aruco_x_two = [] 
        self.aruco_y_two = [] 
        self.setpoint_x_two = [] 
        self.setpoint_y_two = [] 
        self.g_x_two = [] 
        self.g_y_two = [] 
    
        self.target_error_two = []
        self.pose_estimation_error_two = []
        
        #Landing station three
        self.aruco_x_three = [] 
        self.aruco_y_three = [] 
        self.setpoint_x_three = [] 
        self.setpoint_y_three = [] 
        self.g_x_three = [] 
        self.g_y_three = [] 
        
        self.target_error_three = []
        self.pose_estimation_error_three = []

        self.stabilization_time_one = []
        self.landing_time_one = []

        self.stabilization_time_two = []
        self.landing_time_two = []

        self.stabilization_time_three = []
        self.landing_time_three = []

        data = Path('output_data.txt')
        self.data_path = 'output_data.txt'
        if not data.is_file:
            data = open(self.data_path,'r+')
            data.truncate(0)
            data.close
        else:
            data = open(self.data_path,'w+')
            data.close()


        for item in self.data:
            #Find which data belongs to which landing station
            if item[0] == 3:
                self.aruco_x_one.append(item[1])
                self.aruco_y_one.append(item[2])
                self.setpoint_x_one.append(item[3])
                self.setpoint_y_one.append(item[4])
                self.g_x_one.append(item[5])
                self.g_y_one.append(item[6])

                self.target_error_one.append(np.sqrt((item[1]-item[3])**2+(item[2]-item[4])**2))
                self.pose_estimation_error_one.append(np.sqrt((item[1]-item[5])**2+(item[2]-item[6])**2))
    
                self.stabilization_time_one.append(item[7])
                self.landing_time_one.append(item[8])
            
            if item[0] == 4:
                self.aruco_x_two.append(item[1])
                self.aruco_y_two.append(item[2])
                self.setpoint_x_two.append(item[3])
                self.setpoint_y_two.append(item[4])
                self.g_x_two.append(item[5])
                self.g_y_two.append(item[6])
    
                self.target_error_two.append(np.sqrt((item[1]-item[3])**2+(item[2]-item[4])**2))
                self.pose_estimation_error_two.append(np.sqrt((item[1]-item[5])**2+(item[2]-item[6])**2))
            
                self.stabilization_time_two.append(item[7])
                self.landing_time_two.append(item[8])
            
            if item[0] == 5:
                self.aruco_x_three.append(item[1])
                self.aruco_y_three.append(item[2])
                self.setpoint_x_three.append(item[3])
                self.setpoint_y_three.append(item[4])
                self.g_x_three.append(item[5])
                self.g_y_three.append(item[6])
    
                self.target_error_three.append(np.sqrt((item[1]-item[3])**2+(item[2]-item[4])**2))
                self.pose_estimation_error_three.append(np.sqrt((item[1]-item[5])**2+(item[2]-item[6])**2))

                self.stabilization_time_three.append(item[7])
                self.landing_time_three.append(item[8])

    def read_data(self, file_name):
        init = True
        seq = 0
        with open(file_name,"r") as text_file:
            for line in text_file:
                items = line.split(' ')
                items[-1] = items[-1].strip()
                str_to_float = [float(item) for item in items]
                self.data.append(str_to_float)

    def plot_data(self, index, label_x_fig1, label_y_fig1, title, labels, fig_name, radius, s):

        plt.rcParams.update({
        "text.usetex": True})
        
        fig = plt.figure(figsize=(25,25),facecolor='white') #21,15
        fig.set_facecolor((1,1,1)) 
        ax1 = plt.subplot2grid((1,1), (0,0))
        ax1.legend(loc='best',fontsize=60)
        
        #df = pd.read_csv('real_test_landing_board_two/vision_landing_precision_and_accuracy.txt', delimiter=" ")
        df = pd.read_csv('vision_landing_precision_and_accuracy.txt', delimiter=" ")
        
        aruco = pd.Series(index[1], index=index[0])
        setpoint = pd.Series(index[3], index=index[2])
        pose_error = pd.Series(index[4])
        target_error = pd.Series(index[5])
        
        setpoint.plot(ax=ax1, marker='o', linestyle='', ms=20, label=labels[0][0], fontsize=80, color='g')
        aruco.plot(ax=ax1, marker='o', linestyle='', ms=20, label=labels[1][0], fontsize=80,color='b')
        ax1.scatter(x = [index[2][0]], y= [index[3][0]], color='g', s=s, alpha=0.1)
        ax1.scatter(x = [index[2][0]], y= [index[3][0]], color='g', s=s, facecolors='none', linestyle='-.')
        ax1.legend(loc='best',fontsize=60)
        ax1.set_title(title,fontsize=70)
        ax1.set_xlabel(label_x_fig1,fontsize=80)
        ax1.set_ylabel(label_y_fig1,fontsize=80)
        ax1.set_facecolor((1,1,1))
        
        plt.tight_layout()
        plt.xlim((index[2][0]-radius,index[2][0]+radius))
        plt.ylim((index[3][0]-radius,index[3][0]+radius))
        plt.subplots_adjust(bottom=0.1, top=0.95, hspace=0.2, wspace=0)
        plt.savefig(fig_name, facecolor=fig.get_facecolor())

        runs = len(target_error)
        mean_error = target_error.mean()
        std_error = target_error.std()
        min_error = target_error.min()
        max_error = target_error.max()

        #Find number of target errors above 10 cm
        below_threshold = 0
        for error in target_error:
            if error < 0.10:
                below_threshold += 1
        self.errors_above_acc += (len(target_error)-below_threshold)

        print("Runs: " + str(runs))
        print("Mean error: " + "{:.4f}".format(mean_error))
        print("STD error: " + "{:.4f}".format(std_error))
        print("Min error: " + "{:.4f}".format(min_error))
        print("Max error: " + "{:.4f}".format(max_error))
        print("Mean stabilization time: " + "{:.4f}".format(sum(index[6])/len(index[6])))
        print("Mean landing time: " + "{:.4f}".format(sum(index[7])/len(index[7])))
        print("Landings in acceptence region: " + str(below_threshold) + " of " + str(len(target_error)))
        
        data = open(self.data_path,'a')
        data.write(str(runs) + " " + "{:.4f}".format(mean_error) + " " + "{:.4f}".format(std_error) + " " + "{:.4f}".format(min_error) + " " + "{:.4f}".format(max_error))
        data.write('\n')
        data.close()
        
if __name__ == "__main__":

    tt = plot_data()
    
    tt.plot_data([tt.aruco_x_one, tt.aruco_y_one, tt.setpoint_x_one, tt.setpoint_y_one, tt.pose_estimation_error_one, tt.target_error_one,tt.stabilization_time_one,
        tt.landing_time_one], 'Position x [m]', 'Position y [m]', 
            'Precision and accuracy of landing for station one', [['Target landing'],['Final landing position'],['Acceptance buffer']], 'landing_for_station_one.png', radius = 0.2587, s=375000)
    
    tt.plot_data([tt.aruco_x_two, tt.aruco_y_two, tt.setpoint_x_two, tt.setpoint_y_two, tt.pose_estimation_error_two, tt.target_error_two, tt.stabilization_time_two,
        tt.landing_time_two], 'Position x [m]', 'Position y [m]', 
            'Precision and accuracy of landing for station two', [['Target landing'],['Final landing position'],['Acceptance buffer']], 'landing_for_station_two.png', radius = 0.31, s=260000)
    
    tt.plot_data([tt.aruco_x_three, tt.aruco_y_three, tt.setpoint_x_three, tt.setpoint_y_three, tt.pose_estimation_error_three, tt.target_error_three, tt.stabilization_time_three,
        tt.landing_time_three], 'Position x [m]', 'Position y [m]', 
            'Precision and accuracy of landing for station three', [['Target landing'],['Final landing position'],['Acceptance buffer']], 'landing_for_station_three.png', radius = 0.25, s=375000) 
    
    print("Landings outside acceptence region: " + str(tt.errors_above_acc))
