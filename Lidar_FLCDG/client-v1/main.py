import argparse
import os
import cv2
import numpy as np
import socket
from Client import Client
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow


def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
                (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame


def threadBoth(source=0):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()
    c = Client()
    c.img = video_getter.frame
    c.start()

    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        img = video_getter.frame
        img = putIterationsPerSec(img, cps.countsPerSec())
        c.img = img
        video_shower.frame = img
        cps.increment()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=0,
                    help="Path to video file or integer representing webcam index"
                         + " (default 0).")
    args = vars(ap.parse_args())

    # If source is a string consisting only of integers, check that it doesn't
    # refer to a file. If it doesn't, assume it's an integer camera ID and
    # convert to int.
    if (
            isinstance(args["source"], str)
            and args["source"].isdigit()
            and not os.path.isfile(args["source"])
    ):
        args["source"] = int(args["source"])

    threadBoth(args["source"])


if __name__ == "__main__":
    main()
