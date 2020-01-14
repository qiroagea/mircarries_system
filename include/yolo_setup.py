from __future__ import division
from include.util import *
import random
import argparse
import pickle as pkl

classes = load_classes('../data/coco.names')
colors = pkl.load(open('../data/pallete', 'rb'))


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


# if __name__ == '__main__':
#     cfgfile = "../data/yolov3-tiny.cfg"
#     weightsfile = "../data/yolov3-tiny.weights"
#     num_classes = 80
#
#     args = arg_parse()
#     confidence = float(args.confidence)
#     nms_thesh = float(args.nms_thresh)
#     start = 0
#     CUDA = torch.cuda.is_available()
#
#     # noinspection PyRedeclaration
#     num_classes = 80
#     bbox_attrs = 5 + num_classes
#
#     model = Darknet(cfgfile)
#     model.load_weights(weightsfile)
#
#     model.net_info["height"] = args.reso
#     inp_dim = int(model.net_info["height"])
#
#     assert inp_dim % 32 == 0
#     assert inp_dim > 32
#
#     if CUDA:
#         model.cuda()
#
#     model.eval()
#
#     videofile = 'video.avi'
#
#     cap = cv2.VideoCapture(0)
#
#     assert cap.isOpened(), 'Cannot capture source'
#
#     frames = 0
#     start = time.time()
#     while cap.isOpened():
#
#         ret, frame = cap.read()
#         if ret:
#
#             img, orig_im, dim = prep_img(frame, inp_dim)
#
#             if CUDA:
#                 # noinspection PyUnboundLocalVariable
#                 im_dim = im_dim.cuda()
#                 img = img.cuda()
#
#             output = model(Variable(img), CUDA)
#             output = write_results(output, confidence, num_classes, nms=True, nms_conf=nms_thesh)
#
#             if type(output) == int:
#                 frames += 1
#                 # print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
#                 continue
#
#             output[:, 1:5] = torch.clamp(output[:, 1:5], 0.0, float(inp_dim)) / inp_dim
#
#             output[:, [1, 3]] *= frame.shape[1]
#             output[:, [2, 4]] *= frame.shape[0]
#
#             classes = load_classes('../data/coco.names')
#             colors = pkl.load(open("../data/pallete", "rb"))
#
#             list(map(lambda x: write_cli(x), output))
#
#             frames += 1
#             # print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
#         else:
#             break