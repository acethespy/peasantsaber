from datetime import datetime

class CircleManager:

    start_time = datetime.now()

    def __init__():
        self.centers = []
        self.radii = []
        self.colors = []
        self.pattern = None;

    def __init__(file):
        self.centers = []
        self.radii = []
        self.colors = []
        self.pattern = [file]

    def createDefaultCircle(width):
        initialXs = [width / 8, 3 * width / 8, 5 * width / 8, 7 * width / 8]
        centers.append(selectRandom(initialXs))
        radii.append(40)
        colors.append((0, 0, 0))

    def drawCircles(image_np):
        for i in range(centers.size()):
            cv2.circle(image_np, centers[i], radii[i], colors[i], -1)

    def update(time):
        # XXX: randomize or use file
        if (pattern != None):
            # XXX:
            return None
        else:
            # XXX:
            return None

    def checkCollision(points):
        # XXX:
        return null

    def selectRandom(array):
        return array[random.randomint(0, array.size())]
