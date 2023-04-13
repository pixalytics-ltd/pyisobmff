# -*- coding: utf-8 -*-
from .box import Box
from .box import Quantity
from .box import read_box
from .box import read_int
from .stbl import VisualSampleEntry


class HEVCSampleEntry(VisualSampleEntry):
    box_type = "hvc1"
    is_mandatory = True
    quantity = Quantity.ONE_OR_MORE

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = None

    def read(self, file):
        super().read(file)
        self.config = read_box(file)


class HEVCConfigurationBox(Box):
    box_type = "hvcC"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hevc_config = None

    def read(self, file):
        self.hevc_config = HEVCDecoderConfigurationRecord()
        self.hevc_config.read(file)


class HEVCDecoderConfigurationRecord(object):
    def __init__(self):
        self.configuration_version = None  # 8
        self.general_profile_space = None  # 2
        self.general_tier_flag = None  # 1
        self.general_profile_idc = None  # 5
        self.general_profile_compat_flags = None  # 32
        self.general_const_indicator_flags = None  # 48
        self.general_level_idc = None  # 8
        self.reserved1 = 0b1111
        self.min_spatial_segmentation_idc = None  # 12
        self.reserved2 = 0b111111
        self.parallelism_type = None  # 2
        self.reserved3 = 0b111111
        self.chroma_format = None  # 2
        self.reserved4 = 0b11111
        self.bit_depth_luma_minus_8 = None  # 3
        self.reserved5 = 0b11111
        self.bit_depth_chroma_minus_8 = None  # 3
        self.avg_frame_rate = None  # 16
        self.constant_frame_rate = None  # 2
        self.num_temporal_layers = None  # 3
        self.temporal_id_nested = None  # 1
        self.length_size_minus_1 = None  # 2
        self.num_of_arrays = None  # 8
        self.array = []

    def __repr__(self):
        repl = ()
        repl += (f"configuration_version: {self.configuration_version}",)
        repl += (f"general_profile_space: {self.general_profile_space}",)
        repl += (f"general_tier_flag: {bin(self.general_tier_flag)}",)
        repl += (f"general_profile_idc: {self.general_profile_idc}",)
        repl += (
            f"general_profile_compat_flags: {bin(self.general_profile_compat_flags)}",
        )
        repl += (
            f"general_const_indicator_flags: {bin(self.general_const_indicator_flags)}",
        )
        repl += (f"general_level_idc: {self.general_level_idc}",)
        repl += (f"min_spatial_segmentation_idc: {self.min_spatial_segmentation_idc}",)
        repl += (f"parallelism_type: {self.parallelism_type}",)
        repl += (f"chroma_format: {self.chroma_format}",)
        repl += (f"bit_depth_luma_minus_8: {self.bit_depth_luma_minus_8}",)
        repl += (f"bit_depth_chroma_minus_8: {self.bit_depth_chroma_minus_8}",)
        repl += (f"avg_frame_rate: {self.avg_frame_rate}",)
        repl += (f"constant_frame_rate: {self.constant_frame_rate}",)
        repl += (f"num_temporal_layers: {self.num_temporal_layers}",)
        repl += (f"temporal_id_nested: {self.temporal_id_nested}",)
        repl += (f"length_size_minus_1: {self.length_size_minus_1}",)
        return super().repr(repl)

    def read(self, file):
        self.configuration_version = read_int(file, 1)
        #
        byte = read_int(file, 1)
        self.general_profile_space = (byte >> 6) & 0b11
        self.general_tier_flag = (byte >> 5) & 0b1
        self.general_profile_idc = byte & 0b11111  # 5
        #
        self.general_profile_compat_flags = read_int(file, 4)  # 32
        self.general_const_indicator_flags = read_int(file, 6)  # 48
        self.general_level_idc = read_int(file, 1)  # 8
        #
        byte = read_int(file, 1)
        self.reserved1 = (byte >> 4) & 0b1111
        msbyte = (byte & 0b1111) << 8
        lsbyte = read_int(file, 1)
        self.min_spatial_segmentation_idc = (msbyte << 8) | lsbyte
        #
        byte = read_int(file, 1)
        self.reserved2 = (byte >> 2) & 0b111111
        self.parallelism_type = byte & 0b11
        #
        byte = read_int(file, 1)
        self.reserved3 = (byte >> 2) & 0b111111
        self.chroma_format = byte & 0b11  # 2
        #
        byte = read_int(file, 1)
        self.reserved4 = (byte >> 3) & 0b11111
        self.bit_depth_luma_minus_8 = byte & 0b111  # 3
        #
        byte = read_int(file, 1)
        self.reserved5 = (byte >> 3) & 0b11111
        self.bit_depth_chroma_minus_8 = byte & 0b111  # 3
        #
        self.avg_frame_rate = read_int(file, 2)  # 16
        #
        byte = read_int(file, 1)
        self.constant_frame_rate = (byte >> 6) & 0b11  # 2
        self.num_temporal_layers = (byte >> 3) & 0b11  # 2
        self.temporal_id_nested = (byte >> 2) & 0b1  # 1
        self.length_size_minus_1 = byte & 0b11
        #
        num_of_arrays = read_int(file, 1)  # 8
        for _ in range(num_of_arrays):
            self.array.append(self.__read_item(file))

    def __read_item(self, file):
        item = {}
        byte = read_int(file, 1)
        item["array_completeness"] = (byte >> 7) & 0b1
        item["nal_unit_type"] = byte & 0b111111
        # print(item['nal_unit_type'])
        num_nalus = read_int(file, 2)
        item["nal_units"] = []
        for _ in range(num_nalus):
            nal_unit_len = read_int(file, 2)
            nal_unit = file.read(nal_unit_len)
            item["nal_units"].append(nal_unit)
        return item
