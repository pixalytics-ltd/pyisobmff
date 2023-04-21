# -*- coding: utf-8 -*-
from .box import Box
from .box import FullBox
from .box import Quantity
from .box import read_uint
from .box import read_fixed_size_string
from .iprp import ItemFullProperty


# ISO/IEC 23008-12:2022, Section 6.5.3.2
class ImageSpatialExtents(FullBox):
    box_type = b"ispe"

    def read(self, file):
        self.width = read_uint(file, 4)
        self.height = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("width", self.width),)
        tuples += (("height", self.height),)
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.6
class PixelInformationProperty(ItemFullProperty):
    box_type = b"pixi"

    def read(self, file):
        num_channels = read_uint(file, 1)
        self.channels = []
        for _ in range(num_channels):
            channel = {}
            channel["bits_per_channel"] = read_uint(file, 1)
            self.channels.append(channel)

    def contents(self):
        tuples = super().contents()
        for idx, channel in enumerate(self.channels):
            tuples += (
                (f'channel[{idx}]["bits_per_channel"]', channel["bits_per_channel"]),
            )
        return tuples


# ISO/IEC 23008-12:2022, Section 6.5.7
class RelativeInformation(ItemFullProperty):
    box_type = b"rloc"

    def read(self, file):
        self.horizontal_offset = read_uint(file, 4)
        self.vertical_offset = read_uint(file, 4)

    def contents(self):
        tuples = super().contents()
        tuples += (("horizontal_offset", self.horizontal_offset),)
        tuples += (("vertical_offset", self.vertical_offset),)
        return tuples
