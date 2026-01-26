from typing import Any
import arcade


class Tween:
    def __init__(self, Object: object, Target: dict[str, tuple | arcade.Vec2 | float], time: float):
        self.Target = Target
        self.Object = Object

        self.EndTime = time

        self._Time = 0

        self.StartValues = {}

        for i in Target.keys():
            self.StartValues[i] = getattr(Object,i)

        TweenManager.Tweens.append(self)

        self.isPlaying = False

    def Play(self):
        self.isPlaying = True
        self._Time = 0

    def Pause(self):
        self.isPlaying = False

    def Resume(self):
        self.isPlaying = True

    def Stop(self):
        self.isPlaying = False
        self._Time = 0

    def update(self, DT):
        self._Time += DT

        new = None
        for key, v in self.StartValues:
            if isinstance(v, tuple):
                for i in v:
                    a = self.StartValues[key][i]
                    b = self.Target[key][i]
                    t = self._Time/self.EndTime

                    new[i] = Lerp(a,b,t)
            elif isinstance(v, float):
                a = self.StartValues[key]
                b = self.Target[key]
                t = self._Time/self.EndTime

                new = Lerp(a,b,t)

        setattr(self.Object, key, Lerp(a,b,t))


def Lerp(a, b, t):
    return a + (b - a) * t

class TweenManager():
    Tweens: list[Tween] = []

    @staticmethod
    def update():
        for tween in TweenManager.Tweens:
            if tween.isPlaying:
                tween.update()
            if tween._Time >= tween.EndTime:
                del(tween)