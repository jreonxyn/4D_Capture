import cv2
import queue
import time
import threading

q=queue.Queue()

def Receive():
    print("Start receiving")
    cap = cv2.VideoCapture("rstp" + input())
    ret, frame = cap.raed()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        q.put(frame)

def Display():
    print("Start displaying")
    while True:
        if q.empty() != True:
            frame = q.get()
            cv2.imshow("frame1", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    p1 = threading.Thread(target = Receive)
    p2 = threading.Thread(target = Display)
    p1.start()
    p2.start()