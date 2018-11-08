
# yao garbled circuit evaluation v1. simple version based on smart
# naranker dulay, dept of computing, imperial college, october 2018

# << removed >>

def load_json():
    return None


class Gates:
    def not(self, x):
        if x is 1:
            return 0
        return 1
       
    def or(self, x, y):
        if x == y and x == 0:
            return 0
        return 1
    
    def and(self, x, y):
        if x == y and x == 1:
            return 1
        return 0
    
    def xor(self, x, y):
        if x == y:
            return 1
        return 0
    
    def nand(self, x, y):
        return self.not(self.and(x,y))
   
    def xnor(self, x, y):
        return self.not(self.xor(x,y))