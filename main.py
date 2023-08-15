#!/usr/bin/python

import bl00mbox
import captouch
import leds
import os

from st3m.input import InputController, InputState
from st3m.application import Application, ApplicationContext
from st3m.ui.colours import GO_GREEN

from ctx import Context



sample = '/flash/sys/samples/kick.wav'
SAMPLE_DIR = '/flash/sys/samples'


class BloopSlap(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.input = InputController()
        self.blm = bl00mbox.Channel("bloop-slap")
        # self.seq = self.blm.new(bl00mbox.patches.sequencer,
        #                         num_tracks=10, num_steps=32)
        print('loading')
        self.samples = self.load_tunes()

    def load_tunes(self):
        samples = []

        for index, sample in enumerate(os.listdir(SAMPLE_DIR)):
            if index == 10:
                break

            print(sample)
            sample = self.blm.new(bl00mbox.patches.sampler, sample)
            sample.signals.output = self.blm.mixer
            samples.append(sample)

        return samples

    def poll_caps(self):
        ct = captouch.read()
        # 10 petals

        for i in range(10):
            petal = ct.petals[i]
            if petal.pressed:
                print("pressed")
                self.samples[i].signals.trigger.start()

    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms)

        # print(self.input.captouch)

        for i in range(10):
            try:
                petal = ins.captouch.petals[i]
                if petal.pressed:
                    try:
                        self.samples[i].signals.trigger.start()
                    except KeyError:
                        pass
            except IndexError:
                pass

    def draw(self, ctx: Context) -> None:
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = 150
        ctx.font = "Camp Font 1"

        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(*GO_GREEN)

        ctx.move_to(0, 0)
        ctx.save()
        ctx.scale(1.0, 1)
        ctx.text("Bleep bloop")
        ctx.restore()

        leds.set_hsv(int(0.0), abs(1.0) * 360, 1, 0.2)

        leds.update()
