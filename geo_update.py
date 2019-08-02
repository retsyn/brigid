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
        print ("No armature in selection.")
    return { 'meshes':mesh_list, 'armature':armature }


def install_new_geo():
    # Selection will include an armature which will have the old content in it.
    replacements = sort_selection()

    for new_mesh in replacements['meshes']:
        # Each mesh will have a similar name under the armature (hopefully)
        for child in replacements['armature'].children:
            if(child.type == 'MESH'):
                # look for the names to match up
                if(child.name.rpartition('.')[0] == new_mesh.name.rpartition('.')[0]):
                    print ("{} matches {}!".format(child.name, new_mesh.name))
                    copy_skins(child, new_mesh)
            else:
                continue


def copy_skins( source, target ):
    # Make a data xfer modifier on the target and set up it's state.
    mute_profile = mute_modifiers ( target )

    data_mod = source.modifiers.new(name='WeightCopy', type='DATA_TRANSFER')
    if(topo_matching(source, target)):
        data_mod.vert_mapping = 'TOPOLOGY' # Try this first-- on topo inaccuracy, fall back on 
    else:
        data_mod.vert_mapping = 'POLYINTERP_NEAREST'
    data_mod.object = (target)
    data_mod.use_vert_data = True
    data_mod.data_types_verts = {'VGROUP_WEIGHTS'}
    data_mod.mix_mode = 'ADD'

    unmute_modifers(source)

    print ("Created modifer on {} called {}.".format(target, data_mod))


def topo_matching( source, target ):
    # Check if topo matches
    # Caveat-- this is only checking point count, edge count, and vert count, very likely to be the same if topo matches.  
    # But not garunteed to recognize changed edge relationships or re-ordered points.  So in a perfect storm of meshes with exactly the same
    # counts this check will provide false positives. (But never false negatives)
    if(len(source.data.polygons) == len(target.data.polygons)):
        print ("Poly count matches!")
        if(len(source.data.vertices) == len(target.data.vertices)):
            print ("vertex count matches!")
            if(len(source.data.edges) == len(target.data.edges)):
                print ("edges count matches!")
                return True
    
    return False


def mute_modifiers(object):
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
