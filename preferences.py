import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, FloatProperty, FloatVectorProperty, IntProperty

class CrowdManager_Preferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.operator("facecapture.install_deps")

classes = [CrowdManager_Preferences]