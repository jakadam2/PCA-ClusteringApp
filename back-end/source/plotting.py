import attrs
import seaborn as sns

from attrs import field, frozen


def convert_chanel(ch: float | int) -> int:
    if isinstance(ch, float):
        return round(ch*255)
    return ch


@frozen
class RGBA:
    r: int = field(converter=convert_chanel)
    g: int = field(converter=convert_chanel)
    b: int = field(converter=convert_chanel)
    a: int = field(converter=convert_chanel, default=255)

    def __str__(self) -> str:
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a/255})"
    
    def __repr__(self) -> str:
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a/255})"

    def to_str(self) -> str:
        return str(self)

    def change_alfa(self, alfa: int | float) -> 'RGBA':
        return attrs.evolve(self, a=alfa)

    @staticmethod
    def from_tuple(rgba: tuple) -> 'RGBA':
        return RGBA(*rgba)


def get_colour_palette(n: int):
    """Returns color palette to be used for all the plots."""
    return sns.cubehelix_palette(n_colors=n)


def get_colour_palette_rgba(n: int) -> list[RGBA]:
    """Returns color palette to be used for all the plots, each element being of class RGBA."""
    colours = get_colour_palette(n)
    return list(map(RGBA.from_tuple, colours))


