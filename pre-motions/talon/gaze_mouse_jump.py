from typing import cast

from talon import Module, ctrl, ui
from talon.types import Point2d
from talon.track import tobii
from talon_plugins.eye_mouse import tracker

mod = Module()
screen = ui.main_screen()
SIZE_PX = Point2d(screen.width, screen.height)

class GazeFrame:
    def __init__(self):
        self.__current_frame: tobii.GazeFrame | None = None

    def on_gaze(self, frame: tobii.GazeFrame) -> None:
        self.__current_frame = frame
    
    @property
    def current_frame(self):
        return self.__current_frame

gaze_frame = GazeFrame()

tracker.register('gaze', gaze_frame.on_gaze)

@mod.action_class
class Actions:

    def __init__(self):
        self.gaze_frame = gaze_frame

    def mouse_jump() -> None:
        """jump the mouse cursor to the point of gaze"""
        frame = gaze_frame.current_frame
        pos = cast(Point2d, frame.gaze)
        x = pos.x * SIZE_PX.x
        y = pos.y * SIZE_PX.y
        ctrl.mouse_move(x, y)
