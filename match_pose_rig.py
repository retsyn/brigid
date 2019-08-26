'''
Alvin's code initially,
For matching pose rigs to other pose rigs.
'''

import bpy

class object_selection():
    '''
    Class for storing a selection structure
    '''

    active_object = None
    selected_objects = []

    def get_new(self):
        self.active_object = bpy.context.scene.objects.active
        self.selected_objects = bpy.context.selected_objects


    def filter_type(self, type, selection_type='all'):
        
        if(selection_type != 'all'):
            for object in selected_objects:
                if(object.type != selection_type):
                    # Discard any object that is not relevant.
                    selected_objects.remove(object)


    def __init__(self):
        # immediately populate on instantiation;
        self.get_new()



def match_pose():
    # Get and sanitize selection
    selection = object_selection()
    selection.filter_type('ARMATURE')
    print ("Selection is {}".format(selection.selected_objects))

    pose_bone_list = [bone for bone in selection.selected_objects[0].pose.bones if bone.name.partition('.')[0] == 'pos']
    

    #[idx for idx in test_list if idx[0].lower() == check.lower()] 
    # For ease of use, I'd prefer user just selected an entire armature and we sorted which were pose bones

    # Populate bone pose_bone_list with the filtered children of the armature...

    print ("Beginning the iteration.")

    for p_bone in pose_bone_list:
        print ("Checking {}".format(p_bone))
        # creates the modifier and sets the armature and bone
        mod_cns = p_bone.constraints.new('COPY_TRANSFORMS')
        mod_cns.target = selection.active_object
        mod_cns.subtarget = p_bone.name
        # applies the pose.
        bpy.ops.pose.visual_transform_apply()
        # Context pedantic:
        p_bone.constraints.remove(mod_cns)


def find_armatures():
    '''
    Sort and sanitize selection;
    In this case make sure we have a source and a target armature.

    USAGE:
    find_armatures()
    No args; will get it's input from bpy.context.selected_objects.
    '''

    # TODO change all this to a more compact list comprehension
    target = bpy.context.scene.objects.active
    if(target.type != 'ARMATURE'):
        print ("Active selection must be the target armature")

    for object in bpy.context.selected_objects:
        if(object.type == 'ARMATURE'):
            print ("\tFound a {};".format(object.type))
