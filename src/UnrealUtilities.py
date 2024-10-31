from unreal import (                                                # import the following functions from unreal.py:
    AssetToolsHelpers,                                              # allows the code to access asset tools
    EditorAssetLibrary,                                             # allows access to the asset library (including loading assets into it or deleting them from it)
    AssetTools,                                                     # allows the organization and manipulation of assets
    Material,                                                       # allows creation/manipulation of materials
    MaterialFactoryNew,                                             # allows for the creation/addition of material factories (material presets)
    MaterialEditingLibrary,                                         # allows the manipulation of material properties
    MaterialExpressionTextureSampleParameter2D as TexSample2D,      # accesses Unreal's default sample textures - given a shorthand name
    MaterialProperty,                                               # allows the manipulation of material properties (the creation & connecting of nodes/properties)
    AssetImportTask,                                                # contains necessary information for assets to be imported
    FbxImportUI                                                     # contains necessary information for processing FBX files into Unreal
)                                                                   #

import os                                                           # importing native operating system

class UnrealUtility:                                                                    # defining the class
    def __init__(self):                                                                 # establishing variables to be used throughout the class
        self.substanceRootDir='/game/Substance/'                                        # creating a directory for a 'Substance' folder
        self.substanceBaseMatName = 'M_SubstanceBase'                                   # creating a name for the base material to be created
        self.substanceBaseMatPath = self.substanceRootDir + self.substanceBaseMatName   # creating a directory for the material within that folder
        self.substanceTempFolder = 'game/Substance/temp'                                # creating a 'Temp' folder within the 'Substance' folder
        self.baseColorName = "BaseColor"                                                # creating a name for the Albedo channel of the material
        self.normalName = "Normal"                                                      # creating a name for the Normal channel of the material
        self.occRoughnessMetalic = "OcclusionRoughnessMetalic"                          # creating a name for the ORM channel of the material
        
    def GetAssetTools(self)->AssetTools:                                                # defining the function
        return AssetToolsHelpers.get_asset_tools()                                      # calling the asset tools from AssetToolsHelpers
    
    def ImportFromDir(self, dir):                                                       # defining the function
        for file in os.listdir(dir):                                                    # for each file in the designated directory (see 'LoadMeshEntryScript' in 'UnrealSubstancePlugin'),
            if ".fbx" in file:                                                          # if the file ends in '.fbx',
                self.LoadMeshFromPath(os.path.join(dir, file))                          # execute 'LoadMeshFromPath' (see below) using the specified file and directory

    def LoadMeshFromPath(self, meshPath):                                               # defining the function
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")                      # defining the meshName as the end result of the file path with the '.fbx' file ending removed
        importTask = AssetImportTask()                                                  # assigning a variable to the class in unreal.py 'AssetImportTask()'
        importTask.replace_existing = True                                              # calling on AssetImportTask() to overwrite existing assets of the same name
        importTask.filename = meshPath                                                  # the end result of the file path for the mesh is the name to use for the mesh
        importTask.destination_path = '/game/' + meshName                               # defining the destination for the imported mesh (a folder of the same name as the mesh within the 'Content' folder)
        importTask.automated = True                                                     # opting to automate the manual steps of the import process
        importTask.save = True                                                          # opting to save after importing

        fbxImportOption = FbxImportUI()                                                 # assigning a variable to the information contained within 'FbxImportUI()'
        fbxImportOption.import_mesh = True                                              # setting whether to import the mesh
        fbxImportOption.import_as_skeletal = False                                      # setting whether to import mesh bones
        fbxImportOption.import_materials = False                                        # setting whether to import built-in mesh materials
        fbxImportOption.static_mesh_import_data.combine_meshes = True                   # setting whether to combine any separated meshes within the model
        importTask.options = fbxImportOption                                            # setting the import options to the above-specified choices & information
        
        self.GetAssetTools().import_asset_tasks([importTask])                           # get a list of the options (tasks) from AssetImportTask() as they were defined above
        return importTask.get_objects()[0]                                              # list the first object imported

    def FindOrBuildBaseMaterial(self):                                                  # defining the function
        if EditorAssetLibrary.does_asset_exist(self.substanceBaseMatPath):              # if the specified material asset already exists,
            return EditorAssetLibrary.load_asset(self.substanceBaseMatPath)             # update that material instead of creating a new one
        
        baseMat = self.GetAssetTools().create_asset(self.substanceBaseMatName, self.substanceRootDir, Material, MaterialFactoryNew())   # creating the material asset
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0)                                    # creating a node in the material editor for base color
        baseColor.set_editor_property("parameter_name", self.baseColorName)                                                             # setting the name of the node
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)                              # connecting the RGB channel of the node to the material's base color attribute

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)                                     # creating a node in the material editor for the normal map
        normal.set_editor_property("parameter_name", self.normalName)                                                                   # setting the name of the node
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))                   # loading in the sample normal map from Unreal Engine's asset library
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)                                     # connecting the RGB channel of the node to the material's normal attribute

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 800)                        # creating a node in the material editor for the AO, roughness and metallic channels
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalic)                                             # setting the name of the node
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)               # connecting the R channel of the node to the material's ambient occlusion attribute
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS)                       # connecting the G channel of the node to the material's roughness attribute
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC)                        # connecting the B channel of the node to the material's metalness attribute

        EditorAssetLibrary.save_asset(baseMat.get_path_name())                          # save the asset
        return baseMat                                                                  # return the newly created material asset