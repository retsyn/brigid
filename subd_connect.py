# SubD switch maker
# subd_connect.py
# updated: 2019-10-25

#  selected piece of geo and make a subd modifier. 

bl_info = {
    "name": "Subd Switch Connect",
    "author": "Jose Marcano, Matt Riche",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Rigging > Subd Connect",
    "description": "Installed standardized SubD Controls",
    "warning": "",
    "wiki_url": "",
    "category": "Rigging",
    }

import bpy
import sys

class SubdConnectOperator(bpy.types.Operator):
    """
    """
    bl_idname = "rig.subd_connect"
    bl_label = "Create SubD switchs on selection"
    bl_options = {'REGISTER', 'UNDO'}

    def subd_switch_maker(self):

        print ("Creating a subd switch...")
        
        # Find the god node
        armature = bpy.context.scene.SelectedSwitchArmature
        god_node = self.find_god_node()
        if(god_node == None):
            return False

        god_node_bone = armature.pose.bones[god_node.name]
        print ("god_node_bone is {}".format(god_node_bone))
        
        # Mesh needs to be selected in order for this tool to work
        # selects all objects in scene that are mesh
        if(bpy.context.scene.SelectSceneObjects):
            bpy.ops.object.select_by_type(extend=False, type="MESH")
            # Get a list of selections
            targets = bpy.context.selected_objects

        else:
            # Get a list of selections
            targets = bpy.context.selected_objects

        if(targets == []):
            status = self.report({'ERROR_INVALID_INPUT'}, "Must select some geo to apply switches to.\n")
            return False

        # Get the properties on the god node set up:
        # we must modify this section of the code to check for properties
        # check if prop/set properties or character properties
        if "_RNA_UI" not in god_node_bone.keys():
            god_node_bone["_RNA_UI"] = {}

        # Add subd props
        god_node_bone["subd_v"] = 0
        god_node_bone["subd_r"] = 2

        # Update properties to have the appropiate value ranges
        god_node_bone["_RNA_UI"].update({"subd_v":{"min":0, "max":2, "default":0, "description":"Visual Subd"}})
        god_node_bone["_RNA_UI"].update({"subd_r":{"min":0, "max":2, "default":2, "description":"Render Subd"}})

        # Make/Find modifiers and store them
        mod_list = []
        for object in targets:
            self.report({'INFO'}, "Checking {} for a subd mod...".format(object.name))
            mod = self.add_subd_modifier(object)
            mod_list.append(mod)

            print ("Building a driver for {}.".format(mod))
            self.build_driver(bone_target=god_node_bone, source_mod=mod, arm=armature)
        
        return True

    #creates drives for selected geo and set data paths 
    def build_driver(self, bone_target, source_mod, arm):
        # Create driver in the same loop.

            new_driver = source_mod.driver_add("levels").driver
            new_driver.expression = "var"
            driver_var = new_driver.variables.new()
            driver_var.name = "var"
            driver_var.targets[0].id = arm
            driver_var.targets[0].data_path = ("pose.bones[\"" + bone_target.name + "\"][\""+"subd_v"+"\"]")

            new_driver = source_mod.driver_add("render_levels").driver
            new_driver.expression = "var"
            driver_var = new_driver.variables.new()
            driver_var.name = "var"
            driver_var.targets[0].id = arm
            driver_var.targets[0].data_path = ("pose.bones[\"" + bone_target.name + "\"][\""+"subd_r"+"\"]")

    #Finds god node by searching through the armature bone list for [ctl.god.]
    def find_god_node(self):
        # Get the god node from the armature.
        god_node = None
        armature = bpy.context.scene.SelectedSwitchArmature.data

        for bone in armature.bones:
            if((bone.name.split('.')[1] == "god") and (bone.name.split('.')[0] == "ctl")):
                # Found the god node (As per naming conventions)
                god_node = bone

        if(god_node == None):
            self.report({'ERROR'}, "No god_node found!  Is this a proper rig?\n")

        return god_node



    def add_subd_modifier(self, mesh_object):
        # Take a passed in mesh object and apply a driver.  If it already has a driver, return that too.

        bpy.context.view_layer.objects.active = mesh_object
        
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


class TOOLS_PT_subdconnect(bpy.types.Panel):
    """
    Creates panel and button for SubDConnenct
    """

    bl_label = "Connect Subd Switches"
    bl_idname = "TOOLS_PT_subdconnect"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rigging'

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        row = layout.row()

        row.prop_search(scene, "SelectedSwitchArmature",
                                  bpy.data, "objects", 
                                 icon='OUTLINER_OB_ARMATURE')

        row = layout.row()
        row.prop(scene, "SelectSceneObjects")

        # The button:
        row = layout.row()
        row.scale_y = 1.5
        row.operator("rig.subd_connect")


class SubdTargetsGroup(bpy.types.PropertyGroup):
    bpy.types.Scene.SelectedSwitchArmature = bpy.props.PointerProperty(
        type=bpy.types.Object, 
        name = "Armature", 
        description = "Rig Armature"
        )

    bpy.types.Scene.SelectSceneObjects = bpy.props.BoolProperty(
        name="Select all",
        description = "Selects all scene objects"
        ) 

classes = [SubdConnectOperator ,SubdTargetsGroup ,TOOLS_PT_subdconnect] 

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    








