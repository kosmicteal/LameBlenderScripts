# LameBlenderScripts
![](https://img.shields.io/badge/number%20of%20plugins-5-lightgrey) ![](https://img.shields.io/badge/intended%20for-Blender-orange) ![GitHub all releases](https://img.shields.io/github/downloads/KosmicTeal/LameBlenderScripts/total)
![](https://github.com/kosmicteal/LameBlenderScripts/blob/main/03_LameBlenderScripts.png)

## Credits and code adapted from
All extra code has been done by me with adaptations from:
* **Blender UI interface** : [p2or](https://blender.stackexchange.com/users/3710/p2or) and [brockmann](https://blender.stackexchange.com/users/31447/brockmann)
* **Mixing shapekeys**: [Opponent019](https://blender.stackexchange.com/users/13951/opponent019)
* **Rename bones**: [batFINGER](https://blender.stackexchange.com/users/15543/batfinger)
* **Select bones in order**: [Lemon](https://blender.stackexchange.com/users/19156/lemon)

## Main add-on
* **LBS Toolbox** : Includes all the next plugins inside its own Panel (View3D -> Tool).
  * **How it works?**: Download the LBS_toolbox.py file located on the "toolbox" folder, go to Blender -> Edit -> Preferences -> Add-ons -> Install and select the .py file.

* **Main changes between the Add-on versions and the Script ones**: 
   * They all work in buttons and they are grouped in sub-panels
   * Each button disables itself if it's in a mode that it can't work
   * (OBJECT MODE) mirror_L_and_Fuse now avoids throwing an error
   * (OBJECT MODE) ArmatureStandard now requires you to be on Object mode
   * (OBJECT MODE) EasyJointing doesn't require you to be in Scripting mode anymore
   * (EDIT ARMATURE MODE) Parent in Order now can rename bones in order if necessary
   * (EDIT ARMATURE MODE) Tail Inverter now requires you to be on Object mode

## Toolbox Scripts
* **mirror_L_and_fuse**: Grabs all shapekeys that end with ".L", duplicates+mirrors them renaming those to ".R" and creates another that fuses both variations a-la-MMD where you would have "joy.L", "joy.R" and "joy" (which is joy.R+joy.L). Created at 1:26 AM with no python OR blender API knowledge so it's just unoptimized as heck. Adapted from https://blender.stackexchange.com/questions/74949/applying-lots-of-shape-keys-with-blends-using-python-not-working-also-is-there
  * **How it works?**: Just grab your desired object, select the Basis shapekey and run the script. Voilá!
  
* **ArmatureStandard_to_MMD**: Renames all bones into its MMD variation (aka translated into Japanese). Also renames Vertex Groups related to those bones. Who the frick thought it was OK for MMD to have a different bone standard system btw? Adapted from https://blender.stackexchange.com/questions/69505/renaming-bones-with-python
  * **How it works?**: First verse same as second verse: just grab your desired object and run the script.
  
* **EasyJointing_mmd_tools**: This is more of a macro than a script but meh, it works
  * **How it works?**: Install [mmd_tools](https://github.com/powroupi/blender_mmd_tools) for your Blender distribution, then in Scripting mode, select two rigid bodies and it'll make a Joint between those two, useful for skirts, capes and related.

* **Parent In Order**: Parents bones in order of selection, adapted from https://blender.stackexchange.com/questions/76480/how-to-get-the-selected-bones-selected-order-in-python-api . Includes a tail-inverter add-on. 
  * **How it works?**: Select bones in the order you want them to be parented, then press ESC to join those. Both this and the tail inverter work in Edit Armature mode.
