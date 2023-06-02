#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Time    : 2023/06/02 17:00:54
# @Author  : 橙橙橙心滴
# @File    : alipan.py
'''



from aligo import Aligo


class Backup:
    def __init__(self, local_file, ali_file) -> None:
        self.ali = Aligo()
        self.folder = self.ali.get_folder_by_path(ali_file)
        if self.folder == None:
            self.ali.create_folder(ali_file)
            self.folder = self.ali.get_folder_by_path(ali_file)
        self.ali.sync_folder(local_folder=local_file,
                             remote_folder=self.folder.file_id)

    def alidown(self):
        pass


# Backup('E:\\python\\douyu_ffmpeg\\__pycache__','录播/aaa/__pycache__')
