# SubD switch maker
# Matt R

# Will take a selected piece of geo and make a subd modifier.  And if it's already got one, make a switch.

import bpy

def sort_selection():
    # Filter selected objects into list of meshes:
    meshList = []

    ctlBone = None
    ctlFound = False
    for object in bpy.context.selected_objects:
        print ("Searching through selected objects...")
        if(object.type != 'NoneType'):
            print ("TYPE: {}".format(object.type))
        if(object.type == 'MESH'):
            meshList.append(object)
        if(object.type == 'ARMATURE'):
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
    for modifier in mesh_object.modifiers:
        print ("searching through modifiers...")
        if modifier.type == "SUBSURF":
            subd_found = True
            subd_mod = modifier
            break
    
    if(subd_found==False):
        subd_mod = mesh_object.modifiers.new("SubSurface", type='SUBSURF')
        print ("Created new subd modifier: {}".format(subd_mod))
    else:
        print ("Already found a modifier: {}".format(subd_mod))

    return subd_mod


def subd_switch_maker():

    # Build dict of target content:
    targets = sort_selection()
    print ("using target meshes:{} and target controls: {}".format(targets['target_meshes'], targets['target_bones'] ))

    if(targets['target_bones'] == ''):
        print ("No control bone was selected; modifiers will be made but drivers will not.")

    for object in targets['target_meshes']:
        print ("Adding subd to {}...".format(object.name))
        mod = add_subd_modifier(object)
        # We need to edit this mod's state.
        print ("Editing {}...".format(mod))

        # We need to also add the controllers.
        
    print ("Done!")

subd_switch_maker()