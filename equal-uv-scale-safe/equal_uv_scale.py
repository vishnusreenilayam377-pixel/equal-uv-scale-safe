bl_info = {
    "name": "Equal UV Scale (Safe)",
    "author": "vishnu.s",
    "version": (1, 2, 0),
    "blender": (3, 0, 0),
    "location": "UV Editor > Sidebar > Equal UV",
    "description": "Equalize UV scale without collapsing UVs (uses Blender native algorithm)",
    "category": "UV",
}

import bpy


class UV_OT_equal_uv_scale_safe(bpy.types.Operator):
    bl_idname = "uv.equal_uv_scale_safe"
    bl_label = "Equal UV Scale"
    bl_description = "Equalize UV scale safely (keeps UVs exactly as-is)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.edit_object is not None and
            context.edit_object.type == 'MESH'
        )

    def execute(self, context):

        if context.area.type != 'IMAGE_EDITOR':
            self.report({'ERROR'}, "Run this from the UV Editor")
            return {'CANCELLED'}

        # Call Blender's internal, proven operator
        bpy.ops.uv.average_islands_scale()

        return {'FINISHED'}


class UV_PT_equal_uv_panel(bpy.types.Panel):
    bl_label = "Equal UV Scale"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Equal UV'

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Texel Density", icon='UV')

        col = box.column(align=True)
        col.label(text="Safely equalize UV scale")
        col.label(text="(No UV distortion)")

        col.separator()

        col.operator(
            "uv.equal_uv_scale_safe",
            text="Equal UV Scale",
            icon='FULLSCREEN_ENTER'
        )


classes = (
    UV_OT_equal_uv_scale_safe,
    UV_PT_equal_uv_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
