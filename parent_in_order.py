import bpy
from bpy.types import Operator, AddonPreferences
import bgl
import blf
import math

bl_info = {
    "name": "Parent Bones In Order",
    "author": "OSformula (https://osformula.com)",
    "version": (0, 2, 4),
    "blender": (2, 90, 0),
    "location": "Edit Mode -> Armature",
    "description": "Parents bones in order of selection. Includes a tail-inverter add-on.",
    "warning": "",
    "doc_url": "https://blender.stackexchange.com/users/19156/lemon",
    "category": "Armature",
}


def draw_callback_px(self, context):
    font_id = 0 
    blf.color(font_id,1,1,1,1)
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, " / ".join([b.name for b in self.bones]))

class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__


    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Order original plugin done by Lemon @ StackOverflow.")
        layout.label(text="Link to user available on Documentation.")

class InvertBoneTail(bpy.types.Operator):

    bl_idname = "view3d.invertbonetail"
    bl_label = "Invert Bone Tail (Z axis)"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    def execute(self, context):        # execute() is called when running the operator.
        selectedbones = bpy.context.selected_bones
        
        for bone in selectedbones:
            result = math.fabs(bone.head[2] - bone.tail[2])
            if bone.head[2] < bone.tail[2]:
                bone.tail[2] = bone.head[2] - math.fabs(bone.head[2] - bone.tail[2])
            else:
                bone.tail[2] = bone.head[2] + math.fabs(bone.head[2] - bone.tail[2])

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.



class ParentBonesInOrder(bpy.types.Operator):

    bl_idname = "view3d.parentboneorder"
    bl_label = "Parent Bones In Order"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    def modal(self, context, event):
        context.area.tag_redraw()

        #Escape here allows to stop, but you can also do it from any other property from your addon
        if event.type in {'ESC'}:
            number = len(self.bones)
            while number > 1:
                self.bones[number-1].tail = self.bones[number-2].head
                print("Connect ", self.bones[number-1].name, " with ", self.bones[number-2].name)
                number = number - 1
            number = 0
            while number < len(self.bones)-1:
                self.bones[number].parent = self.bones[number+1]
                self.bones[number].use_connect = True
                number = number + 1
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        #Last selected is first in this way of coding
        self.bones = [b for b in context.selected_bones if b not in self.bones] + [b for b in self.bones if b in context.selected_bones]

        #Return PASS_THROUGH in order to allow Blender interpret the events
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        #Check the context for 'EDIT_ARMATURE'
        if context.area.type == 'VIEW_3D' and context.mode == 'EDIT_ARMATURE':
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            #Empty bones at the beginning
            self.bones = []
            #Or allready selected
            #self.bones = context.selected_bones[:]
            #Or from your data
            #self.bones = your previous selection

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

def menu_func(self, context):
    self.layout.operator(ParentBonesInOrder.bl_idname, icon = 'BONE_DATA')
    self.layout.operator(InvertBoneTail.bl_idname, icon = 'FILE_REFRESH')

def register():
    bpy.utils.register_class(ParentBonesInOrder)
    bpy.utils.register_class(InvertBoneTail)
    bpy.utils.register_class(ExampleAddonPreferences)
    bpy.types.VIEW3D_MT_edit_armature.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ParentBonesInOrder)
    bpy.utils.unregister_class(InvertBoneTail)
    bpy.utils.unregister_class(ExampleAddonPreferences)
    bpy.types.VIEW3D_MT_edit_armature.remove(menu_func)

if __name__ == "__main__":
    register()