import random
import boardMovement
import boardAnimation
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.properties import NumericProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.config import Config
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '400')

class GameScreen(Screen):
    pass

class myScreenManager(ScreenManager):
    
    def newboard(self):
        game = self.get_screen("Game")
        self.remove_widget(game)
        self.add_widget(GameScreen())

    def startTime(self):
        game = self.get_screen("Game").ids.board
        Clock.schedule_interval(game.timeKeep.pbUpdate, 1)

class GridEntry(EventDispatcher):
    #identifiers for shapetogs to help with match logic
    row = NumericProperty(0)
    column = NumericProperty(0)
    shape = NumericProperty(0)

class ResetBtn(Button, GridEntry):
    pass

class shapeTog(ToggleButton, GridEntry):
    """Main pieces for userinteraction. These determine shapes,
        matches, and location on the screen. """
        
    def on_state(self, widget, state):
        """toggle buttons version of on_click"""
        if state == 'down': #previously unclicked button
            for key, child in self.parent.brd.items(): # compare to all other shapes
                if child.state == 'down': #then it should be last button clicked
                    if boardMovement.validMove(self, child, self.parent):
                        boardMovement.singleMove(self, child, self.parent)
                        boardMovement.matchFactory(self, child, self.parent)
                        if not boardMovement.getPotentialMatches(self.parent):
                            self.parent.timeKeep.value = self.parent.timeKeep.max
                    if child is not self: #unclicks on invalid moves
                        child.state = 'normal'

def newShapes(board):
    """generator to gaurantee fixed number of shapes. Refills any
        missing shapes after match removal."""

    brd = board.brd

    #drop all shapes to lowest available slot first
    for x in range(1,9): 
        for y in range(1,9):
            if int(brd[str(x)+','+str(y)].shape)==0:
                for n in range(y+1, 9):
                    if not int(brd[str(x)+','+str(n)].shape)==0:
                        brd[str(x)+','+str(n)].row = y
                        brd[str(x)+','+str(y)].row = n
                        brd[str(x)+','+str(y)], brd[str(x)+','+str(n)] = brd[str(x)+','+str(n)], brd[str(x)+','+str(y)]
                        break
                        
    #now fill shapes in from the top down
    for x in range(8,0,-1):
        for y in range(8,0,-1):
            if not int(brd[str(x)+','+str(y)].shape):
                C = brd[str(x)+','+str(y)]
                                                      
                imgs = ['imgs/h1.png','imgs/S2.png','imgs/L3.png','imgs/G4.png',
                        'imgs/T5.png','imgs/W6.png','imgs/Z7.png']
                
                bimgs = ['imgs/h1d.png','imgs/S2d.png','imgs/L3d.png','imgs/G4d.png',
                         'imgs/T5d.png','imgs/W6d.png','imgs/Z7d.png']
                
                img = random.randint(1,7)

                X = .1*x
                Y = 1
                
                I = shapeTog(pos_hint={'x': X, 'y': Y},
                             row = y,
                             column = x,
                             shape = img,
                             background_normal= imgs[img-1],
                             background_down= bimgs[img-1])

                board.add_widget(I)
                brd[str(x)+','+str(y)] = I


class Board(FloatLayout):
    
    score = None
    timeKeep = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        #self.size=(900,800)
        self.pos=(0,0)
        self.brd = {} #dict using cartesian coordinates as keys for widgets 
        blist=[]
        AQ = boardAnimation.animQueue()
        Clock.schedule_interval(lambda self: AQ.update(self), 1/60)
        Clock.schedule_once(self.cleanerCB, 1)

        for x in range(8,0,-1):
            for y in range(8,0,-1):
                
                imgs = ['imgs/h1.png','imgs/S2.png','imgs/L3.png','imgs/G4.png',
                        'imgs/T5.png','imgs/W6.png','imgs/Z7.png']
                
                bimgs = ['imgs/h1d.png','imgs/S2d.png','imgs/L3d.png','imgs/G4d.png',
                         'imgs/T5d.png','imgs/W6d.png','imgs/Z7d.png']
                
                img = random.randint(1,7)
                
                X = .1*x
                Y = .1*(y)
                
                I = shapeTog(pos_hint={'x':X,'y':Y},
                             row = y,
                             column = x,
                             shape = img,
                             background_normal= imgs[img-1],
                             background_down= bimgs[img-1])
 
                self.add_widget(I)
                self.brd[str(x)+','+str(y)] = I
        R = ResetBtn(text="Reset",
                     size_hint = (.1, .1),
                     pos = (0,0))
        self.add_widget(R)

        score = scoreLabel(text = '0',
                      size_hint = (.1, .1),
                      pos_hint = {'x':.1, 'y':0})
        self.score = score
        self.add_widget(score)

        PB = GameTimer(size_hint = (.8, .1),
                         pos_hint = {'x': .1, 'y': .9},
                         max = 120,
                         value = 1)
        self.add_widget(PB)
        self.AQ = AQ
        self.timeKeep = PB
        


    def cleanerCB(self, *args):
        boardMovement.cleanFirstBoard(self)


class scoreLabel(Label):
    pass


class GameOver(Popup):
    def __init__(self, score, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_hint = (.8, .8)
        self.pos_hint = {'x': .1, 'y': .1}
        self.title = 'Game Over'
        B = BoxLayout()
        L = Label(text = 'High Score:' +str(score))
        self.label = L
        B.add_widget(L)
        btn = Button(text = 'Done')
        btn.bind(on_release = self.dismiss)
        B.add_widget(btn)
        self.content = B


class GameTimer(ProgressBar):

    def pbUpdate(self, *args, **kwargs):
        if self.value < 120:
            self.value += 1
        else:
            popup = GameOver(self.parent.score.text)
            popup.open()
            return False
            
        
class MatchApp(App):
    
    def build(self):
        root = myScreenManager()
        return root

if __name__ == '__main__':
    MatchApp().run()
