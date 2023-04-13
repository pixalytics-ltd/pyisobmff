# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_uint


# ISO/IEC 14496-12:2022, Section 8.11.4
class PrimaryItemBox(FullBox):
    box_type = "pitm"
    is_mandatory = False

    def read(self, file):
        self.item_id = read_uint(file, 2)
