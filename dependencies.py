import bpy
from bpy.types import Operator
import subprocess
import sys
import os
import platform

py_exec = str(sys.executable)

class InstallDependencies(Operator):
    bl_label = "Install Dependencies"
    bl_idname = "facecapture.install_deps"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        subprocess.call([py_exec, "-m", "ensurepip", "--user" ])

        install_dep(["cmake", "cmake"])
        install_dep(["wheel", "wheel"])
        install_dep(["cv2", "opencv-python"])
        install_dep(["cv2", "opencv-contrib-python"])
        install_dep(["imutils", "imutils"])
        install_dep(["PIL", "PILLOW"])
        install_dep(["mediapipe", "mediapipe"])


        return {"FINISHED"}


def install_dep(dep):
    try:
        __import__ (dep[0])
    except ImportError:
        subprocess.call([py_exec, "-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", dep[1]])

classes = [InstallDependencies]