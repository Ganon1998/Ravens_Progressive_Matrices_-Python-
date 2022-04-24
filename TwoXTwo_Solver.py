from PIL import Image, ImageChops
from cv2 import cv2
import numpy
from ImageAnalysis import ImageAnalysis



class TwoXTwo_Solver(object):


    def solver(self, problem):

        A = "Problems/" + problem.problemSetName + "/" + problem.name + "/A.png"
        B = "Problems/" + problem.problemSetName + "/" + problem.name + "/B.png"
        C = "Problems/" + problem.problemSetName + "/" + problem.name + "/C.png"

        imageA = Image.open(A).convert("L")
        imageB = Image.open(B).convert("L")
        imageC = Image.open(C).convert("L")


        image_analyzer = ImageAnalysis()



        ###### if the images are identical from A to B
        if image_analyzer.PercentDiff(imageA, imageB) <= 5:
            if image_analyzer.PercentDiff(imageB, imageC) <= 5:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("L")

                    if image_analyzer.PercentDiff(imageB, imageSolution) <= 5:
                        return i
                    i += 1


        ##### check if A and C are identical
        if image_analyzer.PercentDiff(imageA, imageC) <= 5:
            i = 1
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(imageSolution, imageB) <= 5:
                    return i
                i += 1

        # if problem.name == "Challenge Problem B-10":
        # print("here")

        '''if problem.name == "Basic Problem B-06":
            print("here")'''

        ##### Check for some basic transformations from A to B
        VerticalReflect = image_analyzer.ReflectionVertical(imageA, imageB)
        HorizontalReflect = image_analyzer.ReflectHorizontal(imageA, imageB)

        img1 = cv2.imread(A)
        # converting image into grayscale image
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        # setting threshold of gray image
        _, thresholdImg = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)
        # using a findContours() function
        contoursA, _ = cv2.findContours(thresholdImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        threshold = 5
        if len(contoursA) >= 6:
            threshold = 9


        Rotation, RotationValues = image_analyzer.Rotation(imageA, imageB, threshold)

        ### if ANY of the basic transformations ocurred then we just go through each
        ### if condition. if NONE of the if conditions worked then we call  Transformation_Analysis()
        if VerticalReflect:
            i = 1
            index = 0
            baseline = 1000
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(imageSolution, imageC.transpose(method=Image.FLIP_TOP_BOTTOM))
                if test <= threshold and test <= baseline:
                    baseline = test
                    index = i
                i += 1

            if index != 0:
                return index

        if HorizontalReflect:
            i = 1
            index = 0
            baseline = 1000
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(imageSolution, imageC.transpose(method=Image.FLIP_LEFT_RIGHT))
                if test <= threshold and test <= baseline:
                    baseline = test
                    index = i
                i += 1

            if index != 0:
                return index

        if Rotation:
            index = 0
            baseline = 1000
            while len(RotationValues) != 0:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("L")
                    test = image_analyzer.PercentDiff(imageSolution, imageC.rotate(RotationValues[-1]))
                    # if the rotated answer is very similar to the projected rotated imageC
                    if test <= threshold and test <= baseline:
                        baseline = test
                        index = i

                    i += 1

                RotationValues.pop()

            if index != 0:
                return index

        ############ Check for some basic transformations from A to C
        ############################################################

        VerticalReflect = image_analyzer.ReflectionVertical(imageA, imageC)
        HorizontalReflect = image_analyzer.ReflectHorizontal(imageA, imageC)
        Rotation, RotationValues = image_analyzer.Rotation(imageA, imageC, threshold)

        ### if ANY of the basic transformations ocurred then we just go through each
        ### if condition. if NONE of the if conditions worked then we call  Transformation_Analysis()
        if VerticalReflect:
            i = 1
            index = 0
            baseline = 1000
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(imageSolution, imageB.transpose(method=Image.FLIP_TOP_BOTTOM))
                if test <= threshold and test <= baseline:
                    baseline = test
                    index = i
                i += 1

            if index != 0:
                return index

        if HorizontalReflect:
            i = 1
            index = 0
            baseline = 1000
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(imageSolution, imageB.transpose(method=Image.FLIP_LEFT_RIGHT))
                if test <= threshold and test < baseline:
                    index = i
                i += 1

            if index != 0:
                return index

        if Rotation:
            index = 0
            baseline = 1000
            while len(RotationValues) != 0:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("L")
                    test = image_analyzer.PercentDiff(imageSolution, imageB.rotate(RotationValues[-1]))
                    if test <= threshold and test <= baseline:
                        baseline = test
                        index = i
                    i += 1

                RotationValues.pop()

            if index != 0:
                return index



        Info = image_analyzer.ShapeAnalytics(problem, A, B, C)

        # if the function found the answer
        if not isinstance(Info, list):
            return Info

        # if the function only has 1 value that
        if Info[2] > 0 and Info[1] == 0.0 and Info[0] == False:
            return Info[2]

        if Info[1] != 0.0:
            # rotate the image around and stuff
            i = 1
            imageC = Image.open(C).convert("L")
            while i <= 6:
                img_path = problem.figures.get(str(i)).visualFilename

                if image_analyzer.SameShape(img_path, C) == False:
                    i += 1
                    continue

                imageSolution = Image.open(img_path).convert("L")

                # print(problem.name)
                # print(Info)
                if image_analyzer.PercentDiff(imageSolution, imageC.rotate(Info[1])) <= 8:
                    return i
                i += 1

        if Info[0] == True and Info[1] == 0 and Info[2] == 0:
            # run DPR again but make sure to use SameShape()
            sameShape_DPR = image_analyzer.DPR_Analysis_SameShape(A, B, C, problem)
            # if sameShape_DPR != 0:
            return sameShape_DPR

        # if all else fails
        return image_analyzer.DPR_Analysis2x2(A, B, C, problem)