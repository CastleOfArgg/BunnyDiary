# bunny run minigame test
# clicking game: excape the farmer by clicking as much as possable
# with lose (delta) ground to farmer every frame
# click to gain ground
#returns running_minigame_win or running_minigame_lose

init 2 python:
    import time

    #const return results
    running_minigame_win = "bunny"
    running_minigame_lose = "farmer"

    #game difficulty
    running_minigame_strength = 0
    running_minigame_diff = 1  #should be set in call to label runningMinigame

    ##requires images:
    bunny = im.Scale('bunny.png', 300, 300)
    farmer = im.Scale('farmer2.png', 700, 1000)
    running_background = im.Scale('farm2-01.png', 1920, 1080)

    #optional
    keys=config.keymap['running_minigame'] = ['K_e']

    # minigame
    # class overwrites renpy.displayable for a custom minigame
    #param:
        #min: if goes below this then lose
        #max: if goes above this then instant win
        #length: if lasts longer then this number in seconds then win
        #keys: the keys that allow player to move foward
    #returns running_minigame_win or running_minigame_lose
    class RunningMinigameDisplayable(renpy.Displayable):
        def __init__(self,
            min=200,
            max=1000,
            length=10,
            keys=config.keymap['running_minigame']
        ):
            renpy.Displayable.__init__(self)
            config.keymap['running_minigame_key'] = keys
            self.oldst = None
            self.bunny_px = 700
            self.bunny_py = 300
            self.farmer_px = 10
            self.farmer_py = 150
            self.difficulty = running_minigame_diff
            self.value_add = 15 + running_minigame_strength
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

            #check for winner and return running_minigame_win
            # or running_minigame_lose
            self.time_curr = time.time()
            if self.time_curr >= self.time_end or self.bunny_px >= self.max:
                self.winner = running_minigame_win
                renpy.timeout(0)
            elif self.bunny_px <= self.min:
                self.winner = running_minigame_lose
                renpy.timeout(0)

            #redraw and return render object
            renpy.redraw(self, 0)
            return r

        #handle events
        #eccepted events: timeout, excepted click key(s)
        def event(self, ev, x, y, st):
            if renpy.map_event(ev, 'running_minigame_key'):
                self.bunny_px += self.value_add

                #ensure screen updates
                renpy.restart_interaction()

            if self.winner:
                return self.winner
            else:
                raise renpy.IgnoreEvent()


#screen for the running_minigame displayable
screen runningMinigame():
    add running_background
    default runningMinigame = RunningMinigameDisplayable()
    text _("tap 'e' to run away")
    add runningMinigame


#label to call running_minigame
#param:
    #strength: bunny's strength, easier addition
    #diff: the difficulty multiplier
#return true running_minigame_win or running_minigame_lose
label runningMinigame(strength, diff=1):
    $running_minigame_strength = strength
    $running_minigame_diff = diff

    window hide
    $quick_menu = False

    call screen runningMinigame()

    $result = _return

    $quick_menu = True
    window show

    return result
