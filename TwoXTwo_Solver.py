from PIL import Image, ImageChops
from cv2 import cv2
import numpy
from ImageAnalysis import ImageAnalysis



class TwoXTwo_Solver(object):

    # literally just do the DPR for this section
    ####################### just added it here don't know if it works or not
    def InDepth_Transformation_Analysis(self, problem, image_analyzer, A, B, C):

        #### try calculating dark pixel ratio horizontally
        dpr_AB = image_analyzer.dark_pixel_percentage(A) - image_analyzer.dark_pixel_percentage(B)


        # if the ratio decreases from A to B to C but by an INSANE amount
        if dpr_AB <= 0.0:
            index = 0
            i = 1
            while i <= 8:
                img_path = problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_CI = image_analyzer.dark_pixel_percentage(C) - image_analyzer.dark_pixel_percentage(imageSolution)

                if dpr_CI <= dpr_AB and dpr_CI < 0.0:
                    index = i

                i += 1

            if index != 0:
                return index


        # if the ratio increases from A to B to C
        if dpr_AB > 0:
            index = 0
            max = 10000.0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_CI = image_analyzer.dark_pixel_percentage(C) - image_analyzer.dark_pixel_percentage(imageSolution)

                if dpr_CI >= dpr_AB and dpr_CI < max:
                    max = dpr_CI
                    index = i
                i += 1

            if index != 0:
                return index

        else:

            # contourResult = image_analyzer.Contours_Analysis(self.A, self.C, self.Problem)
            # if contourResult != 0:
            # return contourResult

            ### or do diagonal stuff

            return -1




    def solver(self, problem):

        A = "Problems/" + problem.problemSetName + "/" + problem.name + "/A.png"
        B = "Problems/" + problem.problemSetName + "/" + problem.name + "/B.png"
        C = "Problems/" + problem.problemSetName + "/" + problem.name + "/C.png"

        imageA = Image.open(A).convert("RGB")
        imageB = Image.open(B).convert("RGB")
        imageC = Image.open(C).convert("RGB")

        image_analyzer = ImageAnalysis()

        ###### if the images are identical from A to B
        if image_analyzer.PercentDiff(imageA, imageB) <= 5:
            if image_analyzer.PercentDiff(imageB, imageC) <= 5:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if image_analyzer.PercentDiff(imageB, imageSolution) <= 5:
                        return i
                    i += 1

        else:

            ##### check if A and C are identical
            if image_analyzer.PercentDiff(imageA, imageC) <= 5:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if image_analyzer.PercentDiff(imageSolution, imageB) <= 5:
                        return i
                    i += 1

            ##### Check for some basic transformations from A to B
            VerticalReflect = image_analyzer.ReflectionVertical(imageA, imageB)
            HorizontalReflect = image_analyzer.ReflectHorizontal(imageA, imageB)
            Rotation, RotationValues = image_analyzer.Rotation(imageA, imageB)

            ### if ANY of the basic transformations ocurred then we just go through each
            ### if condition. if NONE of the if conditions worked then we call  Transformation_Analysis()
            if VerticalReflect:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if image_analyzer.PercentDiff(imageSolution, imageC.transpose(method=Image.FLIP_TOP_BOTTOM)) <= 5:
                        return i
                    i += 1

            if HorizontalReflect:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if image_analyzer.PercentDiff(imageSolution, imageC.transpose(method=Image.FLIP_LEFT_RIGHT)) <= 8:
                        return i
                    i += 1

            if Rotation:
                while len(RotationValues) != 0:
                    i = 1
                    while i <= 6:
                        img_path = problem.figures.get(str(i)).visualFilename
                        imageSolution = Image.open(img_path).convert("RGB")

                        # if the rotated answer is very similar to the projected rotated imageC
                        if image_analyzer.PercentDiff(imageSolution, imageC.rotate(RotationValues[-1])) <= 8:
                            return i

                        i += 1

                    RotationValues.pop()


            ############ Check for some basic transformations from A to C
            ############################################################
            VerticalReflect = image_analyzer.ReflectionVertical(imageA, imageC)
            HorizontalReflect = image_analyzer.ReflectHorizontal(imageA, imageC)
            Rotation, RotationValues = image_analyzer.Rotation(imageA, imageC)

            ### if ANY of the basic transformations ocurred then we just go through each
            ### if condition. if NONE of the if conditions worked then we call  Transformation_Analysis()
            if VerticalReflect:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if image_analyzer.PercentDiff(imageSolution, imageB.transpose(method=Image.FLIP_TOP_BOTTOM)) <= 8:
                        return i
                    i += 1

            if HorizontalReflect:
                i = 1
                while i <= 6:
                    img_path = problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("RGB")

                    if image_analyzer.PercentDiff(imageSolution, imageB.transpose(method=Image.FLIP_LEFT_RIGHT)) <= 8:
                        return i
                    i += 1

            if Rotation:
                while len(RotationValues) != 0:
                    i = 1
                    while i <= 6:
                        img_path = problem.figures.get(str(i)).visualFilename
                        imageSolution = Image.open(img_path).convert("RGB")

                        if image_analyzer.PercentDiff(imageSolution, imageB.rotate(RotationValues[-1])) <= 8:
                            return i
                        i += 1

                    RotationValues.pop()


            else:
                ###### if none of these work try examinig a more complicated transformation
                ############### one thing that can be done is calculuating thej ratio of dark pixels to white pixels in an image
                return self.InDepth_Transformation_Analysis(problem, image_analyzer, A, B, C)