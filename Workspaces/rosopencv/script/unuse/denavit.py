import numpy as np

def denavitHartenberg():

        # Theta 1 and Theta 2 will be get from arduino ( servo.read() publishing angle to this node)
        theta1 = 0                    # radian value must use (change from degree to radian)
        theta2 = 0
        theta3 = 0
            
        alpha1 = 0
        alpha2 = 180
        alpha3 = 0

        r1 = 12
        r2 = 12
        r3 = 0

        d1 = 55
        d2 = 10
        d3 = 10+12

        homo_0to1 = [[np.cos(theta1),-np.sin(theta1)*(np.cos(alpha1)),np.sin(theta1)*(np.sin(alpha1)),r1*(np.cos(theta1))],
                    [np.sin(theta1),np.cos(theta1)*(np.cos(alpha1)),-np.cos(theta1)*(np.sin(alpha1)),r1*(np.sin(theta1))],
                    [0,np.sin(alpha1),np.cos(alpha1),d1],
                    [0,0,0,1]]
        homo_1to2 = [[np.cos(theta2),-np.sin(theta2)*(np.cos(alpha2)),np.sin(theta2)*(np.sin(alpha2)),r2*(np.cos(theta2))],
                    [np.sin(theta2),np.cos(theta2)*(np.cos(alpha2)),-np.cos(theta2)*(np.sin(alpha2)),r2*(np.sin(theta2))],
                    [0,np.sin(alpha2),np.cos(alpha2),d2],
                    [0,0,0,1]]
        homo_2to3 = [[np.cos(theta3),-np.sin(theta3)*(np.cos(alpha3)),np.sin(theta3)*(np.sin(alpha3)),r3*(np.cos(theta3))],
                    [np.sin(theta3),np.cos(theta3)*(np.cos(alpha3)),-np.cos(theta3)*(np.sin(alpha3)),r3*(np.sin(theta3))],
                    [0,np.sin(alpha3),np.cos(alpha3),d3],
                    [0,0,0,1]]

        result_one = np.dot(homo_0to1,homo_1to2)
        result_two = np.dot(result_one,homo_2to3)

        print(np.matrix(result_two))
        return np.matrix(result_two)

denavitHartenberg()