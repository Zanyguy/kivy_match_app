import math

from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.graphics import Color

Builder.load_string('''
<Ball>:
    canvas.before:
        Color:
            rgba: self.Colour
        Ellipse:
            pos: self.pos
            size: self.size
    size_hint: None, None
    size: 50,50
    pos: 100,200
    text : self.timelbl
''')

class Ball(Label):
    theta = NumericProperty(0)
    count = NumericProperty(0)
    Colour = ListProperty([0,1,0,.8])
    timelbl = StringProperty("186")
    timer = None
    
    def __init__(self, h, k, r, *args, **kwargs):
        self.h = h
        self.k = k
        self.r = r
        super().__init__(*args, **kwargs)
        
    def tick(self, *args):
        if self.theta < 2*math.pi:
            Animation.cancel_all(self)
            step = 2*math.pi/60
            h = self.h
            k = self.k
            r = self.r
            newX= h + r*math.cos(self.theta)
            newY = k - r*math.sin(self.theta)
            self.theta = self.theta + step
            anim = Animation(x=newX, y = newY, duration = .2)
            anim.start(self)
            self.timelbl = str(int(self.timelbl)-1)
        else:

            if self.count == 0:
                self.Colour=[1,1,.1,.75]
                self.theta=0 
            elif self.count == 1:
                self.Colour=[1,0,0,1]
                self.theta=0 
            self.count = self.count+1
            self.timelbl = str(int(self.timelbl)-1)
        if int(self.timelbl) == 0:
            self.timer.cancel()
    def startTicking(self, *args):
        self.timer = Clock.schedule_interval(self.tick, 1)
        
        
class circleBallApp(App):
    def build(self):
        F= FloatLayout()
        B = Ball(300,300,100)
        F.add_widget(B)
        return F

if __name__ == "__main__":
    circleBallApp().run()
