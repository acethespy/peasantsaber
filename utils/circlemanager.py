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
        self.period = 1
        self.speed = 50
        self.lastTime = datetime.now()
        self.margin = 20
        self.explodeCenters = []
        self.explodeRadii = []
        self.explodeColors = []
        self.explodeFactor = 50
        self.explodeMax = 45;
        self.score = 0


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
        self.radii.append(30)
        self.colors.append((0, 0, 0))

    def drawCircles(self, image_np):
        for i in range(len(self.centers)):
            self.cv2.circle(image_np, ((int)(self.centers[i][0]), (int)(self.centers[i][1])), (int)(self.radii[i]), self.colors[i], thickness=-1)
        for i in range(len(self.explodeCenters)):
            self.cv2.circle(image_np, ((int)(self.explodeCenters[i][0]), (int)(self.explodeCenters[i][1])), (int)(self.explodeRadii[i]), self.explodeColors[i], thickness=-1)

    def moveCircles(self):
        for i in range(len(self.centers)):
            loc = self.centers[i]
            self.centers[i] = (loc[0], loc[1] - self.speed * (datetime.now() - self.lastTime).total_seconds())
        for i in range(len(self.explodeCenters)):
            self.explodeRadii[i] += self.explodeFactor * (datetime.now() - self.lastTime).total_seconds()

    def checkFailed(self, height):
        lenn = len(self.centers)
        #removeThese = []
        for i in range(lenn):
            loc = self.centers[lenn - 1 - i]
            if (loc[1] < height*2/3 - self.margin):
                self.centers.pop(lenn - 1 - i)
                self.radii.pop(lenn - 1 - i)
                self.colors.pop(lenn - 1 - i)
        lenn = len(self.explodeRadii)
        for i in range(lenn):
            if (self.explodeRadii[lenn - 1 - i] >= self.explodeMax):
                self.explodeCenters.pop(lenn - 1 - i)
                self.explodeRadii.pop(lenn - 1 - i)
                self.explodeColors.pop(lenn - 1 - i)
                #removeThese.append(lenn - 1 - i)
        """for i in removeThese:
            self.centers.pop(i)
            self.radii.pop(i)
            self.colors.pop(i)"""
        

    def hit(self, x, height, width):
        d = None;
        print(len(self.centers))
        for i in range(len(self.centers)):
            loc = self.centers[i]
            print(abs(loc[1] - (height * 2/3)))
            if abs(loc[1] - (height * 2/3)) <= 20 and abs(loc[0] - x) <= (width / 4):
                d = i
        if d is not None:
            self.explodeCenters.append(self.centers.pop(d))
            self.explodeRadii.append(self.radii.pop(d))
            self.colors.pop(d)
            self.explodeColors.append((0, 255, 0))
            print("PERFECT")

    def update(self, width, height, image_np, points):
        # XXX: randomize or use file
        if (self.pattern == None):
            if datetime.now() - self.start_time >= timedelta(seconds = self.period):
                self.createDefaultCircle(width, height)
                self.start_time = datetime.now()

        else:
            # XXX:
            asdf = None
        if points:
            self.hit(points[0][0], height, width)
        self.checkFailed(height)
        self.moveCircles()
        self.drawCircles(image_np)
        self.lastTime = datetime.now()
