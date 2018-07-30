#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from zipfile import ZipFile, ZipInfo
import os

class ZipFile(ZipFile):
    
    def extract(self, member, path=None, pwd=None):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        if path is None:
            path = os.getcwd()
        

        ret_val = self._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        os.chmod(ret_val, attr)
        return ret_val
