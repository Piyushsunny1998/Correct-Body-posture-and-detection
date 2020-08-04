import cv2
import time
import numpy as np
#import docend

protoFile = "pose_deploy_linevec_faster_4_stages.prototxt" #Dataset
weightsFile = "pose_iter_160000.caffemodel" #Weights for the dataset




#Function to read image and create neural network
def readImage(path):
    
    frame = cv2.imread(path)
    frame = cv2.resize(frame, (368, 368))#Resize image to better fit the dataset
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    threshold = 0.1

    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)#User for neural network
    '''
        Now the next step is to load images in a batch and run them through the network. For this, we use the cv2.dnn.blobFromImage method. '''

    #image dimensions for the network
    inWidth = 368
    inHeight = 368
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False) #Used for preprocessing the image

    net.setInput(inpBlob)

    output = net.forward()
    #print(output)

    H = output.shape[2]
    W = output.shape[3]
   # print(H)
    #print(W)
    
    return output, H, W, frameHeight, frameWidth, threshold, frame

#Returns an array of points which match with various joints in the dataset
def plotPoints(startRange, endRange, path, output, H, W, frameHeight, frameWidth, threshold, frame):
    points = []
    
    for i in range(startRange, endRange + 1):#nPoints
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)#he minMaxLoc function returns the max and min intensity values in a Mat or an array along with the location of these intensities.
        #print(prob)
    
        
        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H

        if prob > threshold : 
            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
        else :
            points.append(None)
            
    return points

#Utility function to calculate angle between joints
def angle(a):
    
    cosine = np.dot(a[0] - a[1],a[2] - a[1])/(np.linalg.norm(a[0] - a[1]) * np.linalg.norm(a[2] - a[1])) # smaller the angle higher the similarity
    angle = np.arccos(cosine)

    return (np.degrees(angle))

#Covers joints from head to right leg
def headToLeg(path):
    
    output, H, W, frameHeight, frameWidth, threshold, frame = readImage(path)
    print(frame.shape)
    pointsArray = [] #Array for final points
    pointsArray = plotPoints(0, 1, path, output, H, W, frameHeight, frameWidth, threshold, frame)
    pointsArray.extend(plotPoints(14, 14, path, output, H, W, frameHeight, frameWidth, threshold, frame))
    pointsArray.extend(plotPoints(8, 10, path, output, H, W, frameHeight, frameWidth, threshold, frame))

    #Connecting all points
    for i in range(0, len(pointsArray)-1):
        cv2.line(frame, pointsArray[i], pointsArray[i+1], (0, 255, 255), 2)#cv2.line(image, (x1, y1), (x2, y2), (0,255,0), lineThickness)
        cv2.circle(frame, pointsArray[i], 8, (0, 0, 255), thickness = -1, lineType = cv2.FILLED)
        temp = pointsArray[i+1]
    cv2.circle(frame, temp, 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    '''

Parameters: 
img (CvArr) – Image where the circle is drawn
center (CvPoint) – Center of the circle
radius (int) – Radius of the circle
color (CvScalar) – Circle color
thickness (int) – Thickness of the circle outline if positive, otherwise this indicates that a filled circle is to be drawn
lineType (int) – Type of the circle boundary, see Line description
shift (int) – Number of fractional bits in the center coordinates and radius value'''

    cv2.imshow('Output-Skeleton', frame) #Displaying skeleton image

    a = [] #Empty array, used to store points in numpy format so that the angle between any 3 can be calculated
    
    for i in pointsArray:
        a.append(np.asarray(i))
    print(a)

    n=np.load('arm.npy')
    print(n)
    arm=angle([a[-1], a[-2], a[-3]])
    print(arm)
    if(n[0]<arm<n[1]):
        print("Correct posture")
    else:
        print("Incorrect Posture")
        diff_left=arm-n[0]
        diff_right=arm-n[1]
        print("YOU NEED TO SHIFT TO LEFT SIDE BY :")
        print(diff_left)
        print("YOU NEED TO SHIFT TO RIGHT SIDE BY :")
        print(diff_right)

    cv2.waitKey(0)

#Function to detect joints from head to right arm
def headToArm(path):
    
    #Variable names represent the same things as in the previous function
    output, H, W, frameHeight, frameWidth, threshold, frame = readImage(path)

    pointsArray = []
    pointsArray = plotPoints(0, 4, path, output, H, W, frameHeight, frameWidth, threshold, frame)

    for i in range(0, len(pointsArray)-1):
        cv2.line(frame, pointsArray[i], pointsArray[i+1], (0, 255, 255), 2)
        cv2.circle(frame, pointsArray[i], 8, (0, 0, 255), thickness = -1, lineType = cv2.FILLED)
        temp = pointsArray[i+1]
    cv2.circle(frame, temp, 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    cv2.imshow('Output-Skeleton', frame)
    a = [] #Empty array, used to store points in numpy format so that the angle between any 3 can be calculated
    
    for i in pointsArray:
        a.append(np.asarray(i))

    #conn.execute("""SELECT Head_to_Rigth_Arm,Head_to_Rigth_Arm1 FROM doctor""")
    #p=conn.fetchone()
   # print(p)
    n=np.load('arm.npy')
    

    arm=angle([a[-1], a[-2], a[-3]])
    print(arm)
    if(n[2]<arm<n[3]):
        print("Correct posture")
    else:
        print("Incorrect Posture")
        diff_left=arm-n[2]
        diff_right=arm-n[3]
        print("YOU NEED TO SHIFT TO LEFT SIDE BY :")
        print(diff_left)
        print("YOU NEED TO SHIFT TO RIGHT SIDE BY :")
        print(diff_right)
    #print(arm)
    cv2.waitKey(0)

#Function to detect joints from head to both shoulders. Image angle should be from front for best results
def shoulders(path):

    output, H, W, frameHeight, frameWidth, threshold, frame = readImage(path)

    pointsArray = []
    pointsArray = plotPoints(0, 0, path, output, H, W, frameHeight, frameWidth, threshold, frame)
    pointsArray.extend(plotPoints(1, 2, path, output, H, W, frameHeight, frameWidth, threshold, frame))
    pointsArray.extend(plotPoints(5, 5, path, output, H, W, frameHeight, frameWidth, threshold, frame))
    pointsArray[1], pointsArray[2] = pointsArray[2], pointsArray[1] #Swapping for easy line drawing, as points are not arranged from left to right shoulder

    for i in range(1, len(pointsArray)-1):
        cv2.line(frame, pointsArray[i], pointsArray[i+1], (0, 255, 255), 2)
        cv2.circle(frame, pointsArray[i], 8, (0, 0, 255), thickness = -1, lineType = cv2.FILLED)
        temp = pointsArray[i+1]
    cv2.circle(frame, temp, 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
    cv2.line(frame, pointsArray[0], pointsArray[2], (0, 255, 255), 2)
    cv2.circle(frame, pointsArray[0], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    cv2.imshow('Output-Skeleton', frame)
    a = [] #Empty array, used to store points in numpy format so that the angle between any 3 can be calculated
    
    for i in pointsArray:
        a.append(np.asarray(i))

    n=np.load('arm.npy')

    arm=angle([a[-1], a[-2], a[-3]])
    print(arm)
    if(n[4]<arm<n[5]):
        print("Correct posture")
    else:
        print("Incorrect Posture")
        diff_left=arm-n[4]
        diff_right=arm-n[5]
        print("YOU NEED TO SHIFT TO LEFT SIDE BY :")
        print(diff_left)
        print("YOU NEED TO SHIFT TO RIGHT SIDE BY :")
        print(diff_right)
    cv2.waitKey(0)

if __name__ == "__main__":
    headToLeg(0)
    headToArm(0)
    shoulders(0)
