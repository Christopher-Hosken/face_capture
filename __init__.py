#
#    Copyright (C) 2022 Christopher Hosken
#    hoskenchristopher@gmail.com
#
#    Created by Christopher Hosken
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__copyright__ = "(c) 2022,  Christopher Hosken"
__license__ = "GPL v3"

bl_info = {
    "name" : "Face Capture",
    "author" : "Christopher Hosken",
    "description" : "",
    "blender" : (3, 0, 0),
    "version" : (2, 0, 0),
    "location" : "",
    "warning" : "This version is still in development.",
    "category" : "Animation"
}

from . import auto_load
from .dependencies import classes as dependency_classes
from .preferences import classes as preference_classes
from .panel import classes as panel_classes

classes = []
classes += dependency_classes
classes += preference_classes
classes += panel_classes

auto_load.init()


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    try:
        unregister()
        register()
    except Exception as e:
        print(e)
