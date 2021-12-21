from bpy.types import PropertyGroup
from bpy.props import StringProperty


class FaceCapture_UL_Properties(PropertyGroup):
    video_footage: StringProperty(
        name='Video Footage',
        description='Path to video footage',
        default='',
        subtype='FILE_PATH'
    )

    window_name: StringProperty(
        name="Window Name",
        default="Live Capture"
    )


classes = [FaceCapture_UL_Properties]
