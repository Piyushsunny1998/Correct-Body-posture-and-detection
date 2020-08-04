from tkinter import Tk
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from os.path import basename
from PIL import ImageTk, Image
import cv2
import ImageCode as IC
global path
path = None
#Base window for the GUI
root = tk.Tk()
root.geometry("600x450+385+163")
root.title("Posture Calibaration")

#Original Frame
frame = tk.Frame(root)

frame.grid()

anchor = tk.Label(frame)
anchor.grid()
anchor.place(relx=0.083, rely=0.111, height=351, width=224)
anchor.configure(width=224)

def CaptureImage():
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1024)
    print("Opening Camera...")
    while(True):
        ret,frame=cap.read()
        cv2.putText(frame,'Press C to Capture',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        cv2.putText(frame,'Press Q to Exit',(178,639),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        cv2.imshow("Image Capture",frame)
        if cv2.waitKey(27) & 0xFF == ord('c'):  #press q to capture image
            cv2.imwrite("image.png",frame)
            break
        elif(cv2.waitKey(27) & 0xFF == ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Closed Camera...")

#For displaying the Image
def insertImg():

    global path
    path = askopenfilename()
    image = cv2.imread(path)
    image = cv2.resize(image, (224, 351))
    b, g, r = cv2.split(image)#This and next step are used to rearrange the color channels
    image = cv2.merge((r, g, b))#as PIL reads image in r, g, b format, while opencv does it in b, g, r
    #cv2.imshow("", image)
    img = ImageTk.PhotoImage(Image.fromarray(image))
    
    anchor.image = img
    anchor.configure(image = img)
    #anchor.configure(rowspan = 4)
    #panel = tk.Label(frame, image = img)#actually displays the image
    anchor.grid()

def leg():
    IC.headToLeg(path)

def arm():
    IC.headToArm(path)

def shoulder():
    IC.shoulders(path)
def doctor():
    import login

showImage = tk.Button(root, text = "Insert Image", command = insertImg)
showImage.grid()
showImage.place(relx=0.583, rely=0.156, height=44, width=207)
showImage.configure(width=207)

legGet = tk.Button(root, text = "Head to Right Leg", command = leg)
legGet.grid()
legGet.place(relx=0.583, rely=0.333, height=54, width=207)
legGet.configure(width=207)

armGet = tk.Button(root, text = "Head to Right Arm", command = arm)
armGet.grid()
armGet.place(relx=0.583, rely=0.533, height=44, width=207)
armGet.configure(width=207)

shoulderGet = tk.Button(root, text = "Head to Both Shoulders", command = shoulder)
shoulderGet.grid()
shoulderGet.place(relx=0.583, rely=0.711, height=44, width=207)
shoulderGet.configure(width=207)

doctor = tk.Button(root, text = "Doctor", command = doctor)
doctor.grid()
doctor.place(relx=0.583, rely=0.845, height=44, width=207)
doctor.configure(width=207)

take = tk.Button(root, text = "TAKE IMAGE", command = CaptureImage)
take.grid()
take.place(relx=0.1, rely=0.855, height=44, width=207)
take.configure(width=207)

root.mainloop()
