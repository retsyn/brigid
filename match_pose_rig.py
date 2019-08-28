'''
Alvin's code initially,
For matching pose rigs to other pose rigs.
'''

import bpy


class MatchPoseOperator(bpy.types.Operator):
    """
    Matches the locations of pose bones from active armature to selected armature.
    USAGE:
    Select the arranged armature first, and the target armature second before running.
    """

    bl_idname = "rig.match_pose"
    bl_label = "Match Target \'pos.\' Bones to Source"

    def match_pose(self):

        # source and target are captured from the panel.
        source = bpy.context.scene.SelectedSourceArmature
        target = bpy.context.scene.SelectedTargetArmature

        pose_bone_list = [bone for bone in target.pose.bones if bone.name.partition('.')[0] == 'pos']    

        for p_bone in pose_bone_list:
            # creates the modifier and sets the armature and bone.
            mod_cns = p_bone.constraints.new('COPY_TRANSFORMS')
            mod_cns.target = source
            mod_cns.subtarget = p_bone.name
            # print ("Snapping {}:{} to {}:{}".format(source.name, p_bone.name, target.name, p_bone.name))
            # applies the pose.
            bpy.ops.pose.visual_transform_apply()
            # Context pedantic:
            p_bone.constraints.remove(mod_cns)
    
        print ("Finished repose matching.")


    def execute(self, context):
        print ("Executing Match Pose...")
        self.match_pose() # Can this be executed if this definition exists outside the operator?
        return {'FINISHED'}



class MatchPosePanel(bpy.types.Panel):
    """
    Creates panel and button for Match-Pose
    """
    bl_label = "Match Pose"
    bl_idname = "TOOLS_PT_matchpose"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'posemode'
    bl_category = 'Match Pose'

    def draw(self, context):

        layout = self.layout
        active_object = context.object

        # Real Time (?) Selection info
        scene = context.scene
        row = layout.row()
        row.prop_search(scene, "SelectedSourceArmature", bpy.data, "armatures", icon='OUTLINER_OB_ARMATURE')
        row = layout.row()
        row.prop_search(scene, "SelectedTargetArmature", bpy.data, "armatures", icon='OUTLINER_OB_ARMATURE')

        # The button:
        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.match_pose")


class RigObjectGroup(bpy.types.PropertyGroup):
    #source_prop = bpy.props.StringProperty(name="Source", description="Source Armature")
    #target_prop = bpy.props.StringProperty(name="Target", description="Target Armature")

    bpy.types.Scene.SelectedSourceArmature = bpy.props.PointerProperty(type=bpy.types.Object, name = "Source", description = "Source Armature")
    bpy.types.Scene.SelectedTargetArmature = bpy.props.PointerProperty(type=bpy.types.Object, name = "Target", description = "Target Armature")

    # The property for access later will be bpy.types.Scene.SelectedTargetArmature


def register():
    bpy.utils.register_class(MatchPoseOperator)
    bpy.utils.register_class(RigObjectGroup)
    bpy.utils.register_class(MatchPosePanel)

    bpy.types.Scene.matchRepose_props = bpy.props.PointerProperty(type=RigObjectGroup)
    print ("Match Pose Rig Panel/Operator registered.\nScript by Matt & Alvin.  Ask one of them why you're reading this.")


register()

