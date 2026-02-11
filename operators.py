import bpy
import os
from . import geometry

class MESH_OT_generate_lithophane(bpy.types.Operator):
    bl_idname = "mesh.generate_lithophane"
    bl_label = "Gerar Lithophane"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.lithophane_props
        img_path = props.image_path

        if not img_path or not os.path.exists(img_path):
            self.report({'ERROR'}, "Selecione uma imagem válida")
            return {'CANCELLED'}

        context.scene.unit_settings.system = 'METRIC'
        context.scene.unit_settings.scale_length = 0.001

        try:
            img = bpy.data.images.load(img_path)
        except:
            self.report({'ERROR'}, "Erro ao carregar a imagem")
            return {'CANCELLED'}

        width_px = img.size[0]
        height_px = img.size[1]
        aspect = height_px / width_px
        
        if props.model_type == 'CYLINDER':
            import math
            perimeter = math.pi * props.target_width
            base_width = perimeter
            base_height = perimeter * aspect 
        else:
            base_width = props.target_width
            base_height = props.target_width * aspect

        # 1. Gerar Malha Base
        obj = geometry.setup_base_mesh(base_width, base_height, props.resolution)
        
        # 2. Aplicar Deslocamento (Imagem)
        geometry.apply_displacement(obj, img, props.max_thickness_add)
        
        # 3. Aplicar Formato (Curva/Cilindro)
        geometry.apply_shaping(obj, props)
        
        # 4. Finalizar (Solidify e Smooth)
        geometry.finalize_geometry(
            obj, 
            props.min_thickness, 
            props.use_smooth, 
            props.smooth_factor, 
            props.smooth_iters
        )

        self.report({'INFO'}, f"Lithophane {props.model_type} criado!")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MESH_OT_generate_lithophane)

def unregister():
    bpy.utils.unregister_class(MESH_OT_generate_lithophane)