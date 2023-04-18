# -*- coding: utf-8 -*-
from .box import Box
from .box import read_uint
from .stbl import AudioSampleEntry
from .stbl import BitRateBox


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.4
class MHADecoderConfigurationRecord(object):
    def __init__(self, max_offset):
        self.max_offset = max_offset

    def read(self, file):
        self.configurationVersion = read_uint(file, 1)
        self.mpegh3daProfileLevelIndication = read_uint(file, 1)
        self.referenceChannelLayout = read_uint(file, 1)
        self.mpegh3daConfigLength = read_uint(file, 2)
        self.mpegh3daConfig = read_uint(file, self.mpegh3daConfigLength)

    def __repr__(self):
        repl = ()
        repl += (f"configurationVersion: {self.configurationVersion}",)
        repl += (
            f"mpegh3daProfileLevelIndication: {self.mpegh3daProfileLevelIndication}",
        )
        repl += (f"referenceChannelLayout: {self.referenceChannelLayout}",)
        repl += (f"mpegh3daConfigLength: {self.mpegh3daConfigLength}",)
        repl += (f"mpegh3daConfig: {self.mpegh3daConfig}",)
        return "\n".join(repl)


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
class MHAConfigurationBox(Box):
    box_type = b"mhaC"

    def read(self, file):
        self.MHAConfig = MHADecoderConfigurationRecord(max_offset=self.get_max_offset())
        self.MHAConfig.read(file)

    def __repr__(self):
        repl = ()
        repl += (f"MHAConfig: {self.MHAConfig}",)
        return super().repr(repl)


## ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
# class MPEG4BitRateBox(BitRateBox):
#    pass


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
class MPEG4ExtensionDescriptorsBox(Box):
    box_type = b"m4ds"
    # Descriptor Descr[0 .. 255];


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
class MHASampleEntry(AudioSampleEntry):
    box_type = b"mha1"
    box_list = []

    def read(self, file):
        super().read(file)
        self.box_list = self.read_box_list(file)

    def __repr__(self):
        repl = ()
        for box in self.box_list:
            repl += (repr(box),)
        return super().repr(repl)


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.5.2
class MHA2SampleEntry(MHASampleEntry):
    box_type = b"mha2"


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.6.2
class MHMSampleEntry(MHASampleEntry):
    box_type = b"mhm1"


# ISO/IEC 23008-3:2015-Amd-2:2016, Section 20.6.2
class MHM2SampleEntry(MHASampleEntry):
    box_type = b"mhm2"
