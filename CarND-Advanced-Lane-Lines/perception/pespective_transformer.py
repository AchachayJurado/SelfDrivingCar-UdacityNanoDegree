from perception.camera_calibration import *
from perception.undistorter import *
from perception.warper import *


TEST_IMAGES = glob.glob("test_images/*.jpg")


def PerspectiveTransform():
    camera = GetCalibratedCamera()
    warper = Warper()

    f, axs = plt.subplots(len(TEST_IMAGES), 1, figsize=(20, 50))
    f.tight_layout()
    for idx, filename in enumerate(sorted(TEST_IMAGES)):
        image = read_image(filename)
        undistorted = undistort_image(image, camera)
        warped = warp_image(warper, undistorted)

        # Draw
        warper.draw_src(undistorted)
        warper.draw_dst(warped)

        # Concatenate
        vis = np.concatenate((undistorted, warped), axis=1)

        # Display Comparison
        axs[idx].imshow(vis)
        axs[idx].axis("off")

        # Save
        save_image(vis, filename, "bird_eye_view_")

    out_filename = os.path.join("output_images", "perspective_transform.png")
    plt.savefig(out_filename)

    plt.show()
