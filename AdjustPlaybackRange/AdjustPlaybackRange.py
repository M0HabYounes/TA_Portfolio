import maya.cmds as cmds

def camera_frames():
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("No objects selected.")
        return None, None

    selected_camera = None

    for obj in selected_objects:
        # Check if the object is a transform node
        if cmds.nodeType(obj) == 'transform':
            # Check if the transform node has any shapes
            shapes = cmds.listRelatives(obj, shapes=True) or []

            # Look for cameras in the shapes
            cameras = [shape for shape in shapes if cmds.nodeType(shape) == 'camera']
            if cameras:
                selected_camera = cameras[0]  # Use the first camera found
                break  # Found a camera, exit the loop

    if selected_camera is None:
        cmds.warning("No camera selected.")
        return None, None

    # Get the parent transform of the camera
    parent_transform = cmds.listRelatives(selected_camera, parent=True)
    if parent_transform:
        parent_name = parent_transform[0]
    else:
        parent_name = None

    # Get the keyframes for the camera
    keyframes = cmds.keyframe(selected_camera, query=True)
    print (keyframes)
    if not keyframes:
        cmds.warning("No keyframes found for the selected camera.")
        return None, None

    # Define start and end frame based on keyframes
    start_frame = int(min(keyframes))
    end_frame = int(max(keyframes))

    return start_frame, end_frame

def set_playback_range(*args):
    # Get the start and end frames from the camera keyframes
    start_frame, end_frame = camera_frames()

    # If no valid frame range is found, do not update the playback range
    if start_frame is None or end_frame is None:
        return

    # Set the playback range using the playbackOptions command
    cmds.playbackOptions(min=start_frame, max=end_frame , animationStartTime=start_frame , animationEndTime=end_frame)

set_playback_range()

