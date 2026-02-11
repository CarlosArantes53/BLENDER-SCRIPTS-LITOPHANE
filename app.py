bl_info = {
    "name": "Gerador de Lithophane Pro",
    "author": "CarlosArantes53",
    "version": (1, 2),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Lithophane",
    "description": "Gera um objeto 3D de lithophane com suavização e base plana",
    "category": "Mesh",
}

import bpy
import os

class LithophaneProperties(bpy.types.PropertyGroup):
    image_path: bpy.props.StringProperty(
        name="Imagem",
        description="Caminho da imagem",
        default="",
        subtype='FILE_PATH'
    )
    
    target_width: bpy.props.FloatProperty(
        name="Largura (mm)",
        description="Largura do lithophane em milimetros",
        default=100.0,
        min=10.0
    )
    
    min_thickness: bpy.props.FloatProperty(
        name="Espessura mínima (mm)",
        description="Espessura das partes mais claras (fundo)",
        default=0.8,
        min=0.1
    )
    
    max_thickness_add: bpy.props.FloatProperty(
        name="Profundidade de cor (mm)",
        description="Quanto mais escuro, maior a espessura adicionada",
        default=2.5,
        min=0.1
    )
    
    resolution: bpy.props.IntProperty(
        name="Nível de Resolução",
        description="Nível de subdivisão (Cuidado: valores altos deixam lento)",
        default=10,
        min=1,
        max=20
    )
    
    use_smooth: bpy.props.BoolProperty(
        name="Suavizar Degraus",
        description="Ajuda a remover o efeito de pixelização/degraus de imagens jpg/png",
        default=True
    )

    smooth_factor: bpy.props.FloatProperty(
        name="Força da Suavização",
        description="Intensidade da suavização",
        default=1.0,
        min=0.0,
        max=2.5
    )
    
    smooth_iters: bpy.props.IntProperty(
        name="Iterações (Qualidade)",
        description="Quantas vezes aplicar o filtro de suavização",
        default=10,
        min=1,
        max=50
    )

    flat_back: bpy.props.BoolProperty(
        name="Gerar Fundo Plano",
        description="Cria uma base reta atrás (Ideal para impressão 3D vertical). Nota: Isso torna a malha editável (aplica modificadores).",
        default=False
    )

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
        
        target_h = props.target_width * aspect

        # 1. Criar o Plano Base
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0,0,0))
        obj = context.active_object
        obj.name = "Lithophane"

        # 2. Subdivisão
        sub = obj.modifiers.new(name="Litho_Subsurf", type='SUBSURF')
        sub.subdivision_type = 'SIMPLE'
        sub.levels = props.resolution
        sub.render_levels = props.resolution

        # 3. Textura e Deslocamento
        tex = bpy.data.textures.new("Litho_Texture", type='IMAGE')
        tex.image = img
        if img.colorspace_settings.name != 'sRGB':
            try:
                img.colorspace_settings.name = 'sRGB'
            except:
                pass
            
        disp = obj.modifiers.new(name="Litho_Displace", type='DISPLACE')
        disp.texture = tex
        disp.texture_coords = 'UV'
        disp.mid_level = 0.0
        disp.strength = -props.max_thickness_add

        # 4. Suavização (O segredo para remover degraus)
        if props.use_smooth:
            smooth = obj.modifiers.new(name="Litho_Smooth", type='SMOOTH')
            smooth.factor = props.smooth_factor
            smooth.iterations = props.smooth_iters

        # 5. Lógica de Espessura e Fundo
        if props.flat_back:
            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -props.min_thickness)})
            bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
        else:
            # MÉTODO PADRÃO (Solidify Modifier - Fundo segue o relevo)
            sol = obj.modifiers.new(name="Litho_Solidify", type='SOLIDIFY')
            sol.thickness = props.min_thickness
            sol.offset = 1.0 

        # 6. Ajustar Tamanho Final
        obj.dimensions = (props.target_width, target_h, obj.dimensions.z)
        bpy.ops.object.transform_apply(scale=True)
        
        bpy.ops.object.shade_smooth()

        self.report({'INFO'}, f"Lithophane criado com sucesso!")
        return {'FINISHED'}

class VIEW3D_PT_lithophane_panel(bpy.types.Panel):
    bl_label = "Lithophane Maker Pro"
    bl_idname = "VIEW3D_PT_lithophane_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lithophane'

    def draw(self, context):
        layout = self.layout
        props = context.scene.lithophane_props

        # Imagem
        layout.label(text="Configuração de Imagem:", icon='IMAGE_DATA')
        row = layout.row()
        row.prop(props, "image_path", text="")

        layout.separator()

        # Dimensões
        layout.label(text="Dimensões:", icon='DRIVER_DISTANCE')
        layout.prop(props, "target_width")
        
        layout.separator()

        # Espessura
        layout.label(text="Espessuras:", icon='MOD_SOLIDIFY')
        col = layout.column(align=True)
        col.prop(props, "min_thickness")
        col.prop(props, "max_thickness_add")
        
        layout.separator()

        # Qualidade
        layout.label(text="Qualidade da Malha:", icon='MOD_SUBSURF')
        layout.prop(props, "resolution")
        
        # Box de Suavização
        box = layout.box()
        box.prop(props, "use_smooth")
        if props.use_smooth:
            col = box.column(align=True)
            col.prop(props, "smooth_factor")
            col.prop(props, "smooth_iters")
            layout.label(text="Dica: Aumente iterações para remover pixels", icon='INFO')

        layout.separator()
        
        # Opção de Fundo Plano
        layout.label(text="Geometria:", icon='MESH_DATA')
        layout.prop(props, "flat_back")

        layout.separator()

        # Botão Gerar
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mesh.generate_lithophane", icon='OUTLINER_OB_IMAGE')

classes = (
    LithophaneProperties,
    MESH_OT_generate_lithophane,
    VIEW3D_PT_lithophane_panel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.lithophane_props = bpy.props.PointerProperty(type=LithophaneProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.lithophane_props

if __name__ == "__main__":
    register()