# Groom properties
# Sets properties to a certain set of defaults
# updated: 2019-12-03

bl_info = {
    "name": "Groom Properties",
    "author": "Matt Riche",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Rigging > Groom Props",
    "description": "Tool to groom certain default properties.",
    "warning": "",
    "wiki_url": "",
    "category": "Rigging",
    }

import bpy
import sys


class GroomPropOperator(bpy.types.Operator):
    """
    Operator class for Groom Properties
    """
    bl_idname = "rig.groom_props"
    bl_label = "Groom Props to Default"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        resets_count = 0
        keys_count = 0
        self.report({'INFO'}, "Running Groom Properties operation...")
        # The following condition is how it is due to the idea that in the future the enum my groom entirely different properties.
        if(bpy.context.scene.GroomAction == 'subd_v' or bpy.context.scene.GroomAction == 'subd_r' or bpy.context.scene.GroomAction == 'subd_all'):
            resets_count = self.groom_subds()
            if(resets_count > 0):
                success = True

        if(bpy.context.scene.GroomClearKeys):
            keys_count = self.reset_keys()
            if(keys_count > 0):
                success = True

        self.report({'INFO'}, "Reset {} values, and deleted {} keys.".format(resets_count, keys_count))
        if(success):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


    def reset_keys(self):
        self.report({'INFO'}, "Cleaning keys...")
        removal_count = 0

        armatures=bpy.data.armatures
        for armature in armatures:
            rig_name=armature.name
            self.report({'INFO'}, "Checking keys on {}.".format(rig_name))
            try:
                fcurves = bpy.data.objects[rig_name].animation_data.action.fcurves
            except:
                self.report({'WARNING'}, "No fcurves on that armature, moving on.")
                continue

            if (bpy.context.scene.GroomAction == 'subd_v'):
                strings = 'subd_v'
            if (bpy.context.scene.GroomAction == 'subd_r'):
                strings = 'subd_r'
            if (bpy.context.scene.GroomAction == 'subd_all'):
                strings = 'subd'

            for curve in fcurves:
                if(strings in curve.data_path):
                    self.report({'INFO'}, "Deleting keys on {}.".format(curve.data_path))
                    fcurves.remove(curve)
                    removal_count += 1
            
            return removal_count

    
    def groom_subds(self):
        resets_count = 0
        self.report({'INFO'}, "Executing groom subds...")

        # Search string will determine which type of property we edit...
        if(bpy.context.scene.GroomAction == 'subd_v'):
            search_string = "subd_v"
        if(bpy.context.scene.GroomAction == 'subd_r'):
            search_string = "subd_r"
        if(bpy.context.scene.GroomAction == 'subd_all'):
            search_string = "subd"

        try:
            bpy.ops.object.mode_set(mode='POSE')
        except:
            self.report({'ERROR'}, "Couldn't change contexts.  Check that your armatures exist and aren't hidden or off.")
            return False

        controls = [val for key, val in bpy.context.object.pose.bones.items() if 'ctl.' in key]
  
        for ctl in controls:

            cont = bpy.context.object.pose.bones[ctl.name]

            if('_RNA_UI' not in cont.keys()):
                continue

            subd_props = [key for key, val in cont['_RNA_UI'].items() if ((search_string) in key or (search_string) == key)]
            if(subd_props == []):
                continue
            
            for prop in subd_props:
                if('default' in cont['_RNA_UI'][prop].keys()):
                    new_default = cont['_RNA_UI'][prop]['default']
                    cont[prop] = new_default
                    self.report({'INFO'}, "Changing {} on {} back to default of {}".format(prop, cont.name, new_default))
                    resets_count += 1
                else:
                    cont[prop] = 0
                    self.report({'INFO'}, "Changing {} on {} back to 0 (No default value stored)".format(prop, cont.name))
                    resets_count += 1

        success = True
        return resets_count



class TOOLS_PT_groom_properties(bpy.types.Panel):
    """
    Panel class for groom properties tool
    """
    
    bl_label = "Groom Properties"
    bl_idname = "TOOLS_PT_groom_properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rigging'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "GroomAction")

        row = layout.row()
        row.prop(scene, "GroomClearKeys")

        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.groom_props")


class GroomPropGroup(bpy.types.PropertyGroup):

    mode_options = [
        ('subd_v', 'SubD_v\'s only', '', 'Sets all subd_v values to their default', 1),
        ('subd_r', 'SubD_r\'s only', '', 'Sets all subd_r values to their default', 2),
        ('subd_all', 'All SubD\'s', '', 'Sets all subd values to their default', 3),

    ]

    bpy.types.Scene.GroomAction = bpy.props.EnumProperty(
        name="Action",
        items=mode_options,
        description="Available bind actions"
    )
    bpy.types.Scene.GroomClearKeys = bpy.props.BoolProperty(name="Clear Keys")


classes = [GroomPropOperator, GroomPropGroup, TOOLS_PT_groom_properties] 


def register():
    print ("Re-registered.")
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
