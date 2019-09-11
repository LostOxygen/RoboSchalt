import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 35
gauss_faktor = 0
gauss_matrix = (7,7)
min_threshold = 0
max_threshold = 50

def main():
    img1 = cv2.imread('pic1.png', 0) # queryImage
    img2 = cv2.imread('pic2.png', 0) # trainImage

    #img1 = borders(img1)
    #img2 = borders(img2)

    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            print(m)
            good.append(m)

    print(len(good))

    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        print(pts)
        dst = cv2.perspectiveTransform(pts,M)

        img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        #print ("Not enough matches are found " + str(len(good), str(MIN_MATCH_COUNT)))
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = None,
                       matchesMask = matchesMask,
                       flags = 2)
    print(matchesMask)
    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    cv2.imwrite("../bilder/compare_homography", img3) #speichert ein Bild
    plt.imshow(img3, 'gray'),plt.show()

def borders(gray):
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gauss = cv2.GaussianBlur(gray, gauss_matrix, gauss_faktor)
    canny = cv2.Canny(gauss, min_threshold, max_threshold)
    #_, inverted = cv2.threshold(canny, 30, 255, cv2.THRESH_BINARY_INV)
    return canny

if __name__ == "__main__":
    main()
