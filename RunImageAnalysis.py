from PIL import Image, ImageChops
import random
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


    def Banned(self, image_analyzer):
        banned = []
        for i in range(len(self.ImgaeInAr)):
            for j in range(1, 9):
                img_path = self.Problem.figures.get(str(j)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                if image_analyzer.PercentDiff(imageSolution, self.ImgaeInAr[i]) <= 2.5:
                    banned.append(j)
                    break
        return banned



    def DPR_Analysis_SameShape(self, image_analyer):

        dpr_AB = image_analyer.dark_pixel_percentage(self.imageA) - image_analyer.dark_pixel_percentage(
            self.imageB)
        dpr_BC = image_analyer.dark_pixel_percentage(self.imageB) - image_analyer.dark_pixel_percentage(
            self.imageC)
        dpr_GH = image_analyer.dark_pixel_percentage(self.imageG) - image_analyer.dark_pixel_percentage(
            self.imageH)

        # if the ratio decreases from A to B to C but by an INSANE amount
        if dpr_BC <= dpr_AB and dpr_BC < 0.0:
            index = 0
            min = -1000
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                if image_analyer.SameShape(img_path, self.C) == False:
                    i += 1
                    continue
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyer.dark_pixel_percentage(self.imageH) - image_analyer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI < dpr_GH and dpr_HI > min:
                    min = dpr_HI
                    index = i

                i += 1

            if index != 0:
                return index


        # if the ratio decreases from A to B to C but by a normal amount
        elif dpr_BC <= dpr_AB:
            index = 0
            min = 0.0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                if image_analyer.SameShape(img_path, self.C) == False:
                    i += 1
                    continue
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyer.dark_pixel_percentage(self.imageH) - image_analyer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI < dpr_GH and dpr_HI > min:
                    min = dpr_HI
                    index = i
                i += 1

            # verify the solution
            if index != 0:
                return index

        # if the ratio increases from A to B to C
        elif dpr_BC >= dpr_AB:
            index = 0
            max = 10000.0
            i = 1
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                if image_analyer.SameShape(img_path, self.C) == False:
                    i += 1
                    continue
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyer.dark_pixel_percentage(self.imageH) - image_analyer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI > dpr_GH and dpr_HI < max:
                    max = dpr_HI
                    index = i
                i += 1

            if index != 0:
                return index

        return random.randint(1, 8)






    def Basic_DPR(self, image_analyzer):
        #### try calculating dark pixel ratio horizontally

        banned = self.Banned(image_analyzer)
        j = 1
        if len(banned) == 7:
            while j <= 8:
                if j not in banned:
                    return j
                j += 1

        dpr_AB = image_analyzer.dark_pixel_percentage(self.imageA) - image_analyzer.dark_pixel_percentage(self.imageB)
        dpr_BC = image_analyzer.dark_pixel_percentage(self.imageB) - image_analyzer.dark_pixel_percentage(self.imageC)
        dpr_GH = image_analyzer.dark_pixel_percentage(self.imageG) - image_analyzer.dark_pixel_percentage(self.imageH)



        # if the ratio decreases from A to B to C but by an INSANE amount
        if dpr_BC <= dpr_AB and dpr_BC < 0.0:
            index = 0
            min = -1000
            i = 1
            while i <= 8:
                if i in banned:
                    i += 1
                    continue
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) - image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI <= dpr_GH and dpr_BC - 2.5 <= dpr_HI <= dpr_BC + 2.5:
                    min = dpr_HI
                    index = i

                i += 1

            if index != 0:
                return index



        # if the ratio decreases from A to B to C but by a normal amount
        if dpr_BC <= dpr_AB:
            index = 0
            min = 0.0
            i = 1
            while i <= 8:
                if i in banned:
                    i += 1
                    continue
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) - image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI <= dpr_GH and dpr_BC - 2.5 <= dpr_HI <= dpr_BC + 2.5:
                    index = i
                i += 1


            # verify the solution
            if index != 0:
                return index

        # if the ratio increases from A to B to C
        if dpr_BC >= dpr_AB:
            index = 0
            max = 10000.0
            i = 1
            while i <= 8:
                if i in banned:
                    i += 1
                    continue
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) - image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_HI >= dpr_GH and dpr_BC - 2.5 <= dpr_HI <= dpr_BC + 2.5:
                    max = dpr_HI
                    index = i
                i += 1

            if index != 0:
                ##### verify the solution found
                ################################
                return index


        return 0





    def Non_Linear_DPR(self, image_analyzer):
        ######### TEST DPR on non-linear relationsships A->F->H B->#->D

        ##### USE THESE if the answer returns -1

        banned = self.Banned(image_analyzer)
        j = 1
        if len(banned) == 7:
            while j <= 8:
                if j not in banned:
                    return j
                j += 1

        dpr_AF = image_analyzer.dark_pixel_percentage(self.imageA) - image_analyzer.dark_pixel_percentage(self.imageF)
        dpr_FH = image_analyzer.dark_pixel_percentage(self.imageF) - image_analyzer.dark_pixel_percentage(self.imageH)
        dpr_GH = image_analyzer.dark_pixel_percentage(self.imageG) - image_analyzer.dark_pixel_percentage(self.imageH)

        dpr_AD = image_analyzer.dark_pixel_percentage(self.imageA) - image_analyzer.dark_pixel_percentage(self.imageD)
        dpr_DG = image_analyzer.dark_pixel_percentage(self.imageD) - image_analyzer.dark_pixel_percentage(self.imageG)
        dpr_CF = image_analyzer.dark_pixel_percentage(self.imageC) - image_analyzer.dark_pixel_percentage(self.imageF)


        if dpr_FH >= dpr_AF:
            # check to make sure that there are no answers that are identical to already existing images in A.png to H.png
            # this is applicable for niche scenarios like problem D-07 and others
            index = 0
            max = 10000.0
            i = 1
            while i <= 8:
                if i in banned:
                    i += 1
                    continue

                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_BI = image_analyzer.dark_pixel_percentage(self.imageB) - image_analyzer.dark_pixel_percentage(imageSolution)
                dpr_ID = image_analyzer.dark_pixel_percentage(imageSolution) - image_analyzer.dark_pixel_percentage(self.imageD)

                if dpr_ID >= dpr_BI and dpr_FH - 2.5 <= dpr_ID <= dpr_FH + 2.5:
                    index = i
                i += 1

            if index != 0:
                return index



        if dpr_FH <= dpr_AF:

            # check to make sure that there are no answers that are identical to already existing images in A.png to H.png
            # this is applicable for niche scenarios like problem D-07 and others
            i = 1
            min = -1000
            index = 0
            while i <= 8:
                if i in banned:
                    i += 1
                    continue

                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_BI = image_analyzer.dark_pixel_percentage(self.imageB) - image_analyzer.dark_pixel_percentage(imageSolution)
                dpr_ID = image_analyzer.dark_pixel_percentage(imageSolution) - image_analyzer.dark_pixel_percentage(self.imageD)

                if dpr_ID <= dpr_BI and dpr_FH - 2.5 <= dpr_ID <= dpr_FH + 2.5:
                    index = i
                i += 1

            if index != 0:
                return index


        #### if the dpr is similar => they are identical images like in basic C-08
        if dpr_GH <= dpr_CF:
            index = 0
            i = 1
            while i <= 8:
                if i in banned:
                    i += 1
                    continue
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_HI = image_analyzer.dark_pixel_percentage(self.imageH) - image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_GH - 2.5 <= dpr_HI <= dpr_GH + 2.5:
                    index = i
                i += 1

            if index != 0:
                return index



        if dpr_AD <= dpr_DG:
            index = 0
            i = 1
            while i <= 8:
                if i in banned:
                    i += 1
                    continue
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_FI = image_analyzer.dark_pixel_percentage(self.imageF) - image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_AD - 2.5 <= dpr_FI <= dpr_AD + 2.5:
                    index = i
                i += 1

            if index != 0:
                return index


        if dpr_AD >= dpr_DG:
            index = 0
            i = 1
            while i <= 8:
                if i in banned:
                    i += 1
                    continue
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")

                dpr_FI = image_analyzer.dark_pixel_percentage(self.imageF) - image_analyzer.dark_pixel_percentage(
                    imageSolution)

                if dpr_AD - 2.5 <= dpr_FI <= dpr_AD + 2.5:
                    index = i
                i += 1

            if index != 0:
                return index





        return random.randint(1, 8)






    def Bitwise_Operations_Check(self, image_analyzer):

        ###### PLACE SHAPE DETECTION BEFORE DPR THING IN THREEXTHREE
        ###### UPDATE SIDESADDED() TO NOT RETURN i but do if index != 0 return index
        banned = self.Banned(image_analyzer)
        j = 1
        if len(banned) == 7:
            while j <= 8:
                if j not in banned:
                    return j
                j += 1


        #### NICHE APPLICATION FOR C-12
        DorB = image_analyzer.OR_images(self.imageD, self.imageB)
        ForH = image_analyzer.OR_images(self.imageF, self.imageH)
        if image_analyzer.PercentDiff(DorB, self.imageE) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                result = image_analyzer.PercentDiff(imageSolution, ForH)
                if result <= 2.5 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index



        AorB = image_analyzer.OR_images(self.imageA, self.imageB)
        GorH = image_analyzer.OR_images(self.imageG, self.imageH)
        if image_analyzer.PercentDiff(AorB, self.imageC) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                result = image_analyzer.PercentDiff(imageSolution, GorH)
                if result <= 2.5 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index


        ###### down the column
        AorD = image_analyzer.OR_images(self.imageA, self.imageD)
        CorF = image_analyzer.OR_images(self.imageC, self.imageF)
        if image_analyzer.PercentDiff(AorD, self.imageG) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                result = image_analyzer.PercentDiff(imageSolution, CorF)
                if result <= 3.8 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index



        AorF = image_analyzer.OR_images(self.imageA, self.imageF)
        if image_analyzer.PercentDiff(AorF, self.imageH) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                xord = image_analyzer.OR_images(imageSolution, self.imageB)
                result = image_analyzer.PercentDiff(xord, self.imageD)
                if result <= 3.8 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index





        ################## AND BITWISE ######################
        ####################################################
        AandB = image_analyzer.AND_images(self.imageA, self.imageB)
        GandH = image_analyzer.AND_images(self.imageG, self.imageH)
        if image_analyzer.PercentDiff(AandB, self.imageG) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                result = image_analyzer.PercentDiff(imageSolution, GandH)
                if result <= 3.8 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index

        AandD = image_analyzer.AND_images(self.imageA, self.imageD)
        CandF = image_analyzer.AND_images(self.imageC, self.imageF)
        if image_analyzer.PercentDiff(AandD, self.imageG) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                result = image_analyzer.PercentDiff(imageSolution, CandF)
                if result <= 3.8 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index


        AandF = image_analyzer.AND_images(self.imageA, self.imageF)
        if image_analyzer.PercentDiff(AandF, self.imageH) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                andd = image_analyzer.AND_images(imageSolution, self.imageB)
                result = image_analyzer.PercentDiff(andd, self.imageD)
                if result <= 3.8 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index




        ################## XOR BITWISE ######################
        ####################################################
        AxorB = image_analyzer.XOR_images(self.imageA, self.imageB)
        GxorH = image_analyzer.XOR_images(self.imageG, self.imageH)
        if image_analyzer.PercentDiff(AxorB, self.imageC) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                result = image_analyzer.PercentDiff(imageSolution, GxorH)
                if result <= 3.8 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index


        AxorD = image_analyzer.XOR_images(self.imageA, self.imageD)
        CxorF = image_analyzer.XOR_images(self.imageC, self.imageF)
        if image_analyzer.PercentDiff(AxorD, self.imageG) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                result = image_analyzer.PercentDiff(imageSolution, CxorF)
                if result <= 3.8 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index


        AxorF = image_analyzer.XOR_images(self.imageA, self.imageF)
        if image_analyzer.PercentDiff(AxorF, self.imageH) <= 2.8:
            i = 1
            index = 0
            min = 1000
            while i <= 8:
                img_path = self.Problem.figures.get(str(i)).visualFilename
                imageSolution = Image.open(img_path).convert("L")
                xord = image_analyzer.XOR_images(imageSolution, self.imageB)
                result = image_analyzer.PercentDiff(xord, self.imageD)
                if result <= 3.8 and result < min:
                    min = result
                    index = i
                i += 1

            if index != 0:
                return index


        return 0
