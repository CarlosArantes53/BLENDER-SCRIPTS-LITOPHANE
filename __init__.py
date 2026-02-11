bl_info = {
    "name": "Gerador de Lithophane Pro Modular",
    "author": "CarlosArantes53",
    "version": (2, 0),
    "blender": (4, 5, 2),
    "location": "View3D > Sidebar > Lithophane",
    "description": "Gera lithophanes planos, curvos, cilindros e domos",
    "category": "Mesh",
}

import bpy
from . import properties, ui, operators

modules = [properties, ui, operators]

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in reversed(modules):
        mod.unregister()

if __name__ == "__main__":
    register()