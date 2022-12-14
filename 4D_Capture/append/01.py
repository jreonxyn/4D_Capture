import cv2
import c02
from c02 import image_resize

in_str = input("Enter the address of the camera:")
url = "rtsp://" + in_str
cap = cv2.VideoCapture(url)
ret, frame = cap.read()

while ret:
    ret, frame = cap.read()
    frame = image_resize(frame)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()