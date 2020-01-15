from __future__ import division
from include.darknet import Darknet
from include.yolo_setup import *


class ObjectDetection:
    def __init__(self):
        cfgfile = "data/yolov3-tiny.cfg"
        weightsfile = "data/yolov3-tiny.weights"
        num_classes = 80

        args = arg_parse()
        self.confidence = float(args.confidence)
        self.nms_thesh = float(args.nms_thresh)
        start = 0
        self.CUDA = torch.cuda.is_available()

        # noinspection PyRedeclaration
        self.num_classes = 80
        bbox_attrs = 5 + num_classes

        self.model = Darknet(cfgfile)
        self.model.load_weights(weightsfile)

        self.model.net_info["height"] = args.reso
        self.inp_dim = int(self.model.net_info["height"])

        assert self.inp_dim % 32 == 0
        assert self.inp_dim > 32

        if self.CUDA:
            self.model.cuda()

        self.model.eval()

        videofile = 'video.avi'

        self.cap = cv2.VideoCapture(0)

        assert self.cap.isOpened(), 'Cannot capture source'

        self.frames = 0
        start = time.time()

    def human(self):
        ret, frame = self.cap.read()
        if ret:

            img, orig_im, dim = prep_img(frame, self.inp_dim)

            if self.CUDA:
                # noinspection PyUnboundLocalVariable
                self.im_dim = self.im_dim.cuda()
                img = img.cuda()

            output = self.model(Variable(img), self.CUDA)
            output = write_results(output, self.confidence, self.num_classes, nms=True, nms_conf=self.nms_thesh)

            if type(output) == int:
                self.frames += 1
                # print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
                return

            output[:, 1:5] = torch.clamp(output[:, 1:5], 0.0, float(self.inp_dim)) / self.inp_dim

            output[:, [1, 3]] *= frame.shape[1]
            output[:, [2, 4]] *= frame.shape[0]

            list(map(lambda x: person_safe(x), output))

            print(lambda x:person_safe(x))

            self.frames += 1
            # print("FPS of the video is {:5.2f}".format(frames / (time.time() - start)))
        else:
            return
