from kivy.animation import Animation
def animateBlinking(widget):
    if widget.animatingBlinkOpacity:
        return
    anim = Animation(blinkOpacity=0.1, duration=.25)
    anim += Animation(blinkOpacity=0.3, duration=.25)
    anim.repeat = True
    anim.start(widget)
    widget.animatingBlinkOpacity = True

def animateProgress(widget):
    if (widget.value >= widget.max):
        widget.blink = False
        Animation(progressOpacity=0.0, duration = 0.4).start(widget)
    else:
        Animation(progressOpacity=0.1, duration = 0.4).start(widget)
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