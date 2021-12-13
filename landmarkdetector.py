import bpy
import os
import cv2
import imutils
import mediapipe as mp
from imutils import face_utils
from bpy.types import Operator


class LiveLandmarkDetector(Operator):
    bl_idname = 'facecapture.live_detect'
    bl_label = 'Landmark Detector'
    bl_description = 'Detects facial landmarks from live video feed'

    _key = None
    _timer = None
    _vid = None

    def modal(self, context, event):
        # Check if the user has tried closing the live window.
        if (event.type in {'RIGHTMOUSE', 'ESC'}) == True or self._key == 27:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            self.init_vid()  # Initiate camera.
            __, image = self._vid.read()  # Read the camera feed.

            mp_face_mesh = mp.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh()

            #image = imutils.resize(image, width=480, height=320)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            result = face_mesh.process(rgb_image)

            if result.multi_face_landmarks is not None:
                for facial_landmarks in result.multi_face_landmarks:
                    for i in range(0, 468):
                        pt1 = facial_landmarks.landmark[i]
                        x = int(pt1.x * self._vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                        y = int(pt1.y * self._vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

                        cv2.circle(image, (x, y), 1, (0, 255, 255), -1)

            cv2.imshow("Live Capture", image)
            cv2.waitKey(1)
            if cv2.getWindowProperty("Live Capture", cv2.WND_PROP_VISIBLE) < 1:
                self.cancel(context)
                return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        self._key = cv2.waitKey(30) & 0xff  # Keyboard definition.
        # Add a timer.
        self._timer = context.window_manager.event_timer_add(
            0.02, window=context.window)
        context.window_manager.modal_handler_add(self)  # Run modal.
        return {'RUNNING_MODAL'}

    def init_vid(self):
        if self._vid == None:
            self._vid = cv2.VideoCapture(0)
            self._vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self._vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def cancel(self, context):
        # Remove the timer.
        context.window_manager.event_timer_remove(self._timer)
        self._vid.release()  # Stop the camera.
        self._vid = None
        cv2.destroyAllWindows()  # Destroy the live window.


class VideoLandmarkDetector(Operator):
    bl_idname = 'facecapture.video_detect'
    bl_label = 'Landmark Detector'
    bl_description = 'Detects facial landmarks from live video feed'

    def execute(self, context):
        wm = context.window_manager

        self._vid = cv2.VideoCapture(wm.facecapture_props.video_footage)
        #self._vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self._vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while (self._vid.isOpened()):

            __, image = self._vid.read()  # Read the camera feed.

            mp_face_mesh = mp.solutions.face_mesh
            face_mesh = mp_face_mesh.FaceMesh()

            #image = imutils.resize(image, width=480, height=320)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            result = face_mesh.process(rgb_image)

            if result.multi_face_landmarks is not None:
                for facial_landmarks in result.multi_face_landmarks:
                    for i in range(0, 468):
                        pt1 = facial_landmarks.landmark[i]
                        x = int(pt1.x * self._vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                        y = int(pt1.y * self._vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

                        cv2.circle(image, (x, y), 1, (0, 255, 255), -1)

            cv2.imshow("Playback", image)
            cv2.waitKey(1)
            if cv2.getWindowProperty("Playback", cv2.WND_PROP_VISIBLE) < 1:
                return {'CANCELLED'}

            key = cv2.waitKey(30) & 0xff  # Check if the esc key is pressed.
            if key == 27:
                return {'CANCELLED'}

        cv2.destroyAllWindows()
        self._vid.release()
        return {'FINISHED'}


classes = [LiveLandmarkDetector, VideoLandmarkDetector]
