while True:
    try:
        import os, sys, json, time, turtle #Base modules
        import ait, cv2, numpy, pyautogui #Dependencies
        import pynput.mouse as ms

        from pynput.mouse import Button
        from pynput import keyboard
        from turtle import mode, Terminator
        break
    except ImportError:
        dep = ["pynput","autoit","numpy","opencv-python","pyautogui","pillow"] #For every dep added put it in this list
        print("Import error\nDownloading dependencies")
        time.sleep(3)
        for i in dep:
            os.system(f"cmd /c pip install {i}")

#global
global __time__ 
global __drawspeed__ 
global __xoffset__ 
global __yoffset__
global __bar_type__
#Default Settings
__time__        = 5
__drawspeed__   = 0.08
__xoffset__     = 15
__yoffset__     = 15
__bartype__     = 1

#Info
__author__  = "https://github.com/The-Glit-ch"
__version__ = "1.1.0"

#Vars
progress_list = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]
mouse = ms.Controller()

#Drawing Info
global did_run
did_run = False #For the progress bar

def estimatedtime(pointArr):
    return (len(pointArr)*2) * __drawspeed__

def currentprogress(pointArr,index):
    return round((index*100)/len(pointArr),2)

def progress_handler(progress,prev_progress,bar_type):
    global did_run
    length = 40 #Default Value
    #Bar Type
    #1 = Original
    #2 = Standard
    if round(progress) in progress_list and round(progress) != prev_progress:
        if bar_type == 1:
                print(f"{round(progress)}% done!")
        elif bar_type == 2:
            sys.stdout.write("|||")
            sys.stdout.flush()
    elif round(progress) < 5:
        if bar_type == 2:
            if did_run:
                pass
            else:
                # setup toolbar
                sys.stdout.write("[%s]" % (" " * length))
                sys.stdout.flush() #i have no clue what this does lmao
                sys.stdout.write("\b" * (length+1))
                did_run = True

    return round(progress) #Returns new prev_progress

#Misc?
def getXandY(data,select):
    temp = str(data).split(",")
    if "n" in str(data):
        temp.remove("n")
        #print(f"Removed special char:\n{temp}") Just for debugging
    
    return int(temp[select])

def datafileoption_bare(pointArr):
        global did_run
        did_run = False
        prev_progress = None
        t_time = estimatedtime(pointArr)
        print(f"Now starting. Estimated total time is {t_time} seconds")
        mouse.position = (getXandY(pointArr[0],0),getXandY(pointArr[0],1)) #First entry is the start position
        ait.move(mouse.position[0],mouse.position[1]) #Update "physical" mouse
        
        for i in range(1,len(pointArr)): #Skip first entry
            if "n" in pointArr[i]:
                mouse.position = (getXandY(pointArr[i],0),getXandY(pointArr[i],1)) #Position the mouse to the new area
                ait.move(mouse.position[0],mouse.position[1]) #Update "physical" mouse
            
            if mouse.position == (0,0):
                sys.exit()

            prev_progress = progress_handler(currentprogress(pointArr, i),prev_progress,__bartype__)
            

            mouse.press(Button.left)
            time.sleep(__drawspeed__)
            mouse.position = (getXandY(pointArr[i],0),getXandY(pointArr[i],1))
            
            #These few lines is what makes all of this work for the roblox client. DO NOT FUCKING TOUCH
            time.sleep(__drawspeed__)
            ait.move(mouse.position[0],mouse.position[1])
            time.sleep(__drawspeed__)
            
            mouse.release(Button.left)
            time.sleep(__drawspeed__)
        
        mouse.release(Button.left)
        if __bartype__ == 1:
            print("\nFinished!")
        else:
            print("]\nFinished!")

#Settings
def save_settings():
    #Very simple and easy to read
    export_Settings = {
        "startDelay":__time__,
        "drawSpeed":__drawspeed__,
        "x_offset":__xoffset__,
        "y_offset":__yoffset__,
        "bar_type":__bartype__
    }
    settings_file = open("settings.json","w")
    json.dump(export_Settings, settings_file)
    settings_file.close()

def load_settings():
    print("Loading settings...")
    sys.stdout.flush()
    if os.path.exists("settings.json"):
        settings_file = open("settings.json","r") #Open file as read
        settingsJSON = json.load(settings_file) #Load the json

        #Start changing setting variables
        global __time__
        __time__        = settingsJSON["startDelay"]
        #print("Start delay loaded\n",__time__)      #Just for debugging
        global __drawspeed__
        __drawspeed__   = settingsJSON["drawSpeed"]
        #print("Draw speed loaded\n",__drawspeed__)  #Just for debugging
        global __xoffset__
        __xoffset__     = settingsJSON["x_offset"]
        #print("X offset loaded\n",__xoffset__)      #Just for debugging
        global __yoffset__
        __yoffset__     = settingsJSON["y_offset"]
        #print("Y offset loaded\n",__yoffset__)      #Just for debugging
        global __bartype__
        __bartype__     = settingsJSON["bar_type"]
    else:
        print("No settings file found, falling back to default")
        open("settings.json","a").close() #First make the new file
        settings_file = open("settings.json","w") #Then open the file as write
        default_settings = {
            "startDelay":3,
            "drawSpeed":0.08,
            "x_offset":15,
            "y_offset":15,
            "bar_type": 1
        }
        json.dump(default_settings,settings_file) #Dump default settings
        settings_file.close() #Close file when we're done
    print("Settings loaded!")

#Options
def DataFileOption(fn):
    global did_run
    did_run = False
    with open(f"{fn}.json","r") as dataFile:
        JSONData = json.load(dataFile)
        pointArr = JSONData["pointarr"]
        #print(pointArr) Just for debugging
        prev_progress = None
        t_time = estimatedtime(pointArr)
        print(f"Now starting. Estimated total time is {t_time} seconds")
        
        mouse.position = (getXandY(pointArr[0],0) + __xoffset__,getXandY(pointArr[0],1) + __yoffset__) #First entry is the start position
        ait.move(mouse.position[0],mouse.position[1]) #Update "physical" mouse
        
        for i in range(1,len(pointArr)): #Skip first entry
            if "n" in pointArr[i]:
                mouse.position = (getXandY(pointArr[i],0) + __xoffset__,getXandY(pointArr[i],1) + __yoffset__) #Position the mouse to the new area
                ait.move(mouse.position[0],mouse.position[1]) #Update "physical" mouse
            
            if mouse.position == (0,0):
                sys.exit()
            
            prev_progress = progress_handler(currentprogress(pointArr, i),prev_progress,__bartype__)

            mouse.press(Button.left)
            time.sleep(__drawspeed__)
            mouse.position = (getXandY(pointArr[i],0) + __xoffset__,getXandY(pointArr[i],1) + __yoffset__)
            
            #These few lines is what makes all of this work for the roblox client. DO NOT FUCKING TOUCH
            time.sleep(__drawspeed__)
            ait.move(mouse.position[0],mouse.position[1])
            time.sleep(__drawspeed__)
            
            mouse.release(Button.left)
            time.sleep(__drawspeed__)
        
        mouse.release(Button.left)
        if __bartype__ == 1:
            print("\nFinished!")
        else:
            print("]\nFinished!")

def ImageFileOption(fn):
    #https://www.tutorialspoint.com/line-detection-in-python-with-opencv
    #thank you
    outdata = []
    img = cv2.imread(fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, numpy.pi/180, 30, maxLineGap=5)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        outdata.append(f"n,{x1+__xoffset__},{y1+__yoffset__}")
        outdata.append(f"{x2+__xoffset__},{y2+__yoffset__}")

    datafileoption_bare(outdata)

def CustomDataFileOption():
    outdata = []

    def on_press(key):
        if key == keyboard.Key.enter:
            x = mouse.position[0]
            y = mouse.position[1]
            outdata.append(f"n,{x},{y}")
            print(f"New line data appended: '{x},{y}'!")
        elif key == keyboard.Key.esc:
            pass
        else:
            x = mouse.position[0]
            y = mouse.position[1]
            outdata.append(f"{x},{y}")
            print(f"Data appended: '{x},{y}'!")

    def on_release(key):
        if key == keyboard.Key.esc:
            open("outdata.json","a").close()
            Dict = {
                "pointarr":outdata
            }
            File = open("outdata.json","w")
            json.dump(Dict,File)
            File.close()
            print("Data file created!")
            return False

    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

def CustomDataFileFromImageOption(fn):
    #https://www.tutorialspoint.com/line-detection-in-python-with-opencv
    #thank you again
    outdata = []
    img = cv2.imread(fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, numpy.pi/180, 30, maxLineGap=5)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        outdata.append(f"n,{x1},{y1}")
        outdata.append(f"{x2},{y2}")
    
    open("outdata_image.json","a").close()
    Dict = {"pointarr":outdata}
    File = open("outdata_image.json","w")
    json.dump(Dict,File)
    File.close()
    print("Data file created!")

def ShowOverlay(fn):
    #So you might say "why didnt you use tkinter for the overlay?"
    #Simple. It sucks and "canvas.create_line()" is shit
    
    pyautogui.screenshot("./bg.png") #We take a screenshot and use it for the "overlay"

    #Screen setup
    window = turtle.Screen()
    window.setup(width=1.0, height=1.0, startx=None, starty=None)

    centerY = window.window_height() / 2 #Center the image(we only need Y)
    centerX = window.window_width() / 2

    #Turtle refs
    try:
        t = turtle.Turtle()
    except Terminator: 
        #https://stackoverflow.com/questions/50438762/python-turtle-window-crashes-every-2nd-time-running
        #....WHY????????????????
        t = turtle.Turtle()
    
    s = turtle.Screen()

    mode("world") #I forgot what this does but if its not here it ruins everything

    t.hideturtle() #Hide the turtle
    t.color("red")

    s.bgpic("bg.png") #Set the image as the background making a "overlay"
    s.title("Image Preview")
    s.tracer(0,0) #Disable draw animation
    s.update()

    def invert(x,side):
        if side == 0:
            #When Negative-Positive: Image is at normal state(left) and matches original image
            #When Positive-Negative: Image is flipped on the X and appears on the right
            if x <= centerX:
                return -abs(centerX-x)
            else:
                return abs(x-centerX)
        elif side == 1:
            #When Positive-Negative: Image matches original image in terms of Y axis. Position of the image depends on the X
            #When Negative-Positive: Image is flipped on the Y. Position of the image depends on the X 
            if x <= centerY:
                return abs(centerY-x)
            else:
                return -abs(x-centerY)
    # def OLD_invert(x):
    #     if x < 0:
    #         return abs(x)#make positive
    #     else:
    #         return -abs(x)#make negative
    
    #We need to invert the numbers because of how turtle maps the screen(see comment drawing below)
    #stupid but whatever

    #################\\#################
    #####(-x,+y)#####\\#####(+x,+y)#####
    #################\\#################
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #################\\#################
    #####(-x,-y)#####\\#####(+x,-y)#####
    #################\\#################

    with open(fn+".json","r") as dataFile:
        JSONData = json.load(dataFile)
        pointArr = JSONData["pointarr"]

        #Similar to "Draw from x" we must hold(pendown) and release(penup) the Lmb(turtle)
        t.penup()
        t.goto(invert(getXandY(pointArr[0],0) + __xoffset__,0),invert(getXandY(pointArr[0],1) + __yoffset__,1)) #First entry is the start position
        for i in range(1,len(pointArr)): #Skip first enrty
            if "n" in pointArr[i]:
                t.goto(invert(getXandY(pointArr[i],0) + __xoffset__,0),invert(getXandY(pointArr[i],1) + __yoffset__,1))

            t.pendown()
            t.goto(invert(getXandY(pointArr[i],0) + __xoffset__,0),invert(getXandY(pointArr[i],1) + __yoffset__,1))
            t.penup()
    
    s.mainloop()

#Main loop
print(f"Free Draw Bot v{__version__}\nMade by The-Glit-ch({__author__})")
load_settings()
while True:
    print("--------------------")
    print("Please choose an option:\n(1) Draw from data file\n(2) Draw from image\n(3) Make your own data file\n(4) See preview\n(5) Change settings")
    while True:
        option_raw = input(":")
        try:
            option = int(option_raw)
            break
        except Exception:
            print("Please enter in a valid option")
    
    if option == 1: #Draw from data file
        print("Enter in the file name")
        while True:
            fn = str(input(":")).replace(".json","") #If the user is stupid and puts "filename.json"
            if os.path.exists(fn+".json"):
                print("In case of an emergency move your mouse to the top left corner to stop the program")
                print(f"Drawing process will begin in {__time__} seconds. Please switch to your drawing app or game client")
                time.sleep(__time__)
                DataFileOption(fn)
                break
            else:
                print("Please enter in a valid file name")
    elif option == 2: #Draw from image file
        print("Enter in the file name of the image(with extension)")
        while True:
            fn = input(":")
            if os.path.exists(fn):
                print("In case of an emergency move your mouse to the top left corner to stop the program")
                print(f"Drawing process will begin in {__time__} seconds. Please switch to your drawing app or game client")
                time.sleep(__time__)
                ImageFileOption(fn)
                break
            else:
                print("Please enter in a valid file name with extension")
    elif option == 3: #Make data file
        print("Please choose an option:\n(1) Make a new empty data file\n(2) Make a data file from an image\n(3) Back")
        while True:
            option_raw = input(":")
            try:
                option = int(option_raw)
                break
            except Exception:
                print("Please enter in a valid option")
        
        if option == 1: #Make a new blank data file
            print("Controls:\nAny Key: Mark a new point\n'Enter': Mark a new seperate point\n'Esc': Create and output the data file")
            CustomDataFileOption()
        elif option == 2: #Make a data file from an image
            print("Enter in the file name of the image(with extension)")
            while True:
                fn = input(":")
                if os.path.exists(fn):
                    CustomDataFileFromImageOption(fn)
                    break
                else:
                    print("Please enter in a valid file name with extension")
        elif option == 3: #Return
            pass
        else:
            print("Please enter in a valid option")
    elif option == 4: #Preview
        print("Enter in the data file name")
        while True:
            fn = str(input(":")).replace(".json","") #If the user is stupid and puts "filename.json"
            if os.path.exists(fn+".json"):
                print("Now previewing")
                ShowOverlay(fn)
                os.remove("bg.png") #Should remove image when window is closed
                break
            else:
                print("Please enter in a valid data file name")
    elif option == 5: #Settings
        print("Please choose an option:\n(1) Change start delay\n(2) Change drawing speed\n(3) Change drawing offset\n(4) Change the progress bar style\n(5) View current settings\n(6) Back")
        option_raw = input(":")
        try:
            option = int(option_raw)
        except Exception:
            print("Please enter in a valid option")
        
        if option == 1: #Change start delay
            print("Enter in a number")
            while True:
                delay_raw = input(":")
                try:
                    delay = int(delay_raw)
                    break
                except Exception:
                    print("Please enter in a valid number")

            print(f"Are you sure you want to set the delay time to: {delay}?(y/n)")
            option_raw = input(":")
            while True:
                if option_raw == "y" or option_raw == "yes":
                    print(f"Start delay time now set to {delay} seconds")
                    __time__ = delay
                    save_settings()
                    break
                elif option_raw == "n" or option_raw == "no":
                    print("Canceling...")
                    break
                else:
                    print("Please enter in a valid option")
        elif option == 2: #Change draw speed
            print("Enter in a number(Higher = Slower, Lower = Faster)")
            while True:
                speed_raw = input(":")
                try:
                    speed = float(speed_raw)
                    break
                except Exception:
                    print("Please enter in a valid number")
            
            print(f"Are you sure you want to set the drawing speed to: {speed}?(y/n)")
            option_raw = input(":")
            while True:
                if option_raw == "y" or option_raw == "yes":
                    print(f"Drawing speed now set to {speed} seconds")
                    __drawspeed__ = speed
                    save_settings()
                    break
                elif option_raw == "n" or option_raw == "no":
                    print("Canceling...")
                    break
                else:
                    print("Please enter in a valid option")
        elif option == 3: #Change offset
            print("Which offset would you like to change?\n(1) X\n(2) Y")
            while True:
                option_raw = input(":")
                try:
                    option = int(option_raw)
                    break
                except Exception:
                    print("Please enter in a valid option")
            
            if option == 1: #Change X offset
                print("Enter in a number")
                while True:
                    Xnumber_raw = input(":")
                    try:
                        Xnumber = abs(int(Xnumber_raw)) #pynput dosent support -numbers for mouse.position I believe
                        break
                    except Exception:
                        print("Please enter in a valid number")
                    
                print(f"Are you sure you want to set the X offset to: {Xnumber}?(y/n)")
                option_raw = input(":")
                while True:
                    if option_raw == "y" or option_raw == "yes":
                        print(f"X offset now set to {Xnumber}")
                        __xoffset__ = Xnumber
                        save_settings()
                        break
                    elif option_raw == "n" or option_raw == "no":
                        print("Canceling...")
                        break
                    else:
                        print("Please enter in a valid option")

            if option == 2: #Change Y offset
                print("Enter in a number")
                while True:
                    Ynumber_raw = input(":")
                    try:
                        Ynumber = abs(int(Ynumber_raw)) #pynput dosent support -numbers for mouse.position I believe
                        break
                    except Exception:
                        print("Please enter in a valid number")
                    
                print(f"Are you sure you want to set the Y offset to: {Ynumber}?(y/n)")
                option_raw = input(":")
                while True:
                    if option_raw == "y" or option_raw == "yes":
                        print(f"Y offset now set to {Ynumber}")
                        __yoffset__ = Ynumber
                        save_settings()
                        break
                    elif option_raw == "n" or option_raw == "no":
                        print("Canceling...")
                        break
                    else:
                        print("Please enter in a valid option")
        elif option == 4: #Change progress bar style
            print(f"Please select a style\n(1) 100% done\n(2) [||||||||||||]")
            while True:
                option_raw = input(":")
                try:
                    option = int(option_raw)
                    break
                except Exception:
                    print("Please enter in a valid option")
            
            if option == 1:
                print(f"Bar style changed to option {option}")
                __bartype__ = option
                save_settings()
            if option == 2:
                print(f"Bar style changed to option {option}")
                __bartype__ = option
                save_settings()
        elif option == 5: #View current settings
            style = None
            if __bartype__ == 1:
                style = f"100% done!"
            elif __bartype__ == 2:
                style = "[|||||||||||||||||]"
            
            print(f"[Current Settings]\nStart delay: {__time__}\nDraw Speed: {__drawspeed__}\nOffsets:\n  X: {__xoffset__}\n  Y: {__yoffset__}\nProgress Bar Style: {__bartype__}\nPrev: {style}")
        elif option == 6: #Back
            pass 
    else:
        print("Please enter in a valid option")