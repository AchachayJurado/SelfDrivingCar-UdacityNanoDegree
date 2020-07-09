import cv2
import glob
import matplotlib.pyplot as plt


def loadImagesRGB(path):
    images_list = []
    for fn in glob.glob(path+"/*.jpg"):
        im = cv2.imread(fn)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        images_list.append(gray)

    for fn in glob.glob(path+"/*.png"):
        im = cv2.imread(fn)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        images_list.append(gray)

    return images_list


def saveImage(img, path):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, img)


def saveBeforeAfterImages(before_img, before_text, after_img, after_text, path):
    mydpi = 80
    width = int((before_img.shape[1] + after_img.shape[1] + 20) / mydpi)
    height = int((before_img.shape[0] + after_img.shape[0] + 30) / mydpi)

    figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(
        width, height), dpi=mydpi, frameon=False)
    ax1.imshow(before_img)
    ax1.set_title(before_text, fontsize=30)
    ax2.imshow(after_img)
    ax2.set_title(after_text, fontsize=30)
    figure.savefig(path, bbox_inches='tight',
                   transparent=True,
                   pad_inches=0)
    plt.close(figure)
