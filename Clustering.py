import numpy as np
import  math
class Clustring:

    dimension  = 300
    g = 100
    k = 3
    NumberOfData = 80
    C_Target = 1000
    D_Original = np.zeros((NumberOfData, NumberOfData))
    D_Current = np.zeros((NumberOfData , NumberOfData))
    data = np.empty((NumberOfData  , dimension))
    R = np.empty(( NumberOfData  , k + 1))
    L = np.arange(NumberOfData)
    C_Current = math.floor(NumberOfData / g)
    def __init__(self , data):

        self.NumberOfData = len(data)
        self.D_Original = np.zeros((len(data), len(data) ))
        self.D_Current = np.zeros((len(data) ,len(data) ))
        self.data = np.empty((len(data)  , self.dimension))
        self.R = np.empty((len(data), self.k + 1))
        self.L = np.arange(len(data))
        self.C_Current = math.floor(len(data) / self.g)
        for ko in range(0 , self.NumberOfData) :
            self.data[ko] = data[ko]


    def main(self):
        if self.C_Current < self.C_Target :
            return self.L
        else:

            self.calculateDistances()
            self.calculateR()
            self.calculateFirstDC()

            while self.C_Current > self.C_Target :
                key_point = self.KeyPoints(self.C_Current)
                self.match_Datas(key_point)
                self.Update_Matris_Distance()
                self.C_Current = math.floor(self.C_Current / self.g)
                print("hello world")
            return self.L







    def claculateDistance(self , i , j):
        value = 0
        for s in range(0 , self.dimension):
            dis =math.pow( self.data[i  , s ]  - self.data[j, s]  , 2)
            value += dis
        return math.sqrt(value)


    def calculateDistances(self):

        for i in range(0 , self.NumberOfData ):
            for j in range(0 , self.NumberOfData) :
                self.D_Original[i , j] = self.claculateDistance(i , j)

    def calculateR(self):

        for i in range( 0 , self.NumberOfData) :
            s = np.argpartition(self.D_Original[i] , self.k)
            for num in range(0 , self.k + 1):

                self.R[i][num] = s[num]
        self.R = self.R.astype(int)

    def calculateFirstDC(self):
        for i in range(0 , self.NumberOfData):
            for j in range(0 , i):
                if i == j:
                    self.D_Current[i][j] = 0
                else:
                    value = 0
                    for z in range(0 , self.k +1 ):
                        for f in range(0 , self.k+1):
                            self.R[i][z] = int(self.R[i][z])

                            value += self.D_Original[self.R[i][z]][self.R[j][f]]

                    value = value / pow(self.k+1 , 2)
                    self.D_Current[i][j] = value
                    self.D_Current[j][i] = value



    def KeyPoints(self , numberOfKeys):
        m = len(self.D_Current)
        min = math.inf
        key_list = []
        key = 0
        for i in range( 0  , m ) :
            dis = 0

            for j in range(0 ,  m):
                 dis += self.D_Current[i][j]
            if dis < min  :
                min = dis
                key = i
        key_list.append(key)
        for k in range(0 , numberOfKeys-1) :
            max = -math.inf
            key1 = 0
            for  o in range(0 , m):
                min1 = math.inf

                for o1 in range(0 , len(key_list)):
                    if self.D_Current[o][key_list[o1]] < min :
                        min1 = self.D_Current[o][key_list[o1]]

                if min1 > max :
                 max = min1
                 key1 = o
            key_list.append(key1)

        return key_list

    def match_Datas(self , key_list):
        m = len(self.D_Current)
        for i in range( 0 , m ):
            min = math.inf
            for j in range( 0 , len(key_list)):
                if self.D_Current[i][j] < min :
                    min = self.D_Current[i][j]
                    self.L[i] = j

    def distenses(self , list1 , list2 ):

        lenth_List1 = len(list1)
        lenth_List2 = len(list2)
        Product = lenth_List2 * lenth_List1
        sum = 0
        for i in range( 0 , lenth_List1) :
            for j in range( 0 , lenth_List2):
                sum += self.D_Original[list1[i]][list2[j]]

        return  sum / Product


    def Update_Matris_Distance(self, key_list):
        m = len(key_list)

        groups = [[] for _ in range(m)]
        for i in range(0 , len(self.L)):
            groups[self.L[i]] = i

        for o in range(0 , m ) :
            for op in range(0 , len(groups[o])):
                groups[o] = list(set().union(groups[o] , self.R[groups[o][op]]))


        self.D_Current = np.zeros((m , m))

        for i in range(0, m):
             for j in range(0, i):
                if i == j:
                    self.D_Current[i][j] = 0
                else:

                    value = self.distenses(groups[j] , groups[i])




                    self.D_Current[i][j] = value
                    self.D_Current[j][i] = value









