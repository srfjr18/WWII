from random import randint
import sys, pygame

screen =  pygame.display.set_mode((640,480))

if __name__ == "__main__":
    sys.exit()

class Gun_Types(object):
    def __init__(self):
        self.mainx = 295
        self.mainy = 215
        self.shotgun = False
        self.flame = False
        
    def getrand_gun_or_blit(self, random_gun=None, angle=None, mainx=295, mainy=215):
        #this has to be number of guns
        if random_gun == None:
            random_gun = randint(1,20)
            self.rand_num = random_gun
        if random_gun == 1:
            return self.stg(angle, mainx, mainy)
        elif random_gun == 2:
            return self.m_one_a_one(angle, mainx, mainy)
        elif random_gun == 3:
            return self.fg_forty_two(angle, mainx, mainy)
        elif random_gun == 4:
            return self.gewehr_forty_three(angle, mainx, mainy)
        elif random_gun == 5:
            return self.m_one_garand(angle, mainx, mainy)
        elif random_gun == 6:
            return self.mp40(angle, mainx, mainy)
        elif random_gun == 7:
            return self.thompson(angle, mainx, mainy)
        elif random_gun == 8:
            return self.ppsh(angle, mainx, mainy)
        elif random_gun == 9:
            return self.m_three(angle, mainx, mainy)
        elif random_gun == 10:
            return self.owen(angle, mainx, mainy)
        elif random_gun == 11:
            return self.m_nineteen_nineteen(angle, mainx, mainy)
        elif random_gun == 12:
            return self.bar(angle, mainx, mainy)
        elif random_gun == 13:
            return self.type_ninety_nine(angle, mainx, mainy)
        elif random_gun == 14:
            return self.svt_forty(angle, mainx, mainy)
        elif random_gun == 15:
            return self.mosin_nagant(angle, mainx, mainy)
        elif random_gun == 16:
            return self.ariaska(angle, mainx, mainy)
        elif random_gun == 17:
            return self.springfield(angle, mainx, mainy)
        elif random_gun == 18:
            return self.double_barrel(angle, mainx, mainy)
        elif random_gun == 19:
            return self.m1987(angle, mainx, mainy)
        elif random_gun == 20:
            return self.thrower(angle, mainx, mainy)
            
    #ASSAULT RIFLES
    def stg(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (54, 0, 0), (70, 28, 11, 20))
            pygame.draw.rect(bg, (54, 63, 57), (72, 3, 5, 22))
            pygame.draw.rect(bg, (54, 63, 57), (68, 14, 14, 20))
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (54, 0, 0), (70, 28, 11, 20)), (None, (54, 63, 57), (72, 3, 5, 22)), (None, (54, 63, 57), (68, 14, 14, 20))] #list of rect stuff
        self.shotgun = False
        return 10, "full-auto", 15, 30, 150, 13
    def m_one_a_one(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 0, 0), (68, 32, 0, 14))
            pygame.draw.rect(bg, (0, 0, 0), (81, 33, 0, 14))
            pygame.draw.rect(bg, (0, 0, 0), (67, 48, 15, 0))
            pygame.draw.rect(bg, (0, 0, 0), (70, 2, 6, 22))
            pygame.draw.rect(bg, (41, 20, 0), (65, 15, 18, 21))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 0, 0), (68, 32, 0, 14)), (None, (0, 0, 0), (81, 33, 0, 14)), (None, (0, 0, 0), (67, 48, 15, 0)), (None, (0, 0, 0), (70, 2, 6, 22)), (None, (41, 20, 0), (65, 15, 18, 21))]
        self.shotgun = False
        return 5, "semi-auto", 10, 15, 160, 6
    def fg_forty_two(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (80, 44, 27), (70, 36, 11, 11))
            pygame.draw.rect(bg, (80, 44, 27), (71, 15, 10, 9))
            pygame.draw.rect(bg, (2, 3, 2), (71, 23, 10, 13))
            pygame.draw.rect(bg, (2, 3, 2), (72, 6, 8, 10))
            pygame.draw.rect(bg, (2, 3, 2), (75, 1, 1, 12))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (80, 44, 27), (70, 36, 11, 11)), (None, (80, 44, 27), (71, 15, 10, 9)), (None, (2, 3, 2), (71, 23, 10, 13)), (None, (2, 3, 2), (72, 6, 8, 10)), (None, (2, 3, 2), (75, 1, 1, 12))]
        self.shotgun = False
        return 5, "full-auto", 25, 20, 160, 10
    def gewehr_forty_three(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (97, 24, 0), (70, 33, 10, 15))
            pygame.draw.rect(bg, (97, 24, 0), (70, 16, 10, 16))
            pygame.draw.rect(bg, (10, 5, 0), (72, 1, 4, 14))
            pygame.draw.rect(bg, (10, 5, 0), (74, 22, 3, 19))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (97, 24, 0), (70, 33, 10, 15)), (None, (97, 24, 0), (70, 16, 10, 16)), (None, (10, 5, 0), (72, 1, 4, 14)), (None, (10, 5, 0), (74, 22, 3, 19))]
        self.shotgun = False
        return 8, "semi-auto", 12, 10, 110, 6
    def m_one_garand(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (60, 23, 0), (70, 14, 8, 31))
            pygame.draw.rect(bg, (11, 11, 0), (71, 2, 5, 14))
            pygame.draw.rect(bg, (11, 11, 0), (71, 25, 6, 7))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (60, 23, 0), (70, 14, 8, 31)), (None, (11, 11, 0), (71, 2, 5, 14)), (None, (11, 11, 0), (71, 25, 6, 7))]
        self.shotgun = False
        return 10, "semi-auto", 7, 8, 180, 6
        # frames between shots (1 == 0), full/semi-auto, shots to kill, mag size, reload time, recoil
        # shots to kill is more like number of frames bullet collides with enemy
        
    #SMGS
    def mp40(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 0, 0), (70, 12, 9, 21))
            pygame.draw.rect(bg, (0, 0, 0), (73, 1, 3, 18))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 0, 0), (70, 12, 9, 21)), (None, (0, 0, 0), (73, 1, 3, 18))]
        self.shotgun = False
        return 4, "full-auto", 30, 25, 125, 14
    def thompson(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (1, 1, 1), (64, 17, 18, 9))
            pygame.draw.rect(bg, (34, 28, 26), (69, 4, 9, 33))
            pygame.draw.rect(bg, (86, 26, 20), (66, 29, 15, 20))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (1, 1, 1), (64, 17, 18, 9)), (None, (34, 28, 26), (69, 4, 9, 33)), (None, (86, 26, 20), (66, 29, 15, 20))]
        self.shotgun = False
        return 2, "full-auto", 30, 40, 75, 9
    def ppsh(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 0, 0), (69, 2, 0, 21))
            pygame.draw.rect(bg, (0, 0, 0), (78, 3, 0, 21))
            pygame.draw.rect(bg, (0, 0, 0), (67, 2, 12, 1))
            pygame.draw.rect(bg, (26, 29, 29), (61, 17, 25, 8))
            pygame.draw.rect(bg, (131, 70, 29), (67, 25, 13, 24))
            pygame.draw.rect(bg, (0, 0, 0), (69, 10, 10, 1))
            pygame.draw.rect(bg, (0, 0, 0), (73, 1, 1, 15))
            pygame.draw.rect(bg, (0, 2, 1), (67, 17, 12, 11))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 0, 0), (69, 2, 0, 21)), (None, (0, 0, 0), (78, 3, 0, 21)), (None, (0, 0, 0), (67, 2, 12, 1)), (None, (26, 29, 29), (61, 17, 25, 8)), (None, (131, 70, 29), (67, 25, 13, 24)), (None, (0, 0, 0), (69, 10, 10, 1)), (None, (0, 0, 0), (73, 1, 1, 15)), (None, (0, 2, 1), (67, 17, 12, 11))]
        self.shotgun = False
        return 1, "full-auto", 40, 71, 150, 8
    def m_three(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 0, 0), (74, 0, 0, 24))
            pygame.draw.rect(bg, (48, 37, 38), (63, 19, 22, 6))
            pygame.draw.rect(bg, (4, 1, 4), (70, 11, 9, 23))
            pygame.draw.rect(bg, (4, 1, 4), (74, 34, 1, 7))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 0, 0), (74, 0, 0, 24)), (None, (48, 37, 38), (63, 19, 22, 6)), (None, (4, 1, 4), (70, 11, 9, 23)), (None, (4, 1, 4), (74, 34, 1, 7))]
        self.shotgun = False
        return 8, "full-auto", 13, 30, 100, 10
    def owen(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 0, 0), (72, 0, 5, 23))
            pygame.draw.rect(bg, (0, 0, 0), (75, 20, 16, 3))
            pygame.draw.rect(bg, (0, 0, 0), (69, 16, 11, 20))
            pygame.draw.rect(bg, (79, 35, 0), (68, 30, 14, 16))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 0, 0), (72, 0, 5, 23)), (None, (0, 0, 0), (75, 20, 16, 3)), (None, (0, 0, 0), (69, 16, 11, 20)), (None, (79, 35, 0), (68, 30, 14, 16))]
        self.shotgun = False
        return 5, "full-auto", 20, 33, 150, 10
        
    #LMGS
    def m_nineteen_nineteen(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 0, 0), (71, 0, 6, 18))
            pygame.draw.rect(bg, (0, 0, 0), (64, 17, 20, 17))
            pygame.draw.rect(bg, (0, 0, 0), (68, 31, 13, 15))
            pygame.draw.rect(bg, (0, 45, 0), (90, 19, 9, 12))
            pygame.draw.rect(bg, (186, 137, 0), (79, 20, 14, 8))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 0, 0), (71, 0, 6, 18)), (None, (0, 0, 0), (64, 17, 20, 17)), (None, (0, 0, 0), (68, 31, 13, 15)), (None, (0, 45, 0), (90, 19, 9, 12)), (None, (186, 137, 0), (79, 20, 14, 8))]
        self.shotgun = False
        return 9, "full-auto", 16, 250, 1000, 11
    def bar(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (91, 25, 0), (72, 0, 7, 32))
            pygame.draw.rect(bg, (60, 60, 60), (70, 22, 10, 17))
            pygame.draw.rect(bg, (91, 25, 0), (69, 32, 12, 15))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (91, 25, 0), (72, 0, 7, 32)), (None, (60, 60, 60), (70, 22, 10, 17)), (None, (91, 25, 0), (69, 32, 12, 15))]
        self.shotgun = False
        return 7, "full-auto", 16, 20, 200, 9
    def type_ninety_nine(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 0, 0), (71, 0, 5, 42))
            pygame.draw.rect(bg, (0, 0, 0), (61, 8, 24, 1))
            pygame.draw.rect(bg, (0, 0, 0), (75, 16, 18, 10))
            pygame.draw.rect(bg, (60, 0, 0), (68, 32, 10, 16))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 0, 0), (71, 0, 5, 42)), (None, (0, 0, 0), (61, 8, 24, 1)), (None, (0, 0, 0), (75, 16, 18, 10)), (None, (60, 0, 0), (68, 32, 10, 16))]
        self.shotgun = False
        return 6, "full-auto", 12, 30, 180, 10
    
    #SNIPERS/ BOLT ACTION RIFLES
    def svt_forty(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 0, 0), (71, 0, 0, 24))
            pygame.draw.rect(bg, (141, 68, 0), (62, 19, 19, 22))
            pygame.draw.rect(bg, (141, 68, 0), (65, 12, 12, 14))
            pygame.draw.rect(bg, (141, 68, 0), (67, 30, 7, 17))
            pygame.draw.rect(bg, (3, 3, 0), (67, 17, 9, 22))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 0, 0), (71, 0, 0, 24)), (None, (141, 68, 0), (62, 19, 19, 22)), (None, (141, 68, 0), (65, 12, 12, 14)), (None, (141, 68, 0), (67, 30, 7, 17)), (None, (3, 3, 0), (67, 17, 9, 22))]
        self.shotgun = False
        return 145, "semi-auto", 1, 10, 140, 0
    def mosin_nagant(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (77, 28, 0), (70, 12, 9, 37))
            pygame.draw.rect(bg, (77, 28, 0), (72, 1, 4, 12))
            pygame.draw.rect(bg, (8, 1, 0), (68, 19, 12, 16))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (77, 28, 0), (70, 12, 9, 37)), (None, (77, 28, 0), (72, 1, 4, 12)), (None, (8, 1, 0), (68, 19, 12, 16))]
        self.shotgun = False
        return 1, "semi-auto", 1, 1, 130, 0
    def ariaska(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (83, 20, 0), (71, 19, 8, 30))
            pygame.draw.rect(bg, (83, 20, 0), (75, 1, 1, 17))
            pygame.draw.rect(bg, (83, 20, 0), (72, 8, 7, 12))
            pygame.draw.rect(bg, (13, 20, 0), (69, 16, 13, 12))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (83, 20, 0), (71, 19, 8, 30)), (None, (83, 20, 0), (75, 1, 1, 17)), (None, (83, 20, 0), (72, 8, 7, 12)), (None, (13, 20, 0), (69, 16, 13, 12))]
        self.shotgun = False
        return 130, "semi-auto", 1, 5, 200, 0
    def springfield(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (86, 0, 0), (68, 15, 11, 33))
            pygame.draw.rect(bg, (86, 0, 0), (73, 1, 1, 15))
            pygame.draw.rect(bg, (0, 0, 0), (65, 24, 18, 10))
            backup_bg = bg
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (86, 0, 0), (68, 15, 11, 33)), (None, (86, 0, 0), (73, 1, 1, 15)), (None, (0, 0, 0), (65, 24, 18, 10))]
        self.shotgun = False
        return 150, "semi-auto", 1, 5, 120, 0 
        
        
    #shotguns
    def double_barrel(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (78, 71, 69), (73, 3, 6, 27))
            pygame.draw.rect(bg, (160, 56, 27), (71, 27, 9, 21))
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (78, 71, 69), (73, 3, 6, 27)), (None, (160, 56, 27), (71, 27, 9, 21))]
        self.shotgun = True
        return 1, "semi-auto", 20, 2, 100, 0     
    def m1987(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (93, 95, 93), (72, 0, 5, 35))
            pygame.draw.rect(bg, (145, 58, 1), (70, 17, 9, 32))
            pygame.draw.rect(bg, (0, 1, 1), (72, 16, 6, 18))
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (93, 95, 93), (72, 0, 5, 35)), (None, (145, 58, 1), (70, 17, 9, 32)), (None, (0, 1, 1), (72, 16, 6, 18))]
        self.shotgun = True
        return 130, "semi-auto", 9, 6, 200, 0   
    def thrower(self, angle=None, mainx=295, mainy=215):
        if angle != None:
            bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            pygame.draw.rect(bg, (0, 28, 0), (78, 26, 27, 27))
            pygame.draw.rect(bg, (0, 28, 0), (68, 34, 18, 8))
            pygame.draw.rect(bg, (0, 28, 0), (67, 5, 7, 36))
            pygame.draw.rect(bg, (240, 1, 0), (66, 3, 8, 10))
            bg = pygame.transform.rotate(bg, angle)
            screen.blit(bg, (mainx - 25, mainy - 25))
            return [(None, (0, 28, 0), (78, 26, 27, 27)), (None, (0, 28, 0), (68, 34, 18, 8)), (None, (0, 28, 0), (67, 5, 7, 36)), (None, (240, 1, 0), (66, 3, 8, 10))]
        self.shotgun = True
        self.flame = True
        return 6, "full-auto", 30.1, 200, 201, 8 #the 30.1 makes this exclusive and easier to identify in the online mode
          
    
