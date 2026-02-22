import bpy

class LithophaneProperties(bpy.types.PropertyGroup):
    image_path: bpy.props.StringProperty(
        name="Imagem",
        description="Caminho da imagem",
        default="",
        subtype='FILE_PATH'
    )
    
    use_image_processing: bpy.props.BoolProperty(
        name="Ativar Pré-Processamento (Recomendado)",
        description="Aplica cálculos de matriz para melhorar o contraste e nitidez antes do 3D",
        default=True
    )
    
    img_luminance_mode: bpy.props.EnumProperty(
        name="Conversão de Cores",
        description="Técnica 3: Como transformar as cores em tons de cinza",
        items=[
            ('PERCEPTUAL', "Perceptual (Rec.709)", "Ajusta verde/azul como o olho humano vê"),
            ('SIMPLE', "Média Simples", "(R+G+B)/3"),
        ],
        default='PERCEPTUAL'
    )
    
    img_contrast_normalize: bpy.props.BoolProperty(
        name="Maximizar Contraste (Levels)",
        description="Técnica 2: Força os tons mais escuros a ficarem 100% pretos e os claros 100% brancos",
        default=True
    )
    
    img_sharpen: bpy.props.FloatProperty(
        name="Nitidez (Sharpen)",
        description="Técnica 1: Realça bordas aplicando matriz de convolução (Laplaciano)",
        default=0.5, min=0.0, max=3.0
    )
    
    img_cavity_strength: bpy.props.FloatProperty(
        name="Cavidade (Escurecer Bordas)",
        description="Técnica 4: Aprofunda fendas e contornos simulando Ambient Occlusion no relevo",
        default=0.2, min=0.0, max=2.0
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
        description="Cria uma superfície posterior lisa. Em Cilindros/Curvas, o interior será um círculo perfeito.",
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