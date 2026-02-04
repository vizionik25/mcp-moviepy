from moviepy import Effect
import numpy as np
import cv2

class RotatingCube(Effect):
    """
    Simulates a 3D rotating cube effect where the video is mapped to the faces.
    Can rotate horizontally or vertically at a specified speed.
    """
    def __init__(self, speed: float = 45, direction: str = "horizontal", zoom: float = 1.0):
        """
        Args:
            speed (float): Rotation speed in degrees per second.
            direction (str): 'horizontal' (around Y axis) or 'vertical' (around X axis).
            zoom (float): Zoom factor. Higher values make the cube appear closer.
        """
        self.speed = speed
        self.direction = direction.lower()
        self.zoom = zoom

    def apply(self, clip):
        def filter(get_frame, t):
            frame = get_frame(t)
            h, w = frame.shape[:2]
            
            # Current rotation angle
            angle = (self.speed * t) % 360
            
            # Perspective parameters
            focal_length = max(w, h) * self.zoom
            dist = max(w, h) / 2 # Distance from center to faces
            
            # Canvas to draw faces
            canvas = np.zeros_like(frame)
            
            # We'll render 4 faces of the cube in the rotation plane
            face_angles = [0, 90, 180, 270]
            
            # Sort faces by distance (depth) to the viewer if needed, 
            # but for 90-deg faces, simple maximum/masking works.
            # We only render faces that are in front of the camera (abs < 90)
            
            for face_angle in face_angles:
                # Relative angle of the face to the camera
                # Camera is at 'angle', face is at 'face_angle'
                rel_angle = (face_angle - angle + 180) % 360 - 180
                
                # Only faces within the forward 180 degrees are potentially visible
                if abs(rel_angle) > 90:
                    continue
                
                rad = np.deg2rad(rel_angle)
                
                # Define corners of the face at (0, 0, dist)
                # Face size matches original clip size
                c3d = np.array([
                    [-w/2, -h/2, dist],
                    [w/2, -h/2, dist],
                    [w/2, h/2, dist],
                    [-w/2, h/2, dist]
                ])
                
                # Rotation Matrix
                if self.direction == "horizontal":
                    # Pan around Y axis
                    cos_a, sin_a = np.cos(rad), np.sin(rad)
                    rot_m = np.array([
                        [cos_a, 0, sin_a],
                        [0, 1, 0],
                        [-sin_a, 0, cos_a]
                    ])
                else:
                    # Tilt around X axis
                    cos_a, sin_a = np.cos(rad), np.sin(rad)
                    rot_m = np.array([
                        [1, 0, 0],
                        [0, cos_a, -sin_a],
                        [0, sin_a, cos_a]
                    ])
                
                # Apply rotation to corners
                rotated_c3d = c3d @ rot_m.T
                
                # Project 3D points to 2D
                points_2d = []
                visible = True
                for x, y, z in rotated_c3d:
                    # Perspective projection: x' = (x * f) / z
                    # Offset by w/2, h/2 to center on screen
                    if z <= 0.1: # Point is behind or too close to camera
                        visible = False
                        break
                    px = (x * focal_length / z) + w/2
                    py = (y * focal_length / z) + h/2
                    points_2d.append([px, py])
                
                if not visible:
                    continue
                
                # Perform perspective warp
                src_pts = np.array([[0,0], [w,0], [w,h], [0,h]], dtype=np.float32)
                dst_pts = np.array(points_2d, dtype=np.float32)
                
                M = cv2.getPerspectiveTransform(src_pts, dst_pts)
                face_img = cv2.warpPerspective(frame, M, (w, h))
                
                # Merge face into canvas
                # We use bitwise_or or maximum for simple compositing
                # A proper depth buffer would be better for complex 3D, 
                # but for a cube this works well.
                canvas = np.maximum(canvas, face_img)
            
            return canvas

        return clip.transform(filter)
