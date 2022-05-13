import threading
import queue
import cv2
import base64

# Colors for printing in terminal
class bcolors:
    OKBLUE = '\033[94m'
    ENDC = '\033[0m'


# Extracts frames
class Extract(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(Extract,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        # Open the video clip
        vidcap = cv2.VideoCapture('clip.mp4')

        frame_count = 0

        # Get first frame
        success,image = vidcap.read()
        print('Extracting frame: ' + str(frame_count))

        while success and frame_count < 100:
            if not q.full():
                #Encode an put in queue
                success, jpgImage = cv2.imencode('.jpg', image)
                jpgAsText = base64.b64encode(jpgImage)
                q.put(frame_count)

                # Get next frame
                success,image = vidcap.read()
                frame_count += 1
                print('Extracting frame: ' + str(frame_count))

        print(f"{bcolors.OKBLUE}Finished extracting all frames{bcolors.ENDC}")
        return


# Converts frames to grayscale
class Convert(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(Convert,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        frame_count = 0
        while frame_count < 100:
            if not q.empty():

                # Get frame 
                frame = q.get()

                # Convert it
                print('Converting Frame: ' + str(frame_count))
                #grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    

                # Put it back
                q2.put(frame_count)

                frame_count += 1
        
        print(f"{bcolors.OKBLUE}Finished converting all frames{bcolors.ENDC}")
        return


# Dsiplays converted frames
class Display(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(Display,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        frame_count = 0
        while frame_count < 100:
            if not q2.empty():
                
                # Get frame
                frame = q2.get()

                # Display it
                print('Displaying Frame: ' + str(frame_count))
                # cv2.imshow('Video', frame)
                # if cv2.waitKey(42) and 0xFF == ord("q"):
                #     break

                frame_count += 1
        
        print(f"{bcolors.OKBLUE}Finished displaying all frames{bcolors.ENDC}")
        cv2.destroyAllWindows()
        return


if __name__ == '__main__':
    
    q = queue.Queue(10)
    q2 = queue.Queue(10)

    e = Extract(name='producer')
    c = Convert(name='grayscale')
    d = Display(name='consumer')

    e.start()
    c.start()
    d.start()
