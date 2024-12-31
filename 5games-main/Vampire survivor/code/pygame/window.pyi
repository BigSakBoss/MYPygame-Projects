from typing import Optional, Tuple, Union
from typing_extensions import deprecated # added in 3.13

from pygame._common import Coordinate, RectValue
from pygame.locals import WINDOWPOS_UNDEFINED
from pygame.rect import Rect
from pygame.surface import Surface

def get_grabbed_window() -> Optional[Window]: ...

class Window:
    def __init__(
        self,
        title: str = "pygame window",
        size: Coordinate = (640, 480),
        position: Union[int, Coordinate] = WINDOWPOS_UNDEFINED,
        **flags: bool
    ) -> None: ...
    def destroy(self) -> None: ...
    def set_windowed(self) -> None: ...
    def set_fullscreen(self, desktop: bool = False) -> None: ...
    def focus(self, input_only: bool = False) -> None: ...
    def hide(self) -> None: ...
    def show(self) -> None: ...
    def restore(self) -> None: ...
    def maximize(self) -> None: ...
    def minimize(self) -> None: ...
    def set_modal_for(self, parent: Window, /) -> None: ...
    def set_icon(self, icon: Surface, /) -> None: ...
    def get_surface(self) -> Surface: ...
    def flip(self) -> None: ...

    grab_mouse: bool
    grab_keyboard: bool
    title: str
    resizable: bool
    borderless: bool
    always_on_top: bool
    relative_mouse: bool
    opacity: float

    @property
    def mouse_grabbed(self) -> bool: ...
    @property
    def keyboard_grabbed(self) -> bool: ...
    @property
    def id(self) -> int: ...
    @property
    def mouse_rect(self) -> Optional[Rect]: ...
    @mouse_rect.setter
    def mouse_rect(self, value: Optional[RectValue]) -> None: ...
    @property
    def size(self) -> Tuple[int, int]: ...
    @size.setter
    def size(self, value: Coordinate) -> None: ...
    @property
    def minimum_size(self) -> Tuple[int, int]: ...
    @minimum_size.setter
    def minimum_size(self, value: Coordinate) -> None: ...
    @property
    def maximum_size(self) -> Tuple[int, int]: ...
    @maximum_size.setter
    def maximum_size(self, value: Coordinate) -> None: ...
    @property
    def position(self) -> Tuple[int, int]: ...
    @position.setter
    def position(self, value: Union[int, Coordinate]) -> None: ...
    @property
    def opengl(self) -> bool: ...
    @classmethod
    @deprecated("since 2.4.0. Use either the display module or the Window class with get_surface and flip. Try not to mix display and Window")
    def from_display_module(cls) -> Window: ...
