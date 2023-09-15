import cv2
import vidgear

# URL de la vidéo YouTube en entrée
stream = CamGear(source="https://www.youtube.com/watch?v=gxG3pdKvlIs", y_tube =True, time_delay=1, logging=True).start() # YouTube Video URL as input
print(stream)
while True:
    frame = stream.read()
    if frame is None:
      break
      
    cv2.imshow("Output Frame", frame)
    key = cv2.waitKey(30)

    if key == ord("q"):
      break

cv2.destroyAllWindows()
stream.stop()
