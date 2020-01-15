from __future__ import division
from include.util import *
import random
import argparse
import pickle as pkl
from include.motor_control import Control
import time

classes = load_classes("data/coco.names")
colors = pkl.load(open("data/pallete", "rb"))
control = Control()


def get_test_input(input_dim, cuda):
    image = cv2.imread("imgs/messi.jpg")
    image = cv2.resize(image, (input_dim, input_dim))
    img_ = image[:, :, ::-1].transpose((2, 0, 1))
    img_ = img_[np.newaxis, :, :, :] / 255.0
    img_ = torch.from_numpy(img_).float()
    # noinspection PyArgumentList
    img_ = Variable(img_)
    if cuda:
        img_ = img_.cuda()
    return img_


def prep_img(image, inpDim):
    """
    Prepare image for inputting to the neural network.

    Returns a Variable
    """
    origIm = image
    dimension = origIm.shape[1], origIm.shape[0]
    image = cv2.resize(origIm, (inpDim, inpDim))
    img_ = image[:, :, ::-1].transpose((2, 0, 1)).copy()
    img_ = torch.from_numpy(img_).float().div(255.0).unsqueeze(0)
    return img_, origIm, dimension


def write(x, image):
    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    color = random.choice(colors)
    cv2.rectangle(image, c1, c2, color, 1)
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
    c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
    cv2.rectangle(image, c1, c2, color, -1)
    cv2.putText(image, label, (c1[0], c1[1] + t_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)
    return image


def write_cli(x):
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    print(label)


def person_safe(x):
    cls = int(x[-1])
    label = "{0}".format(classes[cls])
    print(label)
    if label == "person":
        control.stop()
        time.sleep(3)


def arg_parse():
    """
    Parse arguements to the detect module

    """
    parser = argparse.ArgumentParser(description='YOLO v3 Cam Demo')
    parser.add_argument("--confidence", dest="confidence", help="Object Confidence to filter predictions", default=0.25)
    parser.add_argument("--nms_thresh", dest="nms_thresh", help="NMS Threshhold", default=0.4)
    parser.add_argument(
        "--reso",
        dest='reso',
        help="Input resolution of the network. Increase to increase accuracy. Decrease to increase speed",
        default="160",
        type=str
    )
    return parser.parse_args()
