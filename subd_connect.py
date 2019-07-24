# SubD switch maker
# Matt R

# Will take a selected piece of geo and make a subd modifier.  And if it's already got one, make a switch.

import bpy

def sort_selection():
    # Filter selected objects into list of meshes:
    meshList = []
    boneList = []
    ctlFound = False
    for object in bpy.context.selected_objects:
        if(object.type == 'MESH'):
            meshList.append(object)
        if(object.type == 'BONE'):
            ctlBone = object
            ctlFound = True

    print("Constructed mesh list from selection:\n{}".format(meshList))
    if(ctlFound):
        print("A ctl bone(s) were in the selection.  The last one selected was {}".format())
    else:
        print("No control was found.")
    
    # Return the sorted content
    return [meshList, boneList]


def add_subd_modifier(mesh_object):
    # Take a passed in mesh object and apply a driver.
    bpy.context.scene.objects.active = mesh_object

    subd_found = False
    for modifier in mesh_object.modifiers:
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








    



