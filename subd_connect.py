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

        # Store scene properties locally:
        subd_max = bpy.context.scene.SwitchMakerLevels

        print ("Creating a subd switch...")
        # Find the god node
        armature = bpy.context.scene.SelectedSwitchArmature
        god_node = self.find_god_node()
        if(god_node == None):
            return False

        god_node_bone = armature.pose.bones[god_node.name]
        print ("god_node_bone is {}".format(god_node_bone))
        
        # Get a list of selections
        targets = bpy.context.selected_objects
        if(targets == []):
            status = self.report({'ERROR_INVALID_INPUT'}, "Must select some geo to apply switches to.\n")
            return False

        custom_prop_name = self.create_property_name()
        self.report({'INFO'}, "Making a property called {}".format(custom_prop_name))

        # Get the new property on the god node set up:
        god_node_bone[custom_prop_name] = 0
        if "_RNA_UI" not in god_node_bone.keys():
            god_node_bone["_RNA_UI"] = {}

        god_node_bone["_RNA_UI"].update({custom_prop_name: {"min":0, "max":subd_max, "soft_min":0, "soft_max":1}})

        # Make/Find modifiers and store them
        mod_list = []
        for object in targets:
            self.report({'INFO'}, "Checking {} for a subd mod...".format(object.name))
            mod = self.add_subd_modifier(object)
            mod_list.append(mod)

            print ("Building a driver for {}.".format(mod))
            self.build_driver(bone_target=god_node_bone, source_mod=mod, prop=custom_prop_name, arm=armature)
        
        return True

    
    def build_driver(self, bone_target, source_mod, prop, arm):
        # Create driver in the same loop.
        # self.report({'INFO'}, "Adding to driver to {}->{}.".format(bone_target.name, mod.name))

        new_driver = source_mod.driver_add("levels").driver
        new_driver.expression = "var"
        driver_var = new_driver.variables.new()
        driver_var.name = prop
        driver_var.targets[0].id = arm
        driver_var.targets[0].data_path = ("pose.bones[\"" + bone_target.name + "\"][\"" + prop + "\"]")
        #pose.bones["ctl.god.C.001"]["subd_r_body"]


    def create_property_name(self):

        name_from_select = bpy.context.scene.SwitchUseSelection
        part_one = ""

        if(name_from_select):
            part_one = bpy.context.selected_objects[0].name.split('.')[1]
        else:
            if(bpy.context.scene.SwitchDriverName != ''):
                part_one = bpy.context.scene.SwitchDriverName
            else:
                self.report({'ERROR'}, "Can't have no name!  Select \"Decide name from selection\" if you're that lazy.")

        full_string = ("subd_" + part_one)

        if(bpy.context.scene.SwitchViewportLevels):
            full_string = (full_string + "_v")
        if(bpy.context.scene.SwitchRenderLevels):
            full_string = (full_string + "_r")

        print ("Name of new property will be {}.".format(full_string))

        return full_string


    def find_god_node(self):
        # Get the god node from the armature.
        god_node = None
        armature = bpy.context.scene.SelectedSwitchArmature

        for bone in armature.data.bones:
            if((bone.name.split('.')[1] == "god") and (bone.name.split('.')[0] == "ctl")):
                # Found the god node (As per naming conventions)
                god_node = bone

        if(god_node == None):
            self.report({'ERROR'}, "No god_node found!  Is this a proper rig?\n")

        return god_node


    def add_subd_modifier(self, mesh_object):
        # Take a passed in mesh object and apply a driver.  If it already has a driver, return that too.
        bpy.context.scene.objects.active = mesh_object
        subd_found = False

        # Check for existing sub-surf modifiers-- return existing one if so.
        for modifier in mesh_object.modifiers:
            print ("Checking modifier...")
            if modifier.type == "SUBSURF":
                self.report({'WARNING'}, "SubD mod already exists on {}.".format(mesh_object.name))
                print ("Where is the warning?")
                subd_found = True
                subd_mod = modifier
                break
    
        # If no subd modifiers were found, make one.
        if(subd_found==False):
            subd_mod = mesh_object.modifiers.new("SubSurface", type='SUBSURF')

        return subd_mod


    def execute(self, context):
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
        row = layout.row()
        row.prop(scene, "SwitchDriverName")
        row = layout.row()
        row.prop(scene, "SwitchUseSelection")

        # The button:
        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.subd_connect")


class SubdTargetsGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.SelectedSwitchArmature = bpy.props.PointerProperty(type=bpy.types.Object, name = "Armature", description = "Rig Armature")
    bpy.types.Scene.SwitchMakerLevels = bpy.props.IntProperty(name="SubD Limit")
    bpy.types.Scene.SwitchRenderLevels = bpy.props.BoolProperty(name="For Render")
    bpy.types.Scene.SwitchViewportLevels = bpy.props.BoolProperty(name="For Viewport")
    bpy.types.Scene.SwitchDriverName = bpy.props.StringProperty(name="Switch Name")
    bpy.types.Scene.SwitchUseSelection = bpy.props.BoolProperty(name="Decide name from Selection")
    

def register():
    bpy.utils.register_class(SubdConnectOperator)
    bpy.utils.register_class(SubdTargetsGroup)
    bpy.utils.register_class(SubdConnectPanel)
    print ("Panel/Operator registered.\nScript by Matt.")

register()







