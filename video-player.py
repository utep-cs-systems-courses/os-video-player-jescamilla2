#!/usr/bin/env python3

import cv2
import threading
from Queue import Queue

# globals
outputDir = 'frames'
clipFileName = 'clip.mp4'
frameDelay = 42  # the answer to everything

'''
produces for queue1
'''
def extract_frames(q):
    global clipFileName                            # global variable from above
    count = 0                                      # initialize frame count
    vidcap = cv2.VideoCapture(clipFileName)        # open the video clip
    success, image = vidcap.read()                 # read one frame

    print(f'Reading frame {count} {success}\n')
    while success:
        q.enqueue(image)                           # send frame to queue (replaces line 26 from demo)
        success, image = vidcap.read()
        print(f'Reading frame {count}')
        count += 1

    # Determine whether you are at the end of the file
    q.enqueue('END')

'''
consumes from queue1 and produces for queue2
'''
def convert_to_grayscale(q1, q2):
    count = 0                                                          # initialize frame count          

    while True:
        inputFrame = q1.dequeue()                                      # next frame

        if inputFrame == 'END':
            break
        print(f'Converting frame {count}\n')
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)  # convert to grayscale
        q2.enqueue(grayscaleFrame)                                     # input for q2
        count += 1

    # When gray scale is done, enqueue END
    q2.enqueue('END')

'''
consumes from queue2
'''
def display_frames(q):
    count = 0                                      # initializes frame count      

    while True:
        frame = q.dequeue()                        # load the frame

        # We have reached end of video
        if frame == 'END':
            break

        print(f'Displaying frame {count}\n')
        cv2.imshow('Video', frame)                 # Display frame in window "Video"

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break

        count += 1

    cv2.destroyAllWindows()                        # cleanup windows

'''
the actual program starts here. It goes something like this...

t1 ===> [q1] ===> t2 ===> [q2] ===> t3

'''

q1 = Queue()  # thread1 produces for queue1, thread2 consumes from queue1
q2 = Queue()  # thread2 produces for queue2, thread3 consumes from queue2


'''
class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)

This constructor should always be called with keyword arguments. Arguments are:

target is the callable object to be invoked by the run() method. 
Defaults to None, meaning nothing is called.

args is the argument tuple for the target invocation. Defaults to ().
'''
t1 = threading.Thread(target=extract_frames, args=(q1,))
t2 = threading.Thread(target=convert_to_grayscale, args=(q1, q2 ))
t3 = threading.Thread(target=display_frames, args=(q2,))

# Start executing all threads
t1.start()
t2.start()
t3.start()
