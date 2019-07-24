# SubD switch maker
# subd_connect.py
# Matt R
# 2019

# Will take a selected piece of geo and make a subd modifier.  And if it's already got one, make a switch.

import bpy
import sys

def sort_selection():
    # Filter selected objects into list of meshes:
    meshList = []

    ctlBone = None
    ctlFound = False
    
    print ("Searching through selected objects...")

    for object in bpy.context.selected_objects:
        if(object.type != 'NoneType'):
            print ("\tFound a {};".format(object.type))
        if(object.type == 'MESH'):
            meshList.append(object)
            print ("\t--Appended {} to the list.".format(object.name))
        if((object.type == 'ARMATURE') and (ctlFound)):
            print ("Two armatures have been found.  Aborting-- make sure only one is in the selection!")
            return None
        if((object.type == 'ARMATURE') and (ctlFound==False)):
            print ("\t--{} now is the target armature.".format(object.name))
            ctlBone = object
            ctlFound = True

    print("Constructed mesh list from selection:\n{}".format(meshList))
    if(ctlFound):
        print("A ctl bone(s) were in the selection.  The last one selected was {}".format(ctlBone.name))
    else:
        print("No control was found.")
    
    # Return the sorted content
    return { 'target_meshes':meshList, 'target_bones':ctlBone }


def add_subd_modifier(mesh_object):
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


def subd_switch_maker():
    # Build dict of target content:
    targets = sort_selection()
    if(targets == None):
        print("Exiting.")
        return
        
    print ("using target meshes:{} and target controls: {}".format(targets['target_meshes'], targets['target_bones'] ))

    # Find the god node
    if(targets['target_bones'] == ''):
        print ("No control bone was selected; modifiers will be made but drivers will not.")
    else:
        god_node = find_god_node(targets['target_bones'])

    # Make/Find modifiers and store them
    mod_list = []
    for object in targets['target_meshes']:
        print ("Adding subd to {}...".format(object.name))
        mod = add_subd_modifier(object)
        mod_list.append(mod)

        
    print ("Done!")


def find_god_node(armature):
    # Get the god node from the armature.
    god_node = None

    for bone in armature.data.bones:
        if((bone.name.split('.')[1] == "god") and (bone.name.split('.')[0] == "ctl")):
            # Found the god node (As per naming conventions)
            god_node = bone

    print ("The god node is {}.".format(god_node))

    return god_node

subd_switch_maker()