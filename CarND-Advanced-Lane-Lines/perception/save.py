import os
import stat
import matplotlib as plt

import cv2


def save_image(image, filename, prefix="", suffix=""):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)

    out_name = os.path.join("output_images", prefix + name + suffix + ext)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(out_name, image)


def save_image_before_after(original, original_text, after_img, after_text, path):
    mydpi = 80
    width = int((original.shape[1] + after_img.shape[1] + 20) / mydpi)
    height = int((original.shape[0] + after_img.shape[0] + 30) / mydpi)

    figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(
        width, height), dpi=mydpi, frameon=False)
    ax1.imshow(original)
    ax1.set_title(original_text, fontsize=30)
    ax2.imshow(after_img)
    ax2.set_title(after_text, fontsize=30)
    figure.savefig(path, bbox_inches='tight',
                   transparent=True,
                   pad_inches=0)
    plt.close(figure)


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
