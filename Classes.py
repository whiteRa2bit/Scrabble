from hashing import hashFunc
from itertools import permutations

# NESSESARY?
class Alphabet:
    alphabetSize = 26
    letters = [chr(ord('a') + i) for i in range(26)]


class Word: ### !!! STRING IS STORING WITHOUT \n SYMBOL (use .rstrip()), HASH'S ALSO COUNTING THIS WAY HERE AND IN SORTING !!!
    def __init__(self, string, type): # Is local copy of type really nessesary?
        self.string = string.rstrip()
        self.dictType = type
        self.hash = hashFunc(self.string)

    def isWord(self):
        from config import hashesAI
        return self.hash in hashesAI[self.dictType].keys() and self.string in hashesAI[self.dictType][self.hash]

    def subWords(self):
        subWordsData = set()
        for length in range(len(self.string)):
            for psiWord in permutations(self.string, length):
                curString = ""
                for letter in psiWord:
                    curString += letter
                curWord = Word(curString, self.dictType)
                if curWord.isWord():
                    subWordsData.add(curWord.string) # STRING JUST TO TEST
        return subWordsData

    def allPossibleWords(self, playBoard):
        emptyData = [[[0, 0] for i in range(playBoard.length)] for j in range(playBoard.height)]
        for i in range(playBoard.height):
            curEmpty = 0
            for j in range(playBoard.length - 1, -1, -1):
                curEmpty += playBoard.board[i][j].isEmpty
                emptyData[i][j][0] = curEmpty
        for i in range(playBoard.length):
            curEmpty = 0
            for j in range(playBoard.height - 1, -1, -1):
                curEmpty += playBoard.board[j][i].isEmpty
                emptyData[j][i][1] = curEmpty
        ### Horizontal
        wordsAndCoords = set()
        wordsOnly = set()
        for i in range(playBoard.height):
            for j in range(playBoard.length - 1, -1, -1):
                maxLetters = min(5, emptyData[i][j][0]) # Hand size irl ()
                for curLen in range(1, maxLetters):
                    currentEmptiness = 0
                    temp = 0
                    stakedLetters = []
                    prevData = []
                    for k in range(j - 1, -1, -1):
                        if playBoard.board[i][k].isEmpty:
                            break
                        else:
                            prevData.insert(0, playBoard.board[i][k].letter)
                    for k in range(len(prevData)):
                        stakedLetters.append((k, prevData[k]))
                    while currentEmptiness != maxLetters:
                     #   print(i, j, j + temp, maxLetters)
                        if playBoard.board[i][j + temp].isEmpty:
                            currentEmptiness += 1
                        else:
                            stakedLetters.append((temp + len(prevData), playBoard.board[i][j + temp].letter))
                        temp += 1
                    for k in range(j + temp, playBoard.length):
                        if playBoard.board[i][k].isEmpty:
                            break
                        else:
                            stakedLetters.append((temp + k + len(prevData), playBoard.board[i][j + temp + k].letter))

                    subWordsData = set()
                    for psiWord in permutations(self.string, curLen):
                        curString = ""
                        psiWord = list(psiWord)
                        for inserts in range(len(stakedLetters)):
                            psiWord.insert(stakedLetters[inserts][0], stakedLetters[inserts][1])
                        for letter in psiWord:
                            curString += letter
                      #  print(curString)
                        curWord = Word(curString, self.dictType)
                        if curWord.isWord():
                            subWordsData.add(curWord.string)  # STRING JUST TO TEST
                    for elem in subWordsData:
                        wordsAndCoords.add((elem, (i, j)))
                        wordsOnly.add(elem)
        print(wordsOnly)

class Cell:
    def __init__(self, row, col):
        from config import bonuses
        self.row = row
        self.col = col
        self.letter = '-'
        self.bonus = bonuses[row][col]
        self.isEmpty = True

    def setLetter(self, letter):
        self.letter = letter
        self.isEmpty = False

class WordOnBoard:
    def __init__(self, cells, type): #Cells is a list of Cell objects
        string = ""
        for el in cells:
            string += el.letter
        self.string = string.rstrip()
        self.dictType = type
        self.hash = hashFunc(self.string)
        self.cells = cells

    def isWord(self):
        from config import hashesAI
        return self.hash in hashesAI[self.dictType].keys() and self.string in hashesAI[self.dictType][self.hash]

    def isConnected(self):
        firstCell = self.cells[0]
        secondCell = self.cells[1]
        rowDif = firstCell.row - secondCell.row
        colDif = firstCell.col - secondCell.col
        answer = True
        for i in range(1, len(self.cells) - 1):
            currentCell = self.cells[i]
            nextCell = self.cells[i + 1]
            if currentCell.row - nextCell.row != rowDif or currentCell.col - nextCell.col != colDif:
                answer = False
                break
        return answer

class Bag:
    def __init__(self):
        self.bag = {' ': 2, 'a': 9, 'b': 2, 'c': 2, 'd': 4, 'e': 12, 'f': 2, 'g': 3,
           'h': 2, 'i': 9, 'j': 1, 'k': 1, 'l': 4, 'm': 2, 'n': 6, 'o': 8,
           'p': 2, 'q': 1, 'r': 6, 's': 4, 't': 6, 'u': 4, 'v': 2, 'w': 2,
           'x': 1, 'y': 2, 'z': 1}

        self.lettersNum = 100

    def removeLetter(self, letter):
        if self.bag[letter] > 0:
            self.bag[letter] -= 1
            self.lettersNum -= 1
            return True
        else:
            return False

    def randomLetter(self):
        from random import randint
        letterNum = randint(0, self.lettersNum - 1)
        counter = 0
        for el in self.bag:
            if counter <= letterNum:
                prevLetter = el
                counter += self.bag[el]
            else:
                break
        self.removeLetter(prevLetter)
        return prevLetter


class Board:
    def __init__(self, boardLength, boardHeight):
        self.board = [[] for x in range(boardHeight)]
        self.length = boardLength
        self.height = boardHeight
        for row in range(boardHeight):
            for col in range(boardLength):
                self.board[row].append(Cell(row, col))

    def addWord(self, word):
        if word.isWord() and word.isConnected():
            rowBegin = word.cells[0].row
            rowEnd = word.cells[len(word.cells) - 1].row
            colBegin = word.cells[0].col
            colEnd = word.cells[len(word.cells) - 1].col
            if rowBegin == rowEnd:  # "Horizontal orientation"
                counter = 0
                for letter in word.string:
                    self.board[rowBegin][colBegin + counter].setLetter(letter)
                    counter += 1

            elif colBegin == colEnd:  # Vertical orientation
                counter = 0
                for letter in word.string:
                    self.board[rowBegin + counter][colBegin].setLetter(letter)
                    counter += 1

    def printBoard(self):
        for row in range(self.height):
            for col in range(self.length):
                print(self.board[row][col].letter, end=" ")
            print()

myBoard = Board(15, 15)
c1 = Cell(5, 6)
c2 = Cell(6, 6)
c3 = Cell(7, 6)
c4 = Cell(8, 6)
c1.setLetter('n')
c2.setLetter('o')
c3.setLetter('s')
c4.setLetter('e')


a = WordOnBoard([c1, c2, c3, c4], "Large")
myBoard.addWord(a)
myBoard.printBoard()

b = Word("huma", "Large")
b.allPossibleWords(myBoard)
