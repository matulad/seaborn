## Author: DominikMatula
## Link:  N/A

import dataclasses
import collections
from typing import Any, Mapping, Tuple, ClassVar

import matplotlib as mpl
import scipy.optimize
import seaborn.objects as so
import numpy as np
from seaborn._marks.base import (
    Mappable,
    MappableColor,
    MappableFloat,
    MappableString,
    resolve_color,
    resolve_properties,
)

class AxlineBase(so.Path):
    _sort: ClassVar[bool] = False

    def _get_passthrough_points(self, x: float, y: float) -> Tuple(Tuple(float, float), (float, float)):
        raise NotImplementedError()
    
    def _plot(self, split_gen, scales, orient):
        
        for keys, _, ax in split_gen():
            vals = resolve_properties(self, keys, scales)
            vals["color"] = resolve_color(self, keys, scales=scales)
            vals["fillcolor"] = resolve_color(self, keys, prefix="fill", scales=scales)
            vals["edgecolor"] = resolve_color(self, keys, prefix="edge", scales=scales)
            artist_kws = self.artist_kws.copy()
            xy1, xy2 = self._get_passthrough_points(x=vals["x"], y=vals["y"])
            if orient == "y":
                xy1 = xy1[::-1]
                xy2 = xy2[::-1]

            ax.axline(
                xy1,
                xy2,
                color=vals["color"],
                linewidth=vals["linewidth"],
                linestyle=vals["linestyle"],
                marker=vals["marker"],
                markersize=vals["pointsize"],
                markerfacecolor=vals["fillcolor"],
                markeredgecolor=vals["edgecolor"],
                markeredgewidth=vals["edgewidth"],
                **artist_kws,
            )


@dataclasses.dataclass
class Axline(AxlineBase):
    """
    A mark adding arbitrary line to your plot.

    See also
    --------
    Axhline : A mark adding horizontal line to your plot.
    Axvline : A mark adding vertical line to your plot.

    Examples
    --------
    .. include:: ../docstrings/objects.Path.rst    # TODO: Add
    """
    intercept: MappableFloat = Mappable(0)
    slope: MappableFloat =Mappable(1)
    color: MappableColor = Mappable("C0")
    alpha: MappableFloat = Mappable(1)
    linewidth: MappableFloat = Mappable(rc="lines.linewidth")
    linestyle: MappableString = Mappable(rc="lines.linestyle")
    marker: MappableString = Mappable(rc="lines.marker")
    pointsize: MappableFloat = Mappable(rc="lines.markersize")
    fillcolor: MappableColor = Mappable(depend="color")
    edgecolor: MappableColor = Mappable(depend="color")
    edgewidth: MappableFloat = Mappable(rc="lines.markeredgewidth")

    def _plot(self, split_gen, scales, orient):
        
        for keys, _, ax in split_gen():
            vals = resolve_properties(self, keys, scales)
            vals["color"] = resolve_color(self, keys, scales=scales)
            vals["fillcolor"] = resolve_color(self, keys, prefix="fill", scales=scales)
            vals["edgecolor"] = resolve_color(self, keys, prefix="edge", scales=scales)

            artist_kws = self.artist_kws.copy()

            xy1 = (0, vals["intercept"])
            xy2 = (1, vals["intercept"] + vals["slope"])
            if orient == "y":
                xy1 = xy1[::-1]
                xy2 = xy2[::-1]

            ax.axline(
                xy1,
                xy2,
                color=vals["color"],
                linewidth=vals["linewidth"],
                linestyle=vals["linestyle"],
                marker=vals["marker"],
                markersize=vals["pointsize"],
                markerfacecolor=vals["fillcolor"],
                markeredgecolor=vals["edgecolor"],
                markeredgewidth=vals["edgewidth"],
                **artist_kws,
            )


@dataclasses.dataclass
class Axhline(so.Mark):
    """
    A mark adding arbitrary line to your plot.

    See also
    --------
    Axline : A mark adding arbitrary line to your plot.
    Axvline : A mark adding vertical line to your plot.

    Examples
    --------
    .. include:: ../docstrings/objects.Path.rst    # TODO: Add
    """
    y: MappableFloat = Mappable(0)

    color: MappableColor = Mappable("C0")
    alpha: MappableFloat = Mappable(1)
    linewidth: MappableFloat = Mappable(rc="lines.linewidth")
    linestyle: MappableString = Mappable(rc="lines.linestyle")
    marker: MappableString = Mappable(rc="lines.marker")
    pointsize: MappableFloat = Mappable(rc="lines.markersize")
    fillcolor: MappableColor = Mappable(depend="color")
    edgecolor: MappableColor = Mappable(depend="color")
    edgewidth: MappableFloat = Mappable(rc="lines.markeredgewidth")

    def _plot(self, split_gen, scales, orient):
        
        # other = {"x": "y", "y": "x"}[orient]
        for keys, data, ax in split_gen():
            vals = resolve_properties(self, keys, scales)
            vals["color"] = resolve_color(self, keys, scales=scales)
            vals["fillcolor"] = resolve_color(self, keys, prefix="fill", scales=scales)
            vals["edgecolor"] = resolve_color(self, keys, prefix="edge", scales=scales)

            artist_kws = self.artist_kws.copy()
            # self._handle_capstyle(artist_kws, vals)

            xy1 = (0, vals["y"])
            xy2 = (1, vals["y"])
            if orient == "y":
                xy1 = xy1[::-1]
                xy2 = xy2[::-1]

            ax.axline(
                xy1,
                xy2,
                color=vals["color"],
                linewidth=vals["linewidth"],
                linestyle=vals["linestyle"],
                marker=vals["marker"],
                markersize=vals["pointsize"],
                markerfacecolor=vals["fillcolor"],
                markeredgecolor=vals["edgecolor"],
                markeredgewidth=vals["edgewidth"],
                **artist_kws,
            )


###
# Horizontal: prochází  (0, y), (1, y)
# Vertical: prochází    (x, 0), (x, 1)
# Arbitrary: prochází   (x, 0), (0, y)