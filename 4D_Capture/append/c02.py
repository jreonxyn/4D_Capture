import cv2

class c02:
    def __init__(self, image):
        self.image = image

    def img_resize(image):
        height, width = image.shape[0], image.shape[1]
        width_new = 1440
        height_new = 900
        if width / height >= width_new / height_new:
            img_new = cv2.resize(image, (width_new, int(height * width_new / width)))
        else:
            img_new = cv2.resize(image, (int(width * height_new / height), height_new))
        return img_new
