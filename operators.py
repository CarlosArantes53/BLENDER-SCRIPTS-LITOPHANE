import bpy
import os
import numpy as np
from . import geometry

def apply_image_processing(image, props):
    w, h = image.size
    
    pixels = np.empty(w * h * 4, dtype=np.float32)
    image.pixels.foreach_get(pixels)
    
    pixels = pixels.reshape((h, w, 4))
    r, g, b = pixels[:,:,0], pixels[:,:,1], pixels[:,:,2]
    
    if props.img_luminance_mode == 'PERCEPTUAL':
        gray = 0.299 * r + 0.587 * g + 0.114 * b
    else:
        gray = (r + g + b) / 3.0
        
    if props.img_contrast_normalize:
        g_min = gray.min()
        g_max = gray.max()
        if g_max > g_min:
            gray = (gray - g_min) / (g_max - g_min)
            
    if props.img_sharpen > 0 or props.img_cavity_strength > 0:
        up = np.roll(gray, 1, axis=0)
        down = np.roll(gray, -1, axis=0)
        left = np.roll(gray, 1, axis=1)
        right = np.roll(gray, -1, axis=1)
        
        up[0, :] = gray[0, :]
        down[-1, :] = gray[-1, :]
        left[:, 0] = gray[:, 0]
        right[:, -1] = gray[:, -1]
        
        laplacian = (4.0 * gray) - up - down - left - right
        
        if props.img_sharpen > 0:
            gray = gray + (laplacian * props.img_sharpen)
            
        if props.img_cavity_strength > 0:
            edges = np.abs(laplacian)
            gray = gray - (edges * props.img_cavity_strength)
            
    gray = np.clip(gray, 0.0, 1.0)
    
    pixels[:,:,0] = gray
    pixels[:,:,1] = gray
    pixels[:,:,2] = gray
    
    new_name = image.name + "_Processada"
    if new_name in bpy.data.images:
        proc_img = bpy.data.images[new_name]
    else:
        proc_img = bpy.data.images.new(name=new_name, width=w, height=h, alpha=True)
        
    proc_img.pixels.foreach_set(pixels.flatten())
    proc_img.pack()
    
    return proc_img


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

        if props.use_image_processing:
            try:
                img = apply_image_processing(img, props)
            except Exception as e:
                self.report({'WARNING'}, f"Falha no pré-processamento (usando original). Erro: {e}")

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

        obj = geometry.setup_base_mesh(base_width, base_height, props.resolution)
        
        geometry.apply_displacement(obj, img, props.max_thickness_add, invert=props.invert_relief)
        
        if props.flat_back:
            geometry.bake_flat_back_geometry(obj, props.min_thickness)
        created_pivots = geometry.apply_shaping(obj, props)
        
        geometry.finalize_geometry(obj, props, created_pivots)

        self.report({'INFO'}, f"Lithophane {props.model_type} criado!")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MESH_OT_generate_lithophane)

def unregister():
    bpy.utils.unregister_class(MESH_OT_generate_lithophane)