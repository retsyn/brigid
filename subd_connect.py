# SubD switch maker
# subd_connect.py
# Matt R
# 2019

# Will take a selected piece of geo and make a subd modifier.  And if it's already got one, make a switch.

import bpy
import sys


class SubdConnectOperator(bpy.types.Operator):
    """
    """

    bl_idname = "rig.subd_connect"
    bl_label = "Create SubD switchs on selection"

    def subd_switch_maker(self):

        print ("Creating a subd switch...")
        # Find the god node
        print("Selected armature is: {}".format(bpy.context.scene.SelectedSwitchArmature))
        god_node = find_god_node(bpy.context.scene.SelectedSwitchArmature)

        # Get a list of selections:
        targets = bpy.context.selected_objects
        if(targets == []):
            status = self.report({'ERROR_INVALID_INPUT'}, "Must select some geo to apply switches to.\n")
            return False


        # Make/Find modifiers and store them
        mod_list = []
        for object in targets['target_meshes']:
            print ("Adding subd to {}...".format(object.name))
            mod = add_subd_modifier(object)
            mod_list.append(mod)
    
        print ("Done!")
        return True


    def find_god_node(self):
        # Get the god node from the armature.
        god_node = None
        armature = bpy.types.Scene.SelectedSwitchArmature

        for bone in armature.data.bones:
            if((bone.name.split('.')[1] == "god") and (bone.name.split('.')[0] == "ctl")):
                # Found the god node (As per naming conventions)
                god_node = bone

        print ("The god node is {}.".format(god_node))
        if(god_node == None):
            self.report({'ERROR'}, "No god_node found!  Is this a proper rig?\n")
        return god_node


    def add_subd_modifier(self, mesh_object):
        # Take a passed in mesh object and apply a driver.  If it already has a driver, return that too.
        bpy.context.scene.objects.active = mesh_object
        subd_found = False

        # Check for existing sub-surf modifiers-- return existing one if so.
        for modifier in mesh_object.modifiers:
            if modifier.type == "SUBSURF":
                subd_found = True
                subd_mod = modifier
                break
    
        # If no subd modifiers were found, make one.
        if(subd_found==False):
            subd_mod = mesh_object.modifiers.new("SubSurface", type='SUBSURF')

        return subd_mod


    def execute(self, context):
        print ("Executing!")
        success = self.subd_switch_maker()
        if(success):
            return {'FINISHED'}
        else:
            return {'CANCELLED'}



class SubdConnectPanel(bpy.types.Panel):
    """
    Creates panel and button for SubDConnenct
    """
    bl_label = "Connect Subd Switches"
    bl_idname = "TOOLS_PT_subdconnect"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    bl_category = 'Rigging'

    def draw(self, context):

        layout = self.layout

        scene = context.scene
        row = layout.row()
        row.prop_search(scene, "SelectedSwitchArmature", bpy.data, "armatures", icon='OUTLINER_OB_ARMATURE')
        row = layout.row()
        row.prop(scene, "SwitchMakerLevels")
        row = layout.row()
        row.prop(scene, "SwitchRenderLevels")
        row.prop(scene, "SwitchViewportLevels")

        # The button:
        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.subd_connect")


class SubdTargetsGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.SelectedSwitchArmature = bpy.props.PointerProperty(type=bpy.types.Object, name = "Armature", description = "Rig Armature")
    bpy.types.Scene.SwitchMakerLevels = bpy.props.IntProperty(name="SubD Limit")
    bpy.types.Scene.SwitchRenderLevels = bpy.props.BoolProperty(name="For Render")
    bpy.types.Scene.SwitchViewportLevels = bpy.props.BoolProperty(name="For Viewport")
    

def register():
    bpy.utils.register_class(SubdConnectOperator)
    bpy.utils.register_class(SubdTargetsGroup)
    bpy.utils.register_class(SubdConnectPanel)
    print ("Panel/Operator registered.\nScript by Matt.")

register()







