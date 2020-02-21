


bl_info = {
    "name": "Bind Support Transfer",
    "author": "Matt Riche",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Repose > Bind Support Transfer",
    "description": "Tools to transfer intially bound weights from .sup bone to correct .def bone.",
    "warning": "",
    "wiki_url": "",
    "category": "Rigging",
    }


import bpy

class BindSupportTransferOperator(bpy.types.Operator):
    """
    Operator class to start the transfer operation
    """

    bl_idname = "rig.xfer_bind_support"
    bl_label = "Transfer Bind Weights"
    bl_options = { 'REGISTER', 'UNDO' }


    def transfer(self):
        """
        Take a selected geo, and iterate through it's influences looking for bones with the prefix
        .sup, and transferring those weights to their parent.
        """
        self.report({'INFO'}, "Starting transfer...")

        bpy.ops.object.mode_set(mode="EDIT")
        obj = bpy.context.edit_object
        if(obj.type != 'MESH'):
            self.report({'ERROR'}, "Select a mesh before running this operation.")
            return False

        self.report({'INFO'}, "Working on {}".format(obj.name))

        # Find the attached rig:
        rig = obj.parent
        if(rig.type != 'ARMATURE'):
            self.report({'ERROR'}, "The parent of the geo is not an armature.  Check that your selected geo is rigged correctly.")
            return false

        bpy.ops.object.mode_set(mode="OBJECT")
        for vtxgrp in obj.vertex_groups:
            if(vtxgrp.name.partition('.')[0] == 'sup'):
                self.report({'INFO'}, "Working vtx group \"{}\"...".format(vtxgrp.name))
                # Now find the bone in the rig with the same name...
                sup_bone = rig.pose.bones[vtxgrp.name]
                parent_def = sup_bone.parent
                self.report({'INFO'}, "Parent of {} is {}...".format(sup_bone.name, parent_def.name))
                self.mix_groups(obj, vtxgrp.name, parent_def.name)

        # Once the bind weights are moved over completely and safely, we can begin to delete sup vtxgrps.
        # TODO Delete sup vtx groups here.                

        self.report({'INFO'}, "Execution finished.")
        return True


    def mix_groups(self, ob, vtxgrp_a_str, vtxgrp_b_str):
        # Get both groups and add them into third
        if (vtxgrp_a_str in ob.vertex_groups and vtxgrp_b_str in ob.vertex_groups):

            self.report({'INFO'}, "Adding {} to {}.".format(vtxgrp_a_str, vtxgrp_b_str))
            for id, vert in enumerate(ob.data.vertices):
                available_groups = [v_group_elem.group for v_group_elem in vert.groups]
                A = B = 0
                if ob.vertex_groups[vtxgrp_a_str].index in available_groups:
                    A = ob.vertex_groups[vtxgrp_a_str].weight(id)
                if ob.vertex_groups[vtxgrp_b_str].index in available_groups:
                    B = ob.vertex_groups[vtxgrp_b_str].weight(id)

                # only add to vertex group is weight is > 0
                sum = A + B
                if sum > 0:
                    vtxgrp_b = ob.vertex_groups[vtxgrp_b_str]
                    vtxgrp_a = ob.vertex_groups[vtxgrp_a_str]
                    vtxgrp_b.add([id], sum, 'REPLACE')
            
            #ob.vertex_groups.remove(vtxgrp_a)
                    
        else:
            self.report({'WARNING'}, "{} and/or {} is not present in the existing vtx groups... skipping it.".format(vtxgrp_a_str, vtxgrp_b_str))


    def execute(self, context):
        success = self.transfer()
        if(success):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class TOOLS_PT_bind_support_transfer(bpy.types.Panel):
    """
    Panel class for Bind support transfer
    """
    
    bl_label = "Transfer Support Weights"
    bl_idname = "TOOLS_PT_bind_support_transfer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Repose Rig'


    def draw(self, context):

        layout = self.layout
        scene = context.scene

        # The button:
        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.xfer_bind_support")


class BindXferPropGroup(bpy.types.PropertyGroup):    
    pass


classes = [BindSupportTransferOperator, TOOLS_PT_bind_support_transfer, BindXferPropGroup] 


# Utility
def get_children(object): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == object: 
            children.append(ob) 
    return children 

# Add-on standard
def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
