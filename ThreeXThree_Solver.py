from PIL import Image, ImageChops
import cv2 as cv
from ImageAnalysis import ImageAnalysis
import numpy


class ThreeXThree_Solver(object):

    def __init__(self, problem):
        self.Problem = problem
        self.A = "Problems/" + problem.problemSetName + "/" + problem.name + "/A.png"
        self.B = "Problems/" + problem.problemSetName + "/" + problem.name + "/B.png"
        self.C = "Problems/" + problem.problemSetName + "/" + problem.name + "/C.png"

        self.D = "Problems/" + problem.problemSetName + "/" + problem.name + "/D.png"
        self.E = "Problems/" + problem.problemSetName + "/" + problem.name + "/E.png"
        self.F = "Problems/" + problem.problemSetName + "/" + problem.name + "/F.png"

        self.G = "Problems/" + problem.problemSetName + "/" + problem.name + "/G.png"
        self.H = "Problems/" + problem.problemSetName + "/" + problem.name + "/H.png"

        self.imageA = Image.open(self.A).convert("L")
        self.imageB = Image.open(self.B).convert("L")
        self.imageC = Image.open(self.C).convert("L")

        self.imageD = Image.open(self.D).convert("L")
        self.imageE = Image.open(self.E).convert("L")
        self.imageF = Image.open(self.F).convert("L")

        self.imageG = Image.open(self.G).convert("L")
        self.imageH = Image.open(self.H).convert("L")




    def InDepth_Transformation_Analysis(self, image_analyzer):


        #### try calculating dark pixel ratio horizontally
        dpr_AB = image_analyzer.dark_pixel_percentage(self.imageA) - image_analyzer.dark_pixel_percentage(self.imageB)
        dpr_BC = image_analyzer.dark_pixel_percentage(self.imageB) - image_analyzer.dark_pixel_percentage(self.imageC)
        dpr_GH = image_analyzer.dark_pixel_percentage(self.imageG) - image_analyzer.dark_pixel_percentage(self.imageH)



        # if the ratio decreases from A to B to C but by an INSANE amount
        if dpr_BC <= dpr_AB and dpr_BC < 0.0:
            index = 0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) - image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI < dpr_GH:
                    index = i

                i += 1

            if index != 0:
                return index


        # if the ratio decreases from A to B to C
        if dpr_BC <= dpr_AB:
            index = 0
            min = 0.0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) - image_analyzer.dark_pixel_percentage(imageSolution)


                if dpr_HI < dpr_GH and dpr_HI > min:
                    min = dpr_HI
                    index = i

                i += 1

            if index != 0:
                return index

        # if the ratio increases from A to B to C
        if dpr_BC >= dpr_AB:
            index = 0
            max = 10000.0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) - image_analyzer.dark_pixel_percentage(imageSolution)

                if dpr_HI > dpr_GH and dpr_HI < max:
                    max = dpr_HI
                    index = i
                i += 1

            if index != 0:
                return index

        else:

            # run basic contour analysis first. check if shapes are being added or deleted
            # contourResult = image_analyzer.Contours_Analysis(self.A, self.C, self.Problem)

            # if contourResult != 0:
            # return contourResult

            return -1




    def solver(self):

        image_analyzer = ImageAnalysis()


        #if self.Problem.name == "Challenge Problem C-02":
            #print("HERE")

        ## if the images are identical diagonally
        if image_analyzer.PercentDiff(self.imageA, self.imageE) <= 3:
            i = 1
            while i <= 6:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(self.imageE, imageSolution) <= 3:
                    return i
                i += 1

        # if the images are identical in general
        if image_analyzer.PercentDiff(self.imageA, self.imageB) <= 3:
            i = 1
            while i <= 6:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(self.imageH, imageSolution) <= 3:
                    return i
                i += 1

        # check for reflection and rotation from A to C and if that works apply it to G to #
        VerticalReflect = image_analyzer.ReflectionVertical(self.imageA, self.imageC)
        HorizontalReflect = image_analyzer.ReflectHorizontal(self.imageA, self.imageC)
        Rotation, RotationValues = image_analyzer.Rotation(self.imageA, self.imageC)

        if VerticalReflect:
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                # percent difference has to be less than 2%
                if image_analyzer.PercentDiff(imageSolution, self.imageG.transpose(method=Image.FLIP_TOP_BOTTOM)) <= 2:
                    return i
                i += 1

        if HorizontalReflect:
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                # percent difference has to be less than 2%
                if image_analyzer.PercentDiff(imageSolution, self.imageG.transpose(method=Image.FLIP_LEFT_RIGHT)) <= 2:
                    return i
                i += 1

        if Rotation:
            while len(RotationValues) != 0:
                i = 1
                while i <= 8:
                    img_path = self.Problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("L")

                    # if the rotated answer is very similar to the projected rotated imageC
                    # percent difference has to be less than 2%
                    if image_analyzer.PercentDiff(imageSolution, self.imageG.rotate(RotationValues[-1])) <= 2:
                        return i

                    i += 1

                RotationValues.pop()


        else:
            '''
            ############
            ############ if none of the basic transformations worked, try DPR then Contours
            ############
            '''
            # perform an indepth analysis
            return self.InDepth_Transformation_Analysis(image_analyzer)