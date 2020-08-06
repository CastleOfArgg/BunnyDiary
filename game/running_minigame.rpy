# bunny run minigame test

init python:
    import time

    ##requires:
    bunny = Image('a.png')
    farmer = Image('a.png')
    running_background = Image('a.png')

    # minigame
    class RunningMinigameDisplayable(renpy.Displayable):
        def __init__(self,
            difficulty=1,
            start=50,
            min=0,
            max=1000,
            length=10,
            keys=config.keymap['dismiss']
        ):
            renpy.Displayable.__init__(self)
            config.keymap['running_minigame_key'] = keys
            self.oldst = None
            self.bunny_px = 300
            self.bunny_py = 30
            self.farmer_px = 10
            self.farmer_py = 10
            self.difficulty = difficulty
            self.value_add = 15
            self.value_sub = 50
            self.min = min
            self.max = max
            self.time_start = time.time()
            self.time_curr = self.time_start
            self.time_end = self.time_start + length
            self.winner = None

        #render
        def render(self, width, height, st, at):
            r = renpy.Render(width, height)

            #calc delta and movement draft
            if self.oldst is None:
                self.oldst = st

            delta = st - self.oldst
            self.oldst = st
            speed = delta * self.value_sub

            self.bunny_px -= speed * self.difficulty

            #draw bunny
            bun = renpy.render(bunny, width, height, st, at)
            r.blit(bun, (int(self.bunny_px), int(self.bunny_py)))

            #draw farmer
            far = renpy.render(farmer, width, height, st, at)
            r.blit(far, (int(self.farmer_px), int(self.farmer_py)))

            #check for winner
            self.time_curr = time.time()
            if self.time_curr >= self.time_end or self.bunny_px >= self.max:
                self.winner = "bunny"
                renpy.timeout(0)
            elif self.bunny_px <= self.min:
                self.winner = "farmer"
                renpy.timeout(0)

            #redraw and return render object
            renpy.redraw(self, 0)
            return r

        #handle events
        def event(self, ev, x, y, st):
            if renpy.map_event(ev, 'running_minigame_key'):
                self.bunny_px += self.value_add

                #ensure screen updates
                renpy.restart_interaction()

            if self.winner:
                return self.winner
            else:
                raise renpy.IgnoreEvent()


screen runningMinigame():
    add running_background
    default runningMinigame = RunningMinigameDisplayable()
    text _('click to run away')
    add runningMinigame

label start:
    "ASDF"
    jump runningMinigame

label runningMinigame:
    window hide
    $qucik_menu = False

    call screen runningMinigame

    $quick_menu = True
    window show

    $winner = _return

    if winner == 'bunny':
        'you win'
    else:
        'you lose'
