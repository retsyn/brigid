# Armature Binder-- Binds a lone armature into the greater structure of a rig.
# armature_bind.py
# updated: 2019-11-25

bl_info = {
    "name": "Crush Influences",
    "author": "Matt Riche",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Rigging > Crush Influences",
    "description": "Tool to prepare weights for reducing influences.",
    "warning": "",
    "wiki_url": "",
    "category": "Rigging",
    }

import bpy

class CrushInfluencesOperator(bpy.types.Operator):
    """
    Operator for Influence Crush.
    """

    bl_idname = "rig.crush_influences"
    bl_label = "Crush"
    bl_options = { 'REGISTER', 'UNDO' }


    def crush(self):
        self.report({'INFO'}, "Beginning Crush Sequence...")

        # TODO make sure an object with influences is selected.
        bpy.ops.object.mode_set(mode="EDIT")
        obj = bpy.context.edit_object
        mesh = obj.data
        verts = [v for v in mesh.vertices]

        # Change contexts or it'll break:
        bpy.ops.object.mode_set(mode = 'WEIGHT_PAINT')

        # First, a normalize operation
        self.report({'INFO'}, "Normalizing...")
        bpy.ops.object.vertex_group_normalize_all()
        # Now a clean operation:
        self.report({'INFO'}, "Cleaning values lesser than 0.1")
        bpy.ops.object.vertex_group_clean(limit=0.1)
        # Now limit total...
        self.report({'INFO'}, "Limiting total to 3.")
        bpy.ops.object.vertex_group_limit_total(limit=3)
        # Normalize a second time.
        self.report({'INFO'}, "Final post-op Normalizing...")
        bpy.ops.object.vertex_group_normalize_all()
        self.report({'INFO'}, "Done.")


    def execute(self, context):
        success = self.crush()
        if(success):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class TOOLS_PT_crush_influences(bpy.types.Panel):
    """
    Panel class for TOOLS_PT_crush_influences
    """
    
    bl_label = "Crush Influences"
    bl_idname = "TOOLS_PT_armature_bind"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rigging'

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        # The button:
        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.crush_influences")


class GroomPropGroup(bpy.types.PropertyGroup):
    
    bpy.types.Scene.CreateDeltaMap = bpy.props.BoolProperty(name="Create Delta Map")
    bpy.types.Scene.CreateCountMap = bpy.props.BoolProperty(name="Create Inf Map")


classes = [CrushInfluencesOperator, TOOLS_PT_crush_influences] 

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)