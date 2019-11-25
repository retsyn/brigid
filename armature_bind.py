# Armature Binder-- Binds a lone armature into the greater structure of a rig.
# mr_armature_bind.py
# updated: 2019-11-25

#  selected piece of geo and make a subd modifier. 

bl_info = {
    "name": "Armature Bind",
    "author": "Matt Riche",
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

    def bind_armature():
        print ("Executing armature bind.")
        pass

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