# **BlenderRender state plugin for Prism Pipeline 2**
A plugin to be used with version 2 of Prism Pipeline 

Prism automates and simplifies the workflow of animation and VFX projects.

You can find more information on the website:

https://prism-pipeline.com/

![Overview](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/405a7826-9605-4690-9ef3-bec9be5b864f)


## **Plugin Usage**

BlenderRender adds a new state to the StateManager.  This state adds additional functionality to Prism's Blender rendering compared to the more generic default ImageRender.  The options selected in the state will not affect to scenefile itself.

![Render_option](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/9c4c40a2-333d-4188-bbc8-a544b8ecf452)

Many options are automatically changed and filled based on the output file type selected.  For example to enable the passes options, the output type must be EXRmulti.

AOV auto naming also uses the user selected options.  If EXRmulti is selected, the default name will be RGB-Data, and if an Alpha channel is used then it will changed to RGBA.  Any custom AOV names may be utilized by using the Custom checkbox.


Note:  When submitting to a render farm, the Prism option "Submit scenefiles together with jobs" must be checked in order for the farm to use the temporary edited scenefile.

![Deadline_option](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/5412bd9c-4943-4e2d-89ca-167c7aa5773c)


Features:

- Blender view layers supported.  An override checkbox allows for single layers to be rendered, or if unchecked all layers will be used as normal.
- 
![Layers](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/d71f6f63-cefb-4038-97de-4e2302af0608)

- 
- Render resolution scaling.
- Option to use or bypass Blenders compositor.
- Option to render an Alpha channel or not.  This helps reduce un-needed file sizes.
- Expanded options for output file types and codecs.
- Re-ordered interface
- 





## **Installation**

This plugin is for Windows only, as Prism2 only supports Windows at this time.

You can either download the latest stable release version from: [Latest Release](https://github.com/AltaArts/DeleteFunctions--Prism-Plugin/releases/latest)

or download the current code zip file from the green "Code" button above or on [Github](https://github.com/JBreckeen/DeleteFunctions--Prism-Plugin/tree/main)

Copy the directory named "BlenderRender" to a directory of your choice, or a Prism2 plugin directory.

Prism's default plugin directories are: *{installation path}\Plugins\Apps* and *{installation Path}\Plugins\Custom*.

It is suggested to have all custom plugins in a seperate folder suchs as: *{drive}\ProgramData\Prism2\plugins\CustomPlugins*

You can add the additional plugin search paths in Prism2 settings.  Go to Settings->Plugins and click the gear icon.  This opens a dialogue and you may add additional search paths at the bottom.

Once added, you can either restart Prism2 (prefered) or select the "Add existing plugin" (plus icon) and navigate to where you saved the DeleteFunctions folder and then click the "Reload all plugins" button.

![Settings_Plugin_Menubar](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/252061e3-9b15-4683-9e23-80bf872d6595)


## **Disabling**

If a user wants to disable BlenderRender, goto Settings->plugins and uncheck BlenderRender.  Then either restart Prism2 or click the "Reload all plugins" to reload the Blender plugin.

## **Issues / Suggestions**

For any bug reports or suggestions, please add to the GitHub repo.  Known issues are listed in GitHub's project and issues tabs.



