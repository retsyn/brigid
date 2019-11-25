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
        print ("Executing armature bind.")
        repose_armature = bpy.context.scene.TargetArmature
        addon_armature = bpy.context.scene.SourceArmature
        # Call the generic "join_rigs"
        print ("DEBUG: repose is {}, and addon is {}".format(repose_armature.name, addon_armature.name))
        self.join_rigs(repose_name = repose_armature.name, addon_name = addon_armature.name)
        # Call the specific parent function.

        return True


    # TODO: This borrowed code from Mike used .name string to re-find the object int he 
    # scene.  Perhaps it's more apropos to send in an object/pointer to object?
    def join_rigs(self, repose_name, addon_name):
        """
        Takes bones from addon rig and makes them components of the target rig.
        """
        # This def's code based on Mike C.'s.
        self.report({'INFO'}, 'Binding rigs together.')

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action = 'DESELECT')

        bpy.context.scene.objects[addon_name].select_set(True)
        bpy.context.scene.objects[repose_name].select_set(True)
        bpy.context.view_layer.objects.active=bpy.data.objects[repose_name]
        bpy.ops.object.join()
        self.report({'INFO'}, 'Success!')


    # TODO: We should consider the parenting-scheme to be some data grew this func can
    # chew on, and be a little be more generic; like a dict that indicates what gets
    # Parent to what, that we can parse with a generic function.  To lazy for right now.
    def parent_teeth(self):
        """
        The parenting scheme specifically for teeth.
        """
        
        bpy.ops.object.mode_set(mode = 'EDIT')

        parent_bone=bpy.data.armatures[rig_name].edit_bones['ctl.head_fk_sub.C.001']
        bpy.data.armatures[rig_name].edit_bones['mst.face_head.C.001'].parent=parent_bone


    def parent_face(self):
        self.report({'WARNING'}, 'Not ready for this yet!')
        
        return False

    def execute(self, context):
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
    bl_category = 'Rigging'

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
        ('face', 'Face', '', 'Face Rig', 2)
    ]

    bpy.types.Scene.ArmatureType = bpy.props.EnumProperty(
        items=mode_options,
        description="Available bind actions"
    )


    bpy.types.Scene.TargetArmature = bpy.props.PointerProperty(
        type=bpy.types.Object, 
        name = "Repose", 
        description = "Rig Armature"
        )

    bpy.types.Scene.SourceArmature = bpy.props.PointerProperty(
        type=bpy.types.Object,
        name = "Addon",
        description = "Rig Armature"
        )



classes = [BindArmatureOperator, BindArmaPropGroup, TOOLS_PT_armature_bind] 

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)