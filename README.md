# EEE4022S_files
This repository contains all the code and testing video for detection a custom made traffic light and stop sign.


Bellow arre the steps you need to take to get the traffic light and stop sign detection running on a raspberry pi 4

Step 1: In command line run: 

    bash step1_requirements.sh

Step 2: Download the detection_code on the raspberry pi

Step 3: In command line run: 

    cd detection_code

Step 4: In command line run: 

    python3 -m venv objdetec-env

Step 5: In command line run: 

    source objdetec-env/bin/activate

Step 6: In command line run: 

    bash step6_requirements_install.sh

Once everything is done installing, exit directory and deactivate virtual environment by running the following in comand line: 

    cd

step 7:  In command line run: 

    cd detection_code

step 8:  In command line run: 

    bash object_detection_beep.sh 
Or 

    bash object_detection_playaudio.sh

The object_detection_beep.sh will run the beep code while the object_detection_playaudio.sh will run the code that verbally say if it is a red light, green light or stop sign.

To run he code after the Raspberry pi has been restarted, repeet step 7 and 8.

Note:

The following line of code needs to be changed in both script as they are the file path to the detection file. Your parth might be different to the one in the code.

    GRAPH_NAME = '/home/project/tflite1/custom_model_lite5/detect_quant.tflite'
    LABELMAP_NAME = '/home/project/tflite1/custom_model_lite5/labelmap.txt'

It you run into any 'module not found error", run the following in command line followed my the modile name:

    pip3 install
    
 
