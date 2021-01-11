#Blender 2.8 plugin
#Adapted Script from    https://blender.stackexchange.com/questions/69505/renaming-bones-with-python
#
#Original by batFINGER; adaptation by OSformula

import bpy
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
("toe.R", "右足先EX")

]


for n in namelist:
    # get the pose bone with name
    pb = obj.pose.bones.get(n[0])
    # continue if no bone of that name
    if pb is None:
        continue
    # rename
    pb.name = n[1]
