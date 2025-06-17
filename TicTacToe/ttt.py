import sys 
import random 
import copy
import pygame
import numpy as np
from constants import *

#Pygame setup
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Tac Toe ")
screen.fill(BG_COLOR)

pygame.mixer.music.load("sound_effects/bg.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

win= pygame.mixer.Sound("sound_effects/win.mp3")
loss= pygame.mixer.Sound("sound_effects/loss.mp3")


clash_sounds = [
    pygame.mixer.Sound('sound_effects/minipekka.wav'),
    pygame.mixer.Sound('sound_effects/hog.wav'),
    pygame.mixer.Sound('sound_effects/magicarcher.wav'),
    pygame.mixer.Sound('sound_effects/megaknight.wav'),
    pygame.mixer.Sound('sound_effects/ram.wav'),
    pygame.mixer.Sound('sound_effects/zap.wav'),
    pygame.mixer.Sound('sound_effects/hogs.wav'),
    pygame.mixer.Sound('sound_effects/gobs.wav'),
    pygame.mixer.Sound('sound_effects/mortar.wav'),
    pygame.mixer.Sound('sound_effects/ragebarb.wav')
]

def play_random_clash_sound():
    sound = random.choice(clash_sounds)
    sound.play()


class Board:

    def __init__(self):
        self.squares=np.zeros((ROWS,COLS))
        self.empty_sqrs=self.squares # [squares]
        self.marked_sqrs=0

    def final_state(self,show=False):
        '''
        @return 0 if no win yet
        @return 1 if player 1 wins 
        @return 2 if player 2 wins
        '''

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col]!=0:
                if show:
                    color=CIRC_COLOR if self.squares[0][col]==2 else CROSS_COLOR
                    ipos=(col*SQSIZE+SQSIZE//2,20)
                    fpos=(col*SQSIZE+SQSIZE//2,HEIGHT-20)
                    pygame.draw.line(screen,color,ipos,fpos,LINE_WIDTH)
                return self.squares[0][col]
            
        #horizontal rows
        for row in range(ROWS):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2]!=0:
                if show:
                    color=CIRC_COLOR if self.squares[row][0]==2 else CROSS_COLOR
                    ipos=(20,row*SQSIZE+SQSIZE//2)
                    fpos=(WIDTH-20,row*SQSIZE+SQSIZE//2)
                    pygame.draw.line(screen,color,ipos,fpos,LINE_WIDTH)
                return self.squares[row][0]
            
        #desc diagonal
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2]!=0:
            if show:
                    color=CIRC_COLOR if self.squares[1][1]==2 else CROSS_COLOR
                    ipos=(20,20)
                    fpos=(WIDTH-20,HEIGHT-20)
                    pygame.draw.line(screen,color,ipos,fpos,LINE_WIDTH)
            return self.squares[1][1]
        
        #asc diagonal
        if self.squares[2][0]==self.squares[1][1]==self.squares[0][2]!=0:
            if show:
                    color=CIRC_COLOR if self.squares[1][1]==2 else CROSS_COLOR
                    ipos=(20,HEIGHT-20)
                    fpos=(WIDTH-20,20)
                    pygame.draw.line(screen,color,ipos,fpos,LINE_WIDTH)
            return self.squares[1][1]
        
        #no win yet
        return 0

    def mark_sqr(self,row,col,player):
        self.squares[row][col]=player
        self.marked_sqrs+=1

    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs=[]
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row,col):
        
                    empty_sqrs.append((row,col))
        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs==9

    
    def isempty(self):
        return self.marked_sqrs==0
    
class AI:
    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player

    def rnd(self,board):
        empty_sqrs=board.get_empty_sqrs()
        idx=random.randrange(0,len(empty_sqrs))
        return empty_sqrs[idx]
    
    def minimax(self,board,maximizing):
        #terminal case
        case = board.final_state()

        #player 1 wins 
        if case == 1:
            return 1 , None
        
        #player 2 wins
        if case ==2:
            return -1 , None 
        
        elif board.isfull():
            return 0 , None
        
        if maximizing:
                max_eval = -100
                best_move =None
                empty_sqrs=board.get_empty_sqrs()

                for (row,col) in empty_sqrs:
                    temp_board=copy.deepcopy(board)
                    temp_board.mark_sqr(row,col,1)
                    eval=self.minimax(temp_board,False)[0]
                    if eval>max_eval:
                        max_eval=eval
                        best_move = (row,col)
                return max_eval, best_move

         
        elif not maximizing:
            min_eval = 100
            best_move =None
            empty_sqrs=board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval=   self.minimax(temp_board,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move = (row,col)
            return min_eval, best_move 
        
    def eval(self,main_board):
        if self.level==0:
            #random choice
            eval='random' 
            move=self.rnd(main_board)
        else:
            #minimax choice
           eval,move = self.minimax(main_board,False)
        print(f'AI has chosen to mark the square in position {move} with an eval of {eval}')
        return move 

class Game:
    def __init__(self):
        self.board=Board()
        self.ai = AI()
        self.gamemode='ai' #pvp or ai
        self.running=True
        self.player=1
        self.show_lines()

    def make_move(self,row,col):
        self.board.mark_sqr(row,col,self.player)
        self.draw_fig(row,col)
        self.next_turn()   


    def show_lines(self):
        screen.fill(BG_COLOR)
        #vertical lines
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(WIDTH-SQSIZE,0),(WIDTH-SQSIZE,HEIGHT),LINE_WIDTH)
        #horizontal lines
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(WIDTH,SQSIZE),LINE_WIDTH)    
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT-SQSIZE),(WIDTH,HEIGHT-SQSIZE),LINE_WIDTH)

    def draw_fig(self,row,col):
        if self.player == 1:
            #draw X
            start_desc=(col*SQSIZE+OFFSET,row*SQSIZE+OFFSET)
            end_desc=(col*SQSIZE+SQSIZE-OFFSET,row*SQSIZE+SQSIZE-OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)

            start_asc=(col*SQSIZE+OFFSET,row*SQSIZE+SQSIZE-OFFSET)
            end_asc=(col*SQSIZE+SQSIZE-OFFSET,row*SQSIZE+OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_asc,end_asc,CROSS_WIDTH)

        elif self.player == 2:
            #draw O
            center=(col*SQSIZE+SQSIZE//2,row*SQSIZE+SQSIZE//2)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode ='ai' if self.gamemode=='pvp' else 'pvp'

    def reset(self):
        self.__init__()

    def isover(self):
        return self.board.final_state(show=True) !=0 or self.board.isfull()

    def show_popup(self, message):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Render the message
        font = pygame.font.SysFont(None, 60)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.update()

        # Wait for user to press a key or click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

def main():

    game=Game()
    board=game.board
    ai=game.ai


    #mainloop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                #g-gamemode
                if event.key==pygame.K_g:
                    game.change_gamemode()
                if event.key==pygame.K_0:
                    ai.level=0
                if event.key==pygame.K_1:
                    ai.level=1
                if event.key==pygame.K_r:
                    game.reset()
                    board=game.board
                    ai=game.ai 

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row= pos[1] //SQSIZE
                col= pos[0] //SQSIZE
                
                if board.empty_sqr(row,col) and game.running:
                    game.make_move(row,col)
                    play_random_clash_sound()

                    if game.isover():
                        game.running=   False   
                        # Determine result
                        winner = board.final_state()
                        if winner == 0:
                            message = "It's a Draw!"
                            win.play()
                        elif winner == 1:
                            message = "Player 1 Wins!" if game.gamemode == 'pvp' else "You Win!"
                            win.play()
                        elif winner == 2:
                            message = "Player 2 Wins!" if game.gamemode == 'pvp' else "AI Wins!"
                            loss.play()
                        game.show_popup(message)
        

               
                    
        if game.gamemode=='ai'and game.player ==ai.player and game.running :
            pygame.display.update()

            #ai methods 
            row,col=ai.eval(board)
            
            game.make_move(row,col)
            
            if game.isover():
                game.running = False
                winner = board.final_state()
                if winner == 0:
                    message = "It's a Draw!"
                    win.play()
                elif winner == 1:
                    message = "You Win!"
                    win.play()
                elif winner == 2:
                    message = "AI Wins!"
                    loss.play()
                game.show_popup(message)
        if board.final_state(show=True) != 0 or board.isfull():
            game.running = False


        pygame.display.update()
        


main()