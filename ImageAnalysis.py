from PIL import Image
from PIL import ImageChops
import cv2
import numpy



class ImageAnalysis():

    # return the percent difference between the two images
    def PercentDiff(self, ModiImage, imageB):
        diff = ImageChops.difference(ModiImage, imageB)
        diffAr = numpy.array(diff)
        result = diffAr.astype(numpy.uint8)
        percentage = (numpy.count_nonzero(result) * 100) / result.size
        return percentage

    def ReflectionVertical(self, imageA, imageB):
        # Flip the original image vertically
        # calculate difference between the images
        vertical_img = imageA.transpose(method=Image.FLIP_TOP_BOTTOM)
        percentage = self.PercentDiff(vertical_img, imageB)

        # if there's only a 5% difference
        if percentage <= 5:
            return True
        return False

    def ReflectHorizontal(self, imageA, imageB):

        # flip image horizontally
        # calculate difference between the images
        hori_img = imageA.transpose(method=Image.FLIP_LEFT_RIGHT)
        percentage = self.PercentDiff(hori_img, imageB)

        # if there's only a 5% difference
        if percentage <= 5:
            return True
        return False

    def Rotation(self, imageA, imageB):

        #### if rotation value is ambigous append them to this array
        rotationValues = []
        rotationBool = False


        if self.PercentDiff(imageA.rotate(45), imageB) <= 5:
            rotationValues.append(45)

        if self.PercentDiff(imageA.rotate(90), imageB) <= 5:
            rotationValues.append(90)

        if self.PercentDiff(imageA.rotate(135), imageB) <= 5:
            rotationValues.append(135)

        if self.PercentDiff(imageA.rotate(180), imageB) <= 5:
            rotationValues.append(180)

        if self.PercentDiff(imageA.rotate(-45), imageB) <= 5:
            rotationValues.append(-45)

        if self.PercentDiff(imageA.rotate(-90), imageB) <= 5:
            rotationValues.append(-90)

        if self.PercentDiff(imageA.rotate(-135), imageB) <= 5:
            rotationValues.append(-135)

        if self.PercentDiff(imageA.rotate(-180), imageB) <= 5:
            rotationValues.append(-180)

        if len(rotationValues) > 0:
            rotationBool = True

        return rotationBool, rotationValues




    def dark_pixel_percentage(self, image):
        pixels = image.getdata()
        dark = 0
        for pixel in pixels:
            if pixel == 255:
                dark += 1
        n = len(pixels)
        return 100.0 * (dark / float(n))


    def black_pixel_distance(self, image, direction, metric):
        if direction == "right":
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == "top":
            image = image.rotate(90)
        elif direction == "bottom":
            image = image.rotate(-90)
        pixels = image.load()
        distances = []
        for i in range(0, image.size[0]):
            for j in range(0, image.size[1]):
                pixel = pixels[i, j]
                # If a non-white pixel is reached, return it
                if pixel != 255:
                    distances.append(j)
                    break
        if distances != []:
            if metric == "min":
                return min(distances)
            elif metric == "max":
                return max(distances)
            elif metric == "avg":
                return sum(distances) / len(distances)
        else:
            return 0



    def Contours_Analysis(self, PathA, PathC, Problem):

        # turns image_path into array
        imA = cv2.imread(PathA)
        imgrayA = cv2.cvtColor(imA, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgrayA, 127, 255, 0)

        # the first contour is always the Frame of the image itself
        contoursA, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        # turns image_path into array
        imC = cv2.imread(PathC)
        imgrayC = cv2.cvtColor(imC, cv2.COLOR_BGR2GRAY)
        retC, threshC = cv2.threshold(imgrayC, 127, 255, 0)

        # the first contour is always the Frame of the image itself
        contoursC, hierarchyC = cv2.findContours(threshC, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #area = cv2.contourArea(contoursA[1])

        # print(len(contoursA))
        # cv2.drawContours(imA, contoursA, -1, (0, 255, 0), 3)
        # cv.imshow('Image', imA)
        # cv.waitKey(0)
        # cv.destroyAllWindows()


        # if there are shapes just being moved around
        # compare shapes using area
        if len(contoursC) == len(contoursA):
            i = 1
            while i <= 8:
                img_path = Problem.figures.get(str(i)).visualFilename
                imageSolution = cv2.imread(img_path)
                imgrayS = cv2.cvtColor(imageSolution, cv2.COLOR_BGR2GRAY)
                retS, threshS = cv2.threshold(imgrayS, 127, 255, 0)

                # the first contour is always the Frame of the image itself
                contoursS, hierarchyS = cv2.findContours(threshS, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(contoursS) == len(contoursC):
                    match = True
                    # check if the shapes are the same
                    for j in range(len(contoursC)):
                        if j == 0:
                            continue
                        if cv2.contourArea(contoursC[j]) != cv2.contourArea(contoursS[j]):
                            match = False
                            break

                    if match:
                        return i

                i += 1

        elif len(contoursC) > len(contoursA):
            i = 1
            while i <= 8:
                img_path = Problem.figures.get(str(i)).visualFilename
                imageSolution = cv2.imread(img_path)
                imgrayS = cv2.cvtColor(imageSolution, cv2.COLOR_BGR2GRAY)
                retS, threshS = cv2.threshold(imgrayS, 127, 255, 0)

                # the first contour is always the Frame of the image itself
                contoursS, hierarchyS = cv2.findContours(threshS, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(contoursS) > len(contoursC):
                    match = True
                    # check if the shapes are the same
                    for j in range(len(contoursC)):
                        if j == 0:
                            continue
                        if cv2.contourArea(contoursC[j]) != cv2.contourArea(contoursS[j]):
                            match = False
                            break

                    if match:
                        return i

                i += 1

        elif len(contoursC) < len(contoursA):
            i = 1
            while i <= 8:
                img_path = Problem.figures.get(str(i)).visualFilename
                imageSolution = cv2.imread(img_path)
                imgrayS = cv2.cvtColor(imageSolution, cv2.COLOR_BGR2GRAY)
                retS, threshS = cv2.threshold(imgrayS, 127, 255, 0)

                # the first contour is always the Frame of the image itself
                contoursS, hierarchyS = cv2.findContours(threshS, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(contoursS) < len(contoursC) and len(contoursS) != 0:
                    match = True
                    # check if the shapes are the same
                    for j in range(len(contoursS)):
                        if j == 0:
                            continue
                        if cv2.contourArea(contoursC[j]) != cv2.contourArea(contoursS[j]):
                            match = False
                            break

                    if match:
                        return i

                i += 1

        return 0




    # it's here just in case I need it. Take from GeeksForGeeks Shape Detection OpenCV page
    def Shape_Detection(self, contours, imgA):
        # reading image
        img = cv2.imread(imgA)

        # converting image into grayscale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # using a findContours() function
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        i = 0

        # list for storing names of shapes
        for contour in contours:

            # here we are ignoring first counter because
            # findcontour function detects whole image as shape
            if i == 0:
                i = 1
                continue

            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

            # using drawContours() function
            # cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

            # finding center point of shape
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])

            # putting shape name at center of each shape
            if len(approx) == 3:
                cv2.putText(img, 'Triangle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 4:
                cv2.putText(img, 'Quadrilateral', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 5:
                cv2.putText(img, 'Pentagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            elif len(approx) == 6:
                cv2.putText(img, 'Hexagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            else:
                cv2.putText(img, 'circle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)