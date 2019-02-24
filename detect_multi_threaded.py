from utils import detector_utils as detector_utils
import cv2
import tensorflow as tf
import multiprocessing
from multiprocessing import Queue, Pool
import time
from utils.detector_utils import WebcamVideoStream
from datetime import datetime
import argparse
from utils import circlemanager

frame_processed = 0
score_thresh = 0.2

point = None;
manager = None;
crossed = False;

def aboveThreshhold(pointA, height):
    return pointA[1] < height*2/3;

# Create a worker thread that loads graph and
# does detection on images in an input queue and puts it on an output queue

def worker(input_q, output_q, cap_params, frame_processed, points):
    print(">> loading frozen model for worker")
    detection_graph, sess = detector_utils.load_inference_graph()
    sess = tf.Session(graph=detection_graph)
    prevPoint = None;
    while True:
        #print("> ===== in worker loop, frame ", frame_processed)
        frame = input_q.get()
        if (frame is not None):
            # Actual detection. Variable boxes contains the bounding box cordinates for hands detected,
            # while scores contains the confidence for each of these boxes.
            # Hint: If len(boxes) > 1 , you may assume you have found atleast one hand (within your score threshold)

            boxes, scores = detector_utils.detect_objects(
                frame, detection_graph, sess)
            # draw bounding boxes
            detectedPoint = detector_utils.draw_box_on_image(
                cap_params['num_hands_detect'], cap_params["score_thresh"],
                scores, boxes, cap_params['im_width'], cap_params['im_height'],
                frame)
            point = detectedPoint

            if detectedPoint is not None:
                #print(detectedPoint)
                if prevPoint is not None:
                    if aboveThreshhold(prevPoint, cap_params["im_height"]) and not aboveThreshhold(detectedPoint, cap_params["im_height"]):
                        print("Detected: " + str(detectedPoint) + "Prev: " + str(prevPoint))
                        print("Under")
                        points.put(detectedPoint);
                    #else:
                        #points.put((-1, -1))
                        #callHits.get()(detectedPoint[0], cap_params["im_height"], cap_params["im_width"])
                        #call circle collision thing
                #else:
                    #points.put((-1, -1))

                prevPoint = detectedPoint
            #else:
                #points.put((-1, -1))
            # add frame annotated with bounding box to queue
            output_q.put(frame)
            frame_processed += 1
        else:
            #points.put((-1, -1))
            output_q.put(frame)
    sess.close()

def get_all_queue_result(queue):

    result_list = []
    while not queue.empty():
        result_list.append(queue.get())

    return result_list

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-src',
        '--source',
        dest='video_source',
        type=int,
        default=0,
        help='Device index of the camera.')
    parser.add_argument(
        '-nhands',
        '--num_hands',
        dest='num_hands',
        type=int,
        default=2,
        help='Max number of hands to detect.')
    parser.add_argument(
        '-fps',
        '--fps',
        dest='fps',
        type=int,
        default=1,
        help='Show FPS on detection/display visualization')
    parser.add_argument(
        '-wd',
        '--width',
        dest='width',
        type=int,
        default=300,
        help='Width of the frames in the video stream.')
    parser.add_argument(
        '-ht',
        '--height',
        dest='height',
        type=int,
        default=200,
        help='Height of the frames in the video stream.')
    parser.add_argument(
        '-ds',
        '--display',
        dest='display',
        type=int,
        default=1,
        help='Display the detected images using OpenCV. This reduces FPS')
    parser.add_argument(
        '-num-w',
        '--num-workers',
        dest='num_workers',
        type=int,
        default=4,
        help='Number of workers.')
    parser.add_argument(
        '-q-size',
        '--queue-size',
        dest='queue_size',
        type=int,
        default=5,
        help='Size of the queue.')
    args = parser.parse_args()

    input_q = Queue(maxsize=args.queue_size)
    output_q = Queue(maxsize=args.queue_size)

    video_capture = WebcamVideoStream(
        src=args.video_source, width=args.width, height=args.height).start()

    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = video_capture.size()
    cap_params['score_thresh'] = score_thresh

    # max number of hands we want to detect/track
    cap_params['num_hands_detect'] = args.num_hands

    print(cap_params, args)

    # spin up workers to paralleize detection.

    manager = circlemanager.CircleManager(cv2)

    #not needed begins
    def callHit(x, height, width):
        manager.hit(x, height, width)
    #not needed ends
    points = Queue(maxsize=args.queue_size)

    pool = Pool(args.num_workers, worker,
                (input_q, output_q, cap_params, frame_processed, points))


    start_time = datetime.now()
    manager.createDefaultCircle(cap_params['im_width'], cap_params['im_height'])
    num_frames = 0
    fps = 0
    index = 0

    #Differ begins
    """
    detection_graph, sess = detector_utils.load_inference_graph()
    sess = tf.Session(graph=detection_graph)
    prevPoint = None;"""
    #Differ ends

    cv2.namedWindow('Multi-Threaded Detection', cv2.WINDOW_NORMAL)


    while True:

        #Differ begins

        """frame = input_q.get()
        if (frame is not None):
            # Actual detection. Variable boxes contains the bounding box cordinates for hands detected,
            # while scores contains the confidence for each of these boxes.
            # Hint: If len(boxes) > 1 , you may assume you have found atleast one hand (within your score threshold)

            boxes, scores = detector_utils.detect_objects(
                frame, detection_graph, sess)
            # draw bounding boxes
            detectedPoint = detector_utils.draw_box_on_image(
                cap_params['num_hands_detect'], cap_params["score_thresh"],
                scores, boxes, cap_params['im_width'], cap_params['im_height'],
                frame)
            point = detectedPoint

            if detectedPoint is not None:
                print(detectedPoint)
                if prevPoint is not None:
                    if aboveThreshhold(prevPoint, cap_params["im_height"]) and not aboveThreshhold(detectedPoint, cap_params["im_height"]):
                        print("Detected: " + str(detectedPoint) + "Prev: " + str(prevPoint))
                        print("Under")
                        manager.hit(detectedPoint[0], cap_params["im_height"], cap_params["im_width"])
                        #call circle collision thing
                prevPoint = detectedPoint
            # add frame annotated with bounding box to queue
            output_q.put(frame)
            frame_processed += 1
        else:
            output_q.put(frame)"""

        #Differ ends


        frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        index += 1

        input_q.put(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        output_frame = output_q.get()
        ##print(points.get())

        output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)

        elapsed_time = (datetime.now() - start_time).total_seconds()
        num_frames += 1
        fps = num_frames / elapsed_time
        # print("frame ",  index, num_frames, elapsed_time, fps)

        if (output_frame is not None):
            pointsList = get_all_queue_result(points)
            detector_utils.draw_base_lines_on_image((int)(cap_params["im_width"]), (int)(cap_params["im_height"]), output_frame)
            manager.update((int)(cap_params["im_width"]), (int)(cap_params["im_height"]), output_frame, pointsList)

            if (args.display > 0):
                if (args.fps > 0):
                    detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                                     output_frame)
                cv2.imshow('PeasantSaber', output_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if (num_frames == 400):
                    num_frames = 0
                    start_time = datetime.now()
                else:
                    print("frames processed: ", index, "elapsed time: ",
                          elapsed_time, "fps: ", str(int(fps)))
        else:
            # print("video end")
            break
    elapsed_time = (datetime.now() - start_time).total_seconds()
    fps = num_frames / elapsed_time
    print("fps", fps)
    pool.terminate()
    video_capture.stop()
    cv2.destroyAllWindows()
