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
#   more functionality to Blender's rendering including view layers.  This plugin will patch some of
#   Prism's original Blender functions to allow BlenderRender to function, and with the plugin enabled, the
#   default ImageRender state will not work.  This is non-destructive.



import os
import sys
import re
import platform
import time
import traceback
import logging
import json
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from bpy.types import (
        CompositorNodeTree,
        CompositorNodeRLayers,
        CompositorNodeOutputFile,
        Node,
        NodeSocket,
        NodeLink,
    )
else:
    CompositorNodeTree = Any
    CompositorNodeRLayers = Any
    CompositorNodeOutputFile = Any
    Node = Any
    NodeSocket = Any
    NodeLink = Any

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

from BlenderRender import BlenderRenderClass

pluginDir = os.path.dirname(os.path.dirname(__file__))
SETTINGSFILE = os.path.join(pluginDir, "BlenderRender_Config.json")


logger = logging.getLogger(__name__)


def renderFinished_handler(dummy):
    import bpy
    bpy.context.scene["PrismIsRendering"] = False



class Prism_BlenderRender_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.exrDefaults = {}
        self.blendPlugin = self.core.getPlugin("Blender")

        self.blendPlugin.formatOptions = {
            "EXR": {
                "bitDepths": ["16 (Half Float)", "32 (Full Float)"],
                "codec": ["NONE", "PIZ", "RLE", "ZIP", "ZIPS", "DWAA", "DWAB"],
                "encoding": ["Multi-part", "Multi-channel"],
                "compressWidget": "cb_exrCodec",
                "compressLabel": "Codec: ",
                "alpha": True,
                "colorSpace": True
                },
            "PNG": {
                "bitDepths": ["8 (Integer)", "16 (Integer)"],
                "compressWidget": "sp_pngCompress",
                "compressLabel": "Compression %: ",
                "alpha": True,
                "colorSpace": False
                },
            "JPG": {
                "compressWidget": "sp_jpegQual",
                "compressLabel": "Quality %: ",
                "alpha": False,
                "colorSpace": False
                },
            }

        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self)
        self.core.registerCallback("pluginLoaded", self.onPluginLoaded, plugin=self)
        self.core.registerCallback("userSettings_loadUI", self.userSettings_loadUI, plugin=self)
        self.core.registerCallback("onUserSettingsSave", self.onUserSettingsSave, plugin=self)

        self.applyBlendPatch()
        self.loadSettings()


    #   If Returns True, The Plugin will be Loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True


    #   Applies MonkeyPatches and Adds Methods to the Prism Blender Plugin
    @err_catcher(name=__name__)
    def applyBlendPatch(self):
        #   Ensures it is not using the Blender_unloaded plugin
        if hasattr(self.blendPlugin, "startup"):
            logger.debug("*** Patching Blender Plugin ***")
            
            #   Methods in Prism_Blender_Functions.py to be Patched
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
                    
            #   Methods in Prism_Blender_Functions.py to be Added
            addFuncList = ["getRenderSamples",
                           "useCompositor",
                           "getPersistentData",
                           "getRenderLayers",
                           "getColorSpaces",
                           "getAovDefault",
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
 


#############################################################
###################    CALLBACKS     ########################


    #   Called When Blender Loads
    @err_catcher(name=__name__)
    def onPluginLoaded(self, plugin):
        # check if the loaded plugin is to be patched
        if plugin.pluginName == "Blender":
            self.applyBlendPatch()


    #   Called When the StateManager Opens in Blender
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


    #   Called When Prism User Settings is Opened
    @err_catcher(name=__name__)
    def userSettings_loadUI(self, origin):
        self.loadMenuUI(origin)


    #   Called When Prism User Settings is Saved
    @err_catcher(name=__name__)
    def onUserSettingsSave(self, origin=None):
        try:
            self.saveSettings()
            logger.debug("Saved settings file.")

        except Exception as e:
            logger.warning(f"ERROR: Unable to save Settings file:  {e}")



#############################################################
################    PATCHED METHODS     #####################


    #   Fixes Prism Native FPS Method
    @err_catcher(name=__name__)
    def setFPS(self, origin, fps):
        import bpy, math

        if isinstance(fps, int):
            bpy.context.scene.render.fps = fps
        else:
            intFps = math.ceil(fps)
            bpy.context.scene.render.fps = intFps
            bpy.context.scene.render.fps_base = intFps/fps


    #   Custom Method
    @err_catcher(name=__name__)
    def sm_render_refreshPasses(self, origin, renderLayer):
        origin.lw_passes.clear()

        passNames = self.core.appPlugin.getNodeAOVs()
        origin.b_addPasses.setVisible(not passNames)
        self.blendPlugin.canDeleteRenderPasses = bool(not passNames)
        if not passNames:
            passNames = self.getViewLayerAOVs(renderLayer)

        if passNames:
            origin.lw_passes.addItems(passNames)


    @err_catcher(name=__name__)
    def getViewLayerAOVs(self, renderLayer):
        import bpy, operator

        availableAOVs = self.getAvailableAOVs(renderLayer)

        #   Get currently selected view layer
        try:
            curlayer = bpy.context.scene.view_layers[renderLayer]
        #   Handles the issue with a renamed view-layer
        except KeyError:
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
    def getAvailableAOVs(self, renderLayer):
        import bpy

        #   Get currently selected view layer
        try:
            curlayer = bpy.context.scene.view_layers[renderLayer]
        #   Handles the issue with a renamed view-layer
        except KeyError:
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
    def removeAOV(self, aovName, renderLayer):
        import bpy

        if self.blendPlugin.useNodeAOVs():
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
                                    passName = "Beauty"

                                if (
                                    passName == aovName.split("_", 1)[1]
                                    and layerName == aovName.split("_", 1)[0]
                                    ):
                                    i.to_node.inputs.remove(i.to_node.inputs[idx])
                                    return
        else:
            self.enableViewLayerAOV(aovName, renderLayer, enable=False)


    @err_catcher(name=__name__)
    def enableViewLayerAOV(self, name, renderLayer, enable=True):
        import bpy

        aa = self.getAvailableAOVs(renderLayer)
        curAOV = [x for x in aa if x["name"] == name]
        if not curAOV:
            return

        curAOV = curAOV[0]
        curlayer = bpy.context.scene.view_layers[renderLayer]

        attrs = curAOV["parm"].split(".")
        obj = curlayer
        for a in attrs[:-1]:
            obj = getattr(obj, a)

        setattr(obj, attrs[-1], enable)


    #   Configure Scene for Render
    @err_catcher(name=__name__)
    def sm_render_preSubmit(self, origin, rSettings):
        import bpy
    
        ###   Capture Original Blend Settings    ###
        rSettings["orig_width"] = bpy.context.scene.render.resolution_x
        rSettings["orig_height"] = bpy.context.scene.render.resolution_y
        rSettings["orig_start"] = bpy.context.scene.frame_start
        rSettings["orig_end"] = bpy.context.scene.frame_end
        rSettings["orig_filePath"] = bpy.context.scene.render.filepath
        rSettings["orig_fileformat"] = bpy.context.scene.render.image_settings.file_format
        rSettings["orig_exrEncoding"] = bpy.context.scene.render.image_settings.use_exr_interleave
        rSettings["orig_overwrite"] = bpy.context.scene.render.use_overwrite
        rSettings["orig_fileextension"] = bpy.context.scene.render.use_file_extension
        rSettings["orig_resolutionpercent"] = bpy.context.scene.render.resolution_percentage
        rSettings["orig_samples"] = bpy.context.scene.cycles.samples
        rSettings["orig_imageType"] = bpy.context.scene.render.image_settings.media_type
        rSettings["orig_imageFormat"] = bpy.context.scene.render.image_settings.file_format
        rSettings["orig_exrCodec"] = bpy.context.scene.render.image_settings.exr_codec
        rSettings["orig_bitDepth"] = bpy.context.scene.render.image_settings.color_depth
        rSettings["orig_ovrColorspace"] = bpy.context.scene.render.image_settings.color_management
        rSettings["orig_colorspace"] = bpy.context.scene.render.image_settings.linear_colorspace_settings.name
        rSettings["orig_alpha"] = bpy.context.scene.render.image_settings.color_mode
        rSettings["orig_persData"] = bpy.context.scene.render.use_persistent_data
        rSettings["orig_useComp"] = bpy.context.scene.render.use_compositing

        ###   Configure State Settings to Blend   ###
        bpy.context.scene.render.resolution_percentage = int(rSettings["scaling"])
        if origin.chb_resOverride.isChecked():
            bpy.context.scene.render.resolution_x = origin.sp_resWidth.value()
            bpy.context.scene.render.resolution_y = origin.sp_resHeight.value()
        
        bpy.context.scene.render.use_overwrite = True
        bpy.context.scene.render.use_file_extension = True

        self.useCompositor(command="set", useComp=rSettings["useComp"])
        self.getPersistentData(command="set", usePD=rSettings["persData"])
        self.getRenderSamples(command="set", samples=int(rSettings["renderSamples"]))

        #   Set Alpha
        alpha = "RGBA" if rSettings["useAlpha"] else "RGB"

        imageFormat = rSettings["imageFormat"]
        imageMode = rSettings["imageMode"]
        enablePasses = rSettings["enablePasses"]
        useSepBeauty = rSettings["useSepBeauty"]
        useSepCrypto = rSettings["useSepCrypto"]

        ##  Configure Output and Compositor based on Mode
        #   Single Layer Output - (Main: Single Layer) (Comp: None)
        if not enablePasses:
            imageType = "IMAGE"
            blendImageFormat = "OPEN_EXR"
            defaults = self.getAovDefault("Single Layer")

        #   Single Layer or Separate Beauty (Main: Single Layer Beauty) (Comp: MultiLayer)
        elif imageMode == "single" or (imageMode == "multi" and useSepBeauty):
            imageType = "IMAGE"
            blendImageFormat = "OPEN_EXR"
            self.setupPasses(rSettings, skipBeauty=True)
            defaults = self.getAovDefault("Beauty")

        #   Multi Layer (Main: Multi Layer) (Comp: None)
        elif not (useSepBeauty or useSepCrypto):
            imageType = "MULTI_LAYER_IMAGE"
            blendImageFormat = "OPEN_EXR_MULTILAYER"
            defaults = self.getAovDefault("Multi-layer Data EXR")

        #   Multi Layer (Main: Multi Layer) (Comp: Multi Layer)
        else:
            imageType = "MULTI_LAYER_IMAGE"
            blendImageFormat = "OPEN_EXR_MULTILAYER"
            self.setupPasses(rSettings, skipBeauty=False)
            defaults = self.getAovDefault("Multi-layer Data EXR")

        #   Get AOV Data for Blender Main Output
        aovData = self.getOutputPathData(defaults["name"], rSettings)
        aovPath = aovData["path"]

        #   Update rSettings
        rSettings["outputPath"] = rSettings["outputName"] = aovPath
        rSettings["version"] = aovData["version"]

        #   Abort with Warning for Filepath Length
        outLength = len(aovPath)
        if platform.system() == "Windows" and os.getenv("PRISM_IGNORE_PATH_LENGTH") != "1" and outLength > 255:
            return [
                origin.text(0)
                + " - error - The outputpath is longer than 255 characters (%s), which is not supported on Windows. Please shorten the outputpath by changing the comment, taskname or projectpath."
                % outLength
            ]

        #   Make Output Dir
        if not os.path.exists(os.path.dirname(aovPath)):
            os.makedirs(os.path.dirname(aovPath))

        #   Set Image Output Settings
        bpy.context.scene.render.image_settings.media_type = imageType
        bpy.context.scene.render.filepath = aovPath

        if imageFormat == ".exr":
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

        #   Setup the Render Layers as Needed
        rSettings = self.setupLayers(rSettings, mode="Set")

        #   Make versionInfo Data
        details = rSettings.copy()
        if "filename" in details:
            del details["filename"]
        if "extension" in details:
            del details["extension"]

        details["version"] = aovData["version"]
        details["sourceScene"] = self.core.getCurrentFileName()
        details["identifier"] = aovData["identifier"]
        details["comment"] = aovData["comment"]

        #   Create versionInfo
        infopath = os.path.dirname(os.path.dirname(aovPath))
        self.core.saveVersionInfo(filepath=infopath, details=details)

        bpy.context.scene["PrismIsRendering"] = True
        
        return rSettings


    @err_catcher(name=__name__)
    def sm_render_startLocalRender(self, origin, rSettings):
        import bpy
    
        try:
            if not origin.renderingStarted:
                origin.waitmsg = QMessageBox(
                    QMessageBox.NoIcon,
                    "ImageRender",
                    "Local rendering - %s - please wait.." % origin.state.text(0),
                    QMessageBox.Cancel,
                    )

                bpy.app.handlers.render_complete.append(renderFinished_handler)
                bpy.app.handlers.render_cancel.append(renderFinished_handler)

                self.renderedChunks = []

            ctx = self.blendPlugin.getOverrideContext(origin)
            if bpy.app.version >= (2, 80, 0):
                if "screen" in ctx:
                    ctx.pop("screen")

                if "area" in ctx:
                    ctx.pop("area")

                
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

                    self.blendPlugin.nextRenderslot()

                    bpy.ops.render.render(
                        ctx,
                        "INVOKE_DEFAULT",
                        animation=not singleFrame,
                        write_still=singleFrame,
                        )
                else:
                    with bpy.context.temp_override(**ctx):

                        self.blendPlugin.nextRenderslot()

                        bpy.ops.render.render(
                            "INVOKE_DEFAULT",
                            animation=not singleFrame,
                            write_still=singleFrame,
                            )
                
                origin.renderingStarted = True
                origin.LastRSettings = rSettings

                self.blendPlugin.startRenderThread(origin)
                self.renderedChunks.append(frameChunk)

                return "publish paused"

            origin.renderingStarted = False

            if hasattr(origin, "waitmsg") and origin.waitmsg.isVisible():
                origin.waitmsg.close()

            if len(os.listdir(os.path.dirname(rSettings["outputPath"]))) > 0:
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
        import bpy, shutil

        if "orig_width" in rSettings:
            bpy.context.scene.render.resolution_x = rSettings["orig_width"]

        if "orig_height" in rSettings:
            bpy.context.scene.render.resolution_y = rSettings["orig_height"]

        if "orig_start" in rSettings:
            bpy.context.scene.frame_start = rSettings["orig_start"]

        if "orig_end" in rSettings:
            bpy.context.scene.frame_end = rSettings["orig_end"]

        if "orig_exrEncoding" in rSettings:
            bpy.context.scene.render.image_settings.use_exr_interleave = rSettings["orig_exrEncoding"]

        if "orig_overwrite" in rSettings:
            bpy.context.scene.render.use_overwrite = rSettings["orig_overwrite"]

        if "orig_fileextension" in rSettings:
            bpy.context.scene.render.use_file_extension = rSettings["orig_fileextension"]

        if "orig_resolutionpercent" in rSettings:
            bpy.context.scene.render.resolution_percentage = rSettings["orig_resolutionpercent"]

        if "orig_samples" in rSettings:
            bpy.context.scene.cycles.samples = rSettings["orig_samples"]

        if "orig_imageType" in rSettings:
            bpy.context.scene.render.image_settings.media_type = rSettings["orig_imageType"]

        if "orig_imageFormat" in rSettings:
            bpy.context.scene.render.image_settings.file_format = rSettings["orig_imageFormat"]

        if "orig_exrCodec" in rSettings:
            bpy.context.scene.render.image_settings.exr_codec = rSettings["orig_exrCodec"]

        if "orig_bitDepth" in rSettings:
            bpy.context.scene.render.image_settings.color_depth = rSettings["orig_bitDepth"]

        if "orig_persData" in rSettings:
            bpy.context.scene.render.use_persistent_data = rSettings["orig_persData"]

        if "orig_useComp" in rSettings:
            bpy.context.scene.render.use_compositing = rSettings["orig_useComp"]

        if "orig_useNodes" in rSettings:
            try:
                bpy.context.scene.use_nodes = rSettings["orig_useNodes"]
            except:
                logger.debug("The Blender Compositor 'Use Nodes' is deprecated.")

        if "orig_alpha" in rSettings:
            bpy.context.scene.render.image_settings.color_mode = rSettings["orig_alpha"]
        
        if rSettings["orig_imageFormat"] in ["OPEN_EXR", "OPEN_EXR_MULTILAYER"]:
            if "orig_ovrColorspace" in rSettings:
                    bpy.context.scene.render.image_settings.color_management = rSettings["orig_ovrColorspace"]

        if "orig_filePath" in rSettings:
            bpy.context.scene.render.filepath = rSettings["orig_filePath"]

        #   Revert Overrided Colorspace to original
            if "orig_colorspace" in rSettings:   
                try:
                    #   Try to restore to original
                    bpy.context.scene.render.image_settings.linear_colorspace_settings.name = rSettings["orig_colorspace"]
                except:
                    #   This could happen if there was no Colorspace in the Blend's UI Override combobox
                    if rSettings["orig_colorspace"] == "":
                        logger.warning("ERROR: Unable to restore original Override Colorspace: BLANK")
                    else:
                        logger.warning(f"ERROR: Unable to restore original Override Colorspace: {rSettings['orig_colorspace']}")

        #   Re-configure Layers
        if rSettings["overrideLayers"]:
            if "orig_layers" in rSettings:
                self.setupLayers(rSettings, mode="Restore")

        #   Re-set Original Comp Node Tree
        try:
            if self.origCompTree:
                bpy.context.scene.compositing_node_group = self.origCompTree

            self.deleteCompNodeTree(treeObj=self.tempCompTree)
        except Exception as e:
            logger.warning(f"ERROR: Unable to Delete Temporary Comp Node Tree: {e}")
 
        if platform.system() == "Windows":
            tmpOutput = os.path.join(os.environ["temp"], "PrismRender")
            if os.path.exists(tmpOutput):
                try:
                    shutil.rmtree(tmpOutput)
                except:
                    pass

        #   Add to Last Render in StateManager
        origin.l_pathLast.setText(rSettings["outputName"])
        origin.l_pathLast.setToolTip(rSettings["outputName"])

        origin.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def sm_render_getRenderPasses(self, origin, renderLayer):
        aovNames = [
            x["name"]
            for x in self.getAvailableAOVs(renderLayer)
            if x["name"] not in self.getViewLayerAOVs(renderLayer)
        ]
        return aovNames


    @err_catcher(name=__name__)
    def sm_render_addRenderPass(self, origin, passName, steps, renderLayer):
        self.enableViewLayerAOV(passName, renderLayer)


    @err_catcher(name=__name__)
    def sm_render_getDeadlineParams(self, origin, dlParams, homeDir):
        dlParams["jobInfoFile"] = os.path.join(
            homeDir, "temp", "blender_submit_info.job"
            )
        dlParams["pluginInfoFile"] = os.path.join(
            homeDir, "temp", "blender_plugin_info.job"
            )

        dlParams["jobInfos"]["Plugin"] = "Blender"
        dlParams["jobInfos"]["Comment"] = "Prism-Submission-BlenderRender"
        dlParams["pluginInfos"]["OutputFile"] = dlParams["jobInfos"]["OutputFilename0"]


#############################################################
################      ADDED METHODS     #####################


    #   Handles Render Samples
    @err_catcher(name=__name__)
    def getRenderSamples(self, command, samples=None):
        import bpy

        if command == "status":
            samples = bpy.context.scene.cycles.samples
            return samples
    
        elif command == "set":
            bpy.context.scene.cycles.samples = samples


    #   Handles Compositor Usage
    @err_catcher(name=__name__)
    def useCompositor(self, command, useComp=False):
        import bpy

        if command == "status":
            isChecked = bpy.context.scene.render.use_compositing
            return isChecked
    
        elif command == "set":
            bpy.context.scene.render.use_compositing = useComp

            #   This will be deprecated by Blender 6.0
            try:
                bpy.context.scene.use_nodes = useComp
            except:
                logger.debug("The Blender Compositor 'Use Nodes' is deprecated.")
    

    #   Handles Persistant Data Usage
    @err_catcher(name=__name__)
    def getPersistentData(self, command, usePD=False):
        import bpy

        if command == "status":
            isChecked = bpy.context.scene.render.use_persistent_data
            return isChecked
        
        elif command == "set":
            bpy.context.scene.render.use_persistent_data = usePD


    #   Returns the Colorspace Settings
    @err_catcher(name=__name__)
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
    

    #   Returns the View Layers in the Scene
    @err_catcher(name=__name__)
    def getRenderLayers(self):
        import bpy

        renderLayers = []

        for viewLayer in bpy.context.scene.view_layers:
            layerName = viewLayer.name
            renderLayers.append(layerName)

        currentLayer = bpy.context.view_layer.name

        return  renderLayers, currentLayer
    

    #   Returns Default for Passed Type
    @err_catcher(name=__name__)
    def getAovDefault(self, fileType:str, defaultName:str = None) -> dict | str:
        passDefaults = self.blendPlugin.defaultSettings["passFileDefaults"]

        if defaultName:
            try:
                return passDefaults[fileType][defaultName]
            except KeyError:
                logger.warning(f"Filetype {fileType} does not exist in the defaults")
                return ""
        else:
            try:
                return passDefaults[fileType]
            except KeyError:
                logger.warning(f"Filetype {fileType} does not exist in the defaults")
                return {}
        

    #   Switches to the Next Render Slot
    @err_catcher(name=__name__)
    def nextRenderslot(self):
        import bpy

        try:
            bpy.data.images['Render Result'].render_slots.active_index += 1
            bpy.data.images['Render Result'].render_slots.active_index %= 7
        except:
            logger.debug("ERROR: Unable to Set Next Render Slot")


    #   Configures the View Layers to be Rendered
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
            rSettings["orig_layers"] = origLayers

            #   If overrideLayers is checked, will set the layers
            if overrideLayers:
                singleLayer = rSettings["renderLayer"] 
                disabledLayers = set()
                tempLayers = {}

                #   Will disable all layers except the selected single layer
                for vl in bpy.context.scene.view_layers:
                    if vl.name != singleLayer:
                        disabledLayers.add(vl.name)
                        vl.use = False
                    else:
                        vl.use = True         

                    tempLayers[vl.name] = vl.use            

                rSettings["tempLayers"] = tempLayers

        if mode == "Restore":
            #   Get Orig Layer Config
            origLayers = rSettings.get("orig_layers", {})

            #   Set thel ayer to the Original State
            for vl in bpy.context.scene.view_layers:
                vl_name = vl.name
                origUse = origLayers.get(vl_name, False)
                vl.use = origUse
        
        return rSettings



#############################################################
#################    MENU UI / SETTINGS    ##################


    #   Adds the BlenderRender Menu to Prism User Settings
    @err_catcher(name=__name__)
    def loadMenuUI(self, origin):
        logger.debug("Loading Blender Render Menu")

        settingsData = self.blendPlugin.defaultSettings

        ####    Main Layout Widget    ###
        origin.w_blendRendMenu = QWidget()
        origin.lo_blendRendMenu = QVBoxLayout(origin.w_blendRendMenu)


        ##     New States Defaults Group     ##
        gb_stateDefaults = QGroupBox("New State Defaults")
        lo_stateDefaults = QVBoxLayout(gb_stateDefaults)
        lo_stateDefaults.setContentsMargins(40, 10, 40, 10)
        
        lo_stateDefaults.addSpacing(10)

        #   Default Master
        lo_default_master = QHBoxLayout()
        l_default_master = QLabel("Master")
        self.cb_default_master = QComboBox()
        self.cb_default_master.addItems(["Don't Update Master",
                                         "Set as Master",
                                         "Add to Master"])
        idx = self.cb_default_master.findText(settingsData["master"])
        if idx != -1:
            self.cb_default_master.setCurrentIndex(idx)

        lo_default_master.addWidget(l_default_master)
        lo_default_master.addWidget(self.cb_default_master)

        #   Default Checkboxes
        self.chb_useCompositor = QCheckBox("Use Compositor")
        self.chb_useCompositor.setChecked(settingsData["useComp"])

        self.chb_usePersistentData = QCheckBox("Use Persistent Data")
        self.chb_usePersistentData.setChecked(settingsData["usePersistentData"])

        self.chb_useAlpha = QCheckBox("Use Alpha")
        self.chb_useAlpha.setChecked(settingsData["useAlpha"])

        lo_stateDefaults.addLayout(lo_default_master)
        lo_stateDefaults.addWidget(self.chb_useCompositor)
        lo_stateDefaults.addWidget(self.chb_usePersistentData)
        lo_stateDefaults.addWidget(self.chb_useAlpha)
        lo_stateDefaults.addSpacing(20)

        origin.lo_blendRendMenu.addWidget(gb_stateDefaults)


        ##     Passes Files Defaults Group     ##
        gb_passFileDefaults = QGroupBox("Passes File Defaults")
        lo_passFileDefaults = QVBoxLayout(gb_passFileDefaults)
        lo_passFileDefaults.setContentsMargins(40, 20, 40, 10)

        #   Output Defaults Grid Layout
        lo_formatDefaults = QGridLayout()
        lo_formatDefaults.setColumnStretch(1, 1)
        lo_formatDefaults.setHorizontalSpacing(8)
        lo_formatDefaults.setVerticalSpacing(6)

        #   Create Pass Default Header
        headers = ["", "Name", "Format", "Encoding", "Compression", "Bit Depth"]
        for col, text in enumerate(headers):
            lbl = QLabel(f"<b>{text}</b>")
            lo_formatDefaults.addWidget(lbl, 0, col)

        #   Create Row for Each Pass File Type in Settings
        passDefaults = settingsData["passFileDefaults"]
        for idx, (defaultName, defaultData) in enumerate(passDefaults.items(), start=1):
            self._add_output_row(lo_formatDefaults, idx, defaultName, defaultData)

        lo_passFileDefaults.addLayout(lo_formatDefaults)
        lo_passFileDefaults.addSpacing(20)

        origin.lo_blendRendMenu.addWidget(gb_passFileDefaults)


        ##      AOV Editor Group       ##
        gb_aovEditor = QGroupBox("AOV Name Mapping")
        lo_aovEditor = QHBoxLayout(gb_aovEditor)
        lo_aovEditor.setContentsMargins(40, 20, 40, 10)

        l_aovEditor = QLabel("Edit AOV Pass Shortnames:  ")
        lo_aovEditor.addWidget(l_aovEditor)
        b_editAOVs = QPushButton("Open Editor")
        b_editAOVs.clicked.connect(lambda: self._openAOVEditor(origin))
        lo_aovEditor.addWidget(b_editAOVs)
        origin.lo_blendRendMenu.addWidget(gb_aovEditor)

        #   Bottom Reset Button
        origin.lo_blendRendMenu.addStretch()

        lo_reset = QHBoxLayout()
        b_resetDefaults = QPushButton("Reset Defaults to Factory Settings")
        lo_reset.addWidget(b_resetDefaults)
        lo_reset.addStretch()
        b_resetDefaults.clicked.connect(self.resetDefaults)

        origin.lo_blendRendMenu.addLayout(lo_reset)

        origin.addTab(origin.w_blendRendMenu, "Blender Render")


    #   Helper for Settings to Create the EXR Rows
    @err_catcher(name=__name__)
    def _add_output_row(self, layout, row:int, dName:str, dData:dict):
        l_name = QLabel(dName)

        le_name = QLineEdit(dData["name"])

        cb_fmt = QComboBox()
        cb_fmt.addItems(self.blendPlugin.formatOptions.keys())
        cb_fmt.setCurrentText(dData["format"])

        cb_encoding = QComboBox()
        cb_encoding.addItems(self.blendPlugin.formatOptions["EXR"]["encoding"])
        cb_encoding.setCurrentText(dData["encoding"])

        cb_codec = QComboBox()
        cb_codec.addItems(self.blendPlugin.formatOptions["EXR"]["codec"])
        cb_codec.setCurrentText(dData["codec"])

        cb_depth = QComboBox()
        cb_depth.addItems(self.blendPlugin.formatOptions["EXR"]["bitDepths"])
        cb_depth.setCurrentText(dData["bitdepth"])

        def _update_exr_controls(fmt):
            is_exr = fmt == "EXR"
            cb_encoding.setEnabled(is_exr)
            cb_codec.setEnabled(is_exr)
            cb_depth.setEnabled(is_exr)

        cb_fmt.currentTextChanged.connect(_update_exr_controls)
        _update_exr_controls(cb_fmt.currentText())

        layout.addWidget(l_name, row, 0)
        layout.addWidget(le_name, row, 1)
        layout.addWidget(cb_fmt, row, 2)
        layout.addWidget(cb_encoding, row, 3)
        layout.addWidget(cb_codec, row, 4)
        layout.addWidget(cb_depth, row, 5)

        #   Store Widgets for Saving with saveSettings()
        self.exrDefaults[dName] = {
            "label": l_name,
            "name": le_name,
            "format": cb_fmt,
            "encoding": cb_encoding,
            "codec": cb_codec,
            "bitdepth": cb_depth,
        }
    

    #   Helper to Display the AOV Name Popup
    @err_catcher(name=__name__)
    def _openAOVEditor(self, origin):
        edited = AOVNameEditorDialog.edit(
            self.blendPlugin.defaultSettings["aovNames"],
            parent=origin.w_blendRendMenu
        )

        if edited is None:
            logger.debug("AOV editor cancelled")
            return

        self.blendPlugin.defaultSettings["aovNames"] = edited
        logger.info("AOV names updated")

        self.saveSettings()


    #   Load Settings from BlenderRender Settings json
    @err_catcher(name=__name__)
    def loadSettings(self):
        logger.debug("Loading Settings.")

        try:
            with open(SETTINGSFILE, "r") as json_file:
                self.blendPlugin.defaultSettings = json.load(json_file)

        #   Create the Settings File if it Doesn't Exist
        except FileNotFoundError:
            logger.debug("Settings file does not exist. Creating New.")
            self.createSettings()

        #   Delete and Create Corrupt Settings File
        except:
            logger.warning("ERROR: Settings file corrupt.  Removing existing file.")
            self.core.popup("Error Opening Config File.\n\n"
                            "Reverting to defaults")
            os.remove(SETTINGSFILE)
            self.createSettings()


    #   Create New Default Settings
    @err_catcher(name=__name__)
    def createSettings(self):
        settingsData = {
            "master": "Don't Update Master",
            "useComp": False,
            "usePersistentData": True,
            "useAlpha": True,

            "passFileDefaults": {
                "Single Layer": {
                    "name": "RGB",
                    "format": "EXR",
                    "encoding": "Multi-channel",
                    "codec": "DWAA",
                    "bitdepth": "16 (Half Float)"
                    },
                "Multi-layer Data EXR": {
                    "name": "RGB-DATA",
                    "format": "EXR",
                    "encoding": "Multi-part",
                    "codec": "DWAA",
                    "bitdepth": "16 (Half Float)"
                    },
                "Beauty": {
                    "name": "Beauty",
                    "format": "EXR",
                    "encoding": "Multi-channel",
                    "codec": "DWAA",
                    "bitdepth": "16 (Half Float)"
                    },
                "Cryptomatte": {
                    "name": "Crypto",
                    "format": "EXR",
                    "encoding": "Multi-channel",
                    "codec": "ZIP",
                    "bitdepth": "32 (Full Float)"
                    },
                },

            "aovNames": {
                "Image": "Beauty",
                "Combined": "Beauty",
                "Alpha": "Alpha",

                "Diffuse Color": "DiffColor",
                "Diffuse Direct": "DiffDir",
                "Diffuse Indirect": "DiffIndir",

                "Glossy Color": "GlossColor",
                "Glossy Direct": "GlossDir",
                "Glossy Indirect": "GlossIndir",

                "Transmission Color": "TransColor",
                "Transmission Direct": "TransDir",
                "Transmission Indirect": "TransIndir",

                "Volume Direct": "VolDir",
                "Volume Indirect": "VolIndir",

                "Emission": "Emit",
                "Environment": "Env",

                "Ambient Occlusion": "AO",
                "Normal": "Norm",
                "Position": "Position",
                "Depth": "Z",
                "Vector": "Vec",
                "UV": "UV",

                "Mist": "Mist",
                "IndexOB": "ObjID",
                "IndexMA": "MatID",

                "Shadow Catcher": "Shadow",
                "Shadow Catcher Matte": "ShadowMatte",

                "Albedo": "Albedo",

                "Noisy Image": "Noisy",
                "Denoising Normal": "DenoiseNorm",
                "Denoising Albedo": "DenoiseAlb",
                "Denoising Depth": "DenoiseZ",

                "CryptoObject": "CryptoObj",
                "CryptoMaterial": "CryptoMat",
                "CryptoAsset": "CryptoAsset",
                }
            }

        logger.debug("Created settings file.")
        self.saveSettings(settingsData)
        self.loadSettings()


    #   Reset Defaults to Factory Settings
    @err_catcher(name=__name__)
    def resetDefaults(self):
        #   Show Popup Question
        title = "Reset Defaults"
        msg = ("Do you want to reset the BlenderRender defaults to\n"
               "the factory defaults?")
        buttons = ["Reset", "Cancel"]
        result = self.core.popupQuestion(msg, buttons=buttons, title=title, icon=QMessageBox.Warning)

        if result == "Reset":
            logger.warning("Reseting Defaults to Factory")
            if os.path.exists(SETTINGSFILE):
                os.remove(SETTINGSFILE)
            self.createSettings()
            #   Reload the Settings UI for Refresh
            self.core.prismSettings(restart=True)


    #   Save Settings to BlenderRender Settings json
    @err_catcher(name=__name__)
    def saveSettings(self, settingsData:dict = None):
        #   If Passed from Create
        if settingsData:
            sData = settingsData
        
        else:
            #   Get State Defaults
            sData = {
                "master": self.cb_default_master.currentText(),
                "useComp": self.chb_useCompositor.isChecked(),
                "usePersistentData": self.chb_usePersistentData.isChecked(),
                "useAlpha": self.chb_useAlpha.isChecked(),
            }

            #   Get Pass File Defaults
            pData = {}
            for dName, widgets in self.exrDefaults.items():
                pData[dName] = {
                    "name": widgets["name"].text(),
                    "format": widgets["format"].currentText(),
                    "encoding": widgets["encoding"].currentText(),
                    "codec": widgets["codec"].currentText(),
                    "bitdepth": widgets["bitdepth"].currentText(),
                }
            sData["passFileDefaults"] = pData

            #   Add AOV Names
            sData["aovNames"] = self.blendPlugin.defaultSettings["aovNames"]


        with open(SETTINGSFILE, "w") as json_file:
            json.dump(sData, json_file, indent=4)

        self.loadSettings()
        logger.debug("Settings Saved")


#############################################################
###############    FILE OUTPUT / PASSES       ###############


    @err_catcher(name=__name__)
    def getOutputPathData(self, aovName:str, rSettings:dict, useVersion:str="next") -> dict:
        aovData = self.core.mediaProducts.generateMediaProductPath(
            entity=rSettings,
            task=rSettings["identifier"],
            extension=rSettings["imageFormat"],
            framePadding="",
            version=useVersion if useVersion != "next" else None,
            location=rSettings["location"],
            aov=aovName,
            # singleFrame=singleFrame,
            returnDetails=True,
            mediaType="3drenders",
        )

        return aovData


    #   Called if Passes are Enabled
    @err_catcher(name=__name__)
    def setupPasses(self, rSettings, skipBeauty):
        #   Initial Node Position
        self.node_xLoc = 300
        self.node_yLoc = 50

        #   Call Method Based on Image Mode
        imageMode = rSettings["imageMode"]

        if imageMode == "single":
            self.setupPassSingle(rSettings, skipBeauty=skipBeauty)

        if imageMode == "multi":
            self.setupPassMulti(rSettings, skipBeauty=skipBeauty)


    #   For Single-layer Mode
    @err_catcher(name=__name__)
    def setupPassSingle(self, rSettings, skipBeauty):
        import bpy

        #   Get Defaults
        defaults = self.getAovDefault("Single Layer")
        colorDepth = "32" if defaults["bitdepth"] == "Full Float (32)" else "16"
        codec = defaults["codec"]

        #   Turn On Compositor
        self.useCompositor(command="set", useComp=True)

        #   Get Alpha Mode
        alpha = "RGBA" if rSettings["useAlpha"] else "RGB"

        #   Store Original Comp Node Tree if Exists
        self.origCompTree = self.getActiveCompNodeTree()

        #   Create and Set Temp Comp Node Tree as Active
        tempTree = self.createCompNodeTree("PrismTempTree")
        self.tempCompTree = tempTree
        bpy.context.scene.compositing_node_group = tempTree

        #   Create Renderlayers Node
        rLayers = self.createCompNode(
            tempTree,
            "CompositorNodeRLayers",
            nodeName="PRISM Render Layers",
            location=(0, 0)
        )

        self.passPathDict = {}

        #   Get Active AOV Pass Names
        passNames = self.getRenderPasses(rLayers)
        for passName in passNames:
            #   Skip Alpha and Crypto Passes
            if "alpha" in passName.lower() or "crypto" in passName.lower():
                continue

            #   Skip Image/Beauty if Required
            if skipBeauty and "image" in passName.lower():
                continue

            #   Get Pass ShortName
            try:
                key = passName.lower()
                aovNamesLower = {k.lower(): v for k, v in self.blendPlugin.defaultSettings["aovNames"].items()}

                if key in aovNamesLower:
                    passNameShort = aovNamesLower[key]
                else:
                    raise Exception
            except:
                passNameShort = passName

            #   Get AOV Data
            aovData = self.getOutputPathData(passNameShort, rSettings)

            #   Configure Path and Name for File Output Node Formatting
            directory, filename = os.path.split(aovData["path"])
            filename_base, ext = os.path.splitext(filename)
            filename_hacked = re.sub(r'(_v\d+).*$', r'\1', filename_base)
            filename_hacked = f"{filename_hacked}_"
            passNameStr = f"{passNameShort}.####"

            #   Create File Output Node
            file_node = self.createCompNode(
                tempTree,
                "CompositorNodeOutputFile",
                nodeName="PRISM File Output",
                width=300,
                location=(self.node_xLoc, self.node_yLoc)
            )

            #   Configure File Output Node
            nodeData = {                                            #   TODO - HANDLE NON-EXR FORMATS
                "name": f"PRISM File Output -- {passNameShort}",
                "directory": directory,
                "fileName": filename_hacked,
                "passName": passNameStr,
                "image_mode": "IMAGE",
                "file_format": "OPEN_EXR",
                "color_mode": alpha,
                "color_depth": colorDepth,
                "codec": codec,
            }
            self.configureFileOutputNode(file_node, nodeData)

            #   Rename Default File Slot
            fileItem = file_node.file_output_items[0]
            fileItem.name = passNameStr

            #   Connect RenderLayer Node to File Output Node
            self.connectCompNodes(tempTree,
                                  from_node=rLayers,
                                  from_socketName = passName,
                                  to_node=file_node,
                                  to_socketName=passNameStr)
            
            #   Increment Node Position
            self.node_xLoc += 10
            self.node_yLoc += -50

        #   Create Crypto Multi-layer EXR
        self.createCryptoFile(tempTree, rLayers, rSettings, self.node_xLoc, self.node_yLoc)


    #   For Multi-layer Mode
    @err_catcher(name=__name__)
    def setupPassMulti(self, rSettings, skipBeauty):
        import bpy

        #   Get Defaults
        defaults = self.getAovDefault("Multi-layer Data EXR")
        aovName = defaults["name"]
        colorDepth = "32" if defaults["bitdepth"] == "Full Float (32)" else "16"
        codec = defaults["codec"]
        interweave = True if defaults["encoding"] == "Multi-channel" else False

        #   Turn On Compositor
        self.useCompositor(command="set", useComp=True)

        #   Get Alpha Mode
        alpha = "RGBA" if rSettings["useAlpha"] else "RGB"

        #   Settings from State
        useSepBeauty = rSettings["useSepBeauty"]
        useSepCrypto = rSettings["useSepCrypto"]
        
        #   Store Original Comp Node Tree
        self.origCompTree = self.getActiveCompNodeTree()

        #   Create and Set Temp Comp Node Tree
        tempTree = self.createCompNodeTree("PrismTempTree")
        self.tempCompTree = tempTree
        bpy.context.scene.compositing_node_group = tempTree

        #   Create RenderLayers Node
        rLayers = self.createCompNode(
            tempTree,
            "CompositorNodeRLayers",
            nodeName="PRISM Render Layers",
            location=(0, 0)
        )

        #   Get AOV Data
        aovData = self.getOutputPathData(aovName, rSettings)
        directory, filename = os.path.split(aovData["path"])
        filename_base, ext = os.path.splitext(filename)

        #   Create File Output Node
        file_node = self.createCompNode(
            tempTree,
            "CompositorNodeOutputFile",
            nodeName="PRISM File Output",
            width=300,
            location=(self.node_xLoc, self.node_yLoc)
        )

        #   Configure File Output Node
        nodeData = {
            "name": f"PRISM File Output -- {aovName}",
            "directory": directory,
            "fileName": filename_base,
            "passName": "Image",
            "image_mode": "MULTI_LAYER_IMAGE",
            "file_format": "MULTI_LAYER_EXR",
            "color_mode": alpha,
            "color_depth": colorDepth,
            "codec": codec,
            "interweave": interweave
        }
        self.configureFileOutputNode(file_node, nodeData)
        file_node.file_output_items.clear()

        #   Capture AOV Passes
        passNames = self.getRenderPasses(rLayers)

        #   For Each Pass
        self.passPathDict = {}
        for passName in passNames:
            #   Skip Alpha if Not Used
            if not rSettings["useAlpha"] and passName.lower() in ["alpha"]:
                continue

            #   Skip Image/Beauty if Required
            if useSepBeauty or skipBeauty:
                if "image" in passName.lower():
                    continue

            #   Skip Crypto if Required
            if useSepCrypto:      
                if "crypto" in passName.lower():
                    continue

            #   Get Pass ShortName
            try:
                key = passName.lower()
                aovNamesLower = {k.lower(): v for k, v in self.blendPlugin.defaultSettings["aovNames"].items()}

                if key in aovNamesLower:
                    passNameShort = aovNamesLower[key]
                else:
                    raise Exception
            except:
                passNameShort = passName

            aovPath = aovData["path"]
            self.passPathDict[passNameShort] = aovPath

            #   Create New File Slot for Pass
            file_node.file_output_items.new(socket_type="RGBA", name=passNameShort)

            #   Connect Pass to File Output Node
            self.connectCompNodes(tempTree,
                                  from_node=rLayers,
                                  from_socketName = passName,
                                  to_node=file_node,
                                  to_socketName=passNameShort)
            
        #   Increase Node Position for Next Node
        self.node_xLoc += 10
        self.node_yLoc += -50

        #   Create Separate Crypto File
        if useSepCrypto:
            self.createCryptoFile(tempTree, rLayers, rSettings, self.node_xLoc, self.node_yLoc)


    #   Creates Separate Multi-layer EXR Crypto File
    def createCryptoFile(self, tree, rLayers, rSettings, xLoc, yLoc):
        #   Get Defaults
        defaults = self.getAovDefault("Cryptomatte")
        cryptoName = defaults["name"]
        colorDepth = "32" if defaults["bitdepth"] == "Full Float (32)" else "16"
        codec = defaults["codec"]
        interweave = True if defaults["encoding"] == "Multi-channel" else False

        #   Get Alpha Mode
        alpha = "RGBA" if rSettings["useAlpha"] else "RGB"

        #   Capture Crypto Passes
        passNames = self.getRenderPasses(rLayers)
        cryptoPasses = [
            p for p in passNames
            if "crypto" in p.lower()
        ]
        if not cryptoPasses:
            return

        #   Create AOV Data
        aovData = self.getOutputPathData(cryptoName, rSettings)
        directory, filename = os.path.split(aovData["path"])
        filename_base, ext = os.path.splitext(filename)

        #   Create File Output Node
        crypto_fileOut = self.createCompNode(
            tree,
            "CompositorNodeOutputFile",
            f"PRISM File Output -- {cryptoName}",
            width=300,
            location=(xLoc, yLoc),
        )

        #   Configure File Output Node
        nodeData = {
            "name": f"PRISM File Output -- {cryptoName}",
            "directory": directory,
            "fileName": filename_base,
            "image_mode": "MULTI_LAYER_IMAGE",
            "file_format": "MULTI_LAYER_EXR",
            "color_mode": alpha,
            "color_depth": colorDepth,
            "codec": codec,
            "interweave": interweave
        }
        self.configureFileOutputNode(crypto_fileOut, nodeData)
        crypto_fileOut.file_output_items.clear()

        #   Connect Crypto Passes
        for cryptoPass in cryptoPasses:
            crypto_fileOut.file_output_items.new(socket_type="RGBA", name=cryptoPass)
            
            self.connectCompNodes(
                tree,
                from_node=rLayers,
                from_socketName=cryptoPass,
                to_node=crypto_fileOut,
                to_socketName=cryptoPass,
                )



#############################################################
#################     COMPOSITOR TOOLS     ##################


    #   Returns Active Compositor Node Tree if Exists
    def getActiveCompNodeTree(self) -> CompositorNodeTree | None:
        import bpy

        try:
            return bpy.context.scene.compositing_node_group
        except Exception as e:
            logger.warning(f"ERROR: Uabled to get Current Comp Node Tree: {e}")
            return None


    #   Creates New Compositor Node Tree
    def createCompNodeTree(self, name:str="PrismTempCompTree") -> CompositorNodeTree:
        import bpy

        #   Create new compositor node tree
        tree = bpy.data.node_groups.new(
            name=name,
            type="CompositorNodeTree"
            )

        #   Remove Blender's default nodes
        tree.nodes.clear()
        tree.links.clear()

        return tree
    

    #   Deletes Comp Node Tree from Blend
    def deleteCompNodeTree(self,
                           treeName: str | None = None,
                           treeObj: CompositorNodeTree | None = None
                           ) -> bool:
        import bpy

        #   Determine if Passed Name or a Tree Object
        if treeName:
            tree = bpy.data.node_groups.get(treeName)
        else:
            tree = treeObj

        #   Remove Comp Node Tree
        if tree and getattr(tree, "bl_idname", "") == "CompositorNodeTree":
            bpy.data.node_groups.remove(tree)
            return True

        return False


    #   Returns Node Given Name or Object
    @err_catcher(name=__name__)
    def getCompNode(self,
                    tree: CompositorNodeTree,
                    nodeName: str | None = None,
                    nodeType: str | None = None
                    ) -> Node | None:

        for node in tree.nodes:
            if nodeName and node.name == nodeName:
                return node
            if nodeType and node.bl_idname == nodeType:
                return node
        return None


    #   Creates Comp Node by Type
    def createCompNode(self,
                       tree:        CompositorNodeTree,
                       nodeType:    str | None          = None,
                       nodeName:    str | None          = None,
                       width:       int | None          = None,
                       location:    tuple[int, int]     = (0,0),
                       **kwargs
                       ) -> Node:

        node = tree.nodes.new(nodeType)
        node.location = location

        if nodeName:
            node.label = nodeName

        if width:
            node.width = width

        for key, value in kwargs.items():
            setattr(node, key, value)

        return node


    #   Returns List of Enabled Pass Names
    def getRenderPasses(self, rlayers_node:Node) -> list[str]:
        if rlayers_node is None:
            return []

        passes = [sock.name for sock in rlayers_node.outputs if sock.enabled]

        return passes


    #   Connects Two Node's Sockets by Either Name or Object
    def connectCompNodes(self,
                         tree:              CompositorNodeTree,
                         from_node:         Node | None        = None,
                         from_socketName:   str | None         = None,
                         from_socket:       NodeSocket | None  = None,
                         to_node:           Node | None        = None,
                         to_socketName:     str | None         = None,
                         to_socket:         NodeSocket | None  = None
                         ) -> bool:

        if from_socketName:
            from_socket = from_node.outputs.get(from_socketName)

        if to_socketName:
            to_socket = to_node.inputs.get(to_socketName)

        if from_socket and to_socket:
            tree.links.new(from_socket, to_socket)
            return True
        
        else:
            logger.warning(f"Cannot find sockets: {from_socketName} -> {to_socketName}")
            return False


    #   Set Options of File Output Node
    def configureFileOutputNode(self, node: Node, nData: dict):
        if node.bl_idname != "CompositorNodeOutputFile":
            raise TypeError("Node must be a CompositorNodeOutputFile")

        #   Node Label
        node.label = nData.get("name", node.label)

        node.active_item_index = 0

        #   Format settings
        fmt = node.format

        #   Determine if Single-layer or Multi-layer EXR
        imageMode = nData.get("image_mode", "IMAGE")
        fmt.media_type = imageMode

        if imageMode == "IMAGE":
            fmt.file_format = nData.get("file_format", "OPEN_EXR")
        elif imageMode == "MULTI_LAYER_IMAGE":
            fmt.file_format = "OPEN_EXR_MULTILAYER"
        else:
            raise ValueError("image_mode must be 'IMAGE' or 'MULTI_LAYER_IMAGE'")

        #   Color / Bitdepth
        fmt.color_mode = nData.get("color_mode", "RGBA")
        fmt.color_depth = nData.get("color_depth", "16")

        #   EXR Codec / Compression / Encoding
        if fmt.file_format in {'OPEN_EXR', 'OPEN_EXR_MULTILAYER'}:
            fmt.exr_codec = nData.get("codec", "DWAA")
            if hasattr(fmt, "quality"):
                fmt.quality = nData.get("quality", 90)
            if hasattr(fmt, "use_exr_interleave"):
                fmt.use_exr_interleave = nData.get("interweave", False)

        #   Clear Existing Slots and Create a Default 'Color' Slot
        node.file_output_items.clear()
        item = node.file_output_items.new(socket_type="RGBA", name="Color")
        item.save_as_render = True

        #   Directory / Filename
        node.directory = nData["directory"]
        node.file_name = nData["fileName"]



#############################################################
###############     AOV PASS NAME EDITOR    #################

class AOVNameEditorDialog(QDialog):
    def __init__(self, aov_dict: dict[str, str], parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit AOV Names")
        self.resize(600, 500)

        self._original_dict = aov_dict

        self._buildUI()
        self._populateTable(aov_dict)

    #   Create UI
    def _buildUI(self):
        lo_main = QVBoxLayout(self)

        ##   Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Blender Pass", "AOV / Layer Name"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)

        lo_main.addWidget(self.table)

        ##   Buttons
        lo_buttons = QHBoxLayout()
        lo_buttons.addStretch()

        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        lo_buttons.addWidget(self.btn_save)
        lo_buttons.addWidget(self.btn_cancel)

        lo_main.addLayout(lo_buttons)


    #   Add Items to the Table
    def _populateTable(self, aov_dict: dict[str, str]):
        self.table.setRowCount(len(aov_dict))

        for row, (key, value) in enumerate(aov_dict.items()):
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(value)

            key_item.setFlags(key_item.flags() | Qt.ItemIsEditable)
            value_item.setFlags(value_item.flags() | Qt.ItemIsEditable)

            self.table.setItem(row, 0, key_item)
            self.table.setItem(row, 1, value_item)


    def getResultDict(self) -> dict[str, str]:
        result = {}

        for row in range(self.table.rowCount()):
            key_item = self.table.item(row, 0)
            value_item = self.table.item(row, 1)

            if not key_item:
                continue

            key = key_item.text().strip()
            value = value_item.text().strip() if value_item else ""

            if not key:
                continue

            result[key] = value

        return result


    #   Callable Edit Method
    @staticmethod
    def edit(aov_dict, parent=None):
        dlg = AOVNameEditorDialog(aov_dict, parent)

        if dlg.exec() == QDialog.Accepted:
            return dlg.getResultDict()
        
        return None