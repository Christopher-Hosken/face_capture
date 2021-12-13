import bpy
from bpy.types import Panel

class FACECAPTURE_PT_Panel(Panel):
    bl_label = "Face Capture"
    bl_idname = "PANEL_PT_FaceCapture"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        wm = context.window_manager
        
        layout = self.layout
        row = layout.row()
        row.operator('facecapture.live_detect', text='Start Live Capture', icon='OUTLINER_OB_CAMERA')
        
        layout = self.layout
        row = layout.row()
        row.prop(wm.facecapture_props, 'video_footage')
        split = row.split(factor=0.85)
        col = split.column()
        col.operator('facecapture.video_detect', text='Run Footage Capture', icon='OUTLINER_OB_CAMERA')

def message_box(msg = "", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=msg)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

classes = [FACECAPTURE_PT_Panel]