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
    bl_label = "Match pos Bones Now"

    def execute(self, context):
        print ("Executing Match Pose...")
        match_pose() # Can this be executed if this definition exists outside the operator?
        return {'FINISHED'}

bpy.utils.register_class(MatchPoseOperator)


class MatchPosePanel(bpy.types.Panel):
    """
    Creates panel and button for Match-Pose
    """
    bl_label = "Match Pose"
    bl_idname = "TOOLS_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'posemode'
    bl_category = 'Match Pose'

    def draw(self, context):

        layout = self.layout
        active_object = context.object

        # Real Time (?) Selection info
        scene = context.scene
        layout.prop_search(scene, "rigObject", bpy.data, "objects", icon='OUTLINER_OB_ARMATURE')

        # The button:
        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.match_pose")


class RigObjectGroup(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name=)


def register():
    bpy.utils.register_class(MatchPoseOperator)
    rigObject = bpy.props
    bpy.utils.register_class(MatchPosePanel)



print ("Panel registered.")


class ObjectSelection():
    """
    Class for storing a selection structure
    """

    active_object = None
    selected_objects = []

    def get_new(self):
        self.active_object = bpy.context.scene.objects.active
        self.selected_objects = bpy.context.selected_objects


    def filter_type(self, type, selection_type='all'):
        
        if(selection_type != 'all'):
            for object in selected_objects:
                if(object.type != selection_type):
                    # Discard any object that is not relevant.
                    selected_objects.remove(object)


    def __init__(self):
        # immediately populate on instantiation;
        self.get_new()



def match_pose():
    # Get and sanitize selection
    selection = ObjectSelection()
    selection.filter_type('ARMATURE')

    if(selection.active_object == selection.selected_objects[0]):
        print ("Selection is not unique!  Select two armatures containing repose rigs.")

    if((selection.active_object.type != 'ARMATURE') or (selection.selected_objects[0] != 'ARMATURE')):
        print ("Active object is not an armature!")


    pose_bone_list = [bone for bone in selection.selected_objects[0].pose.bones if bone.name.partition('.')[0] == 'pos']
    # For ease of use, I'd prefer user just selected an entire armature and we sorted which were pose bones
    # Populate bone pose_bone_list with the filtered children of the armature...

    # HACK
    selection.active_object = bpy.data.objects['%s' % 'rig.chr463_teca_male_3.000']


    for p_bone in pose_bone_list:
        # creates the modifier and sets the armature and bone.
        mod_cns = p_bone.constraints.new('COPY_TRANSFORMS')
        mod_cns.target = selection.active_object
        mod_cns.subtarget = p_bone.name
        print ("Snapping {}:{} to {}:{}".format(selection.active_object.name, p_bone.name, selection.selected_objects[0].name, p_bone.name))
        # applies the pose.
        bpy.ops.pose.visual_transform_apply()
        # Context pedantic:
        p_bone.constraints.remove(mod_cns)
    
    print ("Finished.")

