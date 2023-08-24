from tkinter import *
import tkinter.messagebox
import random
from functools import partial
import numpy as np

root = Tk()
root.geometry("800x420+400+200")
root.iconbitmap("C:/Python/Battleship/Icons8-Windows-8-Military-Battleship.ico")

player_coordinates = []
computer_coordinates = []
computer_buttons = []
guessed_list = []
player_ships_left = 3
computer_ships_left = 3
ship_2_hit = False
ship_3_hit = False
last_coord = []

class Ship:
    hits = 0
    def __init__(self, size, player):
        self.size = size
        self.player = player
        self.ship_xy = []
        self.direction = random.randint(0,1)
        self.destroyed = False

    def ship_coords(self):
        global player_coordinates
        global computer_coordinates
        for iter in range(self.size):
            # Choose random starting point for a ship
            if iter < 1:
                # Direction 0 = horizontal, 1 = vertical
                if self.direction == 0:
                    if iter == 0:
                        # Ship size deducted from coordx so that
                        # rest of the parts won't be place outside
                        # of the grid during placement
                        coordx = random.randint(0,9-self.size)
                        coordy = random.randint(0,9)
                        ship_tuple = (coordx, coordy)
                        if self.player == 0:
                            if ship_tuple in player_coordinates:
                                break
                        elif self.player == 1:
                            if ship_tuple in computer_coordinates:
                                break
                elif self.direction == 1:
                    if iter == 0:
                        # Ship size deducted from coordy so that
                        # rest of the parts won't be place outside
                        # of the grid during placement
                        coordx = random.randint(0,9)
                        coordy = random.randint(0,9-self.size)
                        ship_tuple = (coordx, coordy)
                        if self.player == 0:
                            if ship_tuple in player_coordinates:
                                break
                        elif self.player == 1:
                            if ship_tuple in computer_coordinates:
                                break
            # Place rest of the ship parts into the grid.
            # If horizontal parts are placed to the right of the last part.
            # If vertical they are placed below the last part.
            else:
                if self.direction == 0:
                    coordx += 1
                    ship_tuple = (coordx, coordy)
                    if self.player == 0:
                        if ship_tuple in player_coordinates:
                            break
                    elif self.player == 1:
                        if ship_tuple in computer_coordinates:
                            break
                if self.direction == 1:
                    coordy += 1
                    ship_tuple = (coordx, coordy)
                    if self.player == 0:
                        if ship_tuple in player_coordinates:
                            break
                    elif self.player == 1:
                        if ship_tuple in computer_coordinates:
                            break
            self.ship_xy.append(ship_tuple)


ship_1 = Ship(1,0)
ship_1.ship_coords()
player_coordinates.append(ship_1.ship_xy)
ship_2 = Ship(2,0)
ship_2.ship_coords()
player_coordinates.append(ship_2.ship_xy)
ship_3 = Ship(3,0)
ship_3.ship_coords()
player_coordinates.append(ship_3.ship_xy)

ship_comp_1 = Ship(1,1)
ship_comp_1.ship_coords()
computer_coordinates.append(ship_comp_1.ship_xy)
ship_comp_2 = Ship(2,1)
ship_comp_2.ship_coords()
computer_coordinates.append(ship_comp_2.ship_xy)
ship_comp_3 = Ship(3,1)
ship_comp_3.ship_coords()
computer_coordinates.append(ship_comp_3.ship_xy)

print(ship_comp_1.size, ship_comp_2.size, ship_comp_3.size)

print(player_coordinates)
print(ship_1.ship_xy)
print(ship_2.ship_xy)
print(ship_3.ship_xy)

print(computer_coordinates)
print(ship_comp_1.ship_xy)
print(ship_comp_2.ship_xy)
print(ship_comp_3.ship_xy)
print("\n")


grid_column = 0
# Function for creating the player and computer grids
# and their Labels
def play_grid():
    global grid_column
    if grid_column == 0:
        frame_1 = LabelFrame(root, text="Player\tShips Left:" + str(player_ships_left), font=("Arial", 18), fg="white", bg="blue", padx=15, pady=15, borderwidth=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(grid_column, weight=1)
        frame_1.grid(row=0, column=grid_column, sticky="news")
        grid = Frame(frame_1)
        grid.grid(sticky="news", column=grid_column, row=7, columnspan=2)
        frame_1.rowconfigure(7, weight=1)
        frame_1.columnconfigure(grid_column, weight=1)
    else:
        frame_2 = LabelFrame(root, text="Computer\tShips Left:"  + str(player_ships_left), font=("Arial", 18), fg="white", bg="green", padx=15, pady=15, borderwidth=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(grid_column, weight=1)
        frame_2.grid(row=0, column=grid_column, sticky="news")
        grid = Frame(frame_2)
        grid.grid(sticky="news", column=grid_column, row=7, columnspan=2)
        frame_2.rowconfigure(7, weight=1)
        frame_2.columnconfigure(grid_column, weight=1)
    
    # Loops to create 10x10 sized grids
    for x in range(0,10):
        for y in range(10):
            # If creating the player grid the buttons
            # created are Clickable
            if grid_column == 0:
                btn = Button(frame_1, borderwidth=5, text=(str(y)+","+str(x)), command=partial(gridClick,x,y))
                #print(btn)
                btn.grid(column=x, row=y, sticky="news")
                btn.config(command=lambda button=btn, line=x, column=y:gridClick(column, line, button, frame_1))
                # Configuration of the grid frames.
                # Defines how many widgets/buttons are allowed inside the frame
                frame_1.columnconfigure(tuple(range(10)), weight=1)
                frame_1.rowconfigure(tuple(range(10)), weight=1)
            # Computer grids buttons are left with
            # no functionality 
            else:
                btn = Button(frame_2, borderwidth=5, text=(str(x)+","+str(y))) # command=partial(comp_guess, x, y, frame_2))
                computer_buttons.append(btn)
                btn.grid(column=x, row=y, sticky="news")
                btn.config(state=DISABLED)
                # Configuration of the grid frames.
                # Defines how many widgets/buttons are allowed inside the frame
                frame_2.columnconfigure(tuple(range(10)), weight=1)
                frame_2.rowconfigure(tuple(range(10)), weight=1)
    
    grid_column += 1


# Function for button clicks
def gridClick(column, line, button, frame):
    #print("Player X:",column,"Y:", line)
    click_coords = (column, line)
    global player_ships_left
    
    # Loop to check if a part of a ship exists on chosen button coordinate
    # If button is clicked it is disabled and its color changes
    # depending if the click hits a ship or not
    for index in player_coordinates:
        if click_coords in index:
            button.configure(state=DISABLED, bg="red")
            print("Hit")
            # If statements to check if all ship parts of any ship are
            # hit.
            # If all parts are hit the ship Destroyed status changes  to True 
            if click_coords in ship_1.ship_xy:
                ship_1.destroyed = True
                player_ships_left -= 1
                frame.configure(text="Player\tShips Left:" + str(player_ships_left))
                print("Player ship 1 Destroyed: " + str(ship_1.destroyed))
                check_win()
                break
            elif click_coords in ship_2.ship_xy:
                # Increases the ships hits variable by one per hit
                ship_2.hits += 1
                # If hits equal the size of the ship it is "Destroyed"
                if ship_2.hits == ship_2.size:
                    ship_2.destroyed = True
                    player_ships_left -= 1
                    frame.configure(text="Player\tShips Left:" + str(player_ships_left))
                    print("Player ship 2 Destroyed: " + str(ship_2.destroyed))
                    check_win()
                break
            elif click_coords in ship_3.ship_xy:
                ship_3.hits += 1
                if ship_3.hits == ship_3.size:
                    ship_3.destroyed = True
                    player_ships_left -= 1
                    frame.configure(text="Player\tShips Left:" + str(player_ships_left))
                    print("Player ship 3 Destroyed: " + str(ship_3.destroyed))
                    check_win()
                break
        else:
            # With a missed "shot" the button is greyed out and disabled
            button.configure(state=DISABLED, bg="gray")
    
    comp_guess()

# TODO: Try to find out how to access a button that is next to the one hit last round
# if the ship is bigger than one coordinate/button and see if it has a ship part.
def comp_guess():
    global computer_coordinates
    global computer_buttons
    global computer_ships_left
    global ship_2_hit
    global ship_3_hit
    global last_coord
    row = 0
    column = 0

    while True:
        
        rand_button = random.choice(computer_buttons)
        row = rand_button.grid_info()['row']
        column = rand_button.grid_info()['column']
        coord_guess = (column,row)
        #print(rand_button.grid_info())

        if coord_guess in guessed_list:
            continue
        else:
            guessed_list.append(coord_guess)
            break

    print("Computer X:",column,"Y:", row)
    check_coord = coord_guess in (item for sublist in computer_coordinates for item in sublist)

    if check_coord == True:
        rand_button.configure(state=DISABLED, bg="red")
        
        if coord_guess in ship_comp_1.ship_xy:
            ship_comp_1.destroyed = True
            computer_ships_left -= 1
            #frame_2.configure(text=frame_2.configure(text="Computer\tShips Left:" + str(computer_ships_left)))
            print("Computer ship 1 Destroyed: " + str(ship_comp_1.destroyed))
            check_win()
        elif coord_guess in ship_comp_2.ship_xy:
            # Increases the ships hits variable by one per hit
            ship_comp_2.hits += 1
            ship_2_hit = True
            last_coord.append(coord_guess)
            # If hits equal the size of the ship it is "Destroyed"
            if ship_comp_2.hits == ship_comp_2.size:
                ship_comp_2.destroyed = True
                computer_ships_left -= 1
                #frame_2.configure(text=frame_2.configure(text="Computer\tShips Left:" + str(computer_ships_left)))
                print("Computer ship 2 Destroyed: " + str(ship_comp_2.destroyed))
                check_win()
        elif coord_guess in ship_comp_3.ship_xy:
            ship_comp_3.hits += 1
            ship_3_hit = True
            last_coord.append(coord_guess)
            if ship_comp_3.hits == ship_comp_3.size:
                ship_comp_3.destroyed = True
                computer_ships_left -= 1
                #frame_2.configure(text=frame_2.configure(text="Computer\tShips Left:" + str(computer_ships_left)))
                print("Computer ship 3 Destroyed: " + str(ship_comp_3.destroyed))
                check_win()
    else:
        rand_button.configure(state=DISABLED, bg="gray")
    return


# For checkin if either side has won and for showing a message.
# TODO: Later make this function to ask if the player wants a new game.
# If yes, restart the game. If not, quit the game.
def check_win():
    if computer_ships_left == 0:
        tkinter.messagebox.showinfo("LOSE!", "COMPUTER WON!")
    elif player_ships_left == 0:
        tkinter.messagebox.showinfo("WIN!", "YOU WON!")
    else:
        return
            
player_grid = play_grid()
computer_grid = play_grid()

root.mainloop()