# Import packages
import os
import cv2
import numpy as np
import importlib.util
import time
import sounddevice as sd
import soundfile as sf

# Import TensorFlow libraries
# Import interpreter from tflite_runtime
pkg = importlib.util.find_spec('tflite_runtime')
from tflite_runtime.interpreter import Interpreter

#Initilize location of .tflite and label map file
GRAPH_NAME = '/home/project/tflite1/custom_model_lite5/detect_quant.tflite'
LABELMAP_NAME = '/home/project/tflite1/custom_model_lite5/labelmap.txt'


# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]


# Load the Tensorflow Lite model.
interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]


outname = output_details[0]['name']
boxes_idx, classes_idx, scores_idx = 1, 3, 0


x = 0
#parameters to calculate frame per second    
counter = 0
fps = 0
start_time = time.time()
fps_avg_frame_count = 10

# initialise capture
cap = cv2.VideoCapture(0)
cap.set(3,480) # set Width #3
cap.set(4,360) # set Height #4
cap.set(cv2.CAP_PROP_FPS, 10)
imW = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
imH = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while(cap.isOpened()):

    # Acquire frame and resize to expected shape [1xHxWx3]
    ret, frame = cap.read()
    if not ret:
      print('Reached the end of the video!')
      break
    #Calculating fps
    counter += 1
    if counter % fps_avg_frame_count == 0:
        end_time = time.time()
        fps = fps_avg_frame_count / (end_time - start_time)
        start_time = time.time()
        
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)


    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects
    if (x == 10):
        for i in range(2):
            if  scores[i] > 0.5:
                if classes[i] == 3.:
                    filename = 'stopsign.wav'
                    # Extract data and sampling rate from file
                    data, fs = sf.read(filename, dtype='int16')  
                    sd.play(data, fs)
                    status = sd.wait()
                    
                if classes[i] == 1.:
                    filename = 'redlight.wav'
                    # Extract data and sampling rate from file
                    data, fs = sf.read(filename, dtype='int16')  
                    sd.play(data, fs)
                    status = sd.wait()
                    
                if classes[i] == 2.:
                    filename = 'greenlight.wav'
                    # Extract data and sampling rate from file
                    data, fs = sf.read(filename, dtype='int16')  
                    sd.play(data, fs)
                    status = sd.wait()          
        x = 0
    x+=1
    # Loop over all detections and draw detection box if confidence is above minimum threshold
    for i in range(len(scores)):
        if ((scores[i] > 0.5) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 4)

            # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
            
        
        cv2.putText(frame,'FPS: {0:.2f}'.format(fps),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
