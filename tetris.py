import pygame, sys, random
from copy import deepcopy

pygame.init()

cell_size = 40
cell_width, cell_height = 10, 20

screen = pygame.display.set_mode((cell_size * cell_width, cell_size * cell_height)) # 20x10 cells for tetris
clock = pygame.time.Clock()

#   pygame.rect(x, y, w, h)
grid = [pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size) for x in range(cell_width) for y in range(cell_height)]


#   timer
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 1)   #   amount of changes in mil-seconds for screen update, which can be game speed


blocks_in_xyvalue = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, 0)]]

#(x, y, w, h), where as w h dont matter since its position values regarding where the shape is going to be generated
# y + 1 since some shape will be drew over y by 1; prevent over indexing.
blocks_rect_position = [[pygame.Rect(x + cell_width//2, y + 1, 0, 0) for x, y in position] for position in blocks_in_xyvalue]

#   below grabs tetris shape coordinates from blocks_in_xy_values, and draw them    (tetris points at which block to draw)
#   -2 is so they can been seen as seperate blocks

#   and 0, 0 for x y because again, those value will be updated to the pointer ( tetris ) in the while loop.
single_shape_x_y_value = pygame.Rect(0, 0, cell_size - 2, cell_size - 2)

#   deepcopy to check for border
tetris = deepcopy(blocks_rect_position[random.randint(0,6)])

def check_borders():
    #   - 1 for cell width because 0 is counted, result in over indexxing
    if tetris[blocks].x < 0 or tetris[blocks].x > cell_width - 1:
        return False
    elif tetris[blocks].y > cell_height - 1 or field[tetris[blocks].y][tetris[blocks].x]:
        return False
    return True

#   free fall value
#   basically using the frames / speed of while loop to declare when y - 1

#   counter for reset/growth rate/limit
anim_count, anim_speed, anim_limit = 0, 60, 2000

#   field to mark the position of fallen figures
field = [[0 for width in range(cell_width)] for height in range(cell_height)]

class MAIN():
    def __init__(self):
        #   insert class in here if need
        pass


main_game = MAIN()

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == SCREEN_UPDATE:
            #main_game.update()
            pass
        
    #   this copies the = object attributes, and we use this to avoid illegal movements
    #   such as outside the border, glitches in position and etc.
        tetris_clone = deepcopy(tetris)
        
    #   controll for left and right
        left_or_right = 0
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_or_right = -1
            elif event.key == pygame.K_RIGHT:
                left_or_right = 1
            elif event.key == pygame.K_UP:
                rotation = True
                
            #   reducing limit = less rate for fall, thus more fall speed
            if event.key == pygame.K_DOWN:
                anim_limit = 200
            else:
                anim_limit = 2000
            if event.key == pygame.K_SPACE:
                anim_limit = 0
    
    #   movement for x after controll
    for blocks in range(4):
        tetris[blocks].x += left_or_right
        if not check_borders():
            tetris = deepcopy(tetris_clone)
            break
    
    #   free fall for y with no controll
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        tetris_clone = deepcopy(tetris)
             
        for blocks in range(4):
            tetris[blocks].y += 1
            if not check_borders():
                tetris = deepcopy(blocks_rect_position[random.randint(0,6)])
               
                #   reset the limit when the block touch, so next block works as fine
                anim_limit = 2000
                break 
    

    screen.fill((0, 0, 0))
    [pygame.draw.rect(screen, (50, 50, 50), i_amount_of_rect, 1) for i_amount_of_rect in grid]

    #   draw the 4 block, or the tetris block with its position for whatever tetris[block] points to
    for drawing_the_block in range(4):
        single_shape_x_y_value.x = tetris[drawing_the_block].x * cell_size
        single_shape_x_y_value.y = tetris[drawing_the_block].y * cell_size
        pygame.draw.rect(screen, (255, 255, 255), single_shape_x_y_value)
    
    
    pygame.display.update()
            
            
    clock.tick(60)
    
