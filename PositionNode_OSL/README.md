# OSL Shader: PositionNode

## Overview

This project is my first dive into shading languages, especially OSL (Open Shading Language). It's been a challenging yet rewarding journey, helping me understand shading and procedural texturing basics.

The script currently works as an OSL shader but requires implementation into Maya's Arnold API using **C++** for full functionality—a task I've just begun exploring.

## Features

1. **Position-Based Masking**:
   - Generates a black-and-white mask based on the **object's position** in space, rather than relying on UVs.

2. **Customizable Parameters**:
   - **Axis Selection**: Choose which axis (X, Y, or Z) to base the mask on.
   - **Inversion**: Invert the mask for quick toggling.
   - **Fade Control**: Adjust the fade for smooth transitions.
   - **Midpoint Adjustment**: Set the midpoint to customize the preferred mask location.

## Why This Shader?
Unlike UV-dependent ramps, this shader is **object-space-aware**, offering more control for effects like procedural texturing, masking, or environment blending.

## Current Status
- **OSL and Mathematics**: Almost complete, leveraging foundational shading concepts and equations.
- **Arnold API Integration**: In progress, with plans to transition to **C++** for deeper integration within Maya.

## Personal Reflection
This project represents a significant step in my journey as a Technical Artist. It's a blend of creative experimentation and technical learning, pushing the boundaries of what I can achieve in shading and procedural workflows.


![osl](https://github.com/user-attachments/assets/a8804377-5b8d-4f51-b421-f1011fe3c897)
