import bpy

class LithophaneProperties(bpy.types.PropertyGroup):
    image_path: bpy.props.StringProperty(
        name="Imagem",
        description="Caminho da imagem",
        default="",
        subtype='FILE_PATH'
    )
    
    model_type: bpy.props.EnumProperty(
        name="Formato",
        description="Escolha a geometria base do Lithophane",
        items=[
            ('FLAT', "Plano", "Placa reta tradicional"),
            ('CURVE_OUTER', "Curva Externa", "Curvado para fora (Convexo)"),
            ('CURVE_INNER', "Curva Interna", "Curvado para dentro (Côncavo)"),
            ('CYLINDER', "Cilindro Completo", "Tubo fechado 360 graus"),
            ('DOME', "Domo (Esférico)", "Projeção sobre topo de esfera"),
        ],
        default='FLAT'
    )

    curve_angle: bpy.props.FloatProperty(
        name="Ângulo da Curva",
        description="Graus de curvatura (ex: 180 para meia lua)",
        default=90.0,
        min=10.0,
        max=360.0
    )

    target_width: bpy.props.FloatProperty(
        name="Largura/Diâmetro (mm)",
        description="Largura total (ou diâmetro se for cilindro)",
        default=100.0,
        min=10.0
    )
    
    min_thickness: bpy.props.FloatProperty(
        name="Espessura mínima (mm)",
        default=0.8,
        min=0.1
    )
    
    max_thickness_add: bpy.props.FloatProperty(
        name="Profundidade de cor (mm)",
        default=2.5,
        min=0.1
    )
    
    invert_relief: bpy.props.BoolProperty(
        name="Inverter Relevo (Negativo)",
        description="Se marcado, partes escuras ficam profundas (efeito madeira). Padrão é desmarcado (Lithophane luz).",
        default=False
    )
    
    resolution: bpy.props.IntProperty(
        name="Nível de Resolução",
        description="Subdivisão da malha",
        default=10,
        min=1,
        max=20
    )
    
    use_smooth: bpy.props.BoolProperty(
        name="Suavizar Degraus",
        default=True
    )

    smooth_factor: bpy.props.FloatProperty(
        name="Força da Suavização",
        default=1.0,
        min=0.0, max=2.5
    )
    
    smooth_iters: bpy.props.IntProperty(
        name="Iterações",
        default=10,
        min=1, max=50
    )

    flat_back: bpy.props.BoolProperty(
        name="Gerar Fundo Plano/Liso",
        description="Cria uma superfície posterior lisa. Em Cilindros/Curvas, o interior será um círculo perfeito (sem ondulações).",
        default=False
    )

    apply_modifiers: bpy.props.BoolProperty(
        name="Aplicar Modificadores",
        description="Converte o objeto final em uma malha estática (aplica todos os modificadores) e limpa auxiliares.",
        default=False
    )

def register():
    bpy.utils.register_class(LithophaneProperties)
    bpy.types.Scene.lithophane_props = bpy.props.PointerProperty(type=LithophaneProperties)

def unregister():
    del bpy.types.Scene.lithophane_props
    bpy.utils.unregister_class(LithophaneProperties)