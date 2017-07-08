#!/usr/bin/env python

from distutils.core import setup,Extension,os
import string

def cmd1(str):
    return os.popen(str).readlines()[0][:-1]

def cmd2(str):
    return cmd1(str).split()

setup(name = "mecab-python",
	version = "0.996/ko-0.9.0",
	py_modules=["MeCab"],
	ext_modules = [
		Extension("_MeCab",
			["MeCab_wrap.cxx",],
			include_dirs=["C:\\project_c++\\mecab2\\libmecab"],
			library_dirs=["C:\\project_c++\\mecab2\\x64\\Debug"],
			libraries=["libmecab"])
			])
