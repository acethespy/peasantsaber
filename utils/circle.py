centers = [];
radii = [];
colors = [];

def drawCircles(image_np):
    for i in range(centers.size()):
        cv2.circle(image_np, centers[i], radii[i], colors[i], -1)
