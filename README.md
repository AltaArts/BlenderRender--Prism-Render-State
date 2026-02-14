# **BlenderRender state plugin for Prism Pipeline 2**
A plugin to be used with version 2 of Prism Pipeline 

Prism automates and simplifies the workflow of animation and VFX projects.

You can find more information on the website:

https://prism-pipeline.com/

<br/>

## **Release Versions**

For Blender 4.x and Prism 2.0.x, use BlenderRender release version 1.7

For Blender 5.x and Prism 2.1.x, use BlenderRender version 2.x (in progress)

 - NOTE: Docs still show version 1.7

<br/>

![Overview](https://github.com/user-attachments/assets/86d953bf-729c-4d3e-aa44-7af7a921391c)

BlenderRender adds a new state to the StateManager.  This state adds additional functionality to Prism's Blender rendering compared to the more generic default ImageRender.  BlenderRender will only be available in the StateManager of Blender and will not affect other DCC's.  The options selected in the state will not affect the scenefile itself and this plugin will not over-write any existing Prism files, but will patch Prism Blender functions at runtime.

Tooltips are included for all functions.

## **Plugin Usage**

![RenderOptions](https://github.com/user-attachments/assets/308d6034-1479-410f-8c9d-620dcd44e88e)

Many options are automatically toggled and filled based on the selected options.  For example to enable the passes options, the output type EXRmulti should be selected.

AOV auto naming also uses the user-selected options.  For example the logic is:
<pre>
EXR, PNG:               RGB
EXR, PNG with alpha:    RGBA
EXRmulti:               RGB-Data
EXRmulti with alpha:    RGBA-Data

JPG:                    beauty
</pre>
Or any custom AOV names may be utilized by using the Custom checkbox.
<br>
<br>
**Notes:**<br>
- When BlenderRender is enabled, the default ImageRender state will not be available in Blender's StateManager.  All other DCC's will have the normal ImageRender behaviour.  See below to temporarily disable BlenderRender or remove if needed.

- When submitting to a render farm, the Prism option "Submit scenefiles together with jobs" must be checked in order for the farm to use the temporary scenefile.

![Deadline_option](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/5412bd9c-4943-4e2d-89ca-167c7aa5773c)
<br>
<br>

## **Features**

Blender view layers supported.  An override checkbox allows for single layers to be rendered, or if unchecked all layers will be used as normal.
  
![Layers](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/a47723e7-cccb-49f6-8bda-91970b40ea6c)

![FG_element-small](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/9ba243c1-5040-465c-bbac-800f1b9b7db6)![BG_element-small](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/b49ec09b-1122-4acf-abae-26b7430bf885)![Env_layer-small](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/9cf48b98-8b12-48b0-8960-8e5074a7fc6b)![Shadow_layer-small](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/0cf5ccde-66c8-4184-bfee-99d660f1cb83)

<br>
<br>

**Passes per layer**: When adding passes, if the Render Layer override is not checked selected passes will be added/removed to all view layers in the .blend.  But if the override is enabled, passes will be added to the selected layer.  This allows specific passes to be selected for each layer.
  
![Red_passes](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/729611d4-8f8e-48e4-8d3d-0e3a1d567219)  ![Green_passes](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/5c6ef015-3afe-42b1-901b-63a883d6ac5f)

<br>
<br>

**Resolution scaling**: allows quick changing the render's output resolution.  For example when a tracked scene has a non-standard "overscan" resolution, this allows to quickly render a 50% test.  The standard resolution override can be used to select a preset.
  
![Scaling](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/7547fbd7-9c86-472a-bf5e-16838aaeaac6)

<br>
<br>

**Expanded options** for output file types and codecs.
  
![Codecs](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/f8adb875-5834-443e-a19c-c6b89eefedf0)

<br>
<br>

**Color Space override**:  adds the ability to choose the render output colorspace for saved images.  This option is available for .exr output.  When a new BlenderRender state is made, it will default to the .blend's settings under "Output Properties" (either "Follow Scene" or "Override").  This will use the OCIO config that is being used in the current Blender enviroment.  By default, Blender has its own OCIO config, but an "external" OCIO may be utilized via normal methods.  If rendering with separate machines (render farm), ensure the same OCIO config is loaded on each machine, just as in any other DCC.

![Colorspace - inactive](https://github.com/user-attachments/assets/348147f9-419a-4c71-b8bf-f703d04972ee)  ![Colorspace - dropdown](https://github.com/user-attachments/assets/acb2bf6d-558d-4513-9a85-0566c36e65f5)

<br>
<br>

- **Compositor**: option to use or bypass Blenders compositor.
- **Persistent Data**: option to enable Blenders Persistent Data to speed up render scene load times.
- **Alpha channel**: option to render an Alpha channel or not.  This helps reduce un-needed file sizes.

<br>
<br>

## **Installation**

This plugin is for Windows only, as Prism2 only supports Windows at this time.

You can either download the latest stable release version from: [Latest Release](https://github.com/AltaArts/BlenderRender--Prism-Render-State/releases/latest)

or download the current code zip file from the green "Code" button above or on [Github](https://github.com/JBreckeen/BlenderRender--Prism-Render-State/tree/main)

Copy the directory named "BlenderRender" to a directory of your choice, or a Prism2 plugin directory.

Prism's default plugin directories are: *{installation path}\Plugins\Apps* and *{installation Path}\Plugins\Custom*.

It is suggested to have all custom plugins in a seperate folder suchs as: *{drive}\ProgramData\Prism2\plugins\CustomPlugins*

You can add the additional plugin search paths in Prism2 settings.  Go to Settings->Plugins and click the gear icon.  This opens a dialogue and you may add additional search paths at the bottom.

Once added, you can either restart Prism2 (prefered) or select the "Add existing plugin" (plus icon) and navigate to where you saved the BlenderRender folder and then click the "Reload all plugins" button.

![Settings_Plugin_Menubar](https://github.com/AltaArts/BlenderRender--Prism-Render-State/assets/86539171/252061e3-9b15-4683-9e23-80bf872d6595)


## **Disabling**

If a user wants to disable BlenderRender, goto Settings->plugins and uncheck BlenderRender.  Then either restart Prism2 or click the "Reload all plugins" to reload the Blender plugin.

## **Issues / Suggestions**

For any bug reports or suggestions, please add to the GitHub repo.  Known issues are listed in GitHub's project and issues tabs.



