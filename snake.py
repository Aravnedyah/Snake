from cmath import rect
from operator import truediv
import random
import pygame as pg

#begin
pg.init()

#declare colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

#define app size
dis_width = 800
dis_height = 600

#initiate display
dis=pg.display.set_mode((dis_width,dis_height))
pg.display.set_caption('Snake Game By Hayden') 

#set font type and size
font=pg.font.SysFont('helvetica',25)


#function for snake length
def snake(snake_list):
    for x in snake_list:
        pg.draw.rect(dis, white, [x[0], x[1], 10, 10])

#function for snake length
def snake2(snake_list,snake2_list):
    for x in snake_list:
        pg.draw.rect(dis, white, [x[0], x[1], 10, 10])
    for x in snake2_list:
        pg.draw.rect(dis, green, [x[0], x[1], 10, 10])

#function that returns movement updates based on key press
def move(press, dict):
        movement=dict.get(press)
        return [movement[0], movement[1]]

#function that detects collision with border   
def collision(list,head):
            for x in list[:-1]:
                if x==head:
                    return True
            return False  

#function detects out of bounds and returns bool based on resutl
def out_bounds(x,y,w,h):
            if x >= w or x < 0 or y >= h or y < 0:
                return True
        
#function for displaying score        
def score(current_score):
    value = font.render("Your Score: " + str(current_score), True, yellow)
    dis.blit(value, [0, 0])

#function for displaying score two player       
def score2(current_score1,current_score2):
    value = font.render("White: " + str(current_score1) +" Green: "+str(current_score2), True, yellow)
    dis.blit(value, [0, 0])


#initiate clock 
clock = pg.time.Clock()

#function for pop up message. Text within centered rectangle
def message(msg,color):
        mesg = font.render(msg, True, color)
        coords = mesg.get_rect()
        coords.center = pg.Rect(dis_width/2,dis_height/2,10,10).center
        dis.blit(mesg, coords)
        
#generate random position
def random_spot(size):
    return round(random.randrange(0, size - 30) / 10.0) *10

#simplified game ticks with function(writeless)
def next_tick():
    pg.display.update()

#menu page
def menu():
    
    start = False
    while not start:

        dis.fill(white)
        message('Press "1" To Start. Press "2" For 2 Player',blue)
        next_tick()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_1:
                    start=True
                    game_loop()
                elif event.key==pg.K_2:
                    start=True
                    game2_loop()
            if event.type == pg.QUIT:
                pg.quit()
                quit()



#function for whole game
def game_loop():
    #initiate variable
    #set start point    (x1, y1 player one | x2, y2 player two)
    x1=dis_width/2
    y1=dis_height/2

    x1_change=0 
    y1_change=0
    last_move=[]
    
    
    snake_list=[]
    snake_length=1
    #beginning speed
    snake_speed=10
    dif_interval=2

    game_over=False
    game_close=False

    #keybind dictionary
    move_dict = {
             pg.K_LEFT : (-10, 0),
             pg.K_RIGHT: ( 10, 0),
             pg.K_UP   : ( 0,-10),
             pg.K_DOWN : ( 0, 10),
             }

    #set x and y for first food piece
    foodx = random_spot(dis_width)
    foody = random_spot(dis_height)


    #loop containing game
    while not game_over:

        #if game over, game close will become false and trigger ending selection
        while game_close:
            dis.fill(white)
            message("You lost! Press Q-Quit or C-Back to Menu",red)
            next_tick()

            #keystrokes
            for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_q:
                            game_over = True
                            game_close = False
                        elif event.key == pg.K_c:
                            menu()
                    if event.type == pg.QUIT:
                        game_over=True
                        game_close=False

        #key strokes
        for event in pg.event.get():
            if event.type==pg.QUIT:
                game_over=True   
            if event.type==pg.KEYDOWN:
                if event.key in move_dict.keys():
                    m = move(event.key, move_dict)
                    if m!=last_move: #so you cant step on yourself
                        x1_change=m[0]  
                        y1_change=m[1]  
                        last_move=[-m[0],-m[1]]
          
        #movement
        x1+=x1_change
        y1+=y1_change

        #detect out of bounds 
        game_close = out_bounds(x1,y1,dis_width,dis_height)

        dis.fill(black)

        #create food piece on screen
        pg.draw.rect(dis, blue, [foodx, foody, 10, 10])

        #create snake head position x and y
        snake_head=[x1,y1]

        #append to snake
        snake_list.append(snake_head)

        #keep snake length accurate
        if len(snake_list) > snake_length :
            del snake_list[0]

        #collision detection
        for x in snake_list[:-1]:
            if x==snake_head:
                game_close=True

        #call snake function with snake size parameter
        snake(snake_list)

        #set score as -1 because snake it 1 greater than beginning score
        score(snake_length-1)
       
       
        #!make difficutly setting frequency of speed changes
        if (snake_length-1) == dif_interval:
            dif_interval+=1
            snake_speed+=1

        next_tick()

        #on food colision
        if x1 == foodx and y1 == foody:
            foodx = random_spot(dis_width)
            foody = random_spot(dis_height)

            #grow snake
            snake_length+=1
            
            
        #speed
        clock.tick(snake_speed)  

    #end program    
    pg.quit()
    quit()

#function for vs mode
def game2_loop():
    #initiate variable
    #set start point    (x1, y1 player one | x2, y2 player two)
    x1=dis_width/2
    y1=dis_height/2

    x2=dis_width/2
    y2=dis_height/2

    x1_change=0 
    y1_change=0
    last_move=[]

    x2_change=0 
    y2_change=0
    last2_move=[]
    
    snake_list=[]
    snake_length=1
    #beginning speed
    snake_speed=10
    dif_interval=2

    snake2_list=[]
    snake2_length=1
    #beginning speed
    snake2_speed=10    
 

    game2_over=False
    game2_close=False
    

    #keybind dictionary
    move_dict = {
            pg.K_LEFT : (-10, 0),
            pg.K_RIGHT: ( 10, 0),
            pg.K_UP   : ( 0,-10),
            pg.K_DOWN : ( 0, 10),
             }
    #player2
    move2_dict= {
             pg.K_a    : (-10, 0),
             pg.K_d    : ( 10, 0),
             pg.K_w    : ( 0,-10),
             pg.K_s    : ( 0, 10)
             }

    #set x and y for first food piece
    foodx = random_spot(dis_width)
    foody = random_spot(dis_height)


    #loop containing game
    while not game2_over:
    
        #create if statement for player 1 or 2 win
        while game2_close:
            dis.fill(white)

            #determine winner
            if snake_length > snake2_length:  
                message("White Wins! Press 'c' To Play again",red)
            elif snake_length < snake2_length:
                message("Green Wins! Press 'c' To Play again",red)
            else:
                message("Tie! Press 'c' Play again",red)
            next_tick()

            #keystrokes options
            for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_q:
                            game2_over = True
                            game2_close = False
                        elif event.key == pg.K_c:
                            menu()
                    if event.type == pg.QUIT:
                        game2_over=True
                        game2_close=False

        #key strokes
        for event in pg.event.get():
            #actions        
            if event.type==pg.QUIT:
                game2_over=True
            if event.type==pg.KEYDOWN:
                if event.key in move_dict.keys():
                        m = move(event.key, move_dict)
                        if m!=last_move: #so you cant step on yourself
                            x1_change=m[0]  
                            y1_change=m[1]  
                            last_move=[-m[0],-m[1]]
                if event.key in move2_dict.keys():    
                    m2 = move(event.key, move2_dict)
                    if m2!=last2_move: #so you cant step on yourself
                        x2_change=m2[0]  
                        y2_change=m2[1]  
                        last2_move=[-m2[0],-m2[1]]  
            
        #movement p1
        x1+=x1_change
        y1+=y1_change

        #movement p2
        x2+=x2_change
        y2+=y2_change

        dis.fill(black)

        #create food piece on screen
        pg.draw.rect(dis, blue, [foodx, foody, 10, 10])

        #create snake head position x and y p1
        snake_head=[x1,y1]
        #create snake head position x and y p2
        snake2_head=[x2,y2]
      
        #append to snake p1
        snake_list.append(snake_head)
         #append to snake p2
        snake2_list.append(snake2_head)

        #keep snake length accurate p1
        if len(snake_list) > snake_length :
            del snake_list[0]
         #keep snake length accurate p2
        if len(snake2_list) > snake2_length :
            del snake2_list[0]

        #collision detection p1
        game2_close=collision(snake_list,snake_head)
        #collision detection p2
        game2_close=collision(snake2_list,snake2_head)

        #out of bounds
        if out_bounds(x1,y1,dis_width,dis_height) or out_bounds(x2,y2,dis_width,dis_height):
            game2_close=True

        #update snake sizes
        snake2(snake_list,snake2_list)
        #set score as -1 because snake it 1 greater than beginning score | two player
        score2(snake_length-1,snake2_length-1)
       
        #speed up  
        if (snake_length-1) == dif_interval or (snake2_length-1)==dif_interval:
            #future functionality for difficulty
            dif_interval+=1
            snake_speed+=1
            snake2_speed+=1

        next_tick()

        #on food colision p1
        if x1 == foodx and y1 == foody:
            foodx = random_spot(dis_width)
            foody = random_spot(dis_height)

            #grow snake
            snake_length+=1

         #on food colision p2
        if x2 == foodx and y2 == foody:
            foodx = random_spot(dis_width)
            foody = random_spot(dis_height)

            #grow snake
            snake2_length+=1
            
        #speed
        clock.tick(snake_speed)  

    #end program    
    pg.quit()
    quit()

#call game function to begin
menu()

