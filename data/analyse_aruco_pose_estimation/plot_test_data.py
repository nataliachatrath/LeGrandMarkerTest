import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
import glob
import os

class plot_data():
    
    def __init__(self):

        self.data = []
        dir_ = 'landing_board_three_steady_state_test/'
        
        self.cur_dir = dir_

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

        self.aruco_mean = 0.0
        self.aruco_std = 0.0
        
        self.read_dir_files(dir_)


    def read_dir_files(self, path):
        
        path = path + '*.txt' #Read all txt files in tests directory
        files = glob.glob(path)
        
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

            #Time
            self.time = np.array([item[12] for item in self.data])

            #Sum pos error for x, y and z for aruco pose estimation error and setpoint error
            aruco_error_mean = []
            aruco_error_std = []
            setpoint_error_mean = []
            setpoint_error_std = []
            
            self.plot_data([aruco_x, g_x], 'Time [s]', 'Time [s]', 'Position [m]', 
                'Error [m]', 'Error in x', [['Aruco pos x'],['Ground truth x']], 
                self.error_x_plot_path + 'pose_error_x_test' + str(test) + '.png')

            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)

            self.plot_data([aruco_y, g_y], 'Time [s]', 'Time [s]', 'Position [m]', 
                'Error [m]', 'Error in y', [['Aruco pos y'],['Ground truth y']], 
                self.error_y_plot_path + 'pose_error_y_test' + str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)
            
            self.plot_data([aruco_z, g_z], 'Time [s]', 'Time [s]', 'Position [m]', 
                'Error [m]', 'Error in z', [['Aruco pos z'],['Ground truth z']], 
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
                'Error [degress]', 'Error in roll', [['Aruco angle roll'],['Ground truth roll']], 
                self.error_roll_plot_path + 'pose_error_roll_test' + str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)

            self.plot_data([aruco_pitch, g_pitch], 'Time [s]', 'Time [s]', 'Angle [degress]', 
                    'Error [degress]', 'Error in pitch', [['Aruco angle pitch'],['Ground truth pitch']], 
                    self.error_pitch_plot_path + 'pose_error_pitch_test' + str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)
            
            self.plot_data([aruco_yaw, g_yaw], 'Time [s]', 'Time [s]', 'Angle [degress]', 
                    'Error [degress]', 'Error in yaw', [['Aruco angle yaw'],['Ground truth yaw']], 
                    self.error_yaw_plot_path + 'pose_error_yaw_test' + str(test) + '.png')
            
            aruco_error_mean.append(self.aruco_mean)
            aruco_error_std.append(self.aruco_std)

            self.mean_error_aruco_angle.append(sum(aruco_error_mean)/len(aruco_error_mean))
            self.std_error_aruco_angle.append(sum(aruco_error_std)/len(aruco_error_std))


        print("Mean error aruco pos: " +str(sum(self.mean_error_aruco_pos)/len(self.mean_error_aruco_pos)))
        print("STD error aruco pos: " +str(sum(self.std_error_aruco_pos)/len(self.std_error_aruco_pos)))
        #print("Min error aruco pos: " +str(min(self.mean_error_aruco_pos)))
        #print("Max error aruco pos: " +str(max(self.mean_error_aruco_pos)) + '\n')
        
        print("Mean error aruco angle: " +str(sum(self.mean_error_aruco_angle)/len(self.mean_error_aruco_angle)))
        print("STD error aruco angle: " +str(sum(self.std_error_aruco_angle)/len(self.std_error_aruco_angle)))
        #print("Min error aruco angle: " +str(min(self.mean_error_aruco_angle)))
        #print("Max error aruco angle: " +str(max(self.mean_error_aruco_angle)) + '\n')
        
    def read_data(self, file_name):
        init = True
        seq = 0
        with open(file_name,"r") as text_file:
            for line in text_file:
                items = line.split(' ')
                items[-1] = items[-1].strip()
                str_to_float = [float(item) for item in items]
                self.data.append(str_to_float)

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
if __name__ == "__main__":

    tt = plot_data()
