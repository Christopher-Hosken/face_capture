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

        install_dep(["cv2", "opencv-python"])
        install_dep(["imutils", "imutils"])
        install_dep(["PIL", "PILLOW"])
        install_dep(["cmake", "cmake"])
        install_dep(["wheel", "wheel"])

        if (platform.system() == "Windows"):
            install_dep(["dlib", os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "dlib-19.22.99-cp39-cp39-win_amd64.whl")])
        elif (platform.system() == "Linux"):
            install_dep(["dlib", "dlib"])
        else:
            message = ("\n\n"
                "Your Operating System is not supported. Sorry!\n"
            )
            raise Exception(message)

        return {"FINISHED"}


def install_dep(dep):
    try:
        __import__ (dep[0])
    except ImportError:
        subprocess.call([py_exec, "-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", dep[1]])

classes = [InstallDependencies]