

class animQueue():
    """handles the starting, stopping, and delaying of animations in sequence"""
    def __init__(self):
        self.animating = False
        self.dropping = False
        self.animations = []
        self.removableWidgets = []

    def update(self, board, *args):
        
        #dropping should be smooth and continue without delay
        if self.dropping and not self.animating:
            if len(self.animations):
                i = 0
                while i<len(self.animations[0]):
                    nextanim = self.animations[0][i][0]
                    w = self.animations[0][i][1]
                    nextanim.bind(on_complete=self.drop_complete)
                    nextanim.start(w)
                    i+=1
                del self.animations[0]
                self.animating = True

        #matches should be animated in sequence to help illustrate cascades
        elif not self.animating:
            if len(self.animations):
                i=0
                while i<len(self.animations[0]):
                    nextanim = self.animations[0][i][0]
                    w = self.animations[0][i][1]
                    nextanim.bind(on_complete=lambda instance, board:
                                                  self.complete(board))
                    self.removableWidgets.append(w)
                    nextanim.start(w)
                    i+=1
                del self.animations[0]
                self.animating = True

    def complete(self, board, *args):
        """Callable to remove widget and allow next animation"""
        self.animating = False
    #never stopped removing widgets for some reason. Had to create hard ceiling.
        if len(self.removableWidgets) < 32:
            for widget in self.removableWidgets:
                board.remove_widget(widget)

    def drop_complete(self, *args):
        """Callable to complete dropping and allow next animation"""
        self.dropping = False
        self.animating = False
