import os
import stat

import cv2


def save_image(image, fname, prefix="", suffix=""):
    basename = os.path.basename(fname)
    name, ext = os.path.splitext(basename)

    out_name = os.path.join("output_images", prefix + name + suffix + ext)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(out_name, image)


def chmod_rw_all(filename):
    os.chmod(
        filename,
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IRGRP
        | stat.S_IWGRP
        | stat.S_IROTH
        | stat.S_IWOTH,
    )


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
