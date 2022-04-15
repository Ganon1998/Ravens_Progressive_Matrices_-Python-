from PIL import Image, ImageChops
from ThreeXThree_Solver import ThreeXThree_Solver


class RunImageAnalysis(object):

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

        self.ImgaeInAr = [self.imageA, self.imageB, self.imageC, self.imageD, self.imageE, self.imageF, self.imageG,
                          self.imageH]


    def Verify_with_IPR(self):
        pass



    def Banned(self, image_analyzer):
        banned = []
        for i in range(len(self.ImgaeInAr)):
            for j in range(1, 9):
                img_path = self.Problem.figures.get(str(j)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(imageSolution, self.ImgaeInAr[i]) <= 5.0:
                    banned.append(j)
                    break
        return banned





    def Basic_DPR(self, image_analyzer):
        #### try calculating dark pixel ratio horizontally

        dpr_AB = image_analyzer.dark_pixel_percentage(self.imageA) / image_analyzer.dark_pixel_percentage(self.imageB)
        dpr_BC = image_analyzer.dark_pixel_percentage(self.imageB) / image_analyzer.dark_pixel_percentage(self.imageC)
        dpr_GH = image_analyzer.dark_pixel_percentage(self.imageG) / image_analyzer.dark_pixel_percentage(self.imageH)


        # if the ratio decreases from A to B to C but by an INSANE amount
        if dpr_BC <= dpr_AB and dpr_BC < 0.0:
            index = 0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) / image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI < dpr_GH:
                    index = i

                i += 1

            ##### verify the solution found BY TRYING NONLINEAR DPR FIRST!!!!!!!!!!!!
            ################################
            if index != 0:
                '''verified_index = self.Non_Linear_DPR(image_analyzer)

                if verified_index != 0 and index == verified_index:
                    return verified_index'''

                img_path = self.Problem.figures.get(str(index)).visualFilename
                verified_index = image_analyzer.Contours_Analysis(self.G, img_path, [], self.Problem)

                if verified_index != 0 and index == verified_index:
                    return verified_index

                return index

            ## If this update doesn't work, then when the DPRs find an answer "vet" it by passing it to the IPR analysis functions.
            # If they both return the same number then bingo. If not, then just return the IPR and see what happens

        # if the ratio decreases from A to B to C but by a normal amount
        elif dpr_BC <= dpr_AB:
            index = 0
            min = 0.0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) / image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI < dpr_GH and dpr_HI > min:
                    min = dpr_HI
                    index = i
                i += 1


            # verify the solution
            if index != 0:
                img_path = self.Problem.figures.get(str(index)).visualFilename
                verified_index = image_analyzer.Contours_Analysis(self.G, img_path, [], self.Problem)

                if verified_index != 0 and index == verified_index:
                    return verified_index

                return index

        # if the ratio increases from A to B to C
        elif dpr_BC >= dpr_AB:
            index = 0
            max = 10000.0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) / image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI > dpr_GH and dpr_HI < max:
                    max = dpr_HI
                    index = i
                i += 1

            if index != 0:
                ##### verify the solution found
                ################################

                img_path = self.Problem.figures.get(str(index)).visualFilename
                verified_index = image_analyzer.Contours_Analysis(self.G, img_path, [], self.Problem)

                if verified_index != 0 and index == verified_index:
                    return verified_index

                return index


        return 0





    def Non_Linear_DPR(self, image_analyzer):
        ######### TEST DPR on non-linear relationsships A->F->H B->#->D

        ##### USE THESE if the answer returns -1
        dpr_AF = image_analyzer.dark_pixel_percentage(self.imageA) / image_analyzer.dark_pixel_percentage(self.imageF)
        dpr_FH = image_analyzer.dark_pixel_percentage(self.imageF) / image_analyzer.dark_pixel_percentage(self.imageH)

        if dpr_FH >= dpr_AF:
            # check to make sure that there are no answers that are identical to already existing images in A.png to H.png
            # this is applicable for niche scenarios like problem D-07 and others
            banned = self.Banned(image_analyzer)

            j = 1
            if len(banned) == 7:
                while j <= 8:
                    if j not in banned:
                        return j

                    j += 1

            index = 0
            max = 10000.0
            i = 1
            while i <= 8:
                if i in banned:
                    i += 1
                    continue

                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_BI = image_analyzer.dark_pixel_percentage(self.imageB) / image_analyzer.dark_pixel_percentage(imageSolution)
                dpr_ID = image_analyzer.dark_pixel_percentage(imageSolution) / image_analyzer.dark_pixel_percentage(self.imageD)

                if dpr_ID >= dpr_BI and dpr_ID <= max:
                    max = dpr_ID
                    index = i
                i += 1

            if index != 0:
                img_path = self.Problem.figures.get(str(index)).visualFilename
                verified_index = image_analyzer.Contours_Analysis(self.G, img_path, banned, self.Problem)

                if verified_index != 0 and index == verified_index:
                    return verified_index

                return index






        if dpr_FH <= dpr_AF:

            # check to make sure that there are no answers that are identical to already existing images in A.png to H.png
            # this is applicable for niche scenarios like problem D-07 and others
            banned = self.Banned(image_analyzer)

            j = 1
            if len(banned) == 7:
                while j <= 8:
                    if j not in banned:
                        return j
                    j += 1

            i = 1
            min = 0
            index = 0
            while i <= 8:
                if i in banned:
                    i += 1
                    continue

                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_BI = image_analyzer.dark_pixel_percentage(self.imageB) / image_analyzer.dark_pixel_percentage(imageSolution)
                dpr_ID = image_analyzer.dark_pixel_percentage(imageSolution) / image_analyzer.dark_pixel_percentage(self.imageD)

                if dpr_ID <= dpr_BI and dpr_ID >= min:
                    min = dpr_ID
                    index = i
                i += 1

            if index != 0:
                verified_index = self.Non_Linear_DPR(image_analyzer)

                if verified_index != 0 and index == verified_index:
                    return verified_index
                '''img_path = self.Problem.figures.get(str(index)).visualFilename
                verified_index = image_analyzer.Contours_Analysis(self.G, img_path, banned, self.Problem)

                if verified_index != 0 and index == verified_index:
                    return verified_index'''

                return index


        return 0





    def Bitwise_Operations_Check(self, image_analyzer):

        AandB = image_analyzer.AND_images(self.imageA, self.imageB)
        GandH = image_analyzer.AND_images(self.imageG, self.imageH)
        if image_analyzer.PercentDiff(AandB, self.imageC) <= 3.8:
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(imageSolution, GandH) <= 3.8:
                    return i
                i += 1

        AorB = image_analyzer.OR_images(self.imageA, self.imageB)
        GorH = image_analyzer.OR_images(self.imageG, self.imageH)
        if image_analyzer.PercentDiff(AorB, self.imageC) <= 3.8:
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(imageSolution, GorH) <= 3.8:
                    return i
                i += 1

        AxorB = image_analyzer.XOR_images(self.imageA, self.imageB)
        GxorH = image_analyzer.XOR_images(self.imageG, self.imageH)
        if image_analyzer.PercentDiff(AxorB, self.imageC) <= 3.8:
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(imageSolution, GxorH) <= 3.8:
                    return i
                i += 1

        return 0
