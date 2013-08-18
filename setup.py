from distutils.core import setup
import py2exe

setup(name="presentation",
      windows=["DSDM.py"],    # put the name of your main script here
      options = {"py2exe": {"packages": ["encodings"]}}
)