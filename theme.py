from kivy.animation import Animation
def animateWaiting(widget):
	if widget.animatingWaitOpacity:
		return
	anim = Animation(waitOpacity=0.1, duration=.3)
	anim += Animation(waitOpacity=1.0, duration=.3)
	anim.repeat = True
	anim.start(widget)
	widget.animatingWaitOpacity = True