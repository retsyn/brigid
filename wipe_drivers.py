"""
    wipe_drivers.py

    Matthew Riche 2019

    Wipe all drivers connected to selected bones in a blender scene.
"""
import bpy

def wipe_drivers():
'''
    USAGE:
        Select one or more objects and run to delete all drivers attached to it.

    CAVEATS:
        Doesn't presently interact with modifiers.
        May complain about context.
'''
    # iterate over all bones of the active object
    for bone in bpy.context.selected_objects:
        drivers = bone.animation_data.drivers
        for dr in drivers:
            print ("Removed {}".format(dr.data_path))
            bone.driver_remove(dr.data_path, -1)

