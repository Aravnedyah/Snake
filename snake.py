from cmath import rect
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
        
#function for displaying score        
def score(current_score):
    value = font.render("Your Score: " + str(current_score), True, yellow)
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

#simplified game ticks with function
def next_tick():
    pg.display.update()

#function to update speed 
def update_speed(speed):
    return speed+1

def menu():
    menu_options = {
        pg.K_SPACE : 1,
        pg.K_v     : 2,
    }
    start = False
    while not start:

        dis.fill(white)
        message('Press SPACE To Start',blue)
        next_tick()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    start=True
                    game_loop(1)
            if event.type == pg.QUIT:
                pg.quit()
                quit()



#function for whole game
def game_loop(players):

    #initiate variables

    #set start point
    x1=dis_width/2
    y1=dis_height/2

    x1_change=0 
    y1_change=0
      
    snake_list=[]
    snake_length=1
    #beginning speed
    snake_speed=10
    dif_interval=2

    game_over=False
    game_close=False

    #keybind dictionary
    move_dict = {
             pg.K_LEFT : [-10, 0],
             pg.K_RIGHT: [ 10, 0],
             pg.K_UP   : [ 0,-10],
             pg.K_DOWN : [ 0, 10],
             }
    #future player 2 
    move_dict2= {
             pg.K_a    : [-10, 0],
             pg.K_d    : [ 10, 0],
             pg.K_w    : [ 0,-10],
             pg.K_s    : [ 0, 10]
             }

    #set x and y for first food piece
    foodx = random_spot(dis_width)
    foody = random_spot(dis_height)


    #loop containing game
    while not game_over:

        #if game over, game close will become false and trigger ending selection
        while game_close:
            dis.fill(white)
            message("You lost! Press Q-Quit or C-Play Again",red)
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
            #actions
            if event.type==pg.QUIT:
                game_over=True
            if event.type==pg.KEYDOWN:
                movement=move_dict.get(event.key) 
                x1_change=movement[0]  
                y1_change=movement[1]  
          
        #movement
        x1+=x1_change
        y1+=y1_change

        #detect out of bounds 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        dis.fill(black)

        #create food piece on screen
        pg.draw.rect(dis, blue, [foodx, foody, 10, 10])

        #create snake head position x and y
        snake_head=[]
        snake_head.append(x1)
        snake_head.append(y1)

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
            snake_speed = update_speed(snake_speed)

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

#call game function to begin
menu()

