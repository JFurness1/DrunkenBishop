import numpy as np
import hashlib

class Board:
    START = None
    END = None
    XDIM = 17
    YDIM = 9
    
    symbols = [' ', '.', 'o', '+', '=', '*', 'B', '0', 'X', '@', '%', '&', '#', '/', '^']
    START_SYMBOL = 'S'
    END_SYMBOL = 'E'
    
    field = None  # initialised to (XDIM, YDIM) numpy array of zeros   
    i_string = None
    i_bytes = None
    
    def __init__(self, title:str=None, xdim:int=17, ydim:int=9):
        self.XDIM = xdim
        self.YDIM = ydim
        self.START = (self.XDIM//2, self.YDIM//2)
        self.title = title
        
        self.clear_board()
        
    def clear_board(self):
        self.field = np.zeros((self.XDIM, self.YDIM), dtype=np.int)
        
    def resize(self, xdim: int, ydim: int):
        self.XDIM = xdim
        self.YDIM = ydim
        self.clear_board()
        
    def __str__(self):
        if self.title is None:
            ostr = "+" + "-"*self.XDIM + "+\n"
        else:
            if len(self.title) > self.XDIM - 2:
                tstr = "["+self.title[:self.XDIM - 5]+"...]"
            else:
                tstr = "["+self.title+"]"
            ostr = "+" + tstr.center(self.XDIM, '-') + "+\n"
        
        for y in range(self.YDIM):
            ostr += "|"
            for x in range(self.XDIM):
                if x == self.START[0] and y == self.START[1]:
                    ostr += self.START_SYMBOL
                elif x == self.END[0] and y == self.END[1]:
                    ostr += self.END_SYMBOL
                else:
                    ostr += self.symbols[self.field[x, y]]
            ostr += "|\n"
        
        ostr += "+" + "-"*(self.XDIM) + "+\n"
        return ostr

    
    def make_art(self, istr: str, do_md5:bool=True, is_hex:bool=False) -> str:
        self.i_string = istr
        if is_hex:
            self.i_bytes = bytes.fromhex(self.i_string)
        elif do_md5:
            md5 = hashlib.md5()
            md5.update(self.i_string.encode('utf-8'))
            self.i_bytes = md5.digest()
        else:
            self.i_bytes = self.i_string.encode('utf-8')
        
        
        bishop = list(self.START)  # copy the start position
        # Don't need to increment start as it will always be "S"
        
        
        for byte in self.i_bytes:
            # Extract the pairs of bits from the byte into an array. 
            # Least significant first
            w = byte
            pairs = []
            for i in range(4):
                b1 = int(w&1 != 0)
                w = w >> 1
                b2 = int(w&1 != 0)
                w = w >> 1
                pairs.append((b2, b1))
            
            for p in pairs:
                dy = p[0]*2 - 1
                dx = p[1]*2 - 1
                    
                # Move the bishop, sliding along walls as necessary
                bishop[0] = max(min(bishop[0] + dx, self.XDIM - 1), 0)
                bishop[1] = max(min(bishop[1] + dy, self.YDIM - 1), 0)
                
                # Drop a coin on the current square
                self.field[bishop[0], bishop[1]] += 1
        
        # We are done. Mark the end point
        self.END = bishop
        
        return str(self)

b = Board(title=" RSA 1024")
print(b.make_art("fc94b0c1e5b0987c5843997697ee9fb7", is_hex=True))