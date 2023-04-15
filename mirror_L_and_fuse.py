#Blender 2.8 plugin
#Adapted Script from    https://blender.stackexchange.com/questions/74949/
#                       applying-lots-of-shape-keys-with-blends-using-python-not-working-also-is-there
#
#Original by Opponent019; adaptation by KosmicTeal

import bpy
 
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

        
#Hard-coded exceptions
bpy.data.shape_keys[shapeKeySetName].key_blocks["wink"].name = "blink"          #winkL + winkR
bpy.data.shape_keys[shapeKeySetName].key_blocks["wink_happy"].name = "smile"    #wink_smileL + wink_smileR
