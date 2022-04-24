from PIL import Image
from PIL import ImageChops
import cv2
import numpy
import random

class ImageAnalysis():

    def StartBan(self, problem):
        A = "Problems/" + problem.problemSetName + "/" + problem.name + "/A.png"
        B = "Problems/" + problem.problemSetName + "/" + problem.name + "/B.png"
        C = "Problems/" + problem.problemSetName + "/" + problem.name + "/C.png"

        D = "Problems/" + problem.problemSetName + "/" + problem.name + "/D.png"
        E = "Problems/" + problem.problemSetName + "/" + problem.name + "/E.png"
        F = "Problems/" + problem.problemSetName + "/" + problem.name + "/F.png"

        G = "Problems/" + problem.problemSetName + "/" + problem.name + "/G.png"
        H = "Problems/" + problem.problemSetName + "/" + problem.name + "/H.png"

        imageA = Image.open(A).convert("L")
        imageB = Image.open(B).convert("L")
        imageC = Image.open(C).convert("L")

        imageD = Image.open(D).convert("L")
        imageE = Image.open(E).convert("L")
        imageF = Image.open(F).convert("L")

        imageG = Image.open(G).convert("L")
        imageH = Image.open(H).convert("L")

        return [imageA, imageB, imageC, imageD, imageE, imageF, imageG, imageH]


    def DPR_Analysis2x2(self, A, B, C, problem):
        imageA = Image.open(A).convert("L")
        imageB = Image.open(B).convert("L")
        imageC = Image.open(C).convert("L")

        dpr_AB = self.dark_pixel_percentage(imageA) - self.dark_pixel_percentage(imageB)

        # if the ratio decreases from A to B to C but by an INSANE amount
        if dpr_AB <= 0.0:
            index = 0
            i = 1
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                dpr_CI = self.dark_pixel_percentage(imageC) - self.dark_pixel_percentage(
                    imageSolution)

                if dpr_AB - 3.8 <= dpr_CI <= dpr_AB + 3.8:
                    index = i

                i += 1

            if index != 0:
                return index

        # if the ratio increases from A to B to C
        if dpr_AB > 0:
            index = 0

            i = 1
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                dpr_CI = self.dark_pixel_percentage(imageC) - self.dark_pixel_percentage(
                    imageSolution)

                if dpr_AB - 3.8 <= dpr_CI <= dpr_AB + 3.8:
                    index = i
                i += 1

            if index != 0:
                return index

        return random.randint(1, 6)


    ######### ADD DPR FOR COLUMN RELATIONSHIPS!!!
    def DPR_Analysis_SameShape(self, A, B, C, problem):
        imageA = Image.open(A).convert("L")
        imageB = Image.open(B).convert("L")
        imageC = Image.open(C).convert("L")

        dpr_AB = self.dark_pixel_percentage(imageA) - self.dark_pixel_percentage(imageB)

        #dpr_AC = self.dark_pixel_percentage(imageA) - self.dark_pixel_percentage(imageC)
        # if the ratio decreases from A to B to C but by an INSANE amount
        if dpr_AB <= 0.0:
            index = 0
            i = 1
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                if self.SameShape(img_path, C) == False:
                    i += 1
                    continue

                imageSolution = Image.open(img_path).convert("L")
                dpr_CI = self.dark_pixel_percentage(imageC) - self.dark_pixel_percentage(
                    imageSolution)

                if dpr_AB - 3.8 <= dpr_CI <= dpr_AB + 3.8:
                    index = i

                i += 1

            if index != 0:
                return index

        # if the ratio increases from A to B to C
        if dpr_AB >= 0:
            index = 0
            i = 1
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                if self.SameShape(img_path, C) == False:
                    i += 1
                    continue
                imageSolution = Image.open(img_path).convert("L")
                dpr_CI = self.dark_pixel_percentage(imageC) - self.dark_pixel_percentage(
                    imageSolution)

                if dpr_AB - 3.8 <= dpr_CI <= dpr_AB + 3.8:
                    index = i
                i += 1

            if index != 0:
                return index

        return random.randint(1, 6)




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

    def Rotation(self, imageA, imageB, threshold):

        #### if rotation value is ambigous append them to this array
        rotationValues = []
        rotationBool = False


        if self.PercentDiff(imageA.rotate(45), imageB) <= threshold:
            rotationValues.append(45)

        if self.PercentDiff(imageA.rotate(90), imageB) <= threshold:
            rotationValues.append(90)

        if self.PercentDiff(imageA.rotate(135), imageB) <= threshold:
            rotationValues.append(135)

        if self.PercentDiff(imageA.rotate(180), imageB) <= threshold:
            rotationValues.append(180)

        if self.PercentDiff(imageA.rotate(-45), imageB) <= threshold:
            rotationValues.append(-45)

        if self.PercentDiff(imageA.rotate(-90), imageB) <= threshold:
            rotationValues.append(-90)

        if self.PercentDiff(imageA.rotate(-135), imageB) <= threshold:
            rotationValues.append(-135)

        if self.PercentDiff(imageA.rotate(-180), imageB) <= threshold:
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



    def CheckOrientation(self, contourA, contourC):

        # returns the angle of the the contour

        if len(contourA) < 5 or len(contourC) < 5:
            return 0

        (x, y), (MA, ma), angle = cv2.fitEllipse(contourA)
        (x, y), (MA, ma), angleC = cv2.fitEllipse(contourC)

        if angle == angleC:
            return 0
        else:
            if angleC < angle:
                return angle - angleC
            else:
                return angleC - angle




    def SameShape(self, imgA_path, imgC_path):

        # reading image
        img1 = cv2.imread(imgA_path)
        img2 = cv2.imread(imgC_path)

        # converting image into grayscale image
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)
        _, threshold2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)

        # using a findContours() function
        contoursA, _ = cv2.findContours(threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursC, _ = cv2.findContours(threshold2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contoursA) <= 1 or len(contoursC) <= 1:
            return False

        # get the shape of the contours
        approxA = cv2.approxPolyDP(contoursA[1], 0.01 * cv2.arcLength(contoursA[1], True), True)
        approxC = cv2.approxPolyDP(contoursC[1], 0.01 * cv2.arcLength(contoursC[1], True), True)

        if len(approxA) != len(approxC):
            return False
        else:
            return True




    def CheckSidesAdded(self, contourG, contourA, contourC, problem):
        # get the shape of the contours

        approxA = cv2.approxPolyDP(contourA, 0.01 * cv2.arcLength(contourA, True), True)
        approxC = cv2.approxPolyDP(contourC, 0.01 * cv2.arcLength(contourC, True), True)
        approxG = cv2.approxPolyDP(contourG, 0.01 * cv2.arcLength(contourA, True), True)


        ################### more sides are being added to the shape in the next image and the next image ISN'T A CIRCLE
        if len(approxA) < len(approxC) and len(approxC) <= 15:

            factorIncrease = len(approxC) - len(approxA)

            if problem.problemType == "2x2":
                i = 1
                while i <= 6:
                    img1 = cv2.imread(problem.figures.get(str(i)).visualFilename)

                    # converting image into grayscale image
                    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

                    # setting threshold of gray image
                    _, threshold1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)

                    # using a findContours() function
                    contoursI, _ = cv2.findContours(threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    ## if the image contains only 1 shape whether it's filled or not
                    if len(contoursI) >= 2:
                        contour = contoursI[1]
                        approxI = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

                        if len(approxG) + factorIncrease == len(approxI):
                            return i
                    i += 1

            elif problem.problemType == "3x3":
                i = 1
                while i <= 8:
                    img1 = cv2.imread(problem.figures.get(str(i)).visualFilename)

                    # converting image into grayscale image
                    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

                    # setting threshold of gray image
                    _, threshold1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)

                    # using a findContours() function
                    contoursI, _ = cv2.findContours(threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    if len(contoursI) >= 2:
                        shape = contoursI[1]
                        approxI = cv2.approxPolyDP(shape, 0.01 * cv2.arcLength(shape, True), True)

                        if len(approxG) + factorIncrease == len(approxI):
                            return i
                    i += 1

        if len(approxA) > len(approxC) and len(approxA) <= 15:

            factorDecrease = len(approxA) - len(approxC)

            if problem.problemType == "2x2":
                i = 1
                while i <= 6:
                    img1 = cv2.imread(problem.figures.get(str(i)).visualFilename)

                    # converting image into grayscale image
                    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

                    # setting threshold of gray image
                    _, threshold1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)

                    # using a findContours() function
                    contoursI, _ = cv2.findContours(threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    ## if the image contains only 1 shape
                    if len(contoursI) >= 2:
                        contour = contoursI[1]
                        approxI = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                        if len(approxG) - factorDecrease == len(approxI):
                            return i
                    i += 1

            elif problem.problemType == "3x3":
                i = 1
                while i <= 8:
                    img1 = cv2.imread(problem.figures.get(str(i)).visualFilename)

                    # converting image into grayscale image
                    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

                    # setting threshold of gray image
                    _, threshold1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)

                    # using a findContours() function
                    contoursI, _ = cv2.findContours(threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    if len(contoursI) >= 2:
                        contour = contoursI[1]
                        approxI = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

                        if len(approxG) - factorDecrease == len(approxI):
                            return i
                    i += 1


        # the shape most likely goes from a circle to something else or vice versa
        return 0





    # it's here just in case I need it. Take from GeeksForGeeks Shape Detection OpenCV page
    #### THIS CAN BE USED FOR CHALLENGE E-05 FOR SHAPES ADDING MORE SIDES
    def ShapeAnalytics(self, problem, imgA, imgC, imgG):

        banned = []
        if problem.problemType == "3x3":
            ImageAr = self.StartBan(problem)
            for i in range(len(ImageAr)):
                for j in range(1, 9):
                    img_path = problem.figures.get(str(j)).visualFilename
                    imageSolution = Image.open(img_path).convert("L")

                    if self.PercentDiff(imageSolution, ImageAr[i]) <= 1.5:
                        banned.append(j)
                        break



        # reading image
        img1 = cv2.imread(imgA)
        img2 = cv2.imread(imgC)
        img3 = cv2.imread(imgG)

        # converting image into grayscale image
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)
        _, threshold2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)
        _, threshold3 = cv2.threshold(gray3, 127, 255, cv2.THRESH_BINARY)

        # using a findContours() function
        contoursA, _ = cv2.findContours(threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursC, _ = cv2.findContours(threshold2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contoursG, _ = cv2.findContours(threshold3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if problem.problemType == "3x3":
            imageCVB = cv2.imread(problem.figures.get('B').visualFilename)
            grayB = cv2.cvtColor(imageCVB, cv2.COLOR_BGR2GRAY)
            _, thresholdB = cv2.threshold(grayB, 127, 255, cv2.THRESH_BINARY)
            contoursB, _ = cv2.findContours(thresholdB, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            imgF = cv2.imread(problem.figures.get('F').visualFilename)
            imgH = cv2.imread(problem.figures.get('H').visualFilename)

            # converting image into grayscale image
            grayF = cv2.cvtColor(imgF, cv2.COLOR_BGR2GRAY)
            grayH = cv2.cvtColor(imgH, cv2.COLOR_BGR2GRAY)

            # setting threshold of gray image
            _, thresholdF = cv2.threshold(grayF, 127, 255, cv2.THRESH_BINARY)
            _, thresholdH = cv2.threshold(grayH, 127, 255, cv2.THRESH_BINARY)

            # using a findContours() function
            contoursF, _ = cv2.findContours(thresholdF, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contoursH, _ = cv2.findContours(thresholdH, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            imageG = cv2.imread(problem.figures.get('G').visualFilename)
            grayG = cv2.cvtColor(imageG, cv2.COLOR_BGR2GRAY)
            _, thresholdG = cv2.threshold(grayG, 127, 255, cv2.THRESH_BINARY)
            contoursG, _ = cv2.findContours(thresholdG, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            shapeG = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursG[1], True), True)




        #### checking VERY SPECIFIC Conditions like E-12 and D-12
        if problem.problemType == "3x3":

            #### E-12
            if len(contoursA) == 4 and len(contoursB) == 2 and len(contoursC) == 3:
                shapeB = cv2.approxPolyDP(contoursB[1], 0.01 * cv2.arcLength(contoursB[1], True), True)
                shapeF = cv2.approxPolyDP(contoursF[1], 0.01 * cv2.arcLength(contoursF[1], True), True)
                shapeH = cv2.approxPolyDP(contoursH[1], 0.01 * cv2.arcLength(contoursH[1], True), True)


                if self.CheckOrientation(contoursA[1], contoursB[1]) == 0 and len(shapeB) == len(shapeH) and len(shapeB) == len(shapeF):


                    i = 1
                    index = 0
                    while i <= 8:

                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) != len(contoursB):
                            i += 1
                            continue


                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)
                        imageI = Image.open(problem.figures.get(str(i)).visualFilename).convert("L")
                        imageB = Image.open(problem.figures.get('B').visualFilename).convert("L")


                        if len(shapeF) == len(I1) and self.PercentDiff(imageI, imageB.transpose(method=Image.FLIP_TOP_BOTTOM)) <= 0.8:
                            index = i

                        i += 1

                    if index != 0:
                        return index




            #### D-12
            elif len(contoursA) == 4 and len(contoursB) == 5 and len(contoursC) >= 6:

                shapeH = cv2.approxPolyDP(contoursH[1], 0.01 * cv2.arcLength(contoursH[1], True), True)

                if len(contoursG) >= 8 and len(contoursH) >= 6:
                    i = 1
                    index = 0

                    while i <= 8:

                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)
                        if len(contoursI) == 4 and len(I1) != len(shapeG) and len(I1) != len(shapeH):
                            index = i

                        i += 1

                    if index != 0:
                        return index



        if len(contoursA) == 6 and len(contoursC) == 4:
            if problem.problemType == "3x3":

                shapeA = cv2.approxPolyDP(contoursA[4], 0.01 * cv2.arcLength(contoursA[4], True), True)
                shapeF = cv2.approxPolyDP(contoursF[3], 0.01 * cv2.arcLength(contoursF[3], True), True)
                shapeH = cv2.approxPolyDP(contoursH[3], 0.01 * cv2.arcLength(contoursH[3], True), True)


                # if the inner shape matches in image F and image H
                if len(shapeA) == len(shapeF) and len(shapeF) == len(shapeH):

                    shapeB = cv2.approxPolyDP(contoursB[3], 0.01 * cv2.arcLength(contoursB[3], True), True)

                    i = 1
                    index = 0
                    while i <= 8:

                        if i in banned:
                            i += 1
                            continue

                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) != len(contoursA):
                            i += 1
                            continue

                        I1 = cv2.approxPolyDP(contoursI[4], 0.01 * cv2.arcLength(contoursI[4], True), True)

                        if len(shapeB) == len(I1):
                            index = i

                        i += 1

                    if index != 0:
                        # print(index)
                        return index



        ######### 2x2 PROBLEMS WILL GO HERE SOMETIMES

        ##################### there's only 1 shape in the image ############################
        ######## the reason why they're length 3 is becaise shape 1 is the frame, shape 2 is teh outline of the object, shape 3 is the shape of the object inside
        if len(contoursA) == 3 and len(contoursC) == 3:

            approxA = cv2.approxPolyDP(contoursA[1], 0.01 * cv2.arcLength(contoursA[1], True), True)
            approxC = cv2.approxPolyDP(contoursC[1], 0.01 * cv2.arcLength(contoursC[1], True), True)

            ### if they have the same shape
            if len(approxA) == len(approxC):
                angle = self.CheckOrientation(contoursA[1], contoursC[1])
                return [True, angle, 0]
            else:
                # they don't have the same shape
                Info = self.CheckSidesAdded(contoursG[1], contoursA[2], contoursC[2], problem)
                angle = self.CheckOrientation(contoursA[2], contoursC[2])

                return [False, angle, Info]


        ######## there's only 1 shape but image C has been filled
        elif len(contoursA) == 3 and len(contoursC) == 2:
            approxA = cv2.approxPolyDP(contoursA[1], 0.01 * cv2.arcLength(contoursA[1], True), True)
            approxC = cv2.approxPolyDP(contoursC[1], 0.01 * cv2.arcLength(contoursC[1], True), True)

            # if the shape in image 1 has been filled
            if len(approxA) == len(approxC):

                angle = self.CheckOrientation(contoursA[1], contoursC[1])

                if angle == 0.0:
                    return self.DPR_Analysis_SameShape(imgA, imgC, imgG, problem)
                else:
                    return [True, angle, 0]
            else:
                Info = self.CheckSidesAdded(contoursG[1], contoursA[1], contoursC[1], problem)
                if Info != 0:
                    return Info
                return self.DPR_Analysis2x2(imgA, imgC, imgG, problem)


        ## if there are 2 SHAPES in the image with 1 inside of the other like in Basic D-04,
        elif len(contoursA) == 4 and len(contoursC) == 4:

            approxA = cv2.approxPolyDP(contoursA[1], 0.01 * cv2.arcLength(contoursA[1], True), True)
            approxC = cv2.approxPolyDP(contoursC[1], 0.01 * cv2.arcLength(contoursC[1], True), True)

            approxA3 = cv2.approxPolyDP(contoursA[3], 0.01 * cv2.arcLength(contoursA[3], True), True)
            approxC2 = cv2.approxPolyDP(contoursC[2], 0.01 * cv2.arcLength(contoursC[2], True), True)

            approxAn = cv2.approxPolyDP(contoursA[2], 0.01 * cv2.arcLength(contoursA[2], True), True)
            approxCn = cv2.approxPolyDP(contoursC[2], 0.01 * cv2.arcLength(contoursC[2], True), True)

            ###### THIS MAINLY PERTAINS TO D-05 WHERE contoursC[2] == contoursA[3] shapewise
            #########

            if len(approxA) != len(approxC) and len(approxC2) != len(approxA3) and len(approxAn) == len(approxCn):
                if problem.problemType == "3x3":
                    i = 1
                    index = 0
                    while i <= 8:

                        if i in banned:
                            i += 1
                            continue

                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) != len(contoursA):
                            i += 1
                            continue

                        I3 = cv2.approxPolyDP(contoursI[3], 0.01 * cv2.arcLength(contoursI[2], True), True)
                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)

                        if len(approxA) == len(I1) and len(approxA3) == len(I3):
                            index = i

                        i += 1

                    if index != 0:
                        # print(index)
                        return index



            if len(approxA3) == len(approxC2):

                ########## D-05 GOES HERE
                if problem.problemType == "3x3":
                    increase = False

                    if cv2.contourArea(contoursA[1]) > cv2.contourArea(contoursA[1]) and len(approxA) == 4:
                        increase = True

                    G3 = cv2.approxPolyDP(contoursG[3], 0.01 * cv2.arcLength(contoursG[3], True), True)
                    i = 1
                    index = 0
                    while i <= 8:

                        if i in banned:
                            i += 1
                            continue

                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) != len(contoursG):
                            i += 1
                            continue

                        I2 = cv2.approxPolyDP(contoursI[2], 0.01 * cv2.arcLength(contoursI[2], True), True)
                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)


                        ###### if the the second shape in I matches the last shape in image G
                        if increase == True and cv2.contourArea(contoursI[1]) > cv2.contourArea(contoursG[1]) and len(I1) == 4:
                            index = i


                        elif len(G3) == len(I2):
                            index = i

                        i += 1

                    if index != 0:
                        #print(index)
                        return index



            # if shape 1 is different in the next image but shape 2 is the same
            elif len(approxA) != len(approxC) and len(approxA3) == len(approxC2):
                if problem.problemType == "3x3":
                    G1 = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursG[1], True), True)
                    G2 = cv2.approxPolyDP(contoursG[3], 0.01 * cv2.arcLength(contoursG[3], True), True)
                    i = 1
                    index = 0
                    while i <= 8:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) != len(contoursG):
                            i +=1
                            continue

                        I1= cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)
                        I2 = cv2.approxPolyDP(contoursI[3], 0.01 * cv2.arcLength(contoursI[3], True), True)

                        if len(G1) != len(I1) and len(G2) == len(I2):
                            index = i

                        i += 1

                    if index != 0:
                        return index


                if problem.problemType == "2x2":
                    G1 = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursG[1], True), True)
                    G2 = cv2.approxPolyDP(contoursG[3], 0.01 * cv2.arcLength(contoursG[3], True), True)
                    i = 1
                    index = 0
                    while i <= 6:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) != len(contoursG):
                            i +=1
                            continue

                        I1= cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)
                        I2 = cv2.approxPolyDP(contoursI[3], 0.01 * cv2.arcLength(contoursI[3], True), True)

                        if len(G1) != len(I1) and len(G2) == len(I2):
                            index = i


                        i += 1

                    if index != 0:
                        return index


            ####### The shapes are staying the same but they're either rotating or scaling
            if len(approxA) == len(approxC) and len(approxA3) == len(approxC2):
                if problem.problemType == "3x3":
                    G1 = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursG[1], True), True)
                    G2 = cv2.approxPolyDP(contoursG[3], 0.01 * cv2.arcLength(contoursG[3], True), True)
                    i = 1
                    index = 0
                    while i <= 8:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) != len(contoursG):
                            i += 1
                            continue

                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)
                        I2 = cv2.approxPolyDP(contoursI[3], 0.01 * cv2.arcLength(contoursI[3], True), True)

                        if len(G1) == len(I1) and len(G2) == len(I2) and cv2.contourArea(contoursI[1]) > cv2.contourArea(contoursG[1]):
                            index = i

                        i += 1

                    if index != 0:
                        return index

                if problem.problemType == "2x2":
                    G1 = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursG[1], True), True)
                    G2 = cv2.approxPolyDP(contoursG[3], 0.01 * cv2.arcLength(contoursG[3], True), True)
                    i = 1
                    index = 0
                    while i <= 6:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) != len(contoursG):
                            i += 1
                            continue

                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)
                        I2 = cv2.approxPolyDP(contoursI[3], 0.01 * cv2.arcLength(contoursI[3], True), True)

                        if len(G1) == len(I1) and len(G2) == len(I2) and cv2.contourArea(contoursI[1]) > cv2.contourArea(contoursG[1]):
                            index = i

                        i += 1

                    if index != 0:
                        return index



        # A shape is removed when going from image 1 to image 2
        elif len(contoursA) == 4 and len(contoursC) == 3: # and len(contoursG) == 4:


            approxA = cv2.approxPolyDP(contoursA[1], 0.01 * cv2.arcLength(contoursA[1], True), True)
            approxC = cv2.approxPolyDP(contoursC[1], 0.01 * cv2.arcLength(contoursC[1], True), True)

            # even though a shape has been removed, the first shape (outer shape) is the same in images 1 and 2
            if len(approxA) == len(approxC):
                if problem.problemType == "3x3":
                    G1 = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursG[1], True), True)
                    i = 1
                    index = 0
                    while i <= 8:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                            # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                            # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                            # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)

                        if len(G1) == len(I1) and len(contoursI) < len(contoursG):
                            index = i

                        i += 1

                    if index != 0:
                        return index

                if problem.problemType == "2x2":
                    G1 = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursA[1], True), True)
                    i = 1
                    index = 0
                    while i <= 6:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)

                        if len(G1) == len(I1) and len(contoursI) < len(contoursG):
                            index = i

                        i += 1

                    if index != 0:
                        return index

            if len(approxA) > len(approxC):
                if problem.problemType == "3x3":
                    G1 = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursG[1], True), True)
                    i = 1
                    index = 0
                    while i <= 8:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)

                        if len(G1) > len(I1) and len(contoursI) < len(contoursG):
                            index = i

                        i += 1

                    if index != 0:
                        return index

                if problem.problemType == "2x2":
                    G1 = cv2.approxPolyDP(contoursG[1], 0.01 * cv2.arcLength(contoursA[1], True), True)
                    i = 1
                    index = 0
                    while i <= 6:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        I1 = cv2.approxPolyDP(contoursI[1], 0.01 * cv2.arcLength(contoursI[1], True), True)

                        if len(G1) > len(I1) and len(contoursI) < len(contoursG):
                            index = i

                        i += 1

                    if index != 0:
                        return index


        ################## THIS IS FOR BASIC D-08 CHECK CONTOURS FROM A TO E ##############
        elif len(contoursA) == 2:

            if problem.problemType == "3x3":

                imgE = cv2.imread(problem.figures.get('E').visualFilename)
                        # converting image into grayscale image
                grayE = cv2.cvtColor(imgE, cv2.COLOR_BGR2GRAY)
                # setting threshold of gray image
                _, thresholdE = cv2.threshold(grayE, 127, 255, cv2.THRESH_BINARY)
                # using a findContours() function
                contoursE, _ = cv2.findContours(thresholdE, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(contoursA) >= len(contoursE):
                    i = 1
                    index = 0
                    while i <= 8:
                        img_path = problem.figures.get(str(i)).visualFilename

                        imgI = cv2.imread(img_path)
                        # converting image into grayscale image
                        grayI = cv2.cvtColor(imgI, cv2.COLOR_BGR2GRAY)

                        # setting threshold of gray image
                        _, thresholdI = cv2.threshold(grayI, 127, 255, cv2.THRESH_BINARY)

                        # using a findContours() function
                        contoursI, _ = cv2.findContours(thresholdI, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if len(contoursI) == len(contoursA):
                            if self.SameShape(img_path, problem.figures.get('A').visualFilename) == True and self.SameShape(img_path, problem.figures.get('E').visualFilename) == False:
                                index = i
                        i += 1

                    if index != 0:
                        return index


        return [False, 0, 0]




    # the arguments are arrays
    def AND_images(self, image_a, image_b):
        return ImageChops.add(image_a, image_b)

    def OR_images(self, image_a, image_b):
        return ImageChops.multiply(image_a, image_b)

    def XOR_images(self, image_a, image_b):
        image_diff = ImageChops.difference(image_a, image_b)
        return ImageChops.invert(image_diff)