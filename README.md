# LameBlenderScripts
some shark coded this idk ask him

* **mirror_L_and_fuse**: Grabs all shapekeys that end with ".L", duplicates+mirrors them renaming those to ".R" and creates another that fuses both variations a-la-MMD where you would have "joy.L", "joy.R" and "joy" (which is joy.R+joy.L). Created at 1:26 AM with no python OR blender API knowledge so it's just unoptimized as heck. Adapted from https://blender.stackexchange.com/questions/74949/applying-lots-of-shape-keys-with-blends-using-python-not-working-also-is-there
  * **How it works?**: Just grab your desired object, select the Basis shapekey and run the script. Voilá!
  
* **ArmatureStandard_to_MMD**: Renames all bones into its MMD variation (aka translated into Japanese). Also renames Vertex Groups related to those bones. Who the frick thought it was OK for MMD to have a different bone standard system btw? Adapted from https://blender.stackexchange.com/questions/69505/renaming-bones-with-python
* **How it works?**: First verse same as second verse: just grab your desired object and run the script.

