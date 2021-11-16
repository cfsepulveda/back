import config as cf
import model
import os.path


algorithms = ['shell', 'insertion', 'selection', 'quick', 'merge']
# sizes = [1000,2000...512000]
sizes = [(2**x)*1000 for x in range(0,10)]

def outputSortingTest(algorithm, size, time):
    print("Algorithm", algorithm, "size", size, "executed in time", time, "ms.")

class dataSortingTests:

    def __init__(self, filename, rows, columns, flag):
        i = 0
        j = 0
        self.filename = filename
        self.flag = flag
        # matrix rowsxcolumns of 0.0f
        self.matrix = [[0.0]*columns for x in range(0, rows)]
        if (os.path.isfile(filename)):
            with open(filename, 'r') as testsfile:
                line = testsfile.readline()
                line = testsfile.readline()
                while line:
                    line = line.replace('\n','')
                    line = line.split(sep=',')
                    for n in line:
                        if n:
                            self.matrix[i][j] = float(n)
                            j += 1
                    if (j == 5):
                        i+= 1
                        j = 0
                    line = testsfile.readline()
                testsfile.close()
        self.i = i
        self.j = j
    
    def writeTestsToDisk(self):
        with open(self.filename, 'w') as testsfile:
            result = 'shell,insertion,selection,quick,merge\n'
            i = 0
            j = 0
            while i < 10:
                while j < 4 and self.matrix[i][j]:
                    result += str(round(self.matrix[i][j], 2))+','
                    j += 1
                if not self.matrix[i][j]:
                    break
                result += str(round(self.matrix[i][j], 2)) + '\n'
                j = 0
                i += 1
            testsfile.write(result)
            testsfile.close()
    
    def doThreeTests(self, videos):
        k = 0
        time = 0
        success = False
        # self.flag[1] checks if the user wants to let the program find the average
        while k < 3 and self.flag[1]:
            result = model.inefficient_ordering(videos, sizes[self.i], algorithms[self.j])
            time += result[0] / 3
            k += 1
        if k == 3:
            time = round(time, 2)
            self.matrix[self.i][self.j] = time
            outputSortingTest(algorithms[self.j], sizes[self.i], time)
            success = True
        return success

    def testingLoop(self, videos):
        # self.flag[0] checks if the user wants to continue running the tests
        while self.flag[0] and self.i < 10:
            while self.flag[0] and self.j < 5:
                wasSuccess = self.doThreeTests(videos)
                if wasSuccess:
                    self.j += 1
            if self.j == 5:
                self.j = 0
            self.i += 1
    

def doSortingTests(videos, flag):
    data = dataSortingTests('Data/tests.csv', 10, 5, flag)
    data.testingLoop(videos)
    data.writeTestsToDisk()
    