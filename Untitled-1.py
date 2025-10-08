class Ampel(object):
    def __init__(self):
        self.lampeRot = False
        self.lampeGelb = False
        self.lampeGruen = False

    def setLampen(self, startwertLampeRot, startwertLampeGelb, startwertLampeGruen):
        self.lampeRot = startwertLampeRot
        self.lampeGelb = startwertLampeGelb
        self.lampeGruen = startwertLampeGruen

    def schalten(self):
        if (self.lampeRot, self.lampeGelb, self.lampeGruen) == (True, False, False):
            self.lampeGelb = True
        elif (self.lampeRot, self.lampeGelb, self.lampeGruen) == (True, True, False):
            self.lampeRot = False
            self.lampeGelb = False
            self.lampeGruen = True
        elif (self.lampeRot, self.lampeGelb, self.lampeGruen) == (False, False, True):
            self.lampeGruen = False
            self.lampeGelb = True
        elif (self.lampeRot, self.lampeGelb, self.lampeGruen) == (False, True, False):
            self.lampeGelb = False
            self.lampeRot = True

            
Ampel1 = Ampel()
Ampel1.setLampen(True, False, False) 
Ampel1.schalten()                     
print(Ampel1.lampeRot, Ampel1.lampeGelb, Ampel1.lampeGruen)
Ampel1.schalten()                     
print(Ampel1.lampeRot, Ampel1.lampeGelb, Ampel1.lampeGruen)
Ampel1.schalten()                     
print(Ampel1.lampeRot, Ampel1.lampeGelb, Ampel1.lampeGruen)