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


import os
import sys
import platform
import time
import traceback



try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher
from BlenderRender import BlenderRenderClass



class Prism_BlenderRender_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin


        # # check if Blender plugin is loaded
        # blendPlugin = self.core.getPlugin("Blender")
        # if blendPlugin:
        #     # if yes, patch the function
        #     self.applyBlendPatch(blendPlugin)

        # register callback in case plugin will be loaded later on
        # self.core.registerCallback("pluginLoaded",
        #                            self.onPluginLoaded,
        #                            plugin=self
        #                            )

        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self)


    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True
    

    @err_catcher(name=__name__)
    def onPluginLoaded(self, plugin):
        # check if the loaded plugin is to be patched
        if plugin.pluginName == "Blender":
            self.applyBlendPatch(plugin)

    @err_catcher(name=__name__)
    def applyBlendPatch(self, plugin):

        if hasattr(plugin, 'sm_render_preSubmit'):
            # try:
            
            self.core.plugins.monkeyPatch(plugin.sm_render_preSubmit, self.sm_render_preSubmit, self, force=True)
            self.core.plugins.monkeyPatch(plugin.sm_render_startLocalRender, self.sm_render_startLocalRender, self, force=True)

            # except Exception as e:
            #     self.core.popup(f"Execption: {e}")                                      #    TESTING



    @err_catcher(name=__name__)
    def onStateManagerOpen(self, origin):
        #   Will only load BlenderRender state if in Blender
        if self.core.appPlugin.pluginName == "Blender":
            origin.loadState(BlenderRenderClass)



    @err_catcher(name=__name__)
    def sm_render_preSubmit(self, origin, rSettings):

        self.core.popup("In sm_render_preSubmit")                                      #    TESTING

        import bpy

        if origin.chb_resOverride.isChecked():
            rSettings["width"] = bpy.context.scene.render.resolution_x
            rSettings["height"] = bpy.context.scene.render.resolution_y
            bpy.context.scene.render.resolution_x = origin.sp_resWidth.value()
            bpy.context.scene.render.resolution_y = origin.sp_resHeight.value()

        nodeAOVs = self.core.appPlugin.getNodeAOVs()                                    #   CHANGED SELF
        imgFormat = origin.cb_format.currentText()
        if imgFormat in [".exr", ".exrMulti"]:                                          #   EDITED
            if not nodeAOVs and self.core.appPlugin.getViewLayerAOVs():                 #   CHANGED SELF
                fileFormat = "OPEN_EXR_MULTILAYER"
            else:
                fileFormat = "OPEN_EXR"
        elif imgFormat == ".png":
            fileFormat = "PNG"
        elif imgFormat == ".jpg":
            fileFormat = "JPEG"

        rSettings["prev_start"] = bpy.context.scene.frame_start
        rSettings["prev_end"] = bpy.context.scene.frame_end
        rSettings["fileformat"] = bpy.context.scene.render.image_settings.file_format
        rSettings["overwrite"] = bpy.context.scene.render.use_overwrite
        rSettings["fileextension"] = bpy.context.scene.render.use_file_extension
        rSettings["resolutionpercent"] = bpy.context.scene.render.resolution_percentage




#################################################################################
#    vvvvvvvvvvvvvvvvvvvvv           ADDED         vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        

        rSettings["origSamples"] = bpy.context.scene.cycles.samples
        rSettings["origImageformat"] = bpy.context.scene.render.image_settings.file_format
        rSettings["origExrCodec"] = bpy.context.scene.render.image_settings.exr_codec
        rSettings["origBitDepth"] = bpy.context.scene.render.image_settings.color_depth
        rSettings["origAlpha"] = bpy.context.scene.render.image_settings.color_mode
        rSettings["origPersData"] = bpy.context.scene.render.use_persistent_data
        rSettings["origUseComp"] = bpy.context.scene.render.use_compositing
        rSettings["origUseNode"] = bpy.context.scene.use_nodes


        self.core.appPlugin.setTempScene(rSettings)                                 #   CHANGED SELF



        rSettings = self.core.appPlugin.setupLayers(rSettings, mode="Set")          #   CHANGED SELF


        aovName = rSettings["aovName"]                              #   TODO - deal with * ALL LAYERS *

        tempOutputName = rSettings["outputName"]

        tempOutputName = tempOutputName.replace("beauty", aovName)
        tempOutputName = tempOutputName.replace("exrMulti", "exr")
        
        rSettings["outputName"] = tempOutputName

#    ^^^^^^^^^^^^^^^^^^^^^          ADDED       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#####################################################################################




        rSettings["origOutputName"] = rSettings["outputName"]
        bpy.context.scene["PrismIsRendering"] = True
        bpy.context.scene.render.filepath = rSettings["outputName"]
        bpy.context.scene.render.image_settings.file_format = fileFormat
        bpy.context.scene.render.use_overwrite = True
        bpy.context.scene.render.use_file_extension = False
        bpy.context.scene.render.resolution_percentage = 100
        bpy.context.scene.camera = bpy.context.scene.objects[origin.curCam]

        usePasses = False
        if self.core.appPlugin.useNodeAOVs():                                       #   CHANGED SELF
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
                        passName = "beauty"                                 #   TODO

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
                        ].replace("beauty", passName)                               #   TODO
                        + ext,
                    )
                    newOutputPath = os.path.abspath(
                        os.path.join(
                            rSettings["outputName"],
                            "../..",
                            passName,
                            os.path.splitext(os.path.basename(rSettings["outputName"]))[
                                0
                            ].replace("beauty", passName)                           #   TODO
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
        # renderAnim = bpy.context.scene.frame_start != bpy.context.scene.frame_end

        self.core.popup("In sm_render_preSubmit")                                      #    TESTING

        import bpy


        try:
            if not origin.renderingStarted:
                origin.waitmsg = QMessageBox(
                    QMessageBox.NoIcon,
                    "ImageRender",
                    "Local rendering - %s - please wait.." % origin.state.text(0),
                    QMessageBox.Cancel,
                )
                #    self.core.parentWindow(origin.waitmsg)
                #    origin.waitmsg.buttons()[0].setHidden(True)
                #    origin.waitmsg.show()
                #    QCoreApplication.processEvents()

                bpy.app.handlers.render_complete.append(renderFinished_handler)
                bpy.app.handlers.render_cancel.append(renderFinished_handler)

                self.renderedChunks = []

            ctx = self.core.appPlugin.getOverrideContext(origin)
            if bpy.app.version >= (2, 80, 0):
                if "screen" in ctx:
                    ctx.pop("screen")

                if "area" in ctx:
                    ctx.pop("area")




#################################################################################
#    vvvvvvvvvvvvvvvvvvvvv           ADDED         vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv           #   NEEDED???

            #   Adds modified scene options to ctx context for local render.

            ctx['scene'].cycles.samples = int(rSettings["renderSamples"])
            ctx['scene'].render.use_persistent_data = (rSettings["persData"])
            ctx['scene'].render.use_compositing = rSettings["useComp"]
            ctx['scene'].use_nodes = rSettings["useComp"]

            selFileExt = rSettings["imageFormat"]
                           
            if selFileExt in [".exr", "exr", ".EXR", "EXR"]:
                selFileExt = "OPEN_EXR"
            elif selFileExt in [".exrMulti", "exrMulti"]:
                selFileExt = "OPEN_EXR_MULTILAYER"
            elif selFileExt in [".jpg", "jpg", ".JPG", "JPG", ".JPEG", "JPEG"]:
                selFileExt = "JPEG"
            elif selFileExt in [".png", "png", ".PNG", "PNG"]:
                selFileExt = "PNG"

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

                    self.core.appPlugin.nextRenderslot()                           #   ADDED


                    bpy.ops.render.render(
                        ctx,
                        "INVOKE_DEFAULT",
                        animation=not singleFrame,
                        write_still=singleFrame,
                    )
                else:
                    with bpy.context.temp_override(**ctx):

                        self.core.appPlugin.nextRenderslot()                           #   ADDED


                        bpy.ops.render.render(
                            "INVOKE_DEFAULT",
                            animation=not singleFrame,
                            write_still=singleFrame,
                        )
                
                    #   I WANT TO WAIT FOR THE SAVE TO FINISH HERE BEFORE GOING TO NEXT FRAME CHUNK


                origin.renderingStarted = True
                origin.LastRSettings = rSettings

                self.core.appPlugin.startRenderThread(origin)
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