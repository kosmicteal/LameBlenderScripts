#Blender 2.8 plugin
#
#
#Original by KosmicTeal

import bpy
context = bpy.context
selection_names = bpy.context.selected_objects

first_element = selection_names[0].name
second_element = selection_names[1].name

bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'

bpy.context.area.type = 'VIEW_3D'
bpy.ops.view3d.snap_cursor_to_selected()

bpy.ops.mmd_tools.joint_add()

bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects[first_element]
bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects[second_element]

bpy.context.area.type = 'TEXT_EDITOR'
