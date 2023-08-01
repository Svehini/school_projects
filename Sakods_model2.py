import random as rd

def board_maker(placements, grid):
    for key, value in placements.items():
        key = key.split(",")
        p1 = int(key[0])
        p2 = int(key[1])
        for i in range(len(grid)):
            if p1 == i:
                line = grid[i]
                for n in range(len(line)):
                    if p2 == n:
                        if value == "X":
                            line[n] = "X"   # Blue is X
                        elif value == "O":
                            line[n] = "O"   # Red is O
                        grid[i] = line
    return grid


# THIS PART TAKES INPUT FROM USER

print()
grid_row = int(input("What should the row be? (Vertical): "))
grid_col = int(input("What should the col be? (Horizontal): "))
num_of_placements = int(input(f"Number of Red and Blue dots (from 1-{(grid_row*grid_col)-1}): "))
blue_red = input("How many percentage of dots Red/Blue? (Answer as: reds, blue, fks (50,50) ): ")
preference = int(input("How many percentage of each persons neighbors must be alike?: "))


# Used while testing the code
# grid_size = 10
# num_of_placements = 70
# blue_red = "50,50"
# preference = 100
############################


blue_red = blue_red.split(",")
blue = int(blue_red[0])
red = int(blue_red[1])
reds = int(num_of_placements*(red/100))
blues = int(num_of_placements*(blue/100))
places = {
}

###################################

    
def get_coords():
    g1 = rd.randint(0,grid_row-1)
    g2 = rd.randint(0,grid_col-1)
    coord = f"{g1},{g2}"
    return coord

occupied = []
def placer(num, color):
    for i in range(num):
        coord = get_coords()
        str_coord = coord
        while str_coord in occupied:
            coord = get_coords()
            str_coord = coord
        places[coord] = color
        occupied.append(str_coord)


def make_grid(grid_row, grid_col):
    this_grid = []
    for i in range(grid_row):
        grid_line = []
        for n in range(grid_col):
            grid_line.append(".")
            coord = f"{i},{n}"
            places[coord] = "."
        this_grid.append(grid_line)
    return this_grid


def print_board():
    print("Blue agents are X, and red agents are O\n")
    new_grid = board_maker(places, grid)
    for i in range(grid_row):
        line = ""
        for n in range(grid_col):
            line+=(grid[i][n])
        print(line)
        # print(new_grid[i])
    print("\n")


def get_hood(key, value):
    right_n_hood = 0
    wrong_n_hood = 0
    key_coord = key.split(",")
    c1 = int(key_coord[0])
    c2 = int(key_coord[1])
    neighbors = [-1, 0, 1]
    if value == "O":
        other_value = "X"
    elif value == "X":
        other_value = "O"
    for i in neighbors:
        for n in neighbors:
            if c2+n >= 0 and c2+n <= grid_col-1:
                if c1+i >= 0 and c1+i <= grid_row-1:
                    neighbor_value = (grid[c1+i][c2+n])
                else:
                    neighbor_value = 0
            else: 
                neighbor_value = 0
            if neighbor_value == value:
                right_n_hood+=1
            elif neighbor_value == other_value:
                wrong_n_hood+=1
    return right_n_hood, wrong_n_hood

def checks_neighbors():
    satisfied = []
    not_satisfied = []
    for key, value in places.items():
        if value != ".":
            right_n_hood, wrong_n_hood = get_hood(key, value)
            if right_n_hood >= ((right_n_hood+wrong_n_hood)*(preference/100)):
                if key not in satisfied:
                    satisfied.append(key)
            else:
                if key not in not_satisfied:
                    not_satisfied.append(key)
    return  satisfied, not_satisfied


def check_tomove(input_value, switch_value):
    blank_satisfied = []
    blank_not_satisfied = []
    for key, value in places.items():
        if value == switch_value:
            right_n_hood, wrong_n_hood = get_hood(key, input_value)
            if value != ".":
                right_n_hood -=1
            if right_n_hood >= ((right_n_hood+wrong_n_hood)*(preference/100)):
                if key not in blank_satisfied:
                    blank_satisfied.append(key)
            else:
                if key not in blank_not_satisfied:
                    blank_not_satisfied.append(key)
    return blank_satisfied, blank_not_satisfied



def change_spots(possible_moves, c1, c2, nearest):
    short_change = False
    current_smallest = (grid_row*grid_col)
    if nearest == True:
        for i in possible_moves:
            key_coord = i.split(",")
            ct1 = int(key_coord[0]); ct2 = int(key_coord[1])
            distance_to_move = abs(ct1-c1)+abs(ct2-c2)
            if distance_to_move<current_smallest:
                current_smallest = distance_to_move
                change_ct1 = ct1
                change_ct2 = ct2
                short_change = True
    else: 
        i = rd.randint(0,len(possible_moves)-1)
        i = possible_moves[i]
        key_coord = i.split(",")
        change_ct1 = int(key_coord[0]); change_ct2 = int(key_coord[1])
        short_change = True
    if short_change:
        a = grid[c1][c2]; b = grid[change_ct1][change_ct2]
        grid[c1][c2] = b; grid[change_ct1][change_ct2] = a
        coord_old = f"{c1},{c2}"
        coord_new = f"{change_ct1},{change_ct2}"
        places[coord_old] = b; places[coord_new] = a

def change_grid(everyone_happy):
    satisfied, not_satisfied = checks_neighbors()
    if len(not_satisfied) == 0:
        everyone_happy = True
        return everyone_happy
    # print("satisfied: ", satisfied)
    # print("not satisfied: ", not_satisfied)
    for i in range(len(not_satisfied)):
        key_coord = not_satisfied[i].split(",")
        c1 = int(key_coord[0]); c2 = int(key_coord[1])
        wanted_value = "."
        blank_satisfied,blank_not_satisfied = check_tomove(grid[c1][c2], wanted_value)
        if len(blank_satisfied)>0:
            nearest = True
            change_spots(blank_satisfied, c1, c2, nearest)
        else:
            if grid[c1][c2] == "O":
                wanted_value = "X"
            else:
                wanted_value = "O"
            blank_satisfied, x = check_tomove(grid[c1][c2], wanted_value)   # Her it will count itself on both middle and side
            if len(blank_satisfied)>0:
                nearest = True
                change_spots(blank_satisfied, c1, c2, nearest)
            else:
                nearest = False
                change_spots(blank_not_satisfied, c1, c2, nearest)


    return everyone_happy


grid = make_grid(grid_row, grid_col)
placer(reds, "O")           # O is red
placer(blues, "X")          # X is blue
everyone_happy = False


cycle = 0
while everyone_happy == False:
    print("##############################################\n")
    print(f"Cycle: {cycle}\n")
    cycle+=1
    print_board()
    everyone_happy = change_grid(everyone_happy)
print("Preference is met and everyone is happy!\n")
