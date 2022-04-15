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

        self.ImgaeInAr = [self.imageA, self.imageB, self.imageC, self.imageD, self.imageE, self.imageF, self.imageG, self.imageH]




    def Transformation_Analysis(self, image_analyzer):
        from RunImageAnalysis import RunImageAnalysis


        #if self.Problem.name == "Basic Problem D-07":
            #print("HERE")

        TransformationTests = RunImageAnalysis(problem=self.Problem)

        bitwise = TransformationTests.Bitwise_Operations_Check(image_analyzer)
        DPR_Eval = TransformationTests.Basic_DPR(image_analyzer)

        if bitwise != 0:
            return bitwise
        elif DPR_Eval != 0:
            return DPR_Eval
        ### IF BASIC DPR ANALYSIS DOESN'T WORK, LOOK AT NON LINEAR RELATIONSHIPS
        else:
            return TransformationTests.Non_Linear_DPR(image_analyzer)




    def solver(self):

        image_analyzer = ImageAnalysis()

        #if self.Problem.name == "Challenge Problem D-03":
            #print("HERE")


        ## if the images are identical diagonally
        if image_analyzer.PercentDiff(self.imageA, self.imageE) <= 3.8:
            i = 1
            index = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(self.imageE, imageSolution) <= 3.0:
                    index = i
                i += 1
            return index

        # if the images are identical in general
        if image_analyzer.PercentDiff(self.imageA, self.imageB) <= 3.8:
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(self.imageH, imageSolution) <= 3.8:
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

        # perform an indepth analysis
        return self.Transformation_Analysis(image_analyzer)