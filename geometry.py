import bpy
import math

def setup_base_mesh(width, height, resolution, name="Lithophane"):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0,0,0))
    obj = bpy.context.active_object
    obj.name = name
    obj.dimensions = (width, height, 0)
    bpy.ops.object.transform_apply(scale=True)
    
    sub = obj.modifiers.new(name="Litho_Subsurf", type='SUBSURF')
    sub.subdivision_type = 'SIMPLE'
    sub.levels = resolution
    sub.render_levels = resolution
    
    return obj

def apply_displacement(obj, image, strength):
    tex = bpy.data.textures.new(f"{obj.name}_Tex", type='IMAGE')
    tex.image = image
    if image.colorspace_settings.name != 'sRGB':
        try: image.colorspace_settings.name = 'sRGB'
        except: pass
        
    disp = obj.modifiers.new(name="Litho_Displace", type='DISPLACE')
    disp.texture = tex
    disp.mid_level = 0.0
    disp.strength = -strength
    disp.texture_coords = 'UV'

def apply_shaping(obj, props):    
    empty = bpy.data.objects.new("Litho_Pivot", None)
    bpy.context.collection.objects.link(empty)
    empty.location = obj.location
    empty.rotation_euler[0] = math.radians(90)

    m_type = props.model_type

    if m_type == 'FLAT':
        return
        
    elif m_type in {'CURVE_OUTER', 'CURVE_INNER', 'CYLINDER'}:
        bend = obj.modifiers.new(name="Shape_Bend", type='SIMPLE_DEFORM')
        bend.deform_method = 'BEND'
        bend.origin = empty
        bend.deform_axis = 'Z'
        
        if m_type == 'CYLINDER':
            bend.angle = math.radians(360)
            weld = obj.modifiers.new(name="Shape_Weld", type='WELD')
            weld.merge_threshold = 0.01
            
        elif m_type == 'CURVE_OUTER':
            bend.angle = math.radians(props.curve_angle)
        elif m_type == 'CURVE_INNER':
            bend.angle = math.radians(-props.curve_angle)
            
    elif m_type == 'DOME':
        cast = obj.modifiers.new(name="Shape_Dome", type='CAST')
        cast.factor = 1.0
        cast.radius = props.target_width / 2
        obj.modifiers.remove(cast)
        
        bend1 = obj.modifiers.new(name="Dome_X", type='SIMPLE_DEFORM')
        bend1.deform_method = 'BEND'
        bend1.origin = empty
        bend1.deform_axis = 'Z'
        bend1.angle = math.radians(90)
        
        empty2 = bpy.data.objects.new("Litho_Pivot_Y", None)
        bpy.context.collection.objects.link(empty2)
        empty2.rotation_euler[2] = math.radians(90)
        
        bend2 = obj.modifiers.new(name="Dome_Y", type='SIMPLE_DEFORM')
        bend2.deform_method = 'BEND'
        bend2.origin = empty2
        bend2.deform_axis = 'Z'
        bend2.angle = math.radians(90)

def finalize_geometry(obj, min_thickness, use_smooth, smooth_fac, smooth_iter):
    if use_smooth:
        smooth = obj.modifiers.new(name="Litho_Smooth", type='SMOOTH')
        smooth.factor = smooth_fac
        smooth.iterations = smooth_iter

    sol = obj.modifiers.new(name="Litho_Solidify", type='SOLIDIFY')
    sol.thickness = min_thickness
    sol.offset = 1.0
    sol.use_even_offset = True
    sol.use_quality_normals = True
    
    bpy.ops.object.shade_smooth()