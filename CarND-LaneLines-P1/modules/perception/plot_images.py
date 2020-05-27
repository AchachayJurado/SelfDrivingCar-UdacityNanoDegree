import matplotlib.pyplot as plt


def PlotOriginalAndProcessed(filename, total_images, original_image, ego_lanes_image, image_number):
    plot_original_and_processed = plt.figure(171, figsize=(80, 25))
    plot_original_and_processed.add_subplot(2, total_images, image_number)
    plt.imshow(original_image)
    plt.title(
        filename), plt.xticks([]), plt.yticks([])
    plot_original_and_processed.add_subplot(
        2, total_images, image_number+total_images)
    plt.imshow(ego_lanes_image)
    plt.savefig('test_images_output/originalVsProcessed.jpg')


def PlotLaneFindingProcess(filename, gray_image, blur_image, canny_image, region_of_interest, lines_in_image, ego_lanes_image, image_number):
    fig_lane_finding_process = plt.figure(image_number, figsize=(25, 10))
    fig_lane_finding_process.add_subplot(2, 3, 1)
    plt.imshow(gray_image, cmap='gray')
    plt.title("Gray Scaled Image")
    fig_lane_finding_process.add_subplot(2, 3, 2)
    plt.imshow(blur_image, cmap='gray')
    plt.title("Blurred Image")
    fig_lane_finding_process.add_subplot(2, 3, 3)
    plt.imshow(canny_image, cmap='gray')
    plt.title("Edges in the Image"), plt.xticks([]), plt.yticks([])
    fig_lane_finding_process.add_subplot(2, 3, 4)
    plt.imshow(region_of_interest, cmap='gray')
    plt.title("Region Of Interest"), plt.xticks([]), plt.yticks([])
    fig_lane_finding_process.add_subplot(2, 3, 5)
    plt.imshow(lines_in_image, cmap='gray')
    plt.title("Lines in Image"), plt.xticks([]), plt.yticks([])
    fig_lane_finding_process.add_subplot(2, 3, 6)
    plt.imshow(ego_lanes_image, cmap="gray")
    plt.title("Ego Lanes Found"), plt.xticks([]), plt.yticks([])
    plt.savefig('test_images_output/process_'+filename)
