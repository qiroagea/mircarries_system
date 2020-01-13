from include.yolo_setup import *
import time
from include.darknet import Darknet
import pickle as pkl


class ObjectDetection:
    def __init__(self):
        cfg_file = "../data/yolov3-tiny.cfg"
        weights_file = "../data/yolov3-tiny.weights"
        num_classes = 80

        args = arg_parse()
        confidence = float(args.confidence)
        nms_thesh = float(args.nms_thesh)
        start = 0

        bbox_attrs = 5 + num_classes

        model = Darknet(cfg_file)
        model.load_weights(weights_file)

        model.net_info["height"] = args.reso
        inp_dim = int(model.net_info["height"])

        assert inp_dim % 32 == 0
        assert inp_dim > 32

        model.eval()

        video_file = 'video.avi'

        cap = cv2.VideoCapture(0)

        assert cap.isOpened(), 'Cannot capture source'

        # frames = 0
        start = time.time()

    def human(self):
        ret, frame = cap.read()
        if ret:
            img, orig_im, dim = prep_img(frame, inp_dim)

            output = model(Variable(img), CUDA)
            output = write_results(
                output,
                confidence,
                num_classes,
                nms=True,
                nms_conf=nms_thesh
            )

            if type(output) == int:
                # frames += 1
                # continue
                return -1

            output[:, 1:5] = torch.clamp(output[:, 1:5], 0.0, float(inp_dim)) / inp_dim

            output[:, [1, 3]] *= frame.shape[1]
            output[:, [2, 4]] *= frame.shape[0]

            # classes = load_classes('../data/coco.names')
            # colors = pkl.load(open("../data/pallete", "rb"))

            list(map(lambda x: write_cli(x), output))

            # frames += 1
            return 0

        else:
            return -1
