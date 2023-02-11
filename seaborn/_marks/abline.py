## Author: DominikMatula
## Link:  N/A

import dataclasses
import collections
from typing import Any, Mapping, Tuple, ClassVar

import pandas as pd
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

    def _get_passthrough_points(self, data: dict):
        raise NotImplementedError()
    
    def _plot(self, split_gen, scales, orient):
        
        for keys, data, ax in split_gen():
            vals = resolve_properties(self, keys, scales)
            # to enable output of aggregations
            if not "x" in vals and "x" in data.columns:
                vals["x"] = data["x"]
            if not "y" in vals and "y" in data.columns:
                vals["y"] = data["y"]

            vals["color"] = resolve_color(self, keys, scales=scales)
            vals["fillcolor"] = resolve_color(self, keys, prefix="fill", scales=scales)
            vals["edgecolor"] = resolve_color(self, keys, prefix="edge", scales=scales)

            artist_kws = self.artist_kws.copy()
            xy1, xy2 = self._get_passthrough_points(vals)
            if orient == "y":
                xy1 = [xy[::-1] for xy in xy1]
                xy2 = [xy[::-1] for xy in xy2]

            for point1, point2 in zip(xy1, xy2):
                ax.axline(
                    point1,
                    point2,
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
    A mark adding vertical line to your plot.

    See also
    --------
    Axline : A mark adding arbitrary line to your plot.
    Axhline : A mark adding horizontal line to your plot.

    Examples
    --------
    .. include:: ../docstrings/objects.Path.rst    # TODO: Add
    """
    intercept: MappableFloat = Mappable(0)
    slope: MappableFloat =Mappable(1)

    def _get_passthrough_points(self, vals: dict):
        if not hasattr(vals["intercept"], "__iter__"):
            vals["intercept"] = [vals["intercept"]]
        if not hasattr(vals["slope"], "__iter__"):
            vals["slope"] = [vals["slope"]]
            
        xy1 = [(0, intercept) for intercept in vals["intercept"]]
        xy2 = [(1, intercept + slope) for intercept, slope in zip(vals["intercept"], vals["slope"])]
        return xy1, xy2


@dataclasses.dataclass
class Axhline(AxlineBase):
    """
    A mark adding horizontal line to your plot.

    See also
    --------
    Axline : A mark adding arbitrary line to your plot.
    Axvline : A mark adding vertical line to your plot.

    Examples
    --------
    .. include:: ../docstrings/objects.Path.rst    # TODO: Add
    """

    y: MappableFloat = Mappable(0)

    def _get_passthrough_points(self, vals: dict):
        if not hasattr(vals["y"], "__iter__"):
            vals["y"] = [vals["y"]]
        xy1 = ((0, y) for y in  vals["y"])
        xy2 = ((1, y) for y in  vals["y"])
        return xy1, xy2


@dataclasses.dataclass
class Axvline(AxlineBase):
    """
    A mark adding vertical line to your plot.

    See also
    --------
    Axline : A mark adding arbitrary line to your plot.
    Axhline : A mark adding horizontal line to your plot.

    Examples
    --------
    .. include:: ../docstrings/objects.Path.rst    # TODO: Add
    """
    x: MappableFloat = Mappable(0)

    def _get_passthrough_points(self, vals: dict):
        if not hasattr(vals["x"], '__iter__'):
            vals["x"] = [vals["x"]]
        xy1 = ((x, 0) for x in vals["x"])
        xy2 = ((x, 1) for x in vals["x"])
        return xy1, xy2