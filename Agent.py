# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.

from PIL import Image, ImageChops
import cv2 as cv
import numpy
import time
from TwoXTwo_Solver import TwoXTwo_Solver
from ThreeXThree_Solver import ThreeXThree_Solver

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.Time = 0.0
        self.ProblemName = ""



    def CheckBasics(self, problem):

        if problem.problemType == "2x2":
            solve = TwoXTwo_Solver().solver(problem=problem)
            return solve

        else:
            solve = ThreeXThree_Solver(problem)
            return solve.solver()


    def Solve(self, problem):
        startTime = time.perf_counter()

        answer = self.CheckBasics(problem)

        endTime = time.perf_counter()
        self.Time = endTime - startTime
        name = problem.name[0] + " " + problem.name[-4:]
        self.ProblemName = name

        return answer if answer is not None else -1