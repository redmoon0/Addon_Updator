bl_info = {
    "name": "My Addon with Update Checker",
    "author": "Your Name",
    "version": (1, 0, 0.1),
    "blender": (2, 80, 0),
    "description": "Example addon with GitHub update checker.",
    "category": "System",
}

import bpy
from . import addon_updater  # Import our updater module


class UPDATECHECKER_OT_check(bpy.types.Operator):
    bl_idname = "updatechecker.check"
    bl_label = "Check for Updates"

    def execute(self, context):
        current_version = bl_info["version"]
        latest_version = addon_updater1.get_latest_version(
            owner="YOUR_GITHUB_USERNAME",
            repo="YOUR_REPO_NAME",
            use_releases=True,
            token=context.preferences.addons[__name__].preferences.github_token
        )

        if not latest_version:
            self.report({'ERROR'}, "Could not fetch latest version.")
            return {'CANCELLED'}

        if addon_updater1.is_newer_version(current_version, latest_version):
            self.report({'INFO'}, f"Update available: {latest_version}")
        else:
            self.report({'INFO'}, "You are using the latest version.")

        return {'FINISHED'}


class UPDATECHECKER_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    github_token: bpy.props.StringProperty(
        name="GitHub Token",
        description="GitHub personal access token for private repos",
        subtype='PASSWORD',
        default=""
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "github_token")


class UPDATECHECKER_PT_panel(bpy.types.Panel):
    bl_label = "Update Checker"
    bl_idname = "UPDATECHECKER_PT_panel"
    bl_space_type = "PREFERENCES"
    bl_region_type = "WINDOW"
    bl_context = "addons"

    def draw(self, context):
        layout = self.layout
        layout.operator("updatechecker.check", icon="FILE_REFRESH")


classes = (
    UPDATECHECKER_OT_check,
    UPDATECHECKER_Preferences,
    UPDATECHECKER_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
