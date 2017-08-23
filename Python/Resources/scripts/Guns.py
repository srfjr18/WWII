from random import randint
import sys

if __name__ == "__main__":
    sys.exit()

class Gun_Types(object):
    def getrand_gun(self):
        #this has to be number of guns
        random_gun = randint(1,17)
        if random_gun == 1:
            return self.stg()
        elif random_gun == 2:
            return self.m_one_a_one()
        elif random_gun == 3:
            return self.fg_forty_two()
        elif random_gun == 4:
            return self.gewehr_forty_three()
        elif random_gun == 5:
            return self.m_one_garand()
        elif random_gun == 6:
            return self.mp40()
        elif random_gun == 7:
            return self.thompson()
        elif random_gun == 8:
            return self.ppsh()
        elif random_gun == 9:
            return self.m_three()
        elif random_gun == 10:
            return self.owen()
        elif random_gun == 11:
            return self.m_nineteen_nineteen()
        elif random_gun == 12:
            return self.bar()
        elif random_gun == 13:
            return self.type_ninety_nine()
        elif random_gun == 14:
            return self.svt_forty()
        elif random_gun == 15:
            return self.mosin_nagant()
        elif random_gun == 16:
            return self.ariaska()
        elif random_gun == 17:
            return self.springfield()
            
    #ASSAULT RIFLES
    def stg(self):
        return 10, "full-auto", 15, 30, 150, 13
    def m_one_a_one(self):
        return 5, "semi-auto", 10, 15, 160, 6
    def fg_forty_two(self):
        return 5, "full-auto", 25, 20, 160, 10
    def gewehr_forty_three(self):
        return 8, "semi-auto", 12, 10, 110, 6
    def m_one_garand(self):
        return 10, "semi-auto", 7, 8, 180, 6
        # frames between shots (1 == 0), full/semi-auto, shots to kill, mag size, reload time, recoil
        # shots to kill is more like number of frames bullet collides with enemy
        
    #SMGS
    def mp40(self):
        return 4, "full-auto", 30, 25, 125, 14
    def thompson(self):
        return 2, "full-auto", 30, 40, 75, 9
    def ppsh(self):
        return 1, "full-auto", 45, 71, 150, 8
    def m_three(self):
        return 8, "full-auto", 13, 30, 100, 10
    def owen(self):
        return 5, "full-auto", 20, 33, 150, 10
        
    #LMGS
    def m_nineteen_nineteen(self):
        return 9, "full-auto", 16, 250, 1000, 11
    def bar(self):
        return 7, "full-auto", 16, 20, 200, 9
    def type_ninety_nine(self):
        return 6, "full-auto", 12, 30, 180, 10
    
    #SNIPERS/ BOLT ACTION RIFLES
    def svt_forty(self):
        return 145, "semi-auto", 1, 10, 140, 0
    def mosin_nagant(self):
        return 1, "semi-auto", 1, 1, 130, 0
    def ariaska(self):
        return 130, "semi-auto", 1, 5, 200, 0
    def springfield(self):
        return 150, "semi-auto", 1, 5, 120, 0 
    
