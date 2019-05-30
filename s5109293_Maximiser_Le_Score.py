import time

class Ball:
    def __init__(self, value):
        self.bool = False
        self.value = int(value)
        self.total_value = sum_digits(int(value))

    def __str__(self):
        return str(self.value)

class HeapPriorityQ:
    def __init__(self, person, queue=None):
        if queue is None:
            queue = []
        self.person = person
        self.queue = queue
        self.result = []

    def __len__(self):
        return len(self.queue)

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def total_score(self):
        return sum(self.result)

    def is_empty(self):
        return len(self.queue) == 0

    def insert(self, data):
        self.queue.append(data)
        self.sift_up(len(self.queue)-1)

    def swap(self, x, y):
        tmp = self.queue[x]
        self.queue[x] = self.queue[y]
        self.queue[y] = tmp

    def clear(self):
        self.queue.clear()
        self.result.clear()

    def pop(self):
        #---------------------------------------
        # Case one if the heap has only one ball
        # pick that ball
        #---------------------------------------
        if len(self) == 1:
            temp = self.queue.pop()
            if not temp.bool:
                temp.bool = True
                self.result.append(temp.value)
        #--------------------------------------------------
        # Case > 1 then Swap the first ball to the last
        # and pop it off to temp variable and heapify
        #--------------------------------------------------
        elif len(self) > 1:
            self.swap(0,len(self.queue)-1)
            temp = self.queue.pop()
            self.sift_down(0)

            #----------------------------------------
            # If the ball is picked/True recall pop()
            # else flag bool and append to result
            #----------------------------------------
            if temp.bool:
                self.pop()
            else:
                temp.bool = True
                self.result.append(temp.value)

        #--------------------------------------------
        # used keep popping until ball can be picked
        #--------------------------------------------
        else:
            temp = False
        return temp

    #------------------
    # Shift up heapify
    #------------------
    def sift_up(self, position):
        if position != 0:
            # Find the parent
            parent_i = position // 2

            #------------------------------------
            # Based off scott/rusty logic
            # Scott heapifies off value
            # Rusty heapifies off the total_value
            #------------------------------------
            if self.person == "scott":
                if self.queue[parent_i].value < self.queue[position].value:
                    self.swap(parent_i, position)
                    self.sift_up(parent_i)
            else:
                if self.queue[parent_i].total_value < self.queue[position].total_value:
                    self.swap(parent_i, position)
                    self.sift_up(parent_i)
                elif self.queue[parent_i].total_value == self.queue[position].total_value \
                     and self.queue[parent_i].value < self.queue[position].value:
                    self.swap(parent_i, position)
                    self.sift_up(parent_i)

    #----------------------------
    # Based off scott/rusty logic
    # Scott heapifies down off value
    # Rusty heapifies down off the total_value
    #----------------------------
    def sift_down(self, position):
        left_pos = 2*position + 1
        right_pos = 2*position + 2
        max_pos = position

        #---------------------------------------------
        # For Scott check if left and right positions
        # are out of range AND parent is less than the
        # left or right. If so make that position max
        #---------------------------------------------
        if self.person == "scott":
            if left_pos < len(self.queue) \
               and self.queue[max_pos].value < self.queue[left_pos].value:
                max_pos = left_pos

            if right_pos < len(self.queue) \
               and self.queue[max_pos].value < self.queue[right_pos].value:
                max_pos = right_pos

        #---------------------------------------------
        # For Rusty check if left and right positions
        # are out of range AND parent is less than the
        # left or right. If so make that position max
        # Also, if the total_values are equal pick the
        # highest actual value
        #---------------------------------------------
        else:
            if left_pos < len(self.queue):
                if self.queue[max_pos].total_value < self.queue[left_pos].total_value:
                    max_pos = left_pos
                elif self.queue[max_pos].total_value == self.queue[left_pos].total_value \
                     and self.queue[max_pos].value < self.queue[left_pos].value:
                    max_pos = left_pos

            if right_pos < len(self.queue):
                if self.queue[max_pos].total_value < self.queue[right_pos].total_value:
                    max_pos = right_pos
                if self.queue[max_pos].total_value == self.queue[right_pos].total_value \
                   and self.queue[max_pos].value < self.queue[right_pos].value:
                    max_pos = right_pos

        if max_pos != position:
            self.swap(position, max_pos)
            self.sift_down(max_pos)

#----------------------------
# Function to run the game
#----------------------------
def game(turn, n_balls, n_rounds, scott, rusty):

    while not scott.is_empty() or not rusty.is_empty():
        for i in range(n_rounds):
            if turn:
                scott.pop()
            else:
                rusty.pop()
        turn = not turn

    return scott.total_score(), rusty.total_score()

#--------------------------------
# Function to sum all the numbers
# in the value for Rusty
#--------------------------------
def sum_digits(digits):
    total = 0
    while digits:
        total,digits = total+digits%10, digits//10
    return total

#--------------------------------
# Main Function to start's here
#--------------------------------
def main():

    scott = HeapPriorityQ("scott")
    rusty = HeapPriorityQ("rusty")

    #----------------------------
    # Open and read inputLeScore
    #----------------------------
    with open("inputLeScore.txt", encoding = 'utf-8') as file:
        test_cases = int(file.readline())

        #-----------------------------
        # Read in line 3 at a time
        # Each time is one "Game" with
        # Three lines of information
        #-----------------------------
        for x in range(test_cases):
            #-----------------------
            # Start time to solution
            #-----------------------
            start = time.time()
            time.process_time()

            #-------------------------
            # Every three lines equals
            # a games/test cases
            #-------------------------
            for y in range(3):
                line = file.readline()
                temp = line.split()

                #------------------------------------
                # Determine number of balls (n_balls)
                # number of rounds (n_rounds)
                #------------------------------------
                if len(temp) == 2:
                    n_balls = int(temp[0])
                    n_rounds = int(temp[1])

                #-------------------------------
                # Pass temp to make all balls
                # of each number for each player
                #-------------------------------
                elif len(temp) > 2:
                    for z in range(len(temp)):
                        temp_2 = (Ball(int(temp[z])))
                        scott.insert(temp_2)
                        rusty.insert(temp_2)

                #--------------------------
                # Determine who goes first
                #--------------------------
                else:
                    coin_toss = str(temp).strip('[\'\n\']')
                    # Scott Starts
                    if coin_toss == "HEADS":
                        turn = True
                    # Rusty starts
                    elif coin_toss == "TAILS":
                        turn = False

            #------------------------------
            # Here we have to run the game
            # to determine the final score
            #------------------------------
            scott_score, rusty_score = game(turn, n_balls, n_rounds, scott, rusty)
            print(scott_score, "\t" ,rusty_score, "\t", end= ' ')

            #-----------------------------
            # Time that taken to solution
            #-----------------------------
            elapsed = time.time() - start
            print('Time taken: {:.6f}'.format(elapsed))

            scott.clear()
            rusty.clear()

main()

