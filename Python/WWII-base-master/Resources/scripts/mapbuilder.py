#!/usr/bin/env python
import pygame, sys, os

def map_builder():
    pygame.init()

    screen =  pygame.display.set_mode((640,480))
    background = pygame.Surface(screen.get_size())
    background.fill((215,240,255))
    background = background.convert()
    clock = pygame.time.Clock()
    FPS = 80

    collision_list = []

    red = list(range(0, 1000))
    green = list(range(0, 1000))
    blue = list(range(0, 1000))
    x = list(range(0, 1000))
    y = list(range(0, 1000))
    width = list(range(0, 1000))
    height = list(range(0, 1000))
    collision = list(range(0, 1000))
    for num in range(1, 1000):
        red[num] = 1
        green[num] = 1
        blue[num] = 1
        x[num] = 1
        y[num] = 1
        width[num] = 1
        height[num] = 1
        collision[num] = True 
    
    scrollscreenx, scrollscreeny = 0, 0


    number_of_images = 0

    font = pygame.font.SysFont(None, 25)
    while True:
        milliseconds = clock.tick(FPS)
        screen.blit(background, (0, 0))
    
        mousepos = pygame.mouse.get_pos()
        mouse_collision = pygame.Rect((mousepos[0], mousepos[1]), (1, 1))
    
        text = font.render(str((mousepos[0] + scrollscreenx, mousepos[1] + scrollscreeny)),1,(0,0,0))
        screen.blit(text, (mousepos[0] + 10, mousepos[1]))
    
        if pygame.key.get_pressed()[pygame.K_UP]:
            y[number_of_images] -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            y[number_of_images] += 1
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            x[number_of_images] -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            x[number_of_images] += 1
    
        if pygame.key.get_pressed()[pygame.K_i]:
            height[number_of_images] -= 1
        if pygame.key.get_pressed()[pygame.K_k]:
            height[number_of_images] += 1
        if pygame.key.get_pressed()[pygame.K_j]:
            width[number_of_images] -= 1
        if pygame.key.get_pressed()[pygame.K_l]:
            width[number_of_images] += 1
    
    
        if pygame.key.get_pressed()[pygame.K_w]:
            scrollscreeny -= 1
        if pygame.key.get_pressed()[pygame.K_s]:
            scrollscreeny += 1
        if pygame.key.get_pressed()[pygame.K_a]:
            scrollscreenx -= 1
        if pygame.key.get_pressed()[pygame.K_d]:
            scrollscreenx += 1
    
        if pygame.key.get_pressed()[pygame.K_r]:
            red[number_of_images] += 1
            if red[number_of_images] > 255:
                red[number_of_images] = 0
        if pygame.key.get_pressed()[pygame.K_g]:
            green[number_of_images] += 1
            if green[number_of_images] > 255:
                green[number_of_images] = 0
        if pygame.key.get_pressed()[pygame.K_b]:
            blue[number_of_images] += 1
            if blue[number_of_images] > 255:
                blue[number_of_images] = 0
            
    
        for images in range(number_of_images):
            pygame.draw.rect(screen, (red[images], green[images], blue[images]), (x[images] - scrollscreenx, y[images] - scrollscreeny, width[images], height[images]))
            pygame.draw.rect(screen, (0, 0, 0), (x[images] - scrollscreenx, y[images] - scrollscreeny, width[images], height[images]), 3)  
    
        pygame.draw.rect(screen, (red[number_of_images], green[number_of_images], blue[number_of_images]), (x[number_of_images] - scrollscreenx, y[number_of_images] - scrollscreeny, width[number_of_images], height[number_of_images]))
    
        pygame.draw.rect(screen, (0, 0, 0), (x[number_of_images] - scrollscreenx, y[number_of_images] - scrollscreeny, width[number_of_images], height[number_of_images]), 3)
    
        for event in pygame.event.get():  
            if event.type == pygame.QUIT: 
                pygame.quit()
                return #sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return #sys.exit()
                elif event.key == pygame.K_RETURN:
                    number_of_images += 1
                    x[number_of_images] = mousepos[0] + scrollscreenx 
                    y[number_of_images] = mousepos[1] + scrollscreeny
                    red[number_of_images] = red[number_of_images - 1]
                    green[number_of_images] = green[number_of_images - 1]
                    blue[number_of_images] = blue[number_of_images - 1]
                elif event.key == pygame.K_c:
                    collision[number_of_images] = False
                elif event.key == pygame.K_BACKSPACE:
                    number_of_images -= 1
                elif event.key == pygame.K_RSHIFT:
            
                    for images in range(number_of_images):
                        collision_list.append(pygame.Rect((x[images], y[images]), (width[images], height[images])))
            
                    with open('maps', 'w+') as maps:
                        for images in range(number_of_images):
                            maps.write("        pygame.draw.rect(screen, ("+str(red[images])+", "+str(green[images])+", "+str(blue[images])+"), ("+str(x[images])+" - self.imagesx, "+str(y[images])+" - self.imagesy, "+str(width[images])+", "+str(height[images])+"))"+"\n")
                            maps.write("        pygame.draw.rect(screen, (0, 0, 0), ("+str(x[images])+" - self.imagesx, "+str(y[images])+" - self.imagesy, "+str(width[images])+", "+str(height[images])+"), 3)"+"\n")

                        maps.write("map_collisions = [")
                        for images in range(number_of_images):
                            if collision[images]:
                                maps.write("pygame.Rect(("+str(x[images])+" - self.imagesx, "+str(y[images])+" - self.imagesy), ("+str(width[images])+", "+str(height[images])+")), ")
                        maps.seek(-2, os.SEEK_END)
                        maps.truncate()
                        maps.write("]")
                        
                        
        pygame.display.set_caption("x: " + str(x[number_of_images]) + " y: " + str(y[number_of_images]) + " width: " + str(width[number_of_images]) + " height: " + str(height[number_of_images]))         
        pygame.display.flip()
        
if __name__ == "__main__":
    map_builder()
