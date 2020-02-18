


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
            self.report({'INFO'}, "")


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
    bl_category = 'Repose'


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

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
