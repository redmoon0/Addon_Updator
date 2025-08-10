bl_info = {
    "name": "Version Display Addon",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Version Tab",
    "description": "Shows current addon version in the UI",
    "category": "3D View"
}

import bpy
from . import addon_updater_ops

# Operator to show version
class VERSION_OT_show_version(bpy.types.Operator):
    bl_idname = "wm.show_addon_version"
    bl_label = "Show Version"
    bl_description = "Print the current addon version"

    def execute(self, context):
        version_str = ".".join(map(str, bl_info["version"]))
        self.report({'INFO'}, f"Addon Version: {version_str}")
        print(f"Addon Version: {version_str}")
        return {'FINISHED'}

# UI Panel
class VERSION_PT_panel(bpy.types.Panel):
    bl_label = "Addon Version"
    bl_idname = "VERSION_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Version"

    def draw(self, context):
        layout = self.layout
        version_str = ".".join(map(str, bl_info["version"]))
        layout.label(text=f"Current Version: {version_str}")
        layout.operator("wm.show_addon_version")

class MyAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # Enable auto-check for updates by default
    auto_check_update: bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="Automatically check for updates",
        default=True
    )

    # Check for updates as often as possible
    updater_interval_months: bpy.props.IntProperty(
        name='Months',
        default=0,
        min=0, max=120
    )
    updater_interval_days: bpy.props.IntProperty(
        name='Days',
        default=0,
        min=0, max=31
    )
    updater_interval_hours: bpy.props.IntProperty(
        name='Hours',
        default=0,
        min=0, max=23
    )
    updater_interval_minutes: bpy.props.IntProperty(
        name='Minutes',
        default=1,  # minimum practical interval
        min=0, max=59
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Update Settings (Aggressive Mode)")
        addon_updater_ops.update_settings_ui(self, context)



# Register
classes = (VERSION_OT_show_version, VERSION_PT_panel, MyAddonPreferences)

def register():
    addon_updater_ops.register(bl_info)
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    addon_updater_ops.unregister()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
