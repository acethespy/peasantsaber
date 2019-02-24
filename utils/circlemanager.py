from datetime import datetime, timedelta
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
        self.period = 4
        self.speed = 4
        self.lastTime = datetime.now()

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
        self.radii.append(20)
        self.colors.append((0, 0, 0))

    def drawCircles(self):
        for i in range(len(self.centers)):
            self.cv2.circle(image_np, self.centers[i], (int)(self.radii[i]), self.colors[i], thickness=-1)

    def moveCircles(self):
        for i in range(len(self.centers)):
            loc = self.centers[i]
            self.centers[i] = (loc[0], speed * (datetime.now() - self.lastTime))

    def checkCollision(self, height):
        lenn = len(self.centers)
        removeThese = []
        for i in range(lenn):
            loc = self.centers[lenn - 1 - i]
            if (loc[1] < height*2/3):
                removeThese.append(lenn - 1 - i)
        for i in removeThese:
            self.centers.pop(i)

    def update(self, width, height, image_np):

        # XXX: randomize or use file
        if (self.pattern == None):
            if datetime.now() - self.start_time >= timedelta(seconds = self.period):
                createDefaultCircle(self, width, height)
                self.start_time = time

        else:
            # XXX:
            return None
        checkCollision(self, height)
        moveCircles(self)
        drawCircles(self)
        self.lastTime = datetime.now()
