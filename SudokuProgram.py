                                                    # SUDOKU SOLVER PROGRAM 
                                                    # BY DANIEL MONTEIRO
                                                    # START DATE:
                                                    # 12/11/2022
                                                    # START LOCATION:
                                                    # SAN DIEGO, CALIFORNIA


class Box:
    
    def __init__(self) -> None:
        self.members = []
    
    def getMembers(self):
        return self.members
    
    def addMember(self, number):
        self.members.append(number)
    
    def removeMember(self, number):
        self.members.remove(number)

    def isPresent(self, number):
        return number in self.getMembers()
    
    def findMissing(self):
        if len(self.members) != 8:
            return 0
        
        for i in range(1, 10):
            if not i in self.members:
                return i
    
    

def buildGraphs(Row_list, Col_list, Box_list, completeGraph):
    for i in range(9):
        Row_list.append(Box())
        Col_list.append(Box())
        Box_list.append(Box())
        completeGraph.append([None for j in range(10)]) 

def find_box(row, col):

    assert(isinstance(row, int))
    assert(isinstance(col, int))

    if row < 1 or row > 9:
        raise("Row out of bounds")
    if col < 1 or col > 9:
        raise("Column out of bounds")

    
    if row <= 3:
        if col <= 3:
            return 1
        elif col <= 6:
            return 2
        else:
            return 3
    elif row <= 6:
        if col <= 3:
            return 4
        elif col <= 6:
            return 5
        else:
            return 6
    else:
        if col <= 3:
            return 7
        elif col <= 6:
            return 8
        else:
            return 9

class Graph():

    def __init__(self) -> None:
        self.Row_list = [None]
        self.Col_list = [None]
        self.Box_list = [None]
        self.matrix = [None]
        buildGraphs(self.Row_list, self.Col_list, self.Box_list, self.matrix)
        
        pass

    def getRowList(self):
        return self.Row_list
    
    def getColList(self):
        return self.Col_list
    
    def getBoxList(self):
        return self.Box_list
    
    def getMatrix(self):
        return self.matrix

    def __str__(self) -> str:
        
        matrix = self.getMatrix()
        string = "------------\n"
        for i in range(1, 10):
            for j in range(1, 10):
                if j%3 == 1 or j == 1:
                    string += '|'
                if matrix[i][j] == None:
                        string += "X"
                else:
                    string += str(matrix[i][j])
            string += '|\n'
            if i%3 == 0:
                string += '------------\n'
        
        return string 

    def addToGraph(self, row, col, number):
        self.Row_list[row].addMember(number)
        self.Col_list[col].addMember(number)
        box = find_box(row, col)
        self.Box_list[box].addMember(number)
        self.matrix[row][col] = number

    def isFilled(self, row, col):
        if type(self.matrix[row][col]) == int:
            return True
        
        return False

    def getSquare(self, row, col):
        return self.matrix[row][col]

    def removeFromGraph(self, row, col, number):
        self.Row_list[row].removeMember(number)
        self.Col_list[col].removeMember(number)
        
        box = find_box(row, col)
        self.Box_list[box].removeMember(number)
        self.matrix[row][col] = None

    def determineCanAdd(self, row, col, number):
        if number in self.getRowList()[row].getMembers():
            return False
        if number in self.getColList()[col].getMembers():
            return False
        if number in self.getBoxList()[find_box(row, col)].getMembers():
            return False
        
        return True

    def fillRemainder(self):
        
        if self.isComplete():
            return 

        while True:
            flag = 0
            for row in range(1, 10):
                for col in range(1, 10):
                    
                    m1 = self.Row_list[row].findMissing()
                    m2 = self.Col_list[col].findMissing()
                    m3 = self.Box_list[find_box(row, col)].findMissing()

                    if (m1 or m2) or m3:
                        self.addToGraph(row, col, max([m1, m2, m3]))
                        flag = 1
            
            if flag == 0:
                break

    def isComplete(self, other_graph = None):
        for i in range(1, 10):
            if len(self.getRowList()[i].getMembers()) != 9:
                return False
        
        if other_graph == None:
            return True

        for row in range(1, 10):
            for col in range(1, 10):
                if self.isFilled(row, col):
                    num = self.getSquare(row, col)
                    other_graph.addToGraph(row, col, num)
        
        return True


def copyGraph(sudoku: Graph):
    
    newGraph = Graph()

    for row in range(1, 10):
        for col in range(1, 10):
            
            if sudoku.isFilled(row, col):
                num = sudoku.getSquare(row, col)
                newGraph.addToGraph(row, col, num)
    
    return newGraph


def basicSolve(sudoku: Graph):
    sudoku.fillRemainder()
    return
    

def canSolve(sudoku: Graph, result: Graph):

    basicSolve(sudoku) #improves runtime 

    if sudoku.isComplete(result):
        return True
    
    for row in range(1, 10):
        for col in range(1, 10):

            if not sudoku.isFilled(row, col):

                for num in range(1, 10):
                    
                    if sudoku.determineCanAdd(row, col, num):
                        new = copyGraph(sudoku)
                        new.addToGraph(row, col, num)
                        if canSolve(new, result):
                            return True
                    else:
                        continue
                
                if not sudoku.isFilled(row, col):
                    return False
    
    return False
                        
                        

def addTemplate(lst: list, sudoku: Graph):
    for row in range(9):
        for col in range(9):
            if lst[row][col] != None:
                sudoku.addToGraph(row + 1, col + 1, lst[row][col])
    
template1 = [
    [None, 3, 5, 2, 6, 9, 7, 8, 1],
    [6, 8, 2, 5, 7, 1, 4, 9, 3],
    [1, 9, 7, 8, 3, 4, 5, 6, 2],
    [8, 2, 6, 1, 9, 5, 3, 4, 7],
    [3, 7, 4, 6, 8, 2, 9, 1, 5],
    [9, 5, 1, 7, 4, 3, 6, 2, 8],
    [5, 1, 9, 3, 2, 6, 8, 7, 4],
    [2, 4, 8, 9, 5, 7, 1, 3, 6],
    [7, 6, 3, 4, 1, 8, 2, 5, 9]
]

def main():
    
    sudoku = Graph()
    result = Graph()
    addTemplate(template1, sudoku)
    canSolve(sudoku, result)

    print(result)
    print(result.isComplete())
    # print(sudoku.isComplete())
    

    
if __name__ == "__main__":
    main()



