from kivy.animation import Animation
def animateWorking(widget):
    Animation(progressOpacity = (0.1 if widget.working else 0.0)).start(widget)
    if widget.animatingWaitOpacity:
        return
    anim = Animation(blinkOpacity=0.1, duration=.25)
    anim += Animation(blinkOpacity=1.0, duration=.25)
    anim.repeat = True
    anim.start(widget)
    widget.animatingWaitOpacity = True

def animateProgress(widget):
    Animation(_value = widget.value, duration = .3).start(widget)

def processTextInput(widget):
    if widget.text is not "":
        if widget.text[-1] == '\t':
            widget.text = widget.text[0:len(widget.text)-1]
            widget.next.focus = True
        if widget.text[-1] == '\n':
            widget.text = widget.text[0:len(widget.text)-1]
            widget.enter()

#def animateWorking(widget):
#    Animation(progressOpacity = (.1 if widget.working else .0)).start(widget)