# geo_update.py
# Geo Replacer
#
# Quickly replaces any geo with the same name with data-xfer nodes, to get it re-rigged as quick as possible

import bpy

def sort_selection():
    # Sort selection into a mesh list.
    mesh_list = []
    armature = None

    for object in bpy.context.selected_objects:
        if(object.type == 'MESH'):
            mesh_list.append(object)

        if(object.type == 'ARMATURE'):
            print ("Found the armature; {}".format(object.name))
            if(armature != None):
                print ("Found two armatures in the selection-- skipping the second one.")
                continue
            armature = object

    if(armature == None):
        print ("No armature in selection.  Aborting.")
        return False
    return { 'meshes':mesh_list, 'armature':armature }


def install_new_geo():
    # Selection will include an armature which will have the old content in it.
    replacements = sort_selection()
    if (replacements == False):
        print ("Selection sort failed.  Aborting!")
        return False

    for new_mesh in replacements['meshes']:
        # Each mesh will have a similar name under the armature (hopefully)
        for child in replacements['armature'].children:
            if(child.type == 'MESH'):
                # look for the names to match up
                if(child.name == new_mesh.name):
                    continue
                if(child.name.rpartition('.')[0] == new_mesh.name.rpartition('.')[0]):
                    print ("{} matches {}!".format(child.name, new_mesh.name))
                    # Get it under the armature first
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.scene.objects.active = replacements['armature']
                    new_mesh.select = True
                    
                    bpy.ops.object.parent_set(type='ARMATURE_NAME')
                    # Then copy skins.
                    print ("Copying from {} to {}...".format(child, new_mesh))
                    copy_skins(child, new_mesh)
            else:
                continue


def copy_skins( source, target ):
    print ("Souce is {}, target is {}".format(source, target))
    # Make a data xfer modifier on the target and set up it's state.
    mute_profile = mute_modifiers ( target )

    data_mod = target.modifiers.new(name='WeightCopy', type='DATA_TRANSFER')
    if(topo_matching(source, target)):
        data_mod.vert_mapping = 'TOPOLOGY' # Try this first-- on topo inaccuracy, fall back on 
    else:
        data_mod.vert_mapping = 'POLYINTERP_NEAREST'

    data_mod.object = (source)
    data_mod.use_vert_data = True
    data_mod.data_types_verts = {'VGROUP_WEIGHTS'}
    data_mod.mix_mode = 'ADD'

    # All settings in place-- generate and apply:
    bpy.context.scene.objects.active = target
    bpy.ops.object.datalayout_transfer(modifier=data_mod.name)
    
    unmute_modifiers(source, mute_profile)

    print ("Created modifer on {} called {}.".format(target, data_mod))


def topo_matching( source, target ):
    """
    topo_matching( source, target )

    Usage:
        Supply one mesh for "target" and another for "source".
        Will return true if the analysis matches.

    Purpose:
        Check if the topo of source matches the topo of target.

    Caveat:
        This is only checking point count, edge count, and vert count, very likely to be the same if topo matches.
        There can be no false negatives, but there is small potential for false positives.

    To Do:
        Find bpy alternative that does the same thing, if it exists. 
    """

    if(len(source.data.polygons) == len(target.data.polygons)):
        print ("Poly count matches!")
        if(len(source.data.vertices) == len(target.data.vertices)):
            print ("vertex count matches!")
            if(len(source.data.edges) == len(target.data.edges)):
                print ("edges count matches!")
                return True
    
    return False


def mute_modifiers(object):
    """
    mute_modifiers(object)

    Usage:
        Any object that contains modifiers can be supplied as "object".
        All modifiers that were on or off will be stored in a record in the form of a dict, and returned.

    Purpose:
        Other operations may need to find modifiers muted before executing other processes-- this function
        saves their former state to be re-instated later.

    Caveats:
        Must be used with /unmute_modifiers/.
    """
    # Mute all modifiers on an object, store and return which were on and which were off in a dict.
    on_off_profile = {}
    for mod in object.modifiers:
        # New profile entry:
        on_off_profile[mod.name] = mod.show_viewport
        mod.show_viewport = False

    return on_off_profile


def unmute_modifiers(object, profile):
    # Unmute modifiers using the dict stored from when they had gotten muted.
    for key in profile:
        for mod in object.modifiers:
            if(mod.name == key):
                mod.show_viewport = profile[key]
                break

print ("geo_update module loaded.")
