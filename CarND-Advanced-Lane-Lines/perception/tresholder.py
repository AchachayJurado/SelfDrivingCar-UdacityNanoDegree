from perception.camera_calibration import *
from perception.undistorter import *
from perception.filtering import *

TEST_IMAGES = glob.glob("test_images/*.jpg")


def edge_finder(image):
    edge_detector = EdgeDetector()
    binary = edge_detector.detect(image)
    return binary, edge_detector


class EdgeDetector(object):

    image = None
    result = None
    s_binary = None
    sobel_all_binary = None

    def __init__(self):
        self.sobel = SobelFilter(kernel_size=13)
        self.hls = HLSFilter()

    def detect(self, image):
        # Image converted to gray scale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # HLS
        s_binary, s_channel = self.hls.filter_s(image)

        # Sobel
        sx_binary, sx_scaled, sobel_x = self.sobel.filter_x(gray)
        sy_binary, sy_scaled, sobel_y = self.sobel.filter_y(gray)
        smag_binary, smag_scaled, sobel_mag = self.sobel.filter_mag(
            sobel_x, sobel_y)
        sdir_binary, sobel_dir = self.sobel.filter_dir(sobel_x, sobel_y)

        # Binary
        sobel_xy_binary = np.zeros_like(sx_binary)
        sobel_xy_binary[(sx_binary == 1) & (sy_binary == 1)] = 1
        sobel_md_binary = np.zeros_like(smag_binary)
        sobel_md_binary[(smag_binary == 1) & (sdir_binary == 1)] = 1
        sobel_all_binary = np.zeros_like(sobel_xy_binary)
        sobel_all_binary[(sobel_xy_binary == 1) | (sobel_md_binary == 1)] = 1

        result = np.zeros_like(sobel_all_binary)
        result[(sobel_all_binary == 1) | (s_binary == 1)] = 1

        # keep results for visualization
        self.image = image
        self.s_binary = cv2.cvtColor(s_binary, cv2.COLOR_GRAY2RGB)
        self.sobel_all_binary = cv2.cvtColor(
            sobel_all_binary, cv2.COLOR_GRAY2RGB)
        self.result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)

        return result

    def display_filtering(self):
        """image + s_binary + sobel_all_binary + output"""

        # Scale Binary Images
        max_value = np.max(self.image)
        self.s_binary = self.s_binary * max_value
        self.sobel_all_binary = self.sobel_all_binary * max_value
        self.result = self.result * max_value

        def put_text(image, text, color=(0, 255, 255)):
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, text, (10, 100), font, 3, color, 5, cv2.LINE_AA)

        # Add descriotion title to the pictures
        put_text(self.result, "Edge Detection")
        put_text(self.s_binary, "HLS: S Channel Binary")
        put_text(self.sobel_all_binary, "Sobel Binary")

        # Build 2x2 image grid
        ca = np.concatenate((self.image, self.result), axis=1)
        cb = np.concatenate((self.s_binary, self.sobel_all_binary), axis=1)
        vis = np.concatenate((ca, cb), axis=0)

        return vis

    def display_result(self, filename, ax):
        vis = self.display_filtering()

        # save
        save_image(vis, filename, "edge_detection_", "_result")

        # show
        ax.imshow(vis)
        ax.axis("off")

    def display_hls(self):
        """image + s_channel + s_binary"""
        pass

    def display_sobel(self):
        """image + sx/thresh + sy/thresh + smag/thresh + sdir/thresh + XY + MD + ALL"""
        pass

    def display_pipeline(self, filename, ax):
        self.display_result(filename, ax)
        self.display_sobel()
        self.display_hls()


def DetectEdges():
    camera = GetCalibratedCamera()

    f, axs = plt.subplots(len(TEST_IMAGES), 1, figsize=(20, 70))
    f.tight_layout()
    for idx, filename in enumerate(sorted(TEST_IMAGES)):
        image = read_image(filename)
        undistorted = undistort_image(image, camera)
        _, edge_detector = edge_finder(undistorted)

        edge_detector.display_pipeline(filename, axs[idx])

    plt.show()
