# -*- coding: utf-8 -*-
from .box import FullBox
from .box import read_box
from .box import read_int
from .box import read_string


class ItemInformationBox(FullBox):
    box_type = "iinf"
    is_mandatory = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_infos = []

    def __repr__(self):
        repl = ()
        repl += (f"entry_count: {str(len(self.item_infos))}",)
        for item in self.item_infos:
            repl += (repr(item),)
        return super().repr(repl)

    def read(self, file):
        count_size = 2 if self.version == 0 else 4
        entry_count = read_int(file, count_size)
        for _ in range(entry_count):
            box = read_box(file)
            if not box:
                break
            if box.box_type == "infe":
                self.item_infos.append(box)


class ItemInformationEntry(FullBox):
    box_type = "infe"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = None
        self.item_protection_index = None
        self.item_name = None
        self.item_extension = None
        self.item_type = None
        self.content_type = None
        self.content_encoding = None
        self.uri_type = None

    def __repr__(self):
        repl = ()
        repl += (f"item_id: {self.item_id}",)
        repl += (f"item_protection_index: {self.item_protection_index}",)
        repl += (f"item_name: {self.item_name}",)
        if self.version >= 2:
            repl += (f"item_type: {self.item_type}",)
        return super().repr(repl)

    def read(self, file):
        if self.version == 0 or self.version == 1:
            self.item_id = read_int(file, 2)
            self.item_protection_index = read_int(file, 2)
            self.item_name = read_string(file)
            self.content_type = read_string(file)
            self.content_encoding = read_string(file)

            if self.version == 1:
                extension_type = read_string(file, 4)
                fdel = FDItemInfoExtension()
                fdel.read(file)
                self.item_extension = fdel
        elif self.version >= 2:
            if self.version == 2:
                self.item_id = read_int(file, 2)
            elif self.version == 3:
                self.item_id = read_int(file, 4)
            self.item_protection_index = read_int(file, 2)
            self.item_type = read_string(file, 4)
            self.item_name = read_string(file)

            if self.item_type == "mime":
                self.content_type = read_string(file)
                self.content_encoding = read_string(file)
            elif self.item_type == "uri ":
                self.uri_type = read_string(file)


class FDItemInfoExtension(object):
    def __init__(self):
        self.content_location = None
        self.content_md5 = None
        self.content_length = None
        self.transfer_length = None
        self.group_ids = []

    def read(self, file):
        """read"""
        self.content_location = read_string(file)
        self.content_md5 = read_string(file)
        self.content_length = read_int(file, 8)
        self.transfer_length = read_int(file, 8)
        entry_count = read_int(file, 1)
        for _ in range(entry_count):
            group_id = read_int(file, 4)
            self.group_ids.append(group_id)
