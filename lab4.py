import threading
import time
import cv2
import base64
import queue
 
frame_queue = queue.Queue()
 
# Declaring Semaphores
mutex = threading.Semaphore()
empty = threading.Semaphore(10)
full = threading.Semaphore(0)

# Globals For Producing
outputDir    = 'frames'
clipFileName = 'clip.mp4'
 
# Producer Thread Class
class Producer(threading.Thread):
    def run(self):
     
        global frame_queue, mutex, empty, full

        # open the video clip
        vidcap = cv2.VideoCapture(clipFileName)
        
        frame_produced = 0
        while True:
            if not frame_queue.full():
                # Accquire mutex
                empty.acquire()
                mutex.acquire()

                # Read one frame
                success,image = vidcap.read()
                print(f'Reading frame {frame_produced} {success}')

                # Encode frame
                success, jpgImage = cv2.imencode('.jpg', image)
                jpgAsText = base64.b64encode(jpgImage)

                # Add frame to buffer
                frame_queue.put(image)
                
                # Release mutex
                mutex.release()
                full.release()
                
                time.sleep(.1)
                frame_produced += 1
    
 
# Consumer Thread Class
class Consumer(threading.Thread):
    def run(self):
     
        global frame_queue, mutex, empty, full
        
        frame_consumed = 0
        while True:
            if not frame_queue.empty():
                # Accquire mutex
                full.acquire()
                mutex.acquire()
                
                # Remove frame from buffer
                frame = frame_queue.get()

                # Display frame
                print(f'Displaying frame {frame_consumed}')
                cv2.imshow('Video', frame)
                if cv2.waitKey(42) and 0xFF == ord("q"):
                    break
                
                # Release mutex
                mutex.release()
                empty.release()      
                
                time.sleep(.2)
                frame_consumed += 1
                
            # Clean up
            print('Finished displaying all frames')
            cv2.destroyAllWindows()












 
# Creating threads & queue
producer = Producer()
consumer = Consumer()
 
# Starting threads
consumer.start()
producer.start()
 
# Waiting for threads to complete
producer.join()
consumer.join()