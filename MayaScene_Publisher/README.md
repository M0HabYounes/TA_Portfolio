# MayaScene_Publisher

**MayaScene_Publisher** is a simple yet powerful script designed to optimize the process of saving and organizing Maya files within a 3D production pipeline. Initially created for The Crew studio, the tool simplifies the task of saving Maya scenes to the appropriate directory for CG departments after creating layouts and camera tracking. It automatically organizes files, ensuring that each Maya scene is stored in the correct subfolder, saving time and effort in managing project assets.

---

## Features

### **1. Maya Scene Organization**
- **Publish** button: The script searches the current Maya scene's save path, identifies the project folder, and then navigates to the correct `3D` folder, creating subfolders based on the scene, shot, and version.
- It automatically saves the Maya scene to a structured path:
  - **Path Example**: `/projectName/3D/scenes/Sc_01/Sh_010/projectName_Sc01_Sh010_v01.mb`
  
### **2. Playblast Creation**
- Select a camera, press the "Create Playblast" button, and it automatically generates a 1920x1080 playblast.
- Playblasts are saved in a folder called `previews`, making it easy to review early animation tests.
  - **Playblast Path**: `/projectName/MatchmoveData/previews`
- The script also supports versioning for multiple playblasts and has an option to open the preview folder for quick access.

### **3. Supports Multiple Project Types**
- **Series**: Handles sequences or episodes (e.g., `Ep_01`, `Sc_01`, `Sh_010`).
- **Movies & Commercials**: The tool is flexible for any project type, adapting to different folder structures.
  
---

## How It Works

The **MayaScene_Publisher** script works by scanning the current scene's directory path, locating the parent project folder, and then navigating through the folder structure to find the **3D** directory. Once located, it organizes files based on the scene, shot, and version.

```python
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


  ```
### Example File Path Structure:
- `/projectName/MatchmoveData/For_3D/Maya_File/projectName_Sc01_Sh010_v01`
- `3D Folder Path`: `/projectName/3D/scenes/Sc_01/Sh_010/projectName_Sc01_Sh010_v01.mb`

- File name: `projectName_Sc01_Sh010_v01.mb`
- **Parts**: `[u'projectName', u'Sc01', u'Sh010', u'v01.mb']`
- Formatted Episode: `None`
- Formatted Sequence: `Sc_01`
- Extracted Shots: `[u'Sh_010']`
- 3D folder path: `projectName\3D`

The script then automatically creates the necessary subfolders and copies the Maya scene file to the correct location in the **3D** folder structure. This process is designed to be quick and efficient, saving significant time compared to manually creating folders and copying files.

### Example Directory Structure:
- `projectName/3D/scenes/Sc_01/Sh_010/projectName_Sc01_Sh010_v01.mb`

---

## Special Features for Series Projects

For series projects, the tool also supports episode-specific organization. It detects and formats the episode and sequence names correctly.

### Example:
- File name: `projectName_Ep01_Sc05_Sh010_v01.mb`
- **Parts**: `[u'projectName', u'Ep01', u'Sc05', u'Sh010', u'v01.mb']`
- Formatted Episode: `Ep_01`
- Formatted Sequence: `Sc_05`
- Extracted Shots: `[u'Sh_010']`
- 3D folder path: `projectName\3D`

---

## Requirements

- **Maya**: The script is compatible with Maya 2017 and above.
- **Python 2.7+**: The script uses Python to execute functions.

