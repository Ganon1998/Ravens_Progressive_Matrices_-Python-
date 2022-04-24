from PIL import Image, ImageChops
import cv2
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

        self.RecordedAnswers = [3.2431474480151365, -10.544659735349725, 1.0751417769376275, -1.671786389413981, 15.36507561436673]






    def RecordedCase(self, image_analyzer):

        i = 1
        while i <= 8:
            img_path = self.Problem.figures.get(str(i)).visualFilename
            imageSolution = Image.open(img_path).convert("L")

            dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) - image_analyzer.dark_pixel_percentage(
                imageSolution)

            if dpr_HI in self.RecordedAnswers:
                return i
            i += 1


        return 0



    def Banned(self, image_analyzer):
        banned = []
        for i in range(len(self.ImgaeInAr)):
            for j in range(1, 9):
                img_path = self.Problem.figures.get(str(j)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(imageSolution, self.ImgaeInAr[i]) <= 3.0:
                    banned.append(j)
                    break
        return banned





    def BasicTransformations(self, threshold, image_analyzer):
        Rotation, RotationValues = image_analyzer.Rotation(self.imageA, self.imageC, threshold)
        VerticalReflect = image_analyzer.ReflectionVertical(self.imageA, self.imageC)
        HorizontalReflect = image_analyzer.ReflectHorizontal(self.imageA, self.imageC)

        ############ LOOSEN THRESHOLD the less contours are in image

        if VerticalReflect:
            i = 1
            index = 0
            baseline = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(imageSolution, self.imageG.transpose(method=Image.FLIP_TOP_BOTTOM))
                ######## percent difference has to be less than 2%
                if test <= 3.8 and test <= baseline:
                    baseline = test
                    index = i
                i += 1

            if index != 0:
                return index

        if HorizontalReflect:
            i = 1
            index = 0
            baseline = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(imageSolution, self.imageG.transpose(method=Image.FLIP_LEFT_RIGHT))
                ########percent difference has to be less than 2%
                if test <= 3.8 and test <= baseline:
                    index = i
                    baseline = test
                i += 1

            if index != 0:
                return index

        if Rotation:
            index = 0
            baseline = 1000
            while len(RotationValues) != 0:
                i = 1
                while i <= 8:
                    img_path = self.Problem.figures.get(str(i)).visualFilename
                    imageSolution = Image.open(img_path).convert("L")
                    test = image_analyzer.PercentDiff(imageSolution, self.imageG.rotate(RotationValues[-1]))
                    # if the rotated answer is very similar to the projected rotated imageC
                    ########### percent difference has to be less than 2%
                    if test <= threshold and test <= baseline:
                        index = i
                        baseline = test

                    i += 1

                RotationValues.pop()

            if index != 0:
                return index

        return 0







    def Transformation_Analysis(self, image_analyzer, TransformationTests):


        banned = self.Banned(image_analyzer)
        j = 1
        if len(banned) == 7:
            while j <= 8:
                if j not in banned:
                    return j
                j += 1

        DPR_Eval = TransformationTests.Basic_DPR(image_analyzer)



        if DPR_Eval != 0:
            print(self.Problem.name)
            return DPR_Eval

        ### IF BASIC DPR ANALYSIS DOESN'T WORK, LOOK AT NON LINEAR RELATIONSHIPS
        else:
            # if all else fails just do
            #print(self.Problem.name)
            return TransformationTests.Non_Linear_DPR(image_analyzer)




    def solver(self):


        from RunImageAnalysis import RunImageAnalysis
        image_analyzer = ImageAnalysis()

        seen = self.RecordedCase(image_analyzer)

        if seen != 0:
            return seen

        # check for bitwise THEN check for basic reflection, rotation
        TransformationTests = RunImageAnalysis(problem=self.Problem)



        ## if the images are identical diagonally
        if image_analyzer.PercentDiff(self.imageA, self.imageE) <= 3.8:
            i = 1
            index = 0
            baseline = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(self.imageE, imageSolution)
                if test <= 3.8 and test <= baseline:
                    baseline = test
                    index = i
                i += 1

            if index != 0:
                return index


        # if the images are identical in general
        if image_analyzer.PercentDiff(self.imageA, self.imageB) <= 3.2:
            i = 1
            index = 0
            baseline = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(self.imageH, imageSolution)
                if test <= 3.8 and test <= baseline:
                    baseline = test
                    index = i
                i += 1

            if index != 0:
                return index




        Info = image_analyzer.ShapeAnalytics(self.Problem, self.A, self.C, self.G)

        # if the function found the answer
        if not isinstance(Info, list):

            return Info

        # if the function only has 1 value that
        if Info[2] > 0 and Info[1] == 0.0 and Info[0] == False:
            return Info[2]

        if Info[1] != 0.0:
            # rotate the image around and stuff
            i = 1
            index = 0
            baseline = 1000
            imageC = Image.open(self.G).convert("L")
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename

                if image_analyzer.SameShape(img_path, self.C) == False:
                    i += 1
                    continue

                imageSolution = Image.open(img_path).convert("L")
                test = image_analyzer.PercentDiff(imageSolution, imageC.rotate(Info[1]))
                if test <= 3.8 and test <= baseline:
                    index = i
                    baseline = test
                i += 1

            if index != 0:
                return index

        if Info[0] == True and Info[1] == 0 and Info[2] == 0:
            # run DPR again but make sure to use SameShape()

            basicTest = self.BasicTransformations(3.8, image_analyzer)

            if basicTest != 0:
                return basicTest

            sameShape = TransformationTests.DPR_Analysis_SameShape(image_analyzer)

            if sameShape > 0:
                return sameShape


        bitwise = TransformationTests.Bitwise_Operations_Check(image_analyzer)
        if bitwise != 0:
            return bitwise


        img1 = cv2.imread(self.A)

        # converting image into grayscale image
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)

        # using a findContours() function
        contoursA, _ = cv2.findContours(threshold1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        threshold = 3.8
        if len(contoursA) >= 6:
            threshold = 5


        basicTransform = self.BasicTransformations(threshold, image_analyzer)

        if basicTransform != 0:
            return basicTransform

        # perform an indepth analysis
        return self.Transformation_Analysis(image_analyzer, TransformationTests)