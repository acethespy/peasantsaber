from datetime import datetime
import random

class CircleManager(object):

    def __init__(self, cv2):
        print("INITITITITITITI")
        self.cv2 = cv2
        self.centers = []
        self.radii = []
        self.colors = []
        self.start_time = datetime.now()
        self.pattern = None

    """
    def __init__(self, file, cv2):
        self.centers = []
        self.radii = []
        self.colors = []
        self.pattern = [file]
    """

    def createDefaultCircle(self, width, height):
        initialXs = [width // 8, 3 * width // 8, 5 * width // 8, 7 * width // 8]
        self.centers.append(((int)(initialXs[random.randint(0, len(initialXs) - 1)]), (int)(height)))
        self.radii.append(40)
        self.colors.append((0, 0, 0))

    def drawCircles(self, image_np):
        for i in range(len(self.centers)):
            self.cv2.circle(image_np, self.centers[i], (int)(self.radii[i]), self.colors[i], thickness=-1)

    def update(self, time):
        # XXX: randomize or use file
        if (pattern != None):
            # XXX:
            return None
        else:
            # XXX:
            return None

    def checkCollision(self, points):
        # XXX:
        return null
