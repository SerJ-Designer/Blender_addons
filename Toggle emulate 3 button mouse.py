bl_info = {
    "name": "Toggle Emulate 3 Button Mouse",
    "author": "SerJ https://github.com/SerJ-Designer",
    "version": (1, 0),
    "blender": (5, 0, 0),
    "location": "Topbar (next to Edit menu) / Hotkey: Ctrl+Shift+Alt+E",
    "description": "Quickly toggle the 'Emulate 3 Button Mouse' input preference",
    "category": "Interface",
}

import bpy

class ToggleEmulate3ButtonMouse(bpy.types.Operator):
    """Toggle the Emulate 3 Button Mouse preference"""
    bl_idname = "preferences.toggle_emulate_3_button_mouse"
    bl_label = "Em. 3 Button"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the current input preferences
        prefs = context.preferences
        input_prefs = prefs.inputs

        # Toggle the setting
        input_prefs.use_mouse_emulate_3_button = not input_prefs.use_mouse_emulate_3_button

        # Report status to the user
        status = "ON" if input_prefs.use_mouse_emulate_3_button else "OFF"
        self.report({'INFO'}, f"Emulate 3 Button Mouse: {status}")

        # Force UI update
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        return {'FINISHED'}

def menu_draw(self, context):
    """Draw the toggle button in the topbar menu"""
    layout = self.layout
    layout.separator()
    layout.operator("preferences.toggle_emulate_3_button_mouse")

def register():
    bpy.utils.register_class(ToggleEmulate3ButtonMouse)
    # Add to topbar menu (next to Edit menu)
    bpy.types.VIEW3D_MT_editor_menus.append(menu_draw)

    # Register a default keymap (Ctrl+Shift+Alt+E)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new(
            "preferences.toggle_emulate_3_button_mouse",
            type='E',
            value='PRESS',
            ctrl=True,
            shift=True,
            alt=True
        )

def unregister():
    # Remove keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.get('Window')
        if km:
            for kmi in km.keymap_items:
                if kmi.idname == "preferences.toggle_emulate_3_button_mouse":
                    km.keymap_items.remove(kmi)
                    break

    # Remove from menu
    bpy.types.VIEW3D_MT_editor_menus.remove(menu_draw)
    bpy.utils.unregister_class(ToggleEmulate3ButtonMouse)

if __name__ == "__main__":
    register()