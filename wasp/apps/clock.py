import fonts.clock as digits
import watch
import widgets
import manager

DIGITS = (
        digits.clock_0,
        digits.clock_1,
        digits.clock_2,
        digits.clock_3,
        digits.clock_4,
        digits.clock_5,
        digits.clock_6,
        digits.clock_7,
        digits.clock_8,
        digits.clock_9
)

MONTH = 'JanFebMarAprMayJunJulAugSepOctNovDec'

class ClockApp(object):
    """Simple digital clock application.

    Shows a time (as HH:MM) together with a battery meter and the date.
    """

    def __init__(self):
        self.meter = widgets.BatteryMeter()

    def handle_event(self, event_view):
        """Process events that the app is subscribed to."""
        if event_view[0] == manager.EVENT_TICK:
            self.update()
        else:
            # TODO: Raise an unexpected event exception
            pass

    def foreground(self, manager, effect=None):
        """Activate the application."""
        self.on_screen = ( -1, -1, -1, -1, -1, -1 )
        self.draw(effect)
        manager.request_tick(1000)

    def tick(self, ticks):
        self.update()

    def background(self):
        """De-activate the application (without losing state)."""
        pass

    def sleep(self):
        return True

    def wake(self):
        self.update()

    def draw(self, effect=None):
        """Redraw the display from scratch."""
        draw = watch.drawable

        draw.fill()
        draw.rleblit(digits.clock_colon, pos=(2*48, 80), fg=0xb5b6)
        self.on_screen = ( -1, -1, -1, -1, -1, -1 )
        self.update()
        self.meter.draw()

    def update(self):
        """Update the display (if needed).

        The updates are a lazy as possible and rely on an prior call to
        draw() to ensure the screen is suitably prepared.
        """
        now = watch.rtc.get_localtime()
        if now[3] == self.on_screen[3] and now[4] == self.on_screen[4]:
            if now[5] != self.on_screen[5]:
                self.meter.update()
                self.on_screen = now
            return False

        draw = watch.drawable
        draw.rleblit(DIGITS[now[4]  % 10], pos=(4*48, 80))
        draw.rleblit(DIGITS[now[4] // 10], pos=(3*48, 80), fg=0xbdb6)
        draw.rleblit(DIGITS[now[3]  % 10], pos=(1*48, 80))
        draw.rleblit(DIGITS[now[3] // 10], pos=(0*48, 80), fg=0xbdb6)
        self.on_screen = now

        month = now[1] - 1
        month = MONTH[month*3:(month+1)*3]
        draw.string('{} {} {}'.format(now[2], month, now[0]),
                0, 180, width=240)

        self.meter.update()
        return True
