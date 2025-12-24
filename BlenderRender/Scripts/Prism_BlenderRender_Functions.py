# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.
####################################################
#
#           BlenderRender State Plugin for Prism2
#
#                 Joshua Breckeen
#                    Alta Arts
#                josh@alta-arts.com
#
####################################################


#   This Prism2 plugin will add a render state named BlenderRender to the state manager.  This provides
#   more functunality to Blender's rendering including view layers.  This plugin will patch some of
#   Prism's original Blender functions to allow BlenderRender to function, and with the plugin enabled, the
#   default ImageRender state will not work.  This is non-destructive.


import os
import sys
import platform
import time
import traceback
import logging

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


from PrismUtils.Decorators import err_catcher_plugin as err_catcher
from BlenderRender import BlenderRenderClass

logger = logging.getLogger(__name__)


def renderFinished_handler(dummy):
    import bpy
    bpy.context.scene["PrismIsRendering"] = False



class Prism_BlenderRender_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self)
        self.core.registerCallback("pluginLoaded", self.onPluginLoaded, plugin=self)

        self.blendPlugin = self.core.getPlugin("Blender")
        self.applyBlendPatch()


    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True
    

    @err_catcher(name=__name__)
    def onPluginLoaded(self, plugin):
        # check if the loaded plugin is to be patched
        if plugin.pluginName == "Blender":
            self.applyBlendPatch()


    @err_catcher(name=__name__)
    def applyBlendPatch(self):
        #   Ensures it is not using the Blender_unloaded plugin
        if hasattr(self.blendPlugin, "startup"):
            logger.debug("*** Patching Blender Plugin ***")
            
            #   Functions in Prism_Blender_Functions.py to be patched
            patchList = ["setFPS",
                         "sm_render_refreshPasses", 
                         "getViewLayerAOVs",
                         "getAvailableAOVs",
                         "removeAOV",
                         "enableViewLayerAOV",
                         "sm_render_preSubmit",
                         "sm_render_startLocalRender",
                         "sm_render_undoRenderSettings",
                         "sm_render_getRenderPasses",
                         "sm_render_addRenderPass",
                         "sm_render_getDeadlineParams"
                         ]
            
            #   Iterate through list and patches each
            for patch in patchList:
                try:
                    origFunc = getattr(self.blendPlugin, patch)
                    patchedFunc = getattr(self, patch)
                    self.core.plugins.monkeyPatch(origFunc, patchedFunc, self, force=True)

                    logger.debug(f"Patched:  {patch}")
                    
                except Exception as e:
                    logger.warning(f"Unable to patch: {patch}\n"
                                   f"      {e}")

            addFuncList = ["getRenderSamples",
                           "useCompositor",
                           "getPersistentData",
                           "getRenderLayers",
                           "getColorSpaces",
                           "setTempScene",
                           "nextRenderslot",
                           "setupLayers"]
            
            #   Iterate through list and adds each
            for func in addFuncList:
                try:
                    addedFunc = getattr(self, func)
                    setattr(self.blendPlugin, func, addedFunc)

                    logger.debug(f"Added method:  {func}")
                except Exception as e:
                    logger.warning(f"Unable to add method: {func}\n"
                                   f"      {e}")
 

    @err_catcher(name=__name__)
    def onStateManagerOpen(self, origin):
        if self.core.appPlugin.pluginName == "Blender":
            #   Will only load BlenderRender if in Blender
            try:
                origin.loadState(BlenderRenderClass)
                logger.debug("Added BlenderRender state")
            except Exception as e:
                logger.warning(f"Unable to load BlenderRender state:\n{e}")

            #   Removes default ImageRender state
            try:
                del origin.stateTypes["ImageRender"]
                logger.debug("Removed default ImageRender state")
            except Exception as e:
                logger.warning(f"Unable to remove ImageRender state:\n{e}")


    @err_catcher(name=__name__)
    def setFPS(self, origin, fps):
        import bpy, math                                                        #   ADDED

        if isinstance(fps, int):                                                #   EDITED to fix FPS check
            bpy.context.scene.render.fps = fps                                  #   EDITED
        else:
            intFps = math.ceil(fps)
            bpy.context.scene.render.fps = intFps
            bpy.context.scene.render.fps_base = intFps/fps


    @err_catcher(name=__name__)
    def sm_render_refreshPasses(self, origin, renderLayer):                     #   EDITED
        origin.lw_passes.clear()

        passNames = self.blendPlugin.getNodeAOVs()                              #   EDITED
        origin.b_addPasses.setVisible(not passNames)
        self.blendPlugin.canDeleteRenderPasses = bool(not passNames)            #   EDITED
        if not passNames:
            passNames = self.getViewLayerAOVs(renderLayer)                      #   EDITED

        if passNames:
            origin.lw_passes.addItems(passNames)


    @err_catcher(name=__name__)
    def getViewLayerAOVs(self, renderLayer):                                    #   EDITED
        import bpy, operator                                                    #   ADDED

        availableAOVs = self.getAvailableAOVs(renderLayer)                      #   EDITED

        #   Get currently selected view layer
        try:                                                                    #   ADDED
            curlayer = bpy.context.scene.view_layers[renderLayer]               #   ADDED
        #   Handles the issue with a renamed view-layer
        except KeyError:                                                        #   ADDED
            curlayer = bpy.context.window_manager.windows[0].view_layer
            
        aovNames = []
        for aa in availableAOVs:
            val = None
            try:
                val = operator.attrgetter(aa["parm"])(curlayer)
            except AttributeError:
                logging.debug("Couldn't access aov %s" % aa["parm"])
                pass

            if val:
                if aa["name"] == "Cryptomatte Accurate" and bpy.app.version >= (4, 0, 0):
                    continue
                aovNames.append(aa["name"])

        return aovNames


    @err_catcher(name=__name__)                 
    def getAvailableAOVs(self, renderLayer):                                        #   EDITED
        import bpy                                                                  #   ADDED

        #   Get currently selected view layer
        try:                                                                        #   ADDED
            curlayer = bpy.context.scene.view_layers[renderLayer]                   #   ADDED
        #   Handles the issue with a renamed view-layer
        except KeyError:                                                            #   ADDED
            curlayer = bpy.context.window_manager.windows[0].view_layer

        aovParms = [x for x in dir(curlayer) if x.startswith("use_pass_")]
        aovParms += [
            "cycles." + x for x in dir(curlayer.cycles) if x.startswith("use_pass_")
        ]
        aovs = [
            {"name": "Denoising Data", "parm": "cycles.denoising_store_passes"},
            {"name": "Render Time", "parm": "cycles.pass_debug_render_time"},
        ]
        nameOverrides = {
            "Emit": "Emission",
        }
        for aov in aovParms:
            name = aov.replace("use_pass_", "").replace("cycles.", "")
            name = [x[0].upper() + x[1:] for x in name.split("_")]
            name = " ".join(name)
            name = nameOverrides[name] if name in nameOverrides else name
            aovs.append({"name": name, "parm": aov})

        aovs = sorted(aovs, key=lambda x: x["name"])

        return aovs


    @err_catcher(name=__name__)
    def removeAOV(self, aovName, renderLayer):                                      #   EDITED
        import bpy                                                                  #   ADDED

        if self.blendPlugin.useNodeAOVs():                                          #   EDITED
            rlayerNodes = [
                x for x in bpy.context.scene.node_tree.nodes if x.type == "R_LAYERS"
                ]

            for m in rlayerNodes:
                connections = []
                for i in m.outputs:
                    if len(list(i.links)) > 0:
                        connections.append(i.links[0])
                        break

                for i in connections:
                    if i.to_node.type == "OUTPUT_FILE":
                        for idx, k in enumerate(i.to_node.file_slots):
                            links = i.to_node.inputs[idx].links
                            if len(links) > 0:
                                if links[0].from_socket.node != m:
                                    continue

                                passName = links[0].from_socket.name
                                layerName = links[0].from_socket.node.layer

                                if passName == "Image":
                                    passName = "beauty"

                                if (
                                    passName == aovName.split("_", 1)[1]
                                    and layerName == aovName.split("_", 1)[0]
                                    ):
                                    i.to_node.inputs.remove(i.to_node.inputs[idx])
                                    return
        else:
            self.enableViewLayerAOV(aovName, renderLayer, enable=False)             #   EDITED


    @err_catcher(name=__name__)
    def enableViewLayerAOV(self, name, renderLayer, enable=True):                   #   EDITED
        import bpy                                                                  #   EDITED

        aa = self.getAvailableAOVs(renderLayer)                                     #   EDITED
        curAOV = [x for x in aa if x["name"] == name]
        if not curAOV:
            return

        curAOV = curAOV[0]
        curlayer = bpy.context.scene.view_layers[renderLayer]                       #   EDITED

        attrs = curAOV["parm"].split(".")
        obj = curlayer
        for a in attrs[:-1]:
            obj = getattr(obj, a)

        setattr(obj, attrs[-1], enable)


    @err_catcher(name=__name__)
    def sm_render_preSubmit(self, origin, rSettings):
        import bpy                                                                      #   ADDED

        if origin.chb_resOverride.isChecked():
            rSettings["width"] = bpy.context.scene.render.resolution_x
            rSettings["height"] = bpy.context.scene.render.resolution_y
            bpy.context.scene.render.resolution_x = origin.sp_resWidth.value()
            bpy.context.scene.render.resolution_y = origin.sp_resHeight.value()

        nodeAOVs = self.blendPlugin.getNodeAOVs()                                       #   EDITED
        imgFormat = origin.cb_format.currentText()

        if imgFormat == ".exr":                                                         #   EDITED
            fileFormat = "OPEN_EXR"                                                     
        elif imgFormat == ".exrMulti":
            fileFormat = "OPEN_EXR_MULTILAYER"
        elif imgFormat == ".png":
            fileFormat = "PNG"
        elif imgFormat == ".jpg":
            fileFormat = "JPEG"

        rSettings["prev_start"] = bpy.context.scene.frame_start
        rSettings["prev_end"] = bpy.context.scene.frame_end
        # rSettings["fileformat"] = bpy.context.scene.render.image_settings.file_format
        rSettings["overwrite"] = bpy.context.scene.render.use_overwrite
        rSettings["fileextension"] = bpy.context.scene.render.use_file_extension
        rSettings["resolutionpercent"] = bpy.context.scene.render.resolution_percentage


#################################################################################
#    vvvvvvvvvvvvvvvvvvvvv           ADDED         vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        rSettings["origSamples"] = bpy.context.scene.cycles.samples

        rSettings["origImageType"] = bpy.context.scene.render.image_settings.media_type

        rSettings["origImageformat"] = bpy.context.scene.render.image_settings.file_format
        rSettings["origExrCodec"] = bpy.context.scene.render.image_settings.exr_codec
        rSettings["origBitDepth"] = bpy.context.scene.render.image_settings.color_depth
        rSettings["origAlpha"] = bpy.context.scene.render.image_settings.color_mode
        rSettings["origPersData"] = bpy.context.scene.render.use_persistent_data

        rSettings["origUseComp"] = bpy.context.scene.render.use_compositing
        try:
            rSettings["origUseNode"] = bpy.context.scene.use_nodes
        except:
            logger.debug("The Blender Compositor 'Use Nodes' is deprecated.")

        if fileFormat in ["OPEN_EXR", "OPEN_EXR_MULTILAYER"]:
            rSettings["origOvrColorspace"] = bpy.context.scene.render.image_settings.color_management
            rSettings["origColorspace"] = bpy.context.scene.render.image_settings.linear_colorspace_settings.name

        self.blendPlugin.setTempScene(rSettings, origin)    

        rSettings = self.setupLayers(rSettings, mode="Set")
        aovName = rSettings["aovName"]
        tempOutputName = rSettings["outputName"]
        tempOutputName = tempOutputName.replace("beauty", aovName)
        tempOutputName = tempOutputName.replace("exrMulti", "exr")
        
        rSettings["outputName"] = tempOutputName


#    ^^^^^^^^^^^^^^^^^^^^^          ADDED       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#####################################################################################


        rSettings["origOutputName"] = rSettings["outputName"]
        bpy.context.scene["PrismIsRendering"] = True
        bpy.context.scene.render.filepath = rSettings["outputName"]

        bpy.context.scene.render.use_overwrite = True
        bpy.context.scene.render.use_file_extension = False
        # bpy.context.scene.render.resolution_percentage = 100                      #   COMMENTED OUT FOR TEMP SCENE
        bpy.context.scene.camera = bpy.context.scene.objects[origin.curCam]

        usePasses = False
        if self.blendPlugin.useNodeAOVs():                                          #   EDITED
            outNodes = [
                x for x in bpy.context.scene.node_tree.nodes if x.type == "OUTPUT_FILE"
                ]
            rlayerNodes = [
                x for x in bpy.context.scene.node_tree.nodes if x.type == "R_LAYERS"
                ]

            for m in outNodes:
                connections = []
                for idx, i in enumerate(m.inputs):
                    if len(list(i.links)) > 0:
                        connections.append([i.links[0], idx])

                m.base_path = os.path.dirname(rSettings["outputName"])

                for i, idx in connections:
                    passName = i.from_socket.name

                    if passName == "Image":
                        passName = "beauty"

                    if i.from_node.type == "R_LAYERS":
                        if len(rlayerNodes) > 1:
                            passName = "%s_%s" % (i.from_node.layer, passName)

                    else:
                        if hasattr(i.from_node, "label") and i.from_node.label != "":
                            passName = i.from_node.label

                    extensions = {
                        "PNG": ".png",
                        "JPEG": ".jpg",
                        "JPEG2000": "jpg",
                        "TARGA": ".tga",
                        "TARGA_RAW": ".tga",
                        "OPEN_EXR_MULTILAYER": ".exr",
                        "OPEN_EXR": ".exr",
                        "TIFF": ".tif",
                        }
                    nodeExt = extensions[m.format.file_format]
                    curSlot = m.file_slots[idx]
                    if curSlot.use_node_format:
                        ext = nodeExt
                    else:
                        ext = extensions[curSlot.format.file_format]

                    curSlot.path = "../%s/%s" % (
                        passName,
                        os.path.splitext(os.path.basename(rSettings["outputName"]))[
                            0
                        ].replace("beauty", passName)
                        + ext,
                        )
                    newOutputPath = os.path.abspath(
                        os.path.join(
                            rSettings["outputName"],
                            "../..",
                            passName,
                            os.path.splitext(os.path.basename(rSettings["outputName"]))[
                                0
                            ].replace("beauty", passName)
                            + ext,
                            )
                        )
                    usePasses = True

        if usePasses:
            rSettings["outputName"] = newOutputPath
            if platform.system() == "Windows":
                tmpOutput = os.path.join(
                    os.environ["temp"], "PrismRender", "tmp.####" + imgFormat
                    )
                bpy.context.scene.render.filepath = tmpOutput
                if not os.path.exists(os.path.dirname(tmpOutput)):
                    os.makedirs(os.path.dirname(tmpOutput))


    @err_catcher(name=__name__)
    def sm_render_startLocalRender(self, origin, outputName, rSettings):
        import bpy                                                                          #   ADDED

        # renderAnim = bpy.context.scene.frame_start != bpy.context.scene.frame_end         #   COMMENTED FROM PRISM
        try:
            if not origin.renderingStarted:
                origin.waitmsg = QMessageBox(
                    QMessageBox.NoIcon,
                    "ImageRender",
                    "Local rendering - %s - please wait.." % origin.state.text(0),
                    QMessageBox.Cancel,
                    )
                #    self.core.parentWindow(origin.waitmsg)                                 #   COMMENTED FROM PRISM
                #    origin.waitmsg.buttons()[0].setHidden(True)
                #    origin.waitmsg.show()
                #    QCoreApplication.processEvents()


                bpy.app.handlers.render_complete.append(renderFinished_handler)
                bpy.app.handlers.render_cancel.append(renderFinished_handler)

                self.renderedChunks = []

            ctx = self.blendPlugin.getOverrideContext(origin)                               #   EDITED
            if bpy.app.version >= (2, 80, 0):
                if "screen" in ctx:
                    ctx.pop("screen")

                if "area" in ctx:
                    ctx.pop("area")


#################################################################################
#    vvvvvvvvvvvvvvvvvvvvv           ADDED         vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            #   Adds modified scene options to ctx context for local render.

            if not origin.chb_resOverride.isChecked():
                ctx['scene'].render.resolution_percentage = int(origin.cb_scaling.currentText())

            ctx['scene'].cycles.samples = int(rSettings["renderSamples"])
            ctx['scene'].render.use_persistent_data = (rSettings["persData"])
            ctx['scene'].render.use_compositing = rSettings["useComp"]
            try:
                ctx['scene'].use_nodes = rSettings["useComp"]
            except:
                logger.debug("The Blender Compositor 'Use Nodes' is deprecated.")

            selFileExt = rSettings["imageFormat"]
                           
            if selFileExt in [".exr", "exr", ".EXR", "EXR"]:
                selFileExt = "OPEN_EXR"
            elif selFileExt in [".exrMulti", "exrMulti"]:
                selFileExt = "OPEN_EXR_MULTILAYER"
            elif selFileExt in [".jpg", "jpg", ".JPG", "JPG", ".JPEG", "JPEG"]:
                selFileExt = "JPEG"
            elif selFileExt in [".png", "png", ".PNG", "PNG"]:
                selFileExt = "PNG"

            if selFileExt == "OPEN_EXR_MULTILAYER":
                ctx['scene'].render.image_settings.media_type = "MULTI_LAYER_IMAGE"
            else:
                ctx['scene'].render.image_settings.media_type = "IMAGE"
            
            ctx['scene'].render.image_settings.file_format =  selFileExt

            if selFileExt in ["OPEN_EXR", "OPEN_EXR_MULTILAYER", "PNG"]:
                if rSettings["useAlpha"]:
                    ctx['scene'].render.image_settings.color_mode = "RGBA"
                else:
                    ctx['scene'].render.image_settings.color_mode = "RGB"

                if selFileExt in ["OPEN_EXR", "OPEN_EXR_MULTILAYER"]:
                    bitDepth = rSettings["exrBitDepth"]
                elif selFileExt == "PNG":
                    bitDepth = rSettings["pngBitDepth"]

                ctx['scene'].render.image_settings.color_depth = bitDepth

                ctx['scene'].render.image_settings.exr_codec = rSettings["exrCodec"].upper()

            else:
                ctx['scene'].render.image_settings.color_mode = "RGB"

            if selFileExt in ["OPEN_EXR", "OPEN_EXR_MULTILAYER"]:
                if rSettings["ovrColorspace"] is True:
                    ctx['scene'].render.image_settings.color_management = "OVERRIDE"
                    ctx['scene'].render.image_settings.linear_colorspace_settings.name = rSettings["colorSpace"]
                else:
                    ctx['scene'].render.image_settings.color_management = "FOLLOW_SCENE"

                
#    ^^^^^^^^^^^^^^^^^^^^^          ADDED       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#####################################################################################
                
            if rSettings["startFrame"] is None:
                frameChunks = [[x, x] for x in rSettings["frames"]]
            else:
                frameChunks = [[rSettings["startFrame"], rSettings["endFrame"]]]

            for frameChunk in frameChunks:
                if frameChunk in self.renderedChunks:
                    continue

                bpy.context.scene.frame_start = frameChunk[0]
                bpy.context.scene.frame_end = frameChunk[1]
                singleFrame = rSettings["rangeType"] == "Single Frame"
                if bpy.app.version < (4, 0, 0):

                    self.blendPlugin.nextRenderslot()                               #   ADDED

                    bpy.ops.render.render(
                        ctx,
                        "INVOKE_DEFAULT",
                        animation=not singleFrame,
                        write_still=singleFrame,
                        )
                else:
                    with bpy.context.temp_override(**ctx):

                        self.blendPlugin.nextRenderslot()                           #   ADDED

                        bpy.ops.render.render(
                            "INVOKE_DEFAULT",
                            animation=not singleFrame,
                            write_still=singleFrame,
                            )
                
                origin.renderingStarted = True
                origin.LastRSettings = rSettings

                self.blendPlugin.startRenderThread(origin)                          #   EDITED
                self.renderedChunks.append(frameChunk)

                return "publish paused"

            origin.renderingStarted = False

            if hasattr(origin, "waitmsg") and origin.waitmsg.isVisible():
                origin.waitmsg.close()

            if len(os.listdir(os.path.dirname(outputName))) > 0:
                return "Result=Success"
            else:
                return "unknown error (files do not exist)"

        except Exception as e:
            if hasattr(origin, "waitmsg") and origin.waitmsg.isVisible():
                origin.waitmsg.close()

            exc_type, exc_obj, exc_tb = sys.exc_info()
            erStr = "%s ERROR - sm_default_imageRender %s:\n%s" % (
                time.strftime("%d/%m/%y %X"),
                origin.core.version,
                traceback.format_exc(),
                )
            self.core.writeErrorLog(erStr) 
            return "Execute Canceled: unknown error (view console for more information)"


    @err_catcher(name=__name__)
    def sm_render_undoRenderSettings(self, origin, rSettings):
        import bpy, shutil                                                              #   ADDED
        
        if "width" in rSettings:
            bpy.context.scene.render.resolution_x = rSettings["width"]
        if "height" in rSettings:
            bpy.context.scene.render.resolution_y = rSettings["height"]
        if "prev_start" in rSettings:
            bpy.context.scene.frame_start = rSettings["prev_start"]
        if "prev_end" in rSettings:
            bpy.context.scene.frame_end = rSettings["prev_end"]
        # if "fileformat" in rSettings:
        #     if rSettings["fileformat"] == "OPEN_EXR_MULTILAYER":
        #         bpy.context.scene.render.image_settings.media_type = "MULTI_LAYER_IMAGE"
        #     else:
        #         bpy.context.scene.render.image_settings.media_type = "IMAGE"

        #     bpy.context.scene.render.image_settings.file_format = rSettings["fileformat"]

        if "overwrite" in rSettings:
            bpy.context.scene.render.use_overwrite = rSettings["overwrite"]
        if "fileextension" in rSettings:
            bpy.context.scene.render.use_file_extension = rSettings["fileextension"]
        if "resolutionpercent" in rSettings:
            bpy.context.scene.render.resolution_percentage = rSettings["resolutionpercent"]


#################################################################################
#    vvvvvvvvvvvvvvvvvvvvv           ADDED         vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        if "origSamples" in rSettings:
            bpy.context.scene.cycles.samples = rSettings["origSamples"]

        if "origPersData" in rSettings:
            bpy.context.scene.render.use_persistent_data = rSettings["origPersData"]

        if "origUseComp" in rSettings:
            bpy.context.scene.render.use_compositing = rSettings["origUseComp"]

        if "origUseNode" in rSettings:
            try:
                bpy.context.scene.use_nodes = rSettings["origUseNode"]
            except:
                logger.debug("The Blender Compositor 'Use Nodes' is deprecated.")
        
        if "origImageType" in rSettings:
            bpy.context.scene.render.image_settings.media_type = rSettings["origImageType"]

        if "origImageformat" in rSettings:
            bpy.context.scene.render.image_settings.file_format = rSettings["origImageformat"]

        if "origExrCodec" in rSettings:
            bpy.context.scene.render.image_settings.exr_codec = rSettings["origExrCodec"]

        if "origBitDepth" in rSettings:
            bpy.context.scene.render.image_settings.color_depth = rSettings["origBitDepth"]

        if "origAlpha" in rSettings:
            bpy.context.scene.render.image_settings.color_mode = rSettings["origAlpha"]
        
        if rSettings["origImageformat"] in ["OPEN_EXR", "OPEN_EXR_MULTILAYER"]:
            if "origOvrColorspace" in rSettings:
                    bpy.context.scene.render.image_settings.color_management = rSettings["origOvrColorspace"]

        #   Revert Overrided Colorspace to original
            if "origColorspace" in rSettings:   
                try:
                    #   Try to restore to original
                    bpy.context.scene.render.image_settings.linear_colorspace_settings.name = rSettings["origColorspace"]
                except:
                    #   This could happen if there was no Colorspace in the Blend's UI Override combobox
                    if rSettings["origColorspace"] == "":
                        logger.warning("ERROR: Unable to restore original Override Colorspace: BLANK")
                    else:
                        logger.warning(f"ERROR: Unable to restore original Override Colorspace: {rSettings['origColorspace']}")

        if rSettings["overrideLayers"]:
            if "origLayers" in rSettings:

                self.setupLayers(rSettings, mode="Restore")

#    ^^^^^^^^^^^^^^^^^^^^^          ADDED       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#####################################################################################


        if platform.system() == "Windows":
            tmpOutput = os.path.join(os.environ["temp"], "PrismRender")
            if os.path.exists(tmpOutput):
                try:
                    shutil.rmtree(tmpOutput)
                except:
                    pass

        bDir = os.path.dirname(rSettings["origOutputName"])
        if os.path.exists(bDir) and len(os.listdir(bDir)) == 0:
            try:
                shutil.rmtree(bDir)
            except:
                pass

            origin.l_pathLast.setText(rSettings["outputName"])
            origin.l_pathLast.setToolTip(rSettings["outputName"])
            origin.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def sm_render_getRenderPasses(self, origin, renderLayer):                           #   EDITED
        aovNames = [
            x["name"]
            for x in self.getAvailableAOVs(renderLayer)                                 #   EDITED
            if x["name"] not in self.getViewLayerAOVs(renderLayer)                      #   EDITED
        ]
        return aovNames


    @err_catcher(name=__name__)
    def sm_render_addRenderPass(self, origin, passName, steps, renderLayer):            #   EDITED
        self.enableViewLayerAOV(passName, renderLayer)                                  #   EDITED


    @err_catcher(name=__name__)
    def sm_render_getDeadlineParams(self, origin, dlParams, homeDir):
        dlParams["jobInfoFile"] = os.path.join(
            homeDir, "temp", "blender_submit_info.job"
            )
        dlParams["pluginInfoFile"] = os.path.join(
            homeDir, "temp", "blender_plugin_info.job"
            )

        dlParams["jobInfos"]["Plugin"] = "Blender"
        dlParams["jobInfos"]["Comment"] = "Prism-Submission-BlenderRender"              #   EDITED
        dlParams["pluginInfos"]["OutputFile"] = dlParams["jobInfos"]["OutputFilename0"]



#################################################################################
#    vvvvvvvvvvvvvvvvvvvvv        ADDED METHODS       vvvvvvvvvvvvvvvvvvvvvvvvvvv


    @err_catcher(name=__name__)                                 #   ADDED
    def getRenderSamples(self, command, samples=None):
        import bpy

        if command == "Status":
            samples = bpy.context.scene.cycles.samples
            return samples
    
        elif command == "Set":
            bpy.context.scene.cycles.samples = samples


    @err_catcher(name=__name__)                                 #   ADDED
    def useCompositor(self, command, useComp=False):
        import bpy

        if command == "Status":
            isChecked = bpy.context.scene.render.use_compositing
            return isChecked
    
        elif command == "Set":
            bpy.context.scene.render.use_compositing = useComp

            #   This will be deprecated by Blender 6.0
            try:
                bpy.context.scene.use_nodes = useComp
            except:
                logger.debug("The Blender Compositor 'Use Nodes' is deprecated.")
    

    @err_catcher(name=__name__)                                 #   ADDED
    def getPersistentData(self, command, usePD=False):
        import bpy

        if command == "Status":
            isChecked = bpy.context.scene.render.use_persistent_data
            return isChecked
        
        elif command == "Set":
            bpy.context.scene.render.use_persistent_data = usePD


    @err_catcher(name=__name__)                                 #   ADDED
    def getColorSpaces(self):
        import bpy

        imageSettings = bpy.context.scene.render.image_settings

        if imageSettings.color_management == "OVERRIDE":
            colorOverride = True
        else:
            colorOverride = False

        currSpace = imageSettings.linear_colorspace_settings.name
        spaceList = imageSettings.linear_colorspace_settings.bl_rna.properties['name'].enum_items.keys()

        return colorOverride, currSpace, spaceList
    

    @err_catcher(name=__name__)                                 #   ADDED
    def getRenderLayers(self):
        import bpy

        renderLayers = []

        for viewLayer in bpy.context.scene.view_layers:
            layerName = viewLayer.name
            renderLayers.append(layerName)

        currentLayer = bpy.context.view_layer.name

        return  renderLayers, currentLayer
    

    @err_catcher(name=__name__)                                 #   ADDED
    def setTempScene(self, rSettings, origin):   
        import bpy

        #   Set Render Rez Percentage
        bpy.context.scene.render.resolution_percentage = int(origin.cb_scaling.currentText())

        #   Set Use Comp
        compEnabled = rSettings["useComp"]
        self.useCompositor(command="Set", useComp=compEnabled)

        #   Set Use Persistent Data
        persData = rSettings["persData"]
        self.getPersistentData(command="Set", usePD=persData)

        #   Set Samples
        samples = int(rSettings["renderSamples"])
        self.getRenderSamples(command="Set", samples=samples)

        #   Set Alpha
        imageFormat = rSettings["imageFormat"]
        if rSettings["useAlpha"] == False:
            alpha = "RGB"
        else:
            alpha = "RGBA"

        #   Set Media Type (after Blender 5.0)
        if imageFormat == ".exrMulti":
            bpy.context.scene.render.image_settings.media_type = "MULTI_LAYER_IMAGE"
        else:
            bpy.context.scene.render.image_settings.media_type = "IMAGE"

        if imageFormat in [".exr", ".exrMulti"]:
            if imageFormat == ".exr":
                blendImageFormat = "OPEN_EXR"

            elif imageFormat == ".exrMulti":
                blendImageFormat = "OPEN_EXR_MULTILAYER"
            
            bpy.context.scene.render.image_settings.file_format =  blendImageFormat
            bpy.context.scene.render.image_settings.exr_codec = rSettings["exrCodec"]
            bpy.context.scene.render.image_settings.color_depth = rSettings["exrBitDepth"]
            bpy.context.scene.render.image_settings.color_mode = alpha

            if rSettings["ovrColorspace"] is True:
                bpy.context.scene.render.image_settings.color_management = "OVERRIDE"
                bpy.context.scene.render.image_settings.linear_colorspace_settings.name = rSettings["colorSpace"]
            else:
                bpy.context.scene.render.image_settings.color_management = "FOLLOW_SCENE"

        elif imageFormat == ".png":
            bpy.context.scene.render.image_settings.file_format = "PNG"
            bpy.context.scene.render.image_settings.color_depth = rSettings["pngBitDepth"]
            bpy.context.scene.render.image_settings.compression = rSettings["pngCompress"]
            bpy.context.scene.render.image_settings.color_mode = alpha

        elif imageFormat == ".jpg":
            bpy.context.scene.render.image_settings.file_format = "JPEG"
            bpy.context.scene.render.image_settings.quality = rSettings["jpegQual"]


    @err_catcher(name=__name__)
    def nextRenderslot(self):
        import bpy

        try:
            bpy.data.images['Render Result'].render_slots.active_index += 1
            bpy.data.images['Render Result'].render_slots.active_index %= 7
        except:
            pass


    @err_catcher(name=__name__)
    def setupLayers(self, rSettings, mode):
        import bpy
        
        overrideLayers = rSettings["overrideLayers"]
        renderLayer = rSettings["renderLayer"]

        if mode == "Set":
            origLayers = {}

            #   Iterates through all layers Render and saves the orig state.
            for vl in bpy.context.scene.view_layers:
                origLayers[vl.name] = vl.use

            #   Saves the dict to rSettings
            rSettings["origLayers"] = origLayers

            #   If overrideLayers is checked, will set the layers
            if overrideLayers:
                singleLayer = rSettings["renderLayer"] 
                disabledLayers = set()
                tempLayers = {}

                #   Will disable all layers execpt the selected single layer
                for vl in bpy.context.scene.view_layers:
                    if vl.name != singleLayer:
                        disabledLayers.add(vl.name)
                        vl.use = False
                        
                    else:
                        vl.use = True         

                    tempLayers[vl.name] = vl.use            

                rSettings["tempLayers"] = tempLayers

        if mode == "Restore":
            # Get orig layer config
            origLayers = rSettings.get("origLayers", {})

            #   Set the layer to the original state
            for vl in bpy.context.scene.view_layers:
                vl_name = vl.name
                origUse = origLayers.get(vl_name, False)
                vl.use = origUse
        
        return rSettings

#    ^^^^^^^^^^^^^^^^^^^^^          ADDED       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#####################################################################################
