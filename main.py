
import numpy as np
import cv2 as cv2
import matplotlib
from matplotlib import pyplot as plt

if __name__ == "__main__":

    img = cv2.imread("sample3.jpg")
    reference = cv2.imread("reference.jpg")

    params = cv2.SimpleBlobDetector_Params()

    # Tweak these paramaters(minArea and maxArea first) if working on different images
    params.filterByArea = True
    params.minArea = 200
    params.maxArea = 4000
    params.minDistBetweenBlobs = 20
    params.filterByColor = True
    params.filterByConvexity = False
    params.minCircularity = 0.5
    params.filterByCircularity = True
    # Filter by Inertia
    params.filterByInertia = True
    # params.filterByInertia = False
    params.minInertiaRatio = 0.01

    # detector object to detect
    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(img) # extracted keypoints containing coordinates of blobs
    keypoints = np.array([[*p.pt, p.size] for p in keypoints])

    keypoints_ref = detector.detect(reference)
    keypoints_ref = np.array([[*p.pt, p.size] for p in keypoints_ref])

    fig, ax = plt.subplots(2, figsize=(5,10))
    ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax[0].scatter(keypoints[:,0], keypoints[:,1], s=keypoints[:,2] )
    ax[1].imshow(cv2.cvtColor(reference, cv2.COLOR_BGR2RGB))
    ax[1].scatter(keypoints_ref[:,0], keypoints_ref[:,1], s=keypoints_ref[:,2])
    plt.show()

    shape = (7, 5) # grid size
    ret1, corners1 = cv2.findCirclesGrid(img, shape, flags = cv2.CALIB_CB_SYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING, blobDetector=detector)
    ret2, corners2 = cv2.findCirclesGrid(reference, shape, flags = cv2.CALIB_CB_SYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING, blobDetector=detector)


    print(f"Grid detected in fig1: {ret1}\n Grid detected in fig2: {ret2}" )  

    if ret1 == False or ret2 == False:
        print(f"Failed to detect grid in both images. exiting...")
        exit(0)
    
    # Get homography
    H, _ = cv2.findHomography(corners1, corners2)
    print(f"Homography matrix:{H}")

    # Perspective transform image
    img_warp = cv2.warpPerspective(img, H, (img.shape[1], img.shape[0]))
    fig, ax = plt.subplots(2, figsize=(5,10))
    ax[0].imshow(cv2.cvtColor(img_warp, cv2.COLOR_BGR2RGB))
    ax[1].imshow(cv2.cvtColor(reference, cv2.COLOR_BGR2RGB))
    plt.show()
