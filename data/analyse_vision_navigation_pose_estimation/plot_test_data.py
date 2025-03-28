import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
from matplotlib.patches import Circle, Wedge, Polygon
import glob
import os
class plot_data():
    
    def __init__(self):
        
        self.data = []
        dir_ = 'test1_full_pattern_board/'
        
        self.cur_dir = dir_

        #Show 2d path 
        self.path_x = []
        self.path_y = []

        #Paths for plotting errors vs setpoints and pose 
        self.error_x_plot_path = dir_ + 'error_x/'
        self.error_y_plot_path = dir_ + 'error_y/'
        self.error_z_plot_path = dir_ + 'error_z/'
        self.error_roll_plot_path = dir_ + 'error_roll/'
        self.error_pitch_plot_path = dir_ + 'error_pitch/'
        self.error_yaw_plot_path = dir_ + 'error_yaw/'

        #Make plotting dirs if not existing
        try:
            if not os.path.isdir(self.error_x_plot_path):
                os.mkdir(self.error_x_plot_path)
            if not os.path.isdir(self.error_y_plot_path):
                os.mkdir(self.error_y_plot_path)
            if not os.path.isdir(self.error_z_plot_path):
                os.mkdir(self.error_z_plot_path)
            if not os.path.isdir(self.error_roll_plot_path):
                os.mkdir(self.error_roll_plot_path)
            if not os.path.isdir(self.error_pitch_plot_path):
                os.mkdir(self.error_pitch_plot_path)
            if not os.path.isdir(self.error_yaw_plot_path):
                os.mkdir(self.error_yaw_plot_path)
        except OSError as error:
            print(error)
        
        #Errors for pose and setpoint
        self.mean_error_aruco_pos = []
        self.mean_error_aruco_angle = []
        self.std_error_aruco_pos = []
        self.std_error_aruco_angle = []

        self.mean_error_setpoint_pos = []
        self.mean_error_setpoint_angle = []
        self.std_error_setpoint_pos = []
        self.std_error_setpoint_angle = []
        
        self.aruco_mean = 0.0
        self.aruco_std = 0.0
        self.read_dir_files(dir_)

    def read_dir_files(self, path):
        
        path = path + '*.txt' #Read all txt files in tests directory
        files = glob.glob(path)

        plt.rcParams.update({
        "text.usetex": True})

        fig, ax = plt.subplots(figsize=(15,25),facecolor='white')
        
        print(files)
        test = 0
        
        for fle in files:
            test += 1
            #Read data from each file 
            self.data = []
            self.read_data(fle)
            self.cur_dir = fle
            
            #Aruco pose estimations
            aruco_x = np.array([item[0] for item in self.data])
            aruco_y = np.array([item[1] for item in self.data])
            aruco_z = np.array([item[2] for item in self.data])
            aruco_roll = np.array([item[3] for item in self.data])
            aruco_pitch = np.array([item[4] for item in self.data])
            aruco_yaw = np.array([item[5] for item in self.data])

            #Ground truth data
            g_x = np.array([item[6] for item in self.data])
            g_y = np.array([item[7] for item in self.data])
            g_z = np.array([item[8] for item in self.data])
            g_roll = np.array([item[9] for item in self.data])
            g_pitch = np.array([item[10] for item in self.data])
            g_yaw = np.array([item[11] for item in self.data])

            self.path_x.append(g_x)
            self.path_y.append(g_y)

            #Time
            self.time = np.array([item[12] for item in self.data])

            #Sum pos error for x, y and z for aruco pose estimation error and setpoint error
            aruco_error_mean = []
            aruco_error_std = []
            
            self.plot_data([aruco_x, g_x], 'Time [s]', 'Time [s]', 'Position [m]', 
                'Error [m]', 'Error in position in x', [['Aruco pos x'],['Ground truth x']], 
                self.error_x_plot_path + 'pose_error_x_test' + str(test) + '.png')

            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)

            self.plot_data([aruco_y, g_y], 'Time [s]', 'Time [s]', 'Position [m]', 
                'Error [m]', 'Error in position in y', [['Aruco pos y'],['Ground truth y']], 
                self.error_y_plot_path + 'pose_error_y_test' + str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)
            
            self.plot_data([aruco_z, g_z], 'Time [s]', 'Time [s]', 'Position [m]', 
                'Error [m]', 'Error in position in z', [['Aruco pos z'],['Setpoint z'],['Ground truth z']], 
                self.error_z_plot_path + 'pose_error_z_test'+str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)
            
            #Update list of means for number of tests 
            self.mean_error_aruco_pos.append(sum(aruco_error_mean)/len(aruco_error_mean))
            self.std_error_aruco_pos.append(sum(aruco_error_std)/len(aruco_error_std))
            
            #Sum angle error for roll, pitch and yaw for aruco pose estimation error and setpoint error
            aruco_error_mean = []
            aruco_error_std = []
            
            self.plot_data([aruco_roll, g_roll], 'Time [s]', 'Time [s]', 'Angle [degress]', 
                'Error [degress]', 'Error in angle in roll', [['Aruco angle roll'],['Ground truth roll']], 
                self.error_roll_plot_path + 'pose_error_roll_test' + str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)

            self.plot_data([aruco_pitch, g_pitch], 'Time [s]', 'Time [s]', 'Angle [degress]', 
                    'Error [degress]', 'Error in angle in pitch', [['Aruco angle pitch'],['Ground truth pitch']], 
                    self.error_pitch_plot_path + 'pose_error_pitch_test' + str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)

            self.plot_data([aruco_yaw, g_yaw], 'Time [s]', 'Time [s]', 'Angle [degress]', 
                    'Error [degress]', 'Error in angle in yaw', [['Aruco angle yaw'],['Ground truth yaw']], 
                    self.error_yaw_plot_path + 'pose_error_yaw_test' + str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)

            self.mean_error_aruco_angle.append(sum(aruco_error_mean)/len(aruco_error_mean))
            self.std_error_aruco_angle.append(sum(aruco_error_std)/len(aruco_error_std))

        self.plot_2d_path()

        print("Mean error aruco pos: " +str(sum(self.mean_error_aruco_pos)/len(self.mean_error_aruco_pos)))
        print("STD error aruco pos: " +str(sum(self.std_error_aruco_pos)/len(self.std_error_aruco_pos)))

        print("Mean error aruco angle: " +str(sum(self.mean_error_aruco_angle)/len(self.mean_error_aruco_angle)))
        print("STD error aruco angle: " +str(sum(self.std_error_aruco_angle)/len(self.std_error_aruco_angle)))
        

    def read_data(self, file_name):
        init = True
        seq = 0
        old_lines = []
        with open(file_name,"r") as text_file:
            for line in text_file:
                items = line.split(' ')
                items[-1] = items[-1].strip()
                str_to_float = [float(item) for item in items]
                
                old_lines.append(str_to_float)
                
                #Skip data from gps2vision transition and use only data from the bottom camera 
                if seq > 500:
                    self.data.append([old_lines[-1][0], 
                                      old_lines[-1][1], 
                                      old_lines[-1][2], 
                                      old_lines[-1][5], 
                                      old_lines[-1][6], 
                                      old_lines[-1][7],
                                      old_lines[-1][21],
                                      old_lines[-1][22],
                                      old_lines[-1][23],
                                      old_lines[-1][18],
                                      old_lines[-1][19],
                                      old_lines[-1][20],
                                      old_lines[-1][17]])
                else:
                    seq +=1

    def plot_data(self, index, label_x_fig1, label_x_fig2, label_y_fig1, label_y_fig2, title, labels, fig_name):

        plt.rcParams.update({
        "text.usetex": True})
        
        plt.clf()
        plt.cla()
        fig = plt.figure(figsize=(25,25),facecolor='white') #21,15
        fig.set_facecolor((1,1,1)) 
        ax1 = plt.subplot2grid((2,1), (0,0))
        ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)
        
        ax1.legend(loc='best',fontsize=60)
        
        df = pd.read_csv(self.cur_dir, delimiter=" ")
        aruco = pd.Series(index[0], index=self.time)
        ground_truth = pd.Series(index[1], index=self.time)
        
        aruco.plot(ax=ax1, label=labels[0][0],fontsize=40,color='b')
        ground_truth.plot(ax=ax1,label=labels[1][0],fontsize=80,linestyle='dotted',color='r')

        error_pose_aruco = (aruco - ground_truth)

        #Update errors
        self.aruco_mean = abs(error_pose_aruco).mean()
        self.aruco_std = abs(error_pose_aruco).std()
        
        error_pose_aruco.plot(ax=ax2, label='Pose estimation error',fontsize=80)

        ax1.legend(loc='best',fontsize=60)
        ax1.set_title(title,fontsize=70)
        ax1.set_xlabel(label_x_fig1,fontsize=80)
        ax1.set_ylabel(label_y_fig1,fontsize=80)
        ax2.set_xlabel(label_x_fig2,fontsize=80)
        ax2.set_ylabel(label_y_fig2,fontsize=80)
        ax2.legend(loc='best',fontsize=60)
        
        ax1.set_facecolor((1,1,1))
        ax2.set_facecolor((1,1,1))
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1, top=0.93, hspace=0.2, wspace=0)
        plt.savefig(fig_name, facecolor=fig.get_facecolor())
        plt.close(fig)

    def plot_2d_path(self):

       plt.rcParams.update({
        "text.usetex": True})

       fig, ax = plt.subplots(figsize=(15,15),facecolor='white')
       
       #Paths to the landing stations
       one = [[3.65, 1.10], [3.65, 4.25]]
       two = [[3.65, 4.25], [0.40, 4.25]]
       three = [[3.65, 4.25], [7.10, 4.25]]
       four = [[3.65, 4.25], [3.65, 7.10]]
       five = [[0.40, 4.25], [0.40, 7.10]]
       six = [[7.10, 4.25], [7.10, 7.10]]

       paths = [one, two, three, four, five, six]
       init = True
       for path in paths:
           x = [item[0] for item in path]
           y = [item[1] for item in path]
           if init:
               ax.plot(x,y, linewidth=12, alpha=0.2, color='black', label='Target trajectory')
               init=False
           else:
               ax.plot(x,y, linewidth=12, alpha=0.2, color='black')

       init = True
       for path in paths:
           for waypoint in path:
               if init:
                   c = plt.Circle((waypoint[0],waypoint[1]), 0.05, alpha=0.8, color='blue', label='Target waypoints')
                   init=False
               else:
                   c = plt.Circle((waypoint[0],waypoint[1]), 0.05, alpha=0.8, color='blue')
               
               ax.add_patch(c)

       init = True
       for x,y in zip(self.path_x, self.path_y):
           if init:
               ax.plot(x,y, linewidth=1, color='k', label='Actual path of drone')
               init=False
           else:
               ax.plot(x,y, linewidth=1, color='k')


       #Show text for start and GPS2Vision board locations 
       ax.annotate('GPS2Vision board', xy=(4.50,0.50), xytext=(2.8,0.60), size=25,bbox=dict(boxstyle="round, pad=0.3",fc="white", ec="k", lw=1))
       ax.annotate('Landing station 1', xy=(0.40,7.10), xytext=(-0.35, 7.45), size=25,bbox=dict(boxstyle="round, pad=0.3",fc="white", ec="k", lw=1))
       ax.annotate('Landing station 2', xy=(3.40,7.10), xytext=(2.9, 7.45), size=25,bbox=dict(boxstyle="round, pad=0.3",fc="white", ec="k", lw=1))
       ax.annotate('Landing station 3', xy=(6.40,7.10), xytext=(6.30, 7.45), size=25,bbox=dict(boxstyle="round, pad=0.3",fc="white", ec="k", lw=1))
       
       #Show safe area to change from GPS to vision
       #wedge = Wedge((3.65, 2.99), 5, 180, 360, alpha=0.05, label="Safe GP2Vision transition area")
       
       #Safe GPS2Vision transitiom
       #ax.add_patch(wedge)
       
       #Plot parameters 
       plt.tick_params(axis='x', labelsize=40)
       plt.tick_params(axis='y', labelsize=40)
       ax.legend(loc='best',fontsize=25)
       ax.set_xlim([-1.0, 8.0])
       ax.set_ylim([-1.0, 8.0])
       ax.set_title('Vision based navigation', fontsize=40)
       ax.set_xlabel('x [m]',fontsize=40)
       ax.set_ylabel('y [m]',fontsize=40)
       ax.set_facecolor((1,1,1))
       plt.tight_layout()
       plt.savefig('2d_path.png', facecolor=fig.get_facecolor())

if __name__ == "__main__":

    tt = plot_data()
