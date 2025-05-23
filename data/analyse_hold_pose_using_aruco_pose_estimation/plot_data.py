import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')

class plot_data():
    
    def __init__(self):

        self.data = []

        #self.read_data('hold_pose_landing_board_one_test/test2.txt')
        self.read_data('../hold_pose_using_aruco_pose_estimation.txt')
        
        #Aruco pose estimations
        self.aruco_x = np.array([item[0] for item in self.data])
        self.aruco_y = np.array([item[1] for item in self.data])
        self.aruco_z = np.array([item[2] for item in self.data])
        self.aruco_roll = np.array([item[3] for item in self.data])
        self.aruco_pitch = np.array([item[4] for item in self.data])
        self.aruco_yaw = np.array([item[5] for item in self.data])

        #Target setpoints
        self.setpoint_x = np.array([item[6] for item in self.data])
        self.setpoint_y = np.array([item[7] for item in self.data])
        self.setpoint_z = np.array([item[8] for item in self.data])
        self.setpoint_roll = np.array([item[9] for item in self.data])
        self.setpoint_pitch = np.array([item[10] for item in self.data])
        self.setpoint_yaw = np.array([item[11] for item in self.data])
        
        #Ground truth data
        self.g_x = np.array([item[12] for item in self.data])
        self.g_y = np.array([item[13] for item in self.data])
        self.g_z = np.array([item[14] for item in self.data])
        self.g_roll = np.array([item[15] for item in self.data])
        self.g_pitch = np.array([item[16] for item in self.data])
        self.g_yaw = np.array([item[17] for item in self.data])

        #Time
        self.time = np.array([item[18] for item in self.data])

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
        
        fig = plt.figure(figsize=(25,25),facecolor='white') #21,15
        fig.set_facecolor((1,1,1)) 
        ax1 = plt.subplot2grid((2,1), (0,0))
        ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)
        
        ax1.legend(loc='best',fontsize=60)
        
        df = pd.read_csv('test2_gps2visionBoard_1.0Wind_-1.0y/test1.txt', delimiter=" ")
        aruco = pd.Series(index[0], index=self.time)
        setpoint = pd.Series(index[1], index=self.time)
        ground_truth = pd.Series(index[2], index=self.time)
        
        aruco.plot(ax=ax1, label=labels[0][0],fontsize=40,color='b')
        ground_truth.plot(ax=ax1,label=labels[2][0],fontsize=80,linestyle='dotted',color='r')
        setpoint.plot(ax=ax1,label=labels[1][0], fontsize=80, linestyle=':', color='g')

        error_pose_aruco = aruco - ground_truth
        error_aruco_setpoint = aruco - setpoint
        
        error_pose_aruco.plot(ax=ax2, label='Pose estimation error',fontsize=80)
        error_aruco_setpoint.plot(ax=ax2, label='Setpoint error',fontsize=80)
        
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

if __name__ == "__main__":

    tt = plot_data()
    
    tt.plot_data([tt.aruco_x, tt.setpoint_x, tt.g_x], 'Time [s]', 'Time [s]', 'Position [m]', 
        'Error [m]', 'Error in position and setpoint deviation in x', [['Aruco pos x'],['Setpoint x'],['Ground truth x']], 'pose_error_x.png')
    
    tt.plot_data([tt.aruco_y, tt.setpoint_y, tt.g_y], 'Time [s]', 'Time [s]', 'Position [m]', 
        'Error [m]', 'Error in position and setpoint deviation in y', [['Aruco pos y'],['Setpoint y'],['Ground truth y']], 'pose_error_y.png')
    
    tt.plot_data([tt.aruco_z, tt.setpoint_z, tt.g_z], 'Time [s]', 'Time [s]', 'Position [m]', 
        'Error [m]', 'Error in position and setpoint deviation in z', [['Aruco pos z'],['Setpoint z'],['Ground truth z']], 'pose_error_z.png')
    
    tt.plot_data([tt.aruco_roll, tt.setpoint_roll, tt.g_roll], 'Time [s]', 'Time [s]', 'Angle [degress]', 
        'Error [degress]', 'Error in angle and setpoint deviation in roll', [['Aruco angle roll'],['Setpoint roll'],['Ground truth roll']], 'pose_error_roll.png')
    
    tt.plot_data([tt.aruco_pitch, tt.setpoint_pitch, tt.g_pitch], 'Time [s]', 'Time [s]', 'Angle [degress]', 
            'Error [degress]', 'Error in angle and setpoint deviation in pitch', [['Aruco angle pitch'],['Setpoint pitch'],['Ground truth pitch']], 'pose_error_pitch.png')
    
    tt.plot_data([tt.aruco_yaw, tt.setpoint_yaw, tt.g_yaw], 'Time [s]', 'Time [s]', 'Angle [degress]', 
            'Error [degress]', 'Error in angle and setpoint deviation in yaw', [['Aruco angle yaw'],['Setpoint yaw'],['Ground truth yaw']], 'pose_error_yaw.png')
