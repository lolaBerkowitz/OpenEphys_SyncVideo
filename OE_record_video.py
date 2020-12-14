"""
    A zmq client to test remote control of open-ephys GUI
"""

import zmq
import os
import time
import subprocess
import numpy as np
import cv2
import pandas as pd
from datetime import datetime


def run_client():

    # datetime object containing current date and time
    now = datetime.now()

    # dd-mm-YY-H-M-S 
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")

    # cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap = cv2.VideoCapture(0)

    ## Set properties or else the image is black 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,768)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,494)
    #set focus to 0 so it doesn't autofocus
    cap.set(cv2.CAP_PROP_FOCUS, 0)
    #set the framerate to 30
    cap.set(cv2.CAP_PROP_FPS, 30)
    #set the bitrate to 32
    cap.set(cv2.CAP_PROP_BITRATE, 32)

    # Set up video codec/size parameters. 
    fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('E:/open_ephys/data/'+dt_string+'.avi',fourcc, 30, (width,height))

    # Connect network handler
    ip = 'localhost'
    port = 5556
    timeout = 1.

    url = "tcp://%s:%d" % (ip, port)

    with zmq.Context() as context:
        with context.socket(zmq.REQ) as socket:
            socket.RCVTIMEO = int(timeout * 1000)  # timeout in milliseconds
            socket.connect(url)
            
            # initialize lists for timestamps
            soft_ts = [0.0] # video ts
            event_start = [0.0] # event ts
            event_end = [0.0] # event ts
            # send message to OE to start recordings
            socket.send_string('StartRecord')
            socket.recv_string() 
            start = time.time() # measure time between start record and timestamp record

            while(cap.isOpened()):
                ret, frame = cap.read()

                if ret==True:
                    # write frame
                    out.write(frame)
                    soft_ts.append(time.time())  # timestamp floating point in UTC
                    key = cv2.waitKey(1) & 0xFF # listens for key press every 1ms
                    
                    # To record events
                    if key == ord('s'): # start condition
                        event_start.append(time.time())
                        print('start timestamp recorded')
                    elif key == ord('e'): # end condition
                        event_end.append(time.time())
                        print('stop timestamp recorded')

                    # write frame
                    out.write(frame)

                    # Play frame during recording
                    cv2.imshow('frame',frame)
                    
                    # Quit video 
                    if key == ord('q'):
                        break
  
            cap.release()
            out.release()
            cv2.destroyAllWindows() 

            # okay, recording is over so let's stop OE automatically.
            socket.send_string('StopRecord')
            socket.recv_string()
            end = time.time()
            
            # Finally, stop data acquisition; it might be a good idea to 
            # wait a little bit until all data have been written to hard drive
            time.sleep(5)
            socket.send_string('StopAcquisition')
            socket.recv_string()
            
            ## Save timestamps
            pd.DataFrame(data=soft_ts, columns=["video_ts"]).to_csv('E:/open_ephys/data/'+dt_string+'_video_ts.csv')
            pd.DataFrame(data={'start': np.array(event_start), 'end': np.array(event_end)}).to_csv('E:/open_ephys/data/'+dt_string+'_events_ts.csv')
            pd.DataFrame(data={'start_record': [np.array(start)], 'end_record': [np.array(end)]}).to_csv('E:/open_ephys/data/'+dt_string+'_record_ts.csv')

if __name__ == '__main__':
    run_client()
