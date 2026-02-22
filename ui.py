import bpy

class VIEW3D_PT_lithophane_panel(bpy.types.Panel):
    bl_label = "Lithophane Maker Pro"
    bl_idname = "VIEW3D_PT_lithophane_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lithophane'

    def draw(self, context):
        layout = self.layout
        props = context.scene.lithophane_props

        box = layout.box()
        box.label(text="1. Imagem Base", icon='IMAGE_DATA')
        box.prop(props, "image_path", text="")

        box = layout.box()
        box.label(text="2. Pré-Processamento", icon='NODE_COMPOSITING')
        box.prop(props, "use_image_processing", toggle=True)
        
        if props.use_image_processing:
            box.prop(props, "img_luminance_mode")
            box.prop(props, "img_contrast_normalize")
            row = box.row()
            row.prop(props, "img_sharpen")
            row.prop(props, "img_cavity_strength")

        box = layout.box()
        box.label(text="3. Geometria", icon='MESH_DATA')
        box.prop(props, "model_type")
        
        if props.model_type in {'CURVE_OUTER', 'CURVE_INNER'}:
            box.prop(props, "curve_angle")

        box.prop(props, "target_width")

        box = layout.box()
        box.label(text="4. Detalhes do Relevo", icon='MOD_SOLIDIFY')
        row = box.row()
        row.prop(props, "min_thickness")
        row.prop(props, "max_thickness_add")
        box.prop(props, "invert_relief", toggle=True)
        
        box.prop(props, "resolution")
        box.prop(props, "use_smooth")
        
        if props.use_smooth:
            row = box.row()
            row.prop(props, "smooth_factor")
            row.prop(props, "smooth_iters")

        box = layout.box()
        box.label(text="5. Finalização", icon='CHECKBOX_HLT')
        box.prop(props, "flat_back")
        box.prop(props, "apply_modifiers")

        layout.separator()
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mesh.generate_lithophane", icon='OUTLINER_OB_IMAGE', text="Gerar Lithophane 3D")

def register():
    bpy.utils.register_class(VIEW3D_PT_lithophane_panel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_lithophane_panel)