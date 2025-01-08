import maya.cmds as cmds
import os
import fnmatch
import re
import shutil


def get_shot_info():
    # Get the current Maya scene file name
    scene_name = cmds.file(q=True, sceneName=True, shortName=True)
    print("Scene Name:", scene_name)

    # Split the file name into parts
    parts = scene_name.split('_')
    print("Parts:", parts)

    # Regular expression patterns for episode and sequence
    episode_pattern = re.compile(r'^(EP|Ep|ep)(\d+)$')
    sequence_pattern = re.compile(r'^(Sc|sc)(.*)$')

    # Initialize indices
    episode_index = None
    seq_index = None

    # Find the index of the episode and sequence using regular expressions
    for i, part in enumerate(parts):
        if episode_pattern.match(part):
            episode_index = i
        elif sequence_pattern.match(part):
            seq_index = i

    # Extract the episode if present
    episode = parts[episode_index][:2] + '_' + parts[episode_index][2:] if episode_index is not None else None

    # Extract the sequence if present
    sequence = None
    if seq_index is not None:
        sequence_part = parts[seq_index]
        if sequence_part.strip().lower() == 'sc' and seq_index + 1 < len(parts):
            sequence = sequence_part + '_' + parts[seq_index + 1]
            print sequence

        else:
            sequence = sequence_part[:2] + '_' + sequence_part[2:]
            print sequence

    print("Formatted Episode:", episode)
    print("Formatted Sequence:", sequence)

    # Determine the starting index for extracting shots
    start_index = seq_index + 1 if seq_index is not None else (episode_index + 1 if episode_index is not None else 0)

    # Extract shots
    shots = []
    for i, part in enumerate(parts[start_index:]):
        if part.lower().startswith('sh'):
            shot_parts = [part]  # Start with the current part

            # Check the next part for the version
            if i + start_index + 1 < len(parts):
                next_part = parts[i + start_index + 1]

                # Check if the next part is a version number

                if re.match(r'_v\d+$', next_part):  # Ensure it matches only version patterns
                    shots.append(part)  # Append the shot name only

                else:
                    # Otherwise, continue collecting parts for the shot name
                    for next_part in parts[i + start_index + 1:]:
                        # Stop collecting if we hit a version number or keyword
                        if re.match(r'_v\d+$', next_part) :
                            break  # Stop collecting if we hit a version number or keyword
                        if next_part.endswith('.mb'):
                            break  # Stop if we hit the file extension

                        shot_parts.append(next_part)  # Add the next part to the shot

                    # Format the shot name and add to the list
                    shots.append('_'.join(shot_parts))  # Join all parts collected in shot_parts

    # Remove duplicates while preserving order
    shots = list(dict.fromkeys(shots))
    for index, shot in enumerate(shots):
        if shot.startswith('Sh') and (len(shot) < 3 or shot[2] != '_'):
            shots[index] = re.sub(r'^(Sh)(?!_)', r'\1_', shot)

    print("Extracted Shots:", shots)

    if not shots:
        cmds.warning("No shot information found in the file name!")
        return None, None, None

    return episode, sequence, shots


def get_preview_info():
    scene_name = cmds.file(q=True, sceneName=True, shortName=True)

    # Split by underscores
    parts = scene_name.split('_')

    # Initialize variables to store episode, sequence, and shots
    episode_name = ""
    sequence_name = ""
    shot_names = []

    # Loop through the parts and find episode, sequence, and shot(s)
    for part in parts:
        if part.lower().startswith("ep"):  # Identify the episode
            episode_name = part
        elif part.lower().startswith("sc"):  # Identify the sequence
            sequence_name = part
        elif part.lower().startswith("sh"):  # Identify the shots
            shot_names.append(part)

    # Combine the extracted parts
    if episode_name and sequence_name and shot_names:
        shot_name = "_".join(shot_names)  # Concatenate all shot names
        result_name = "{}_{}_{}".format(episode_name, sequence_name, shot_name)
    else:
        print("Could not extract episode, sequence, or shots from the file name.")

    return result_name


def get_next_version_preview(base_dir, result_name):
    """
    Check for existing files with the same name and return the next available version.
    """
    # List all files in the base directory
    files_in_dir = os.listdir(base_dir)

    # Find all files that match the result_name pattern
    matching_files = fnmatch.filter(files_in_dir, "{}_preview_v*.mov".format(result_name))

    if matching_files:
        # Extract the highest version number from the existing files
        version_numbers = [int(f.split('_v')[-1].split('.')[0]) for f in matching_files]
        next_version = max(version_numbers) + 1
    else:
        next_version = 1

    return next_version


def find_3d_directory(start_dir):
    """
    Traverses upward from the start directory to find a directory named '3D'.
    Uses fnmatch for case-insensitive matching. Returns the path of the found
    '3D' directory or None if not found.
    """
    current_dir = start_dir

    # Loop until we reach the root directory
    while True:
        # List all directories in the current path
        dir_list = os.listdir(current_dir)

        # Use fnmatch to search for '3D' in the list of directories (case-insensitive)
        matched_dirs = fnmatch.filter(dir_list, '3d')

        if matched_dirs:
            found_folder_path = os.path.join(current_dir, matched_dirs[0])
            print("3D folder found at:", found_folder_path)
            return found_folder_path

        # Move up to the parent directory
        parent_dir = os.path.dirname(current_dir)

        # If we've reached the root (no parent), exit the loop
        if parent_dir == current_dir:
            break

        # Update the current directory to the parent directory
        current_dir = parent_dir

    print("3D folder not found in any parent directories.")
    return None


def find_preview_directory(start_dir):
    """
    Traverses upward from the start directory to find a directory named '3D'.
    Uses fnmatch for case-insensitive matching. Returns the path of the found
    '3D' directory or None if not found.
    """
    current_dir = start_dir

    # Loop until we reach the root directory
    while True:
        # List all directories in the current path
        dir_list = os.listdir(current_dir)

        # Use fnmatch to search for '3D' in the list of directories (case-insensitive)
        matched_dirs = fnmatch.filter(dir_list, 'previews')

        if matched_dirs:
            found_folder_path = os.path.join(current_dir, matched_dirs[0])
            print("preview folder found at:", found_folder_path)
            return found_folder_path

        # Move up to the parent directory
        parent_dir = os.path.dirname(current_dir)

        # If we've reached the root (no parent), exit the loop
        if parent_dir == current_dir:
            break

        # Update the current directory to the parent directory
        current_dir = parent_dir

    print("preview folder not found in any parent directories.")
    return None

def create_playblast(*args):  # Accept *args to handle the button command
    selected_objects = cmds.ls(selection=True)

    if not selected_objects:
        cmds.warning("No objects selected.")
        return

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
        return

    camera_name = selected_camera
    # Get the parent transform of the camera
    parent_transform = cmds.listRelatives(camera_name, parent=True)
    if parent_transform:
        parent_name = parent_transform[0]
    else:
        parent_name = None

    keyframes = cmds.keyframe(camera_name, query=True)

    if cmds.checkBox("CustomFrameRangeCheckBox", query=True, value=True):

        # Get start and end frames from text fields
        try:
            start_frame = int(cmds.textField(start_frame_field, query=True, text=True))
            end_frame = int(cmds.textField(end_frame_field, query=True, text=True))
        except ValueError:
            cmds.warning("Invalid frame numbers entered.")
            return
    elif keyframes:
        # Find the start and end keyframe times
        start_frame = int(min(keyframes))
        end_frame = int(max(keyframes))
    else:
        cmds.warning("No keyframes found on the camera.")
        return

    result_name = re.sub(r'_[^_]+$', '', camera_name)  # Remove the last segment after the last underscore

    # Get the current Maya file directory
    current_file_path = cmds.file(q=True, sceneName=True)

    if not current_file_path:
        cmds.warning("No file is currently saved.")
        return

    current_file_dir = os.path.dirname(current_file_path)

    # Search for the "preview" folder by going up the directory tree
    base_dir = find_preview_directory(current_file_dir)

    if not base_dir:
        cmds.warning('Could not find "preview" directory!')
        return

    # Get the next available version number
    next_version = get_next_version_preview(base_dir, result_name)
    version_str = "v{:02d}".format(next_version)  # Format the version as v01, v02, etc.

    # Set the playblast filename with the next available version
    preview_file = "{}_preview_{}.mov".format(result_name, version_str)
    playblast_file = os.path.join(base_dir, preview_file)

    print("Playblast will be saved to: {}".format(playblast_file))  # Debug output

    # Set the playblast settings
    cmds.playblast(
        format='qt',  # Set the format to QuickTime
        filename=playblast_file,  # Specify the output filename
        forceOverwrite=True,  # Allow overwriting of existing files
        sequenceTime=0,  # Set the sequence time
        clearCache=True,  # Clear the cache before creating the playblast
        viewer=True,  # Show the viewer after creation
        showOrnaments=True,  # Show ornaments (UI elements) in the playblast
        fp=4,  # Frame padding
        percent=100,  # Set the percentage of the image quality
        compression="MPEG-4 Video",  # Set the compression type
        quality=100,  # Set the quality to maximum
        widthHeight=(1920, 1080),  # Set the resolution
        startTime=start_frame,  # Specify the start frame
        endTime=end_frame  # Specify the end frame
    )

    # Check if the playblast file was created
    if os.path.exists(playblast_file):
        cmds.confirmDialog(title="Playblast", message="Playblast created at: {}".format(playblast_file), button="OK")
    else:
        cmds.warning("Playblast failed to save. Please check the output path.")


def publish_file(*args):
    # Get the episode, sequence, and shots
    episode, sequence, shots = get_shot_info()

    if not shots:
        cmds.warning("Invalid shot names!")
        return

    # Get the current Maya file directory
    current_file_path = cmds.file(q=True, sceneName=True)

    if not current_file_path:
        cmds.warning("No file is currently saved.")
        return

    current_file_dir = os.path.dirname(current_file_path)

    base_dir = find_3d_directory(current_file_dir) + "/scenes"

    if not base_dir:
        cmds.warning('Could not find the appropriate directory!')
        return

    base_dir = os.path.join(base_dir, episode)

    # Ensure the base directory exists before proceeding
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

        """ 
        ## Special Case for "Z" Directory ##
        # In certain projects, files need to be published to a separate directory, 
        # and this case handles the adaptation to that scenario by choosing 
        # between the Z and Y directories.
        """


        if "Z" in current_file_dir:
            # Ask the user whether to publish to the Z directory or the Y directory
            result = cmds.confirmDialog(
                title="Choose Directory",
                message="You are in the Z directory. Do you want to publish to the Z directory or the Y directory?",
                button=["Z Directory", "Y Directory"],
                defaultButton="Z Directory",
                cancelButton="Y Directory",
                dismissString="dismiss"
            )

            # If user selects "Y Directory", update the base directory path accordingly
            if result == "Y Directory":
                base_dir = find_3d_directory(current_file_dir) + "/scenes"
                base_dir = base_dir.replace("Z", "Y")  # Replace Z with Y in the path

            else:
                # If user stays in the "Z Directory", keep the base directory as is
                base_dir = find_3d_directory(current_file_dir) + "/scenes"

    if sequence:
        base_dir = os.path.join(base_dir, sequence)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

    # Create shot folder(s) inside the last valid directory
    shot_name = "_".join(shots)  # Concatenate shots if there are multiple
    shot_folder = os.path.join(base_dir, shot_name)
    if not os.path.exists(shot_folder):
        os.makedirs(shot_folder)

    # Get the original file name
    original_file_name = os.path.basename(current_file_path)
    save_path = os.path.join(shot_folder, original_file_name)

    # Check if the file already exists
    if os.path.exists(save_path):
        result = cmds.confirmDialog(
            title="File Exists",
            message="The file already exists. Do you want to overwrite it?",
            button=["Yes", "No"],
            defaultButton="No",
            cancelButton="No",
            dismissString="No"
        )

        if result == "No":
            cmds.warning("File not saved.")
            return

    # Copy the Maya file into the shot folder
    shutil.copy2(current_file_path, save_path)

    result = cmds.confirmDialog(
        title="Publish",
        message="File copied to: {}".format(save_path),
        button=["Ok", "Open Folder"],
        defaultButton="OK",
        cancelButton="OK",
        dismissString="OK"
    )

    # Check which button was pressed
    if result == "Open Folder":
        # Open the file path in the default file explorer
        if os.name == 'nt':  # For Windows
            os.startfile(shot_folder)

def open_preview_folder(*args):
    """Opens the preview folder in the file explorer."""
    current_file_path = cmds.file(q=True, sceneName=True)
    if not current_file_path:
        cmds.warning("No file is currently saved.")
        return

    current_file_dir = os.path.dirname(current_file_path)
    preview_dir = find_preview_directory(current_file_dir)

    if preview_dir:
        # Open the folder in the file explorer (works for Windows)
        os.startfile(preview_dir)
    else:
        cmds.warning('Could not find "preview" directory!')


def create_ui():
    """Creates a window for publishing the Maya scene."""
    global start_frame_field, end_frame_field  # Declare global variables for the frame fields
    window_name = "publishWindow"  # Name of the window

    # Check if the window already exists and delete it
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    # Create the window with increased width
    cmds.window(window_name, title="Publish Maya Scene", widthHeight=(500, 400))  # Increased width to 500

    cmds.columnLayout(adjustableColumn=True)

    cmds.separator(height=10, style="none")  # Add a separator for better spacing

    cmds.text(label="Publish your Maya scene to the appropriate folder.", align="center", font="boldLabelFont")

    cmds.separator(height=10, style="none")  # Add a separator for better spacing

    # Button for publishing the file
    cmds.button(label="Publish", command=publish_file, backgroundColor=(0.161, 0.161, 0.161))
    cmds.separator(height=10, style="none")  # Separator after the publish button

    # Title label for the playblast section
    cmds.text(label="Playblast Options", align="center", font="boldLabelFont")
    cmds.separator(height=5, style="none")  # Small separator for spacing

    # Button for creating a playblast
    cmds.button(label="Create Playblast", command=create_playblast, backgroundColor=(0.161, 0.161, 0.161))

    cmds.separator(height=10, style="none")  # Separator after the playblast button

    # Checkbox for custom frame range
    cmds.checkBox("CustomFrameRangeCheckBox", label="Custom Frame Range", changeCommand=toggle_frame_range)
    cmds.separator(height=10, style="none")  # Separator after the checkbox

    # Frame range inputs (initially disabled)
    cmds.text(label="Start Frame:")
    start_frame_field = cmds.textField(enable=False)  # Start frame text field, disabled by default
    cmds.text(label="End Frame:")
    end_frame_field = cmds.textField(enable=False)  # End frame text field, disabled by default

    cmds.separator(height=10, style="none")  # Separator after the frame fields

    # Button to open the preview folder
    cmds.button(label="Open Preview Folder", command=open_preview_folder, backgroundColor=(0.161, 0.161, 0.161))
    cmds.separator(height=10, style="none")  # Separator after the open preview folder button

    cmds.showWindow(window_name)


def toggle_frame_range(checked):
    """Toggle the sensitivity of the frame range fields based on checkbox state."""
    # Enable/disable frame range fields based on checkbox state
    cmds.textField(start_frame_field, edit=True, enable=checked)
    cmds.textField(end_frame_field, edit=True, enable=checked)


create_ui()