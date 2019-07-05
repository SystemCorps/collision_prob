#!/usr/bin/env python

import os
import cv2
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from glob import glob

import numpy as np



def extractor(fdir, toffset=1.5):
    f_list = [y for x in os.walk(fdir) for y in glob(os.path.join(x[0], '*.bag'))]
    f_list.sort()

    fname = f_list[0]

    bag = rosbag.Bag(fname, "r")
    bridge = CvBridge()

    save_col = fdir + '/bag0/col/'
    save_non = fdir + '/bag0/non/'
    try:
        os.makedirs(save_col)
        os.makedirs(save_non)
    except OSError:
        pass



    loaded = bag.read_messages(topics="/zed/zed_node/depth/depth_registered")
    e_time = bag.get_end_time()


    ncount = 0
    ccount = 0

    for topic, msg, t in loaded:
        t_sec = t.to_sec()

        if t_sec >= (e_time - toffset):
            cv_img = bridge.imgmsg_to_cv2(msg, "32FC1")
            #cv_img_arr = np.array(cv_img, dtype=np.float32)
            cv_img_arr = cv_img.copy()
            cv_img_norm = cv2.normalize(cv_img_arr, cv_img_arr, 0, 1, cv2.NORM_MINMAX)
            cv2.imwrite(save_col+'col%d.png'%ccount, cv_img_norm*255)
            ccount += 1

        else:
            cv_img = bridge.imgmsg_to_cv2(msg, "32FC1")
            #cv_img_arr = np.array(cv_img, dtype=np.float32)
            cv_img_arr = cv_img.copy()
            cv_img_norm = cv2.normalize(cv_img_arr, cv_img_arr, 0, 1, cv2.NORM_MINMAX)
            cv2.imwrite(save_non+'non%d.png'%ncount, cv_img_norm*255)
            ncount += 1



def main():
    bag_list_col = [y for x in os.walk('/home/astra/unc_data/collide') for y in glob(os.path.join(x[0], '*.bag'))]
    bag_list_non = [y for x in os.walk('/home/astra/unc_data/noncol') for y in glob(os.path.join(x[0], '*.bag'))]

    col_dir = '/home/astra/unc_data/collide'
    non_dir = '/home/astra/unc_data/noncol'

    bag_list_col.sort()
    bag_list_non.sort()

    extractor(col_dir)


if __name__ == "__main__":
    main()