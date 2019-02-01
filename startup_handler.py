import bpy
import os
from bpy.app.handlers import persistent

from .preferences import get_addon_preferences
from .functions.misc_functions import get_size, absolute_path
from .functions.load_favorites import load_favorites
from .functions.check_size import check_size_changes
from .functions.load_json import load_json_font_file

from .global_variable import json_file, json_favorites
from .global_messages import print_statement, settings_loaded_msg, changes_msg, no_changes_msg

@persistent
def fontselector_startup(scene):
    addon_preferences = get_addon_preferences()
    behavior = addon_preferences.startup_check_behavior
    prefpath = absolute_path(addon_preferences.prefs_folderpath)
    # get prefs files
    json_favorites_file = os.path.join(prefpath, json_favorites)
    json_list_file = os.path.join(prefpath, json_file)

    font_collection = bpy.data.window_managers['WinMan'].fontselector_list
    subdir_collection = bpy.data.window_managers['WinMan'].fontselector_sub

    #check preference path exist
    if os.path.isdir(prefpath) :
        #check font list
        if os.path.isfile(json_list_file) :

            if behavior in {'AUTOMATIC_UPDATE', 'MESSAGE_ONLY'} :
                chk_changes = check_size_changes()

                if chk_changes :
                    print(print_statement + changes_msg)

                    if behavior == 'AUTOMATIC_UPDATE' :
                        bpy.ops.fontselector.modal_refresh()

                    else :
                        bpy.ops.fontselector.dialog_message('INVOKE_DEFAULT', code = 1)

                else :
                    print(print_statement + no_changes_msg)
                    # load json list
                    load_json_font_file(json_list_file, font_collection, subdir_collection)
            
            else :
                # load json list
                load_json_font_file(json_list_file, font_collection, subdir_collection)

            # load favorite list
            if os.path.isfile(json_favorites_file) and len(font_collection) > 0 :
                load_favorites()
            
            # return state to user
            print(print_statement + settings_loaded_msg)