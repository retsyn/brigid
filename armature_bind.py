# Armature Binder-- Binds a lone armature into the greater structure of a rig.
# armature_bind.py
# updated: 2019-11-25

bl_info = {
    "name": "Armature Bind",
    "author": "Matt Riche, Mike Carnovale",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Rigging > Armature Bind",
    "description": "Tool to unify additional armatures to the repose rig.",
    "warning": "",
    "wiki_url": "",
    "category": "Rigging",
    }

import bpy
import sys

class BindArmatureOperator(bpy.types.Operator):
    """
    Operator class for Bind Armature functions.
    """
    bl_idname = "rig.armature_bind"
    bl_label = "Bind Add-on into Repose"
    bl_options = {'REGISTER', 'UNDO'}

    def bind_armature(self):
        self.report({'INFO'}, "Starting armature bind.")

        scene = bpy.context.scene
        repose_armature = scene.TargetArmature
        addon_armature = scene.SourceArmature

        if(repose_armature == None or addon_armature == None):
            self.report({'WARNING'}, "Two armatures need to be selected to perform.")
            return False

        repose_armature.hide_viewport=False
        addon_armature.hide_viewport=False

        # Call the specific parent function.
        if(scene.ArmatureType == 'teeth'):
            self.report({'INFO'}, "Bind target is a Teeth Rig.")

            # This process combines armatures before in-armature parenting begins.
            success = self.join_rigs(repose_name = repose_armature.name, addon_name = addon_armature.name)
            if(success == False):
                self.report({'WARNING'}, "An object was missing, cancelling the process.")
                return False
            self.parent_teeth(repose_armature.name)

        if(scene.ArmatureType == 'crowd_biped'):
            self.report({'INFO'}, "Starting crowd_biped attachment.")
            success = self.parent_crowd()

            if(success == False):
                self.report({'WARNING'}, "An object was missing, cancelling the process.")
                return False

        self.report({'INFO'}, "The binding process completed successfully.")
        return True


    # TODO: This borrowed code from Mike used .name string to re-find the object int he 
    # scene.  Perhaps it's more apropos to send in an object/pointer to object?
    def join_rigs(self, repose_name, addon_name):
        """
        Takes bones from addon rig and makes them components of the target rig.
        """
        # This def's code based on Mike C.'s.
        self.report({'INFO'}, 'Binding armature contents into a single armature.')
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action = 'DESELECT')
        self.report({'INFO'}, "Binding {} with {}".format(addon_name, repose_name))

        try:
            bpy.context.scene.objects[addon_name].select_set(True)
        except:
            self.report({'ERROR'}, "{} doesn't seem to be in the scene.  Is it already bound?".format(addon_name))
            return False

        try:
            bpy.context.scene.objects[repose_name].select_set(True)
        except:
            self.report({'ERROR'}, "{} is not found.  Did you select the repose rig?")
            return False

        self.report({'INFO'}, "")
        bpy.context.view_layer.objects.active=bpy.data.objects[repose_name]

        bpy.ops.object.join()
        self.report({'INFO'}, "Armatures successfully joined.")
        return True

    
    def match_pose(self):
        # Snap pose position of one armature that has any smililar naming scheme.
        

        # Call upon the repose script to disable all the rig contents.
        bpy.ops.ta.disable_deform_ik()
        bpy.ops.object.mode_set(mode = 'POSE')

        # source and target are captured from the panel.
        source = bpy.context.scene.SourceArmature
        target = bpy.context.scene.TargetArmature

        self.report({'INFO'}, "Matching POS from {} to {}.".format(source.name, target.name))
        self.report({'INFO'}, "Pose bone list: {}".format(source.pose.bones))
        #pose_bone_list = [bone for bone in target.pose.bones]
        pose_bone_list = [bone for bone in source.pose.bones if bone.name.partition('.')[0] == 'pos']
        # This is our error, list comprehension is pulling out zero items.
        self.report({'INFO'}, "Comprehended pose-bone list: {}".format(pose_bone_list))

        # Mouse cursor progress bar
        wm = bpy.context.window_manager
        wm.progress_begin(len(pose_bone_list), 0)
    
        # Mike C's code follows.  It creates temporary copy transforms.
        i = 0
        for pose_bone in pose_bone_list:
            i += 1
            wm.progress_update(i)
            # creates the modifier and sets the armature and bone.
            temp_constraint = pose_bone.constraints.new('COPY_TRANSFORMS')
            temp_constraint.target = target
            temp_constraint.subtarget = pose_bone.name
            self.report({'INFO'}, "Snapping {}:{} to {}:{}".format(source.name, pose_bone.name, target.name, pose_bone.name))
            #applies the pose.

            pose_bone.bone.select = True
            bpy.ops.pose.visual_transform_apply()
            # Context pedantic:
            pose_bone.constraints.remove(temp_constraint)
        
        wm.progress_end()
    
        print ("Finished repose matching.")


    # TODO: We should consider the parenting-scheme to be some data grew this func can
    # chew on, and be a little be more generic; like a dict that indicates what gets
    # Parent to what, that we can parse with a generic function.  To lazy for right now.
    def parent_teeth(self, repose_name):
        """
        The parenting scheme specifically for teeth.
        """
        bpy.ops.object.mode_set(mode = 'EDIT')
        parent_bone=bpy.data.armatures[repose_name].edit_bones['ctl.teeth_upper.C.001']
        bpy.data.armatures[repose_name].edit_bones['mst.teeth_top.C.001'].parent=parent_bone
        parent_bone=bpy.data.armatures[repose_name].edit_bones['ctl.teeth_lower.C.001']
        bpy.data.armatures[repose_name].edit_bones['mst.teeth_bottom.C.001'].parent=parent_bone
        self.report({'INFO'}, 'Teeth parented under repose head.')

        # We've made some existing bones redundant:
        try:
            bpy.data.armatures[repose_name].edit_bones.remove('def.teeth_upper.C.001')
            bpy.data.armatures[repose_name].edit_bones.remove('def.teeth_lower.C.001')
        except:
            self.report({'WARNING'}, "Old teeth def bones are already removed.")

        bpy.ops.object.mode_set(mode = 'OBJECT')
        return True


    def parent_crowd(self):
        """
        Specific parent scheme just for Crowd Rigs
        """

        bpy.ops.object.mode_set(mode = 'POSE')
        self.match_pose()


    def parent_face(self):
        self.report({'WARNING'}, 'Not ready for this yet!')        
        return False


    def execute(self, context):
        self.report({'INFO'}, "Executing {}.".format(self))
        success = self.bind_armature()
        if(success):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class TOOLS_PT_armature_bind(bpy.types.Panel):
    """
    Panel class for TOOLS_PT_armature_bind
    """
    
    bl_label = "Armature Bind"
    bl_idname = "TOOLS_PT_armature_bind"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Repose Rig'

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop_search(scene, "TargetArmature", bpy.data, 
            "objects", 
            icon='OUTLINER_OB_ARMATURE'
            )

        row = layout.row()
        row.prop_search(scene, "SourceArmature", bpy.data, 
            "objects", 
            icon='OUTLINER_OB_ARMATURE'
            )

        row = layout.row()
        row.prop(scene, "ArmatureType")

        # The button:
        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.armature_bind")


class BindArmaPropGroup(bpy.types.PropertyGroup):
    """
    Property Group
    """

    mode_options = [
        ('teeth', 'Teeth', '', 'Basic Teeth', 1),
        ('crowd_biped', 'Crowd Biped', '', 'Crowd Biped', 2)
    ]

    bpy.types.Scene.ArmatureType = bpy.props.EnumProperty(
        items=mode_options,
        description="Available bind actions"
    )


    bpy.types.Scene.TargetArmature = bpy.props.PointerProperty(
        type=bpy.types.Object, 
        name = "Target Rig", 
        description = "Rig Armature"
        )

    bpy.types.Scene.SourceArmature = bpy.props.PointerProperty(
        type=bpy.types.Object,
        name = "Rig to Snap",
        description = "Rig Armature"
        )



classes = [BindArmatureOperator, BindArmaPropGroup, TOOLS_PT_armature_bind] 

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)