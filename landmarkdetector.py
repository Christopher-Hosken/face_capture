import bpy
import os
import numpy as np
import cv2
import imutils
import mediapipe as mp
from imutils import face_utils
from imutils.video import WebcamVideoStream, FPS
from bpy.types import Operator
from threading import Thread

from mediapipe.python.solutions.face_mesh import FaceMesh


class LiveLandmarkDetector(Operator):
    bl_idname = 'facecapture.live_detect'
    bl_label = 'Landmark Detector'
    bl_description = 'Detects facial landmarks from live video feed'

    _vid = None
    _timer = None
    _mpdrawing = None
    _mpdrawingstyles = None
    _mpfacemesh = None
    _facemesh = None
    _facemodel = None
    _ratio = None

    def modal(self, context, event):
        if (event.type in {'ESC'}) or cv2.waitKey(30) & 0xff == 27:
            self.cancel(context)
            return {"CANCELLED"}

        if event.type == 'TIMER':
            self.init_vid()
            self.init_model()

            success, image = self._vid.read()

            if self._ratio == None:
                self._ratio = self._vid.get(cv2.CAP_PROP_FRAME_HEIGHT) / self._vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            
            if not success:
                return {'PASS_THROUGH'}

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self._facemesh.process(image)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    if (self._facemodel != None and self._facemodel != None):
                        self.update_mask(face_landmarks, self._ratio)
                    self._mpdrawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=self._mpfacemesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self._mpdrawingstyles
                        .get_default_face_mesh_tesselation_style())
                    

            cv2.imshow(context.window_manager.facecapture_props.window_name, image)
            if cv2.getWindowProperty(context.window_manager.facecapture_props.window_name, cv2.WND_PROP_VISIBLE) < 1:
                self.cancel(context)
                return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        self.init_vid()
        self.init_model()
        self._timer = context.window_manager.event_timer_add(1/100, window=context.window)
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def init_vid(self):
        if self._vid == None:
            self._vid = cv2.VideoCapture(0)

    def init_model(self):
        if self._mpdrawing == None:
            self._mpdrawing = mp.solutions.drawing_utils

        if self._mpdrawingstyles == None:
            self._mpdrawingstyles = mp.solutions.drawing_styles

        if self._facemesh == None or self._mpfacemesh == None:
            self._mpfacemesh = mp.solutions.face_mesh

            self._facemesh = self._mpfacemesh.FaceMesh(
                max_num_faces = 1,
                refine_landmarks = True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )

        if self._facemodel == None:
            bpy.ops.import_scene.obj(filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "canonical_face_model.obj"), split_mode='OFF')
            self._facemodel = bpy.context.selected_objects[0]
            print(self._facemodel)

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        self._vid.release()
        cv2.destroyAllWindows()
        self._vid = None
        self._facemesh = None
        self._mpdrawing = None
        self._mpdrawingstyles = None
        self._mpfacemesh = None
        self._ratio = None
        bpy.data.objects.remove(self._facemodel, do_unlink=True)
        self._facemesh = None

    
    def update_mask(self, face, ratio):
        mesh = bpy.data.objects.get(self._facemodel.name).data
        scale = 10
        for i in range(0, len(face.landmark) + 1):
            if (i > 467):
                continue
            v = mesh.vertices[i]
            v.co[0] = face.landmark[i].x * (1 / ratio)
            v.co[1] = face.landmark[i].z 
            v.co[2] = face.landmark[i].y

        


classes = [LiveLandmarkDetector]
