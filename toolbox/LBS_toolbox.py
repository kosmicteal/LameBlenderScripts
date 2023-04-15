bl_info = {
    "name": "LBS Toolbox",
    "description": "Set of all LameBlenderScripts joined into a single Panel",
    "author": "KosmicTeal (kosmicteal.github.io)",
    "version": (1, 0, 0),
    "blender": (2, 90, 0),
    "location": "3D View > Tool",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "https://github.com/kosmicteal/LameBlenderScripts/blob/main/README.md#credits-and-code-adapted-from",
    "category": "3D View"
}


import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       AddonPreferences,
                       )

import bgl

import blf

import math

# ------------------------------------------------------------------------
#    Special Functions
# ------------------------------------------------------------------------

##Parent Bone In Order: DRAW BONE ORDER
def draw_callback_px(self, context):
    font_id = 0 
    blf.color(font_id,1,1,1,1)
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, " / ".join([b.name for b in self.bones]))

##Blender: ADDON PREFERENCES PANEL WHEN INSTALLING
class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__


    def draw(self, context):
        layout = self.layout
        layout.label(text="Full credits available on Documentation", icon ="INFO")

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):


    PIO_bone_rename: StringProperty(
        name="Rename",
        description="Rename all these bones consecutively. Leave empty if you don't want to rename the bones.",
        default="",
        maxlen=1024,
        )
    
    PIO_bool_status: BoolProperty(
        name="PIO status",
        default = False,
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
########################################## Mirror L and Fuse
class lbs_mirrorLandFuse(Operator):
    bl_label = "Mirror .L and Fuse"
    bl_idname = "lbs.mirrorlandfuse"
    #Only available in Object mode
    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")
    
    def execute(self, context):
        obj = bpy.context.object
        spIndex = obj.active_shape_key_index
        shapeKeySetName = bpy.context.object.active_shape_key.id_data.name
        i = 0

        ### EDITABLE VARIABLES ###
        shapekeysList = []

        for sp in obj.data.shape_keys.key_blocks:
            shapekeysList.append(sp)
            sp.value = 0
            i += 1

        i = spIndex
        x = 0
        skOR = len(shapekeysList)


        while i < skOR:
            shapekeysList[i].value = 1                                              # enable shapekey before copying
            obj.active_shape_key_index = i                                          # select shape key to mix
            
            if str(obj.active_shape_key.name).endswith(".L"):
                #first mirroring the left one
                newname = str(obj.active_shape_key.name).replace(".L",".R")         #new name for the mirror
                obj.shape_key_add(name=newname, from_mix=True)   
                obj.active_shape_key_index = len(shapekeysList) + x
                bpy.ops.object.shape_key_mirror(use_topology=False)
                x += 1
                #now making a shapekey that combines both left and right
                bpy.data.shape_keys[shapeKeySetName].key_blocks[newname].value = 1 
                obj.shape_key_add(name=str(obj.active_shape_key.name).replace(".R",""), from_mix=True)   
                bpy.data.shape_keys[shapeKeySetName].key_blocks[newname].value = 0 
                x += 1
                obj.active_shape_key_index = i                                      # select original selection
            shapekeysList[i].value = 0
            i += 1

                
        #Hard-coded exceptions, checks before changing name if they exist
        if "wink" in bpy.data.shape_keys[shapeKeySetName].key_blocks:
            bpy.data.shape_keys[shapeKeySetName].key_blocks["wink"].name = "blink"          #winkL + winkR
        if "wink_happy" in bpy.data.shape_keys[shapeKeySetName].key_blocks:
            bpy.data.shape_keys[shapeKeySetName].key_blocks["wink_happy"].name = "smile"    #wink_smileL + wink_smileR
        
        return {'FINISHED'}
    
########################################## EasyJointing 
class lbs_EasyJointing(Operator):
    bl_label = "Create Joint between Physics"
    bl_idname = "lbs.easyjointing"
    
    #Only available in Object mode
    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")
        
    def execute(self, context):
        context = bpy.context
        selection_names = bpy.context.selected_objects

        first_element = selection_names[0].name
        second_element = selection_names[1].name

        bpy.context.scene.tool_settings.transform_pivot_point = 'MEDIAN_POINT'

        bpy.ops.view3d.snap_cursor_to_selected()

        bpy.ops.mmd_tools.joint_add()

        bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects[first_element]
        bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects[second_element]
    
        return {'FINISHED'}
    
########################################## Armature Standard to MMD
class lbs_AStoMMD(Operator):
    bl_label = "Standard MMD bone rename"
    bl_idname = "lbs.as_mmd"
    bl_context = "armature_edit"

    #Only available in Object mode
    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")
    
    def execute(self, context):
        context = bpy.context
        obj = context.object

        namelist = [
        ("spine", "下半身"),
        ("spine.002", "上半身"),
        ("spine.003", "上半身2"),
        ("spine.004", "首"),
        ("spine.005", "頭"),
        ("eye.L", "左目"),
        ("eye.R", "右目"),
        ("shoulder.L", "左肩"),
        ("upper_arm.L", "左腕"),
        ("forearm.L", "左ひじ"),
        ("hand.L", "左手首"),
        ("thumb.01.L", "左親指０"),
        ("thumb.02.L", "左親指１"),
        ("thumb.03.L", "左親指２"),
        ("palm.01.L", "左人指０"),
        ("f_index.01.L", "左人指１"),
        ("f_index.02.L", "左人指２"),
        ("f_index.03.L", "左人指３"),
        ("palm.02.L", "左中指０"),
        ("f_middle.01.L", "左中指１"),
        ("f_middle.02.L", "左中指２"),
        ("f_middle.03.L", "左中指３"),
        ("palm.03.L", "左薬指０"),
        ("f_ring.01.L", "左薬指１"),
        ("f_ring.02.L", "左薬指２"),
        ("f_ring.03.L", "左薬指３"),
        ("palm.04.L", "左小指０"),
        ("f_pinky.01.L", "左小指１"),
        ("f_pinky.02.L", "左小指２"),
        ("f_pinky.03.L", "左小指３"),
        ("shoulder.R", "右肩"),
        ("upper_arm.R", "右腕"),
        ("forearm.R", "右ひじ"),
        ("hand.R", "右手首"),
        ("thumb.01.R", "右親指０"),
        ("thumb.02.R", "右親指１"),
        ("thumb.03.R", "右親指２"),
        ("palm.01.R", "右人指０"),
        ("f_index.01.R", "右人指１"),
        ("f_index.02.R", "右人指２"),
        ("f_index.03.R", "右人指３"),
        ("palm.02.R", "右中指０"),
        ("f_middle.01.R", "右中指１"),
        ("f_middle.02.R", "右中指２"),
        ("f_middle.03.R", "右中指３"),
        ("palm.03.R", "右薬指０"),
        ("f_ring.01.R", "右薬指１"),
        ("f_ring.02.R", "右薬指２"),
        ("f_ring.03.R", "右薬指３"),
        ("palm.04.R", "右小指０"),
        ("f_pinky.01.R", "右小指１"),
        ("f_pinky.02.R", "右小指２"),
        ("f_pinky.03.R", "右小指３"),
        ("thigh.L", "左足"),
        ("shin.L", "左ひざ"),
        ("foot.L", "左足首"),
        ("toe.L", "左足先EX"),
        ("thigh.R", "右足"),
        ("shin.R", "右ひざ"),
        ("foot.R", "右足首"),
        ("toe.R", "右足先EX"),
        ("foot.IK.L", "左足ＩＫ"),
        ("toe.IK.L", "左つま先ＩＫ"),
        ("foot.IK.R", "右足ＩＫ"),
        ("toe.IK.R", "右つま先ＩＫ"),
        ]


        for n in namelist:
            # get the pose bone with name
            pb = obj.pose.bones.get(n[0])
            # continue if no bone of that name
            if pb is None:
                continue
            # rename
            pb.name = n[1]
        
        return {'FINISHED'}
########################################## Parent in Order 
class lbs_ParentInOrderSTART(Operator):
    bl_label = "Start selecting bones"
    bl_idname = "lbs.parentorder_start"

    #Only available in Edit Armature mode and when the process hasn't started
    @classmethod
    def poll(cls, context):
        return (not context.scene.my_tool.PIO_bool_status) and (context.mode == "EDIT_ARMATURE")
        
    def modal(self, context, event):
        context.area.tag_redraw()

        #Escape here allows to stop, but you can also do it from any other property from your addon
        if context.scene.my_tool.PIO_bool_status == False:
            #Cancel if list is empty
            if not self.bones:
                bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                return {'CANCELLED'}
            
            number = len(self.bones)
            newname = context.scene.my_tool.PIO_bone_rename #Bone renaming
            
            #Make tails and heads connected
            while number > 1:
                self.bones[number-1].tail = self.bones[number-2].head

                print("Connect ", self.bones[number-1].name, " with ", self.bones[number-2].name)
                number = number - 1
            
            #Start parenting
            number = 0
            while number < len(self.bones)-1:
                self.bones[number].parent = self.bones[number+1]
                self.bones[number].use_connect = True 
                #Rename
                if newname != "":
                    self.bones[number].name = newname + "." + ("%03d" % (len(self.bones)- 1 -number))
                number = number + 1
            #Last one gets the final rename
            self.bones[len(self.bones)-1].name = newname + ".000"
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        #Last selected is first in this way of coding
        self.bones = [b for b in context.selected_bones if b not in self.bones] + [b for b in self.bones if b in context.selected_bones]

        #Return PASS_THROUGH in order to allow Blender interpret the events
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.scene.my_tool.PIO_bool_status = True
        #Check the context for 'EDIT_ARMATURE'
        if context.area.type == 'VIEW_3D' and context.mode == 'EDIT_ARMATURE':
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')

            #Empty bones at the beginning
            self.bones = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

        return {'FINISHED'}
    
class lbs_ParentInOrderEND(Operator):
    bl_label = "Parent selected bones"
    bl_idname = "lbs.parentorder_end"
    
    #Only available in Edit Armature mode and when the process has started    
    @classmethod
    def poll(cls, context):
        return context.scene.my_tool.PIO_bool_status and (context.mode == "EDIT_ARMATURE")
    
    def execute(self, context):
        print("Parent In Order Plugin End")
        context.scene.my_tool.PIO_bool_status = False

        return {'FINISHED'}

########################################## Invert Bone Tail
class lbs_InvertTail(Operator):
    bl_idname = "lbs.inverttail"
    bl_label = "Invert bone tail (Z axis)"
    bl_options = {'REGISTER', 'UNDO'}  

    #Only available in Edit Armature mode   
    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_ARMATURE"
        
    def execute(self, context):
        selectedbones = bpy.context.selected_bones
        
        for bone in selectedbones:
            result = math.fabs(bone.head[2] - bone.tail[2])
            if bone.head[2] < bone.tail[2]:
                bone.tail[2] = bone.head[2] - math.fabs(bone.head[2] - bone.tail[2])
            else:
                bone.tail[2] = bone.head[2] + math.fabs(bone.head[2] - bone.tail[2])

        return {'FINISHED'}            

# ------------------------------------------------------------------------
#    Menus
# ------------------------------------------------------------------------

class LBS_MT_Menu(bpy.types.Menu):
    bl_label = "Select"
    bl_idname = "LBS_MT_Menu"

    def draw(self, context):
        layout = self.layout

        # Built-in operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class LBS_PT_Panel(Panel):
    bl_label = "LBS Toolbox"
    bl_idname = "LBS_PT_Panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tool"  


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout

        
class LBS_PT_SHK(bpy.types.Panel):
    bl_parent_id = "LBS_PT_Panel"
    bl_label = "Shape Keys"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tool"  

    def draw(self, context):
        layout = self.layout
        layout.operator("lbs.mirrorlandfuse", icon ="MOD_MIRROR")
        
class LBS_PT_BON(bpy.types.Panel):
    bl_parent_id = "LBS_PT_Panel"
    bl_label = "Bones"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        mtoon_preview_box = self.layout.box()
        mtoon_preview_box.label(text="Parent Bone In Order", icon = "BONE_DATA")
        mtoon_preview_box.prop(mytool, "PIO_bone_rename")
        mtoon_preview_box.operator("lbs.parentorder_start", icon= "TRACKING_FORWARDS")
        mtoon_preview_box.operator("lbs.parentorder_end", icon = "LIBRARY_DATA_DIRECT")
        #layout.separator()
        layout.operator("lbs.inverttail", icon ="FILE_REFRESH")
        layout.operator("lbs.as_mmd", icon ="OUTLINER_OB_FONT")

class LBS_PT_MMD(bpy.types.Panel):
    bl_parent_id = "LBS_PT_Panel"
    bl_label = "MMD Tools"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tool"   

    def draw(self, context):
        layout = self.layout
        warningboxMMD = self.layout.box()
        warningboxMMD.label(text="This requires having mmd_tools", icon="ERROR")
        warningboxMMD.label(text=" installed to work!")
        layout.operator("lbs.easyjointing", icon ="MESH_CUBE")

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    lbs_mirrorLandFuse,
    lbs_EasyJointing,
    lbs_AStoMMD,
    lbs_ParentInOrderSTART,
    lbs_ParentInOrderEND,
    lbs_InvertTail,
    LBS_MT_Menu,
    LBS_PT_Panel,
    LBS_PT_SHK,
    LBS_PT_BON,
    LBS_PT_MMD
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
