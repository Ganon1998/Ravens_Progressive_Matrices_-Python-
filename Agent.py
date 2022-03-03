from PIL import Image, ImageChops
from cv2 import cv2
import numpy
import time



class Agent:
    def __init__(self):
        self.Time = 0.0
        self.ProblemName = ""

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

        #plt.imshow(imageA.rotate(-90))
        #plt.show()

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


    def Scaled(self, imageA, imageB):
        return 0


    def MakeSemanticNetwork(self, reflect, rotate):
        pass


    def ThreexThreeSolver(self, problem):

        ##### find openCV funciton that can calculate dark pixel ratio

        A = "Problems/" + problem.problemSetName + "/" + problem.name + "/A.png"
        B = "Problems/" + problem.problemSetName + "/" + problem.name + "/B.png"
        C = "Problems/" + problem.problemSetName + "/" + problem.name + "/C.png"

        D = "Problems/" + problem.problemSetName + "/" + problem.name + "/D.png"
        E = "Problems/" + problem.problemSetName + "/" + problem.name + "/E.png"
        F = "Problems/" + problem.problemSetName + "/" + problem.name + "/F.png"

        G = "Problems/" + problem.problemSetName + "/" + problem.name + "/G.png"
        H = "Problems/" + problem.problemSetName + "/" + problem.name + "/H.png"



        return -1


    def TwoxTwoSolver(self, problem):
        A = "Problems/" + problem.problemSetName + "/" + problem.name + "/A.png"
        B = "Problems/" + problem.problemSetName + "/" + problem.name + "/B.png"
        C = "Problems/" + problem.problemSetName + "/" + problem.name + "/C.png"

        imageA = Image.open(A).convert("RGB")
        imageB = Image.open(B).convert("RGB")
        imageC = Image.open(C).convert("RGB")

        ###### if the images are identical from A to B
        if self.PercentDiff(imageA, imageB) <= 5:
            if self.PercentDiff(imageB, imageC) <= 5:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if self.PercentDiff(imageB, imageSolution) <= 5:
                        return i
                    i += 1

        else:

            ##### check if A and C are identical
            if self.PercentDiff(imageA, imageC) <= 5:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if self.PercentDiff(imageSolution, imageB) <= 5:
                        return i
                    i += 1

            ##### Check for some basic transformations from A to B
            VerticalReflect = self.ReflectionVertical(imageA, imageB)
            HorizontalReflect = self.ReflectHorizontal(imageA, imageB)
            Rotation, RotationValues = self.Rotation(imageA, imageB)

            ### if ANY of the basic transformations ocurred then we just go through each
            ### if condition. if NONE of the if conditions worked then we call  Transformation_Analysis()
            if VerticalReflect:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if self.PercentDiff(imageSolution, imageC.transpose(method=Image.FLIP_TOP_BOTTOM)) <= 5:
                        return i
                    i += 1

            if HorizontalReflect:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if self.PercentDiff(imageSolution, imageC.transpose(method=Image.FLIP_LEFT_RIGHT)) <= 8:
                        return i
                    i += 1

            if Rotation:
                while len(RotationValues) != 0:
                    i = 1
                    while i <= 6:
                        img_path = problem.figures.get(str(i)).visualFilename
                        imageSolution = Image.open(img_path).convert("RGB")

                        # if the rotated answer is very similar to the projected rotated imageC
                        if self.PercentDiff(imageSolution, imageC.rotate(RotationValues[-1])) <= 8:
                            return i

                        i += 1

                    RotationValues.pop()

            ############ Check for some basic transformations from A to C
            ############################################################
            VerticalReflect = self.ReflectionVertical(imageA, imageC)
            HorizontalReflect = self.ReflectHorizontal(imageA, imageC)
            Rotation, RotationValues = self.Rotation(imageA, imageC)

            ### if ANY of the basic transformations ocurred then we just go through each
            ### if condition. if NONE of the if conditions worked then we call  Transformation_Analysis()
            if VerticalReflect:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if self.PercentDiff(imageSolution, imageB.transpose(method=Image.FLIP_TOP_BOTTOM)) <= 8:
                        return i
                    i += 1

            if HorizontalReflect:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if self.PercentDiff(imageSolution, imageB.transpose(method=Image.FLIP_LEFT_RIGHT)) <= 8:
                        return i
                    i += 1

            if Rotation:
                while len(RotationValues) != 0:
                    i = 1
                    while i <= 6:
                        img_path = problem.figures.get(str(i)).visualFilename
                        imageSolution = Image.open(img_path).convert("RGB")

                        if self.PercentDiff(imageSolution, imageB.rotate(RotationValues[-1])) <= 8:
                            return i
                        i += 1

                    RotationValues.pop()

            else:
                ###### if none of these work try examinig a more complicated transformation
                ############### one thing that can be done is calculuating thej ratio of dark pixels to white pixels in an image
                return self.Transformation_Analysis(problem)


    def CheckBasics(self, problem):

        if problem.problemType == "2x2":
            return self.TwoxTwoSolver(problem)

        else:
            return self.ThreexThreeSolver(problem)



    def Transformation_Analysis(self, problem):

        return -1

    def Solve(self, problem):
        #startTime = time.perf_counter()
        answer = -1

        answer = self.CheckBasics(problem)

        if answer == 0:
            answer = self.Transformation_Analysis(problem)

        endTime = time.perf_counter()
        #self.Time = endTime - startTime
        #self.ProblemName = problem.name
        return answer
