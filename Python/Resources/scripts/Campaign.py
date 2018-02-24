import math, pygame, sys

screen = pygame.display.set_mode((640,480))
class Campaign(object):
    def __init__(self):
        self.font = {"big": pygame.font.SysFont("monospace", 50), "medium": pygame.font.SysFont("monospace", 35), "small": pygame.font.SysFont("monospace", 25), "smallish": pygame.font.SysFont("monospace", 20), "extrasmall": pygame.font.SysFont("monospace", 15)}
    
    def donescreen(self, kills, name):
        pygame.time.delay(300)
        
        words = "YOU COMPLETED "+name+"!"+ " " * (40 - len("YOU COMPLETED "+name+"!"))+"KILLS: "+str(kills)
        
        clock_count = 0
        print_words = ""
        num_chars = 0
        pressed = True
        background = pygame.Surface(screen.get_size())
        background.fill((0,0,0))
        background = background.convert()
        while True:
            screen.blit(background, (0, 0))
            clock_count += 1
            if clock_count % 30 == 0:
                num_chars += 1
                try:
                    print_words = words[:num_chars]
                except:
                    pass
            text = self.font["medium"].render(print_words[:40],1,(255,255,255))
            screen.blit(text, (130, screen.get_size()[1] - 300))
            text = self.font["medium"].render(print_words[40:],1,(255,255,255))
            screen.blit(text, (210, screen.get_size()[1] - 240))
            
            if pygame.mouse.get_pressed()[0] and not pressed:
                pygame.time.delay(300)
                return
            elif not pygame.mouse.get_pressed()[0]:
                pressed = False
            
            pygame.display.flip()
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()



        
    def text(self, words):
        pygame.time.delay(300)
        bg = pygame.Surface((screen.get_size()[0],100), pygame.SRCALPHA)
        bg.fill((211,211,211,40))
        clock_count = 0
        print_words = ""
        num_chars = 0
        pressed = True
        screen.blit(bg, (0, screen.get_size()[1] - 100))
        pygame.draw.rect(screen, (0,0,0), (0, screen.get_size()[1] - 100, screen.get_size()[0], 100), 3)
        while True:
            screen.blit(bg, (0, screen.get_size()[1] - 100))
            pygame.draw.rect(screen, (0,0,0), (0, screen.get_size()[1] - 100, screen.get_size()[0], 100), 10)
            clock_count += 1
            if clock_count % 50 == 0:
                num_chars += 1
                try:
                    print_words = words[:num_chars]
                except:
                    pass
            text = self.font["small"].render(print_words,1,(0,0,0))
            screen.blit(text, (20, screen.get_size()[1] - 80))
            
            if pygame.mouse.get_pressed()[0] and not pressed:
                pygame.time.delay(300)
                return
            elif not pygame.mouse.get_pressed()[0]:
                pressed = False
            
            pygame.display.flip()
            for event in pygame.event.get():  
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

