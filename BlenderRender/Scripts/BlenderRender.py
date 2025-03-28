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

import os
import sys
import time
import platform

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher
from StateUserInterfaces import BlenderRender_ui


class BlenderRenderClass(QWidget, BlenderRender_ui.Ui_wg_BlenderRender):

    className = "BlenderRender"
    listType = "Export"
    stateCategories = {"Render": [{"label": className, "stateType": className}]}


    @err_catcher(name=__name__)
    def setup(self, state, core, stateManager, node=None, stateData=None):
        self.state = state
        self.core = core
        self.stateManager = stateManager
        self.canSetVersion = True
        self.customContext = None
        self.allowCustomContext = False

        self.setupUi(self)

        self.cb_context.addItems(["From scenefile", "Custom"])              

        self.curCam = None
        self.renderingStarted = False
        self.cleanOutputdir = True

        self.e_name.setText(state.text(0) + " - {identifier}")

        self.rangeTypes = [
            "Scene",
            "Shot",
            "Single Frame",
            "FML",
            "FMMML",
            "Custom",
            "Expression",
            ]
        
        self.cb_rangeType.addItems(self.rangeTypes)
        for idx, rtype in enumerate(self.rangeTypes):
            self.cb_rangeType.setItemData(
                idx, self.stateManager.getFrameRangeTypeToolTip(rtype), Qt.ToolTipRole
                )
        self.w_frameExpression.setToolTip(
            self.stateManager.getFrameRangeTypeToolTip("ExpressionField")
            )

        self.renderPresets = (
            self.stateManager.stateTypes["RenderSettings"].getPresets(self.core)
            if "RenderSettings" in self.stateManager.stateTypes
            else {}
            )
        if self.renderPresets:
            self.cb_renderPreset.addItems(self.renderPresets.keys())
        else:
            self.w_renderPreset.setVisible(False)

        self.l_name.setVisible(False)
        self.e_name.setVisible(False)
        self.gb_submit.setChecked(False)
        self.f_renderLayer.setVisible(True)

        getattr(self.core.appPlugin, "sm_render_startup", lambda x: None)(self)

        masterItems = ["Set as master", "Add to master", "Don't update master"]
        self.cb_master.addItems(masterItems)
        self.product_paths = self.core.paths.getRenderProductBasePaths()
        self.cb_outPath.addItems(list(self.product_paths.keys()))
        if len(self.product_paths) < 2:
            self.cb_outPath.setVisible(False)
            self.l_outPath.setVisible(False)

        self.mediaType = "3drenders"
        self.tasknameRequired = True

        self.formatOptions = {
            ".exr": {
                "bitDepths": ["16", "32"],
                "codec": ["NONE", "PIZ", "RLE", "ZIP", "ZIPS", "DWAA", "DWAB"],
                "compressWidget": self.cb_exrCodec,
                "compressLabel": "Codec: ",
                "alpha": True,
                "colorSpace": True
                },
            ".exrMulti": {
                "bitDepths": ["16", "32"],
                "codec": ["NONE", "PIZ", "RLE", "ZIP", "ZIPS", "DWAA", "DWAB"],
                "compressWidget": self.cb_exrCodec,
                "compressLabel": "Codec: ",
                "alpha": True,
                "colorSpace": True
                },
            ".png": {
                "bitDepths": ["8", "16"],
                "compressWidget": self.sp_pngCompress,
                "compressLabel": "Compression %: ",
                "alpha": True,
                "colorSpace": False
                },
            ".jpg": {
                "compressWidget": self.sp_jpegQual,
                "compressLabel": "Quality %: ",
                "alpha": False,
                "colorSpace": False
                },
            }

        self.cb_format.addItems(self.formatOptions.keys())

        self.scalings = [
            "25",
            "50",
            "75",
            "100",
            "125",
            "150",
            "200"
            ]
        
        self.cb_scaling.addItems(self.scalings)
        tempIdx = self.cb_scaling.findText("100")
        self.cb_scaling.setCurrentIndex(tempIdx)

        self.resolutionPresets = self.core.projects.getResolutionPresets()
        if "Get from rendersettings" not in self.resolutionPresets:
            self.resolutionPresets.append("Get from rendersettings")

        self.e_osSlaves.setText("All")

        self.connectEvents()

        self.oldPalette = self.b_changeTask.palette()
        self.warnPalette = QPalette()
        self.warnPalette.setColor(QPalette.Button, QColor(200, 0, 0))
        self.warnPalette.setColor(QPalette.ButtonText, QColor(255, 255, 255))

        self.setTaskWarn(True)
        self.nameChanged(state.text(0))

        self.cb_manager.addItems([p.pluginName for p in self.core.plugins.getRenderfarmPlugins()])
        self.core.callback("onStateStartup", self)
        if self.cb_manager.count() == 0:
            self.gb_submit.setVisible(False)

        self.getRenderLayers("load")
        self.getColorSpaces("load")

        self.managerChanged(True)

        self.e_fml.setStyleSheet("border: none;")
        self.e_xRez.setStyleSheet("border: none;")
        self.e_yRez.setStyleSheet("border: none;")
        self.e_fml.setStyleSheet("background: transparent;")
        self.e_xRez.setStyleSheet("background: transparent;")
        self.e_yRez.setStyleSheet("background: transparent;")

        self.setToolTips()

        #   If State exists in .blend, it will load it
        if stateData is not None:
            self.loadStateData(stateData)

        #   Sets Defaults for State when new
        else:   
            self.createNewStateData()


    @err_catcher(name=__name__)
    def connectEvents(self):
        self.e_aovNameCustom.textChanged.connect(self.stateManager.saveStatesToScene)
        self.chb_customAOV.toggled.connect(self.updateUi)
        self.e_name.textChanged.connect(self.nameChanged)
        self.e_name.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.cb_context.activated.connect(self.onContextTypeChanged)
        self.b_context.clicked.connect(self.selectContextClicked)
        self.b_changeTask.clicked.connect(self.changeTask)
        self.cb_scaling.activated.connect(self.updateUi)
        self.chb_renderPreset.stateChanged.connect(self.presetOverrideChanged)
        self.cb_renderPreset.activated.connect(self.stateManager.saveStatesToScene)
        self.cb_rangeType.activated.connect(self.rangeTypeChanged)
        self.sp_rangeStart.editingFinished.connect(self.startChanged)
        self.sp_rangeEnd.editingFinished.connect(self.endChanged)
        self.le_frameExpression.textChanged.connect(self.frameExpressionChanged)
        self.le_frameExpression.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.le_frameExpression.setMouseTracking(True)
        self.le_frameExpression.origMoveEvent = self.le_frameExpression.mouseMoveEvent
        self.le_frameExpression.mouseMoveEvent = self.exprMoveEvent
        self.le_frameExpression.leaveEvent = self.exprLeaveEvent
        self.le_frameExpression.focusOutEvent = self.exprFocusOutEvent
        self.cb_cam.activated.connect(self.setCam)
        self.chb_resOverride.stateChanged.connect(self.resOverrideChanged)
        self.sp_resWidth.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.sp_resHeight.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.b_resPresets.clicked.connect(self.showResPresets)
        self.cb_master.activated.connect(self.stateManager.saveStatesToScene)
        self.e_samples.textChanged.connect(self.stateManager.saveStatesToScene)
        self.cb_outPath.activated[int].connect(self.stateManager.saveStatesToScene)
        self.chb_overrideLayers.toggled.connect(self.updateUi)
        self.cb_renderLayer.currentIndexChanged.connect(self.updateUi)
        self.chb_compositor.toggled.connect(self.stateManager.saveStatesToScene)            
        self.chb_persData.toggled.connect(self.stateManager.saveStatesToScene)              
        self.cb_format.currentIndexChanged.connect(self.setupFormatOptions)                 
        self.cb_format.activated.connect(self.stateManager.saveStatesToScene)
        self.cb_exrCodec.activated.connect(self.stateManager.saveStatesToScene)             
        self.cb_exrBitDepth.activated.connect(self.stateManager.saveStatesToScene)          
        self.cb_pngBitDepth.activated.connect(self.stateManager.saveStatesToScene)          
        self.sp_pngCompress.editingFinished.connect(self.stateManager.saveStatesToScene)    
        self.sp_jpegQual.editingFinished.connect(self.stateManager.saveStatesToScene)       
        self.chb_alpha.toggled.connect(self.updateUi)
        self.chb_colorSpace.toggled.connect(self.updateUi)
        self.cb_colorSpace.activated.connect(self.stateManager.saveStatesToScene)
        self.gb_submit.toggled.connect(self.rjToggled)
        self.cb_manager.activated.connect(self.managerChanged)
        self.sp_rjPrio.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.sp_rjFramesPerTask.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.sp_rjTimeout.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.chb_rjSuspended.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.chb_osDependencies.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.chb_osUpload.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.chb_osPAssets.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.e_osSlaves.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.b_osSlaves.clicked.connect(self.openSlaves)
        self.sp_dlConcurrentTasks.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.sp_dlGPUpt.editingFinished.connect(self.gpuPtChanged)
        self.le_dlGPUdevices.editingFinished.connect(self.gpuDevicesChanged)
        self.gb_passes.toggled.connect(self.stateManager.saveStatesToScene)
        self.b_addPasses.clicked.connect(self.showPasses)
        self.lw_passes.customContextMenuRequested.connect(self.rclickPasses)
        self.b_pathLast.clicked.connect(self.showLastPathMenu)
        self.lw_passes.itemDoubleClicked.connect(
            lambda x: self.core.appPlugin.sm_render_openPasses(self)
            )


    @err_catcher(name=__name__)
    def setToolTips(self):
        tip = "Media Identifier.  Taskname is default."
        self.l_taskName.setToolTip(tip)

        tip = "Click to change Identifier.  This will also rename the State name."
        self.b_changeTask.setToolTip(tip)

        tip = ("Auto-generated AOV name based on output file type and alpha.\n"
               "EXR multilayer:  RGB-Data or RGBA-Data\n"
               "EXR:  RGB or RGBA\n"
               "PNG:  RGB or RGBA\n"
               "JPG:  beauty"
               )
        self.e_aovNameAuto.setToolTip(tip)

        tip = "Custom AOV name."
        self.e_aovNameCustom.setToolTip(tip)

        tip = "Toggle to allow creating custom AOV name."
        self.chb_customAOV.setToolTip(tip)

        tip = ("Frame range type to be rendered.\n"
               "Defaults to:\n"
               "Asset: single frame\n"
               "Shot: shot framereange"
               )
        self.cb_rangeType.setToolTip(tip)

        tip = "Camera to be rendered.  Active scene camera is default."
        self.cb_cam.setToolTip(tip)

        tip = "Use render resolution presets."
        self.chb_resOverride.setToolTip(tip)

        tip = "Master version method.  Default is Do Not Update."
        self.cb_master.setToolTip(tip)

        tip = "Render samples override.  Default is from scenefile."
        self.e_samples.setToolTip(tip)

        tip = "Override of view layer to be rendered.  Unchecked will render view layers as is in scenefile."
        self.chb_overrideLayers.setToolTip(tip)

        tip = "File output type.  EXR multilayer will enable passes."
        self.cb_format.setToolTip(tip)

        tip = ("Compression Codec to be used for EXR:\n"
               "Zip:  lossless\n"
               "ZipS: lossless\n"
               "PIZ:  lossless\n"
               "RLE:  lossless\n"
               "DWAA: lossy\n"
               "DWAB: lossy"
              )
        self.cb_exrCodec.setToolTip(tip)

        tip = ("PNG lossless compression ratio.\n"
               "Higher is smaller but slower."
              )
        self.sp_pngCompress.setToolTip(tip)

        tip = ("JPG quality.\n"
               "Higher is larger but better quality."
              )
        self.sp_jpegQual.setToolTip(tip)

        tip = "Bit depth for EXR and PNG output types."
        self.cb_exrBitDepth.setToolTip(tip)
        self.cb_pngBitDepth.setToolTip(tip)

        tip = "Toggle to use or bypass the Compositor."
        self.chb_compositor.setToolTip(tip)

        tip = ("Use Persistent Data.\n"
               "May speed up render times, but can cause glitches with motion blur."
              )
        self.chb_persData.setToolTip(tip)

        tip = "Toggle to use an Alpha channel."
        self.chb_alpha.setToolTip(tip)

        tip = "Color space for rendered images."
        self.l_colorSpace.setToolTip(tip)
        self.chb_colorSpace.setToolTip(tip)
        self.cb_colorSpace.setToolTip(tip)

        tip = ("Selected AOV passes.  Right-click to delete.\n\n"
               "If using Render Layer override, passes will be per layer."
              )
        self.lw_passes.setToolTip(tip)

        tip = "Submit job to Render Farm."
        self.gb_submit.setToolTip(tip)


    @err_catcher(name=__name__)
    def loadStateData(self, data):
        if "contextType" in data:
            self.setContextType(data["contextType"])
        if "customContext" in data:
            self.customContext = data["customContext"]
        if "taskname" in data:
            self.setTaskname(data["taskname"])

        if "useCustomAOV" in data:
            checked = data["useCustomAOV"]
            self.chb_customAOV.setChecked(checked)
            self.aovNameSetup()

        if "aovNameCustom" in data:                                         
            self.e_aovNameCustom.setText(data["aovNameCustom"])

        if "stateName" in data:
            self.e_name.setText(data["stateName"])
        elif "statename" in data:
            self.e_name.setText(data["statename"] + " - {identifier}")

        if "rezScale" in data:                                              
            idx = self.cb_scaling.findText(data["rezScale"])
            if idx != -1:
                self.cb_scaling.setCurrentIndex(idx)
                self.stateManager.saveStatesToScene()
        else:                                                               
            idx = self.cb_scaling.findText("100")
            self.cb_scaling.setCurrentIndex(idx)
            self.stateManager.saveStatesToScene()

        if "renderpresetoverride" in data:
            res = eval(data["renderpresetoverride"])
            self.chb_renderPreset.setChecked(res)

        if "currentrenderpreset" in data:
            idx = self.cb_renderPreset.findText(data["currentrenderpreset"])
            if idx != -1:
                self.cb_renderPreset.setCurrentIndex(idx)
                self.stateManager.saveStatesToScene()

        if "rangeType" in data:
            idx = self.cb_rangeType.findText(data["rangeType"])
            if idx != -1:
                self.cb_rangeType.setCurrentIndex(idx)
                self.updateRange()

        if "startframe" in data:
            self.sp_rangeStart.setValue(int(data["startframe"]))
        if "endframe" in data:
            self.sp_rangeEnd.setValue(int(data["endframe"]))
        if "frameExpression" in data:
            self.le_frameExpression.setText(data["frameExpression"])

        if "currentcam" in data:
            camName = getattr(self.core.appPlugin, "getCamName", lambda x, y: "")(
                self, data["currentcam"]
                )
            idx = self.cb_cam.findText(camName)
            if idx != -1:
                self.curCam = self.camlist[idx]
                self.cb_cam.setCurrentIndex(idx)
                self.stateManager.saveStatesToScene()

        if "resoverride" in data:
            res = eval(data["resoverride"])
            self.chb_resOverride.setChecked(res[0])
            self.sp_resWidth.setValue(res[1])
            self.sp_resHeight.setValue(res[2])

        if "masterVersion" in data:
            idx = self.cb_master.findText(data["masterVersion"])
            if idx != -1:
                self.cb_master.setCurrentIndex(idx)

        if "renderSamples" in data:                                         
            self.e_samples.setText(data["renderSamples"])

        if "curoutputpath" in data:
            idx = self.cb_outPath.findText(data["curoutputpath"])
            if idx != -1:
                self.cb_outPath.setCurrentIndex(idx)

        if "overrideLayers" in data:                                        
            self.chb_overrideLayers.setChecked(data["overrideLayers"])
            self.cb_renderLayer.setEnabled(data["overrideLayers"])

        if "renderlayer" in data:
            idx = self.cb_renderLayer.findText(data["renderlayer"])
            if idx != -1:
                self.cb_renderLayer.setCurrentIndex(idx)
                self.stateManager.saveStatesToScene()

        if "outputFormat" in data:
            idx = self.cb_format.findText(data["outputFormat"])
            if idx != -1:
                self.cb_format.setCurrentIndex(idx)

        self.setupFormatOptions(mode="Load")                                

        if "codec" in data:                                                 
            idx = self.cb_exrCodec.findText(data["codec"])
            if idx != -1:
                self.cb_exrCodec.setCurrentIndex(idx)

        if "exrBitDepth" in data:                                           
            idx = self.cb_exrBitDepth.findText(data["exrBitDepth"])
            if idx != -1:
                self.cb_exrBitDepth.setCurrentIndex(idx)

        if "pngBitDepth" in data:                                           
            idx = self.cb_pngBitDepth.findText(data["pngBitDepth"])
            if idx != -1:
                self.cb_pngBitDepth.setCurrentIndex(idx)

        if "pngComp" in data:
            self.sp_pngCompress.setValue(int(data["pngComp"]))              

        if "jpegQual" in data:
            self.sp_jpegQual.setValue(int(data["jpegQual"]))                

        if "useAlpha" in data:                                              
            self.chb_alpha.setChecked(data["useAlpha"])

        if "useComp" in data:
            self.chb_compositor.setChecked(data["useComp"])

        if "persData" in data:
            self.chb_persData.setChecked(data["persData"])

        if "ovrColorSpace" in data:
            self.chb_colorSpace.setChecked(data["ovrColorSpace"])

        if "currColorSpace" in data:
            idx = self.cb_colorSpace.findText(data["currColorSpace"])
            if idx != -1:
                self.cb_colorSpace.setCurrentIndex(idx)

        if "submitrender" in data:
            self.gb_submit.setChecked(eval(data["submitrender"]))

        if "rjmanager" in data:
            idx = self.cb_manager.findText(data["rjmanager"])
            if idx != -1:
                self.cb_manager.setCurrentIndex(idx)

            self.managerChanged(True)

        if "rjprio" in data:
            self.sp_rjPrio.setValue(int(data["rjprio"]))
        if "rjframespertask" in data:
            self.sp_rjFramesPerTask.setValue(int(data["rjframespertask"]))
        if "rjtimeout" in data:
            self.sp_rjTimeout.setValue(int(data["rjtimeout"]))
        if "rjsuspended" in data:
            self.chb_rjSuspended.setChecked(eval(data["rjsuspended"]))
        if "osdependencies" in data:
            self.chb_osDependencies.setChecked(eval(data["osdependencies"]))
        if "osupload" in data:
            self.chb_osUpload.setChecked(eval(data["osupload"]))
        if "ospassets" in data:
            self.chb_osPAssets.setChecked(eval(data["ospassets"]))
        if "osslaves" in data:
            self.e_osSlaves.setText(data["osslaves"])
        if "dlconcurrent" in data:
            self.sp_dlConcurrentTasks.setValue(int(data["dlconcurrent"]))
        if "dlgpupt" in data:
            self.sp_dlGPUpt.setValue(int(data["dlgpupt"]))
            self.gpuPtChanged()
        if "dlgpudevices" in data:
            self.le_dlGPUdevices.setText(data["dlgpudevices"])
            self.gpuDevicesChanged()
        if "enablepasses" in data:
            self.gb_passes.setChecked(eval(data["enablepasses"]))
        if "lastexportpath" in data:
            lePath = self.core.fixPath(data["lastexportpath"])
            self.l_pathLast.setText(lePath)
            self.l_pathLast.setToolTip(lePath)
        if "stateenabled" in data:
            if type(data["stateenabled"]) == int:
                self.state.setCheckState(
                    0, Qt.CheckState(data["stateenabled"]),
                )

        self.updateUi()

        self.core.callback("onStateSettingsLoaded", self, data)


    @err_catcher(name=__name__)
    def createNewStateData(self):
        self.e_aovNameCustom.hide()
        self.e_aovNameCustom.setText("beauty")

        context = self.getCurrentContext()
        if context.get("type") == "asset":
            self.setRangeType("Single Frame")
        elif context.get("type") == "shot":
            self.setRangeType("Shot")
        elif self.stateManager.standalone:
            self.setRangeType("Custom")
        else:
            self.setRangeType("Scene")

        start, end = self.getFrameRange("Scene")
        if start is not None:
            self.sp_rangeStart.setValue(start)

        if end is not None:
            self.sp_rangeEnd.setValue(end)

        if context.get("task"):
            self.setTaskname(context.get("task"))

        notUpdateIdx = self.cb_master.findText("Don't update master")
        if notUpdateIdx != -1:
            self.cb_master.setCurrentIndex(notUpdateIdx)

        self.chb_overrideLayers.setChecked(False)                         

        curLayName = self.getRenderLayers("current")
        curIdx = self.cb_renderLayer.findText(curLayName)
        if curIdx != -1:
            self.cb_renderLayer.setCurrentIndex(curIdx)

        #   Options for new instance of BlenderRender
        newOptions = {                                                    
            "format": ".exr",                                                       
            "codec": "DWAA",
            "bitDepth": "16",
            "useAlpha": True
            }
        self.setupFormatOptions(mode="New", loadOptions=newOptions)       

        samples = self.getRenderSamples(command="Status")
        self.e_samples.setText(str(samples))                              

        useComp = self.useCompositor(command="Status")                    
        self.chb_compositor.setChecked(useComp)

        usePD = self.getPersistantData(command="Status")                  
        self.chb_persData.setChecked(usePD)

        ovrColorSpace = self.getColorSpaces(command="isOverride")
        self.chb_colorSpace.setChecked(ovrColorSpace)

        curColorSpace = self.getColorSpaces(command="current")
        curIdx = self.cb_colorSpace.findText(curColorSpace)
        if curIdx != -1:
            self.cb_colorSpace.setCurrentIndex(curIdx)

        self.updateUi()


    @err_catcher(name=__name__)
    def updateUi(self, *arg):
        self.w_context.setHidden(not self.allowCustomContext)
        self.refreshContext()

        # update Cams
        self.cb_cam.clear()
        self.camlist = camNames = []

        if not self.stateManager.standalone:
            self.camlist = self.core.appPlugin.getCamNodes(self, cur=True)
            camNames = [self.core.appPlugin.getCamName(self, i) for i in self.camlist]

        self.cb_cam.addItems(camNames)

        if self.curCam in self.camlist:
            self.cb_cam.setCurrentIndex(self.camlist.index(self.curCam))
        else:
            self.cb_cam.setCurrentIndex(0)
            if len(self.camlist) > 0:
                self.curCam = self.camlist[0]
            else:
                self.curCam = None

            self.stateManager.saveStatesToScene()

        self.rezScaleCalc("load")                                                 
        self.updateRange()

        if not self.core.mediaProducts.getUseMaster():
            self.w_master.setVisible(False)

        self.refreshSubmitUi()
        self.refreshPasses()

        ovrColorspace = self.chb_colorSpace.isChecked()
        self.cb_colorSpace.setEnabled(ovrColorspace)
        if not ovrColorspace:
            sceneColorspace = self.getColorSpaces(command="current")
            curIdx = self.cb_colorSpace.findText(sceneColorspace)
            if curIdx != -1:
                self.cb_colorSpace.setCurrentIndex(curIdx)

        if self.chb_resOverride.isChecked():
            tip1 = tip2 = "Disabled"
            tip3 = "Final render resolution."
            tip4 = "Select Preset"
        else:
            tip1 = "Render resolution scaling for final render."
            tip2 = "Final render resolution based on scaling of the resolution of the scenefile."
            tip3 = tip4 = "Disabled"
        self.cb_scaling.setToolTip(tip1)
        self.e_xRez.setToolTip(tip2)
        self.e_yRez.setToolTip(tip2)
        self.sp_resWidth.setToolTip(tip3)
        self.sp_resHeight.setToolTip(tip3)
        self.b_resPresets.setToolTip(tip4)

        if self.chb_overrideLayers.isChecked():
            tip = "View Layer to be rendered."
        else:
            tip = "Disabled"
        self.cb_renderLayer.setToolTip(tip)

        if self.chb_colorSpace.isChecked():
            tip = "Override Colorspace from scenefile."
        else:
            tip = "Use scenefile Colorspace."
        self.cb_colorSpace.setToolTip(tip)

        if self.cb_format.currentText() == ".exrMulti":
            tip = "Opens dialog to select AOV passes"
        else:
            tip = "Select EXR multilayer to enable AOV passes"
        self.b_addPasses.setToolTip(tip)

        self.nameChanged(self.e_name.text())
        self.aovNameSetup()
        self.stateManager.saveStatesToScene()

        return True
    

    @err_catcher(name=__name__)
    def setupFormatOptions(self, index=None, mode=None, loadOptions=None):
        for widget in [
            self.l_bitDepth, self.cb_exrBitDepth, self.cb_pngBitDepth,
            self.cb_exrCodec, self.sp_pngCompress, self.sp_jpegQual, self.chb_alpha,
            self.l_colorSpace, self.chb_colorSpace, self.cb_colorSpace
            ]:
            widget.hide()

        if mode in ["New", "Load"]:
            for fullFormat in self.formatOptions:
                format = fullFormat.strip('.')
                if format == "exrMulti":
                    format = "exr"
                
                if "bitDepths" in self.formatOptions[fullFormat]:
                    bitDepthComboBox = getattr(self, f"cb_{format}BitDepth")
                    bitDepthComboBox.clear()
                    bitDepthComboBox.addItems(self.formatOptions[fullFormat]["bitDepths"])

                if "codec" in self.formatOptions[fullFormat]:
                    codecComboBox = getattr(self, f"cb_{format}Codec")
                    codecComboBox.clear()
                    codecComboBox.addItems(self.formatOptions[fullFormat]["codec"])

        if mode == "New":
            self.cb_format.setCurrentIndex(self.cb_format.findText(loadOptions.get("format", "")))
            self.cb_exrCodec.setCurrentIndex(self.cb_exrCodec.findText(loadOptions.get("codec", "")))
            self.cb_exrBitDepth.setCurrentIndex(self.cb_exrBitDepth.findText(loadOptions.get("bitDepth", "")))
            self.chb_alpha.setChecked(bool(loadOptions.get("useAlpha", "")))

        currentFormat = self.cb_format.currentText()
        options = self.formatOptions.get(currentFormat, {})

        self.l_fileCompress.setText(options.get("compressLabel", ""))

        if "bitDepths" in options:
            self.l_bitDepth.show()

            if currentFormat in [".exr", ".exrMulti"]:
                self.cb_exrBitDepth.show()
            elif currentFormat == ".png":
                self.cb_pngBitDepth.show()

        if "codec" in options:
            self.cb_exrCodec.show()

        if "compressWidget" in options:
            options["compressWidget"].show()

        if "alpha" in options and options["alpha"]:
            self.chb_alpha.show()
        if "colorSpace" in options and options["colorSpace"]:
            self.l_colorSpace.show()
            self.chb_colorSpace.show()
            self.cb_colorSpace.show()

        self.updateUi()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)                                     
    def aovNameSetup(self, checked=False):
        autoName = not self.chb_customAOV.isChecked()
        fileType = self.cb_format.currentText()
        useAlpha = self.chb_alpha.isChecked()

        self.e_aovNameAuto.setVisible(autoName)
        self.e_aovNameCustom.setVisible(not autoName)

        isEXRmulti = fileType == ".exrMulti"
        self.gb_passes.setChecked(isEXRmulti)
        self.gb_passes.setEnabled(isEXRmulti)
        self.lw_passes.setVisible(isEXRmulti)

        if fileType in [".exr", ".exrMulti", ".png"]:
            aovName = "RGB"
            if useAlpha:
                aovName = aovName + "A"
            if isEXRmulti:
                aovName = aovName + "-Data"
        else:
            aovName = "beauty"
        self.e_aovNameAuto.setText(aovName)

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def showLastPathMenu(self, state=None):
        path = self.l_pathLast.text()
        if path == "None":
            return

        menu = QMenu(self)

        act_open = QAction("Play", self)
        act_open.triggered.connect(lambda: self.core.media.playMediaInExternalPlayer(path))
        menu.addAction(act_open)

        act_open = QAction("Open in Media Browser", self)
        act_open.triggered.connect(lambda: self.openInMediaBrowser(path))
        menu.addAction(act_open)

        act_open = QAction("Open in explorer", self)
        act_open.triggered.connect(lambda: self.core.openFolder(path))
        menu.addAction(act_open)

        act_copy = QAction("Copy", self)
        act_copy.triggered.connect(lambda: self.core.copyToClipboard(path, file=True))
        menu.addAction(act_copy)

        menu.exec_(QCursor.pos())


    @err_catcher(name=__name__)
    def openInMediaBrowser(self, path):
        self.core.projectBrowser()
        self.core.pb.showTab("Media")
        data = self.core.paths.getRenderProductData(path)
        self.core.pb.mediaBrowser.showRender(entity=data, identifier=data.get("identifier"), version=data.get("version"))


    @err_catcher(name=__name__)
    def selectContextClicked(self, state=None):
        self.dlg_entity = self.stateManager.entityDlg(self)
        data = self.getCurrentContext()
        self.dlg_entity.w_entities.navigate(data)
        self.dlg_entity.entitySelected.connect(lambda x: self.setCustomContext(x))
        self.dlg_entity.show()


    @err_catcher(name=__name__)
    def setCustomContext(self, context):
        self.customContext = context
        self.refreshContext()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def onContextTypeChanged(self, state):
        self.refreshContext()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)                                     
    def currentAOVname(self):
        if self.chb_customAOV.isChecked():
            return self.e_aovNameCustom.text()
        
        elif not self.chb_customAOV.isChecked():
            return self.e_aovNameAuto.text()


    @err_catcher(name=__name__)
    def rangeTypeChanged(self, state):
        self.updateUi()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def startChanged(self):
        if self.sp_rangeStart.value() > self.sp_rangeEnd.value():
            self.sp_rangeEnd.setValue(self.sp_rangeStart.value())

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def endChanged(self):
        if self.sp_rangeEnd.value() < self.sp_rangeStart.value():
            self.sp_rangeStart.setValue(self.sp_rangeEnd.value())

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def frameExpressionChanged(self, text=None):
        if not hasattr(self, "expressionWinLabel"):
            return

        frames = self.core.resolveFrameExpression(self.le_frameExpression.text())
        if len(frames) > 1000:
            frames = frames[:1000]
            frames.append("...")

        for idx in range(int(len(frames) / 30.0)):
            frames.insert((idx+1)*30, "\n")

        frameStr = ",".join([str(x) for x in frames]) or "invalid expression"
        self.expressionWinLabel.setText(frameStr)
        self.expressionWin.resize(1, 1)


    @err_catcher(name=__name__)
    def exprMoveEvent(self, event):
        self.showExpressionWin(event)
        if hasattr(self, "expressionWin") and self.expressionWin.isVisible():
            self.expressionWin.move(
                QCursor.pos().x() + 20, QCursor.pos().y() - self.expressionWin.height()
                )
        self.le_frameExpression.origMoveEvent(event)


    @err_catcher(name=__name__)
    def showExpressionWin(self, event):
        if not hasattr(self, "expressionWin") or not self.expressionWin.isVisible():
            if hasattr(self, "expressionWin"):
                self.expressionWin.close()

            self.expressionWin = QFrame()
            ss = getattr(self.core.appPlugin, "getFrameStyleSheet", lambda x: "")(self)
            self.expressionWin.setStyleSheet(
                ss + """ .QFrame{ border: 2px solid rgb(100,100,100);} """
                )

            self.core.parentWindow(self.expressionWin)
            winwidth = 10
            winheight = 10
            VBox = QVBoxLayout()
            frames = self.core.resolveFrameExpression(self.le_frameExpression.text())
            if len(frames) > 1000:
                frames = frames[:1000]
                frames.append("...")

            for idx in range(int(len(frames) / 30.0)):
                frames.insert((idx+1)*30, "\n")

            frameStr = ",".join([str(x) for x in frames]) or "invalid expression"
            self.expressionWinLabel = QLabel(frameStr)
            VBox.addWidget(self.expressionWinLabel)
            self.expressionWin.setLayout(VBox)
            self.expressionWin.setWindowFlags(
                Qt.FramelessWindowHint  # hides the window controls
                | Qt.WindowStaysOnTopHint  # forces window to top... maybe
                | Qt.SplashScreen  # this one hides it from the task bar!
                )

            self.expressionWin.setGeometry(0, 0, winwidth, winheight)
            self.expressionWin.move(QCursor.pos().x() + 20, QCursor.pos().y())
            self.expressionWin.setAttribute(Qt.WA_ShowWithoutActivating)
            self.expressionWin.show()


    @err_catcher(name=__name__)
    def exprLeaveEvent(self, event):
        if hasattr(self, "expressionWin") and self.expressionWin.isVisible():
            self.expressionWin.close()


    @err_catcher(name=__name__)
    def exprFocusOutEvent(self, event):
        if hasattr(self, "expressionWin") and self.expressionWin.isVisible():
            self.expressionWin.close()


    @err_catcher(name=__name__)
    def setCam(self, index):
        self.curCam = self.camlist[index]
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def nameChanged(self, text):
        text = self.e_name.text()
        context = {}
        context["identifier"] = self.getTaskname() or "None"
        num = 0
        try:
            if "{#}" in text:
                while True:
                    context["#"] = num or ""
                    name = text.format(**context)
                    for state in self.stateManager.states:
                        if state.ui.listType != "Export":
                            continue

                        if state is self.state:
                            continue

                        if state.text(0) == name:
                            num += 1
                            break
                    else:
                        break
            else:
                name = text.format(**context)
        except Exception:
            name = text

        if self.state.text(0).endswith(" - disabled"):
            name += " - disabled"

        self.state.setText(0, name)


    @err_catcher(name=__name__)
    def setFormat(self, fmt):
        idx = self.cb_format.findText(fmt)
        if idx != -1:
            self.cb_format.setCurrentIndex(idx)
            self.stateManager.saveStatesToScene()
            return True

        return False


    @err_catcher(name=__name__)
    def getContextType(self):
        contextType = self.cb_context.currentText()
        return contextType


    @err_catcher(name=__name__)
    def setContextType(self, contextType):
        idx = self.cb_context.findText(contextType)
        if idx != -1:
            self.cb_context.setCurrentIndex(idx)
            self.refreshContext()
            return True

        return False


    @err_catcher(name=__name__)
    def getTaskname(self):
        taskName = self.l_taskName.text()
        return taskName


    @err_catcher(name=__name__)
    def setTaskname(self, taskname):
        self.l_taskName.setText(taskname)
        self.setTaskWarn(not bool(taskname))
        self.updateUi()


    @err_catcher(name=__name__)
    def getSortKey(self):
        return self.getTaskname()


    @err_catcher(name=__name__)
    def changeTask(self):
        from PrismUtils import PrismWidgets
        self.nameWin = PrismWidgets.CreateItem(
            startText=self.getTaskname(),
            showTasks=True,
            taskType="3d",
            core=self.core,
        )
        self.core.parentWindow(self.nameWin)
        self.nameWin.setWindowTitle("Change Identifier")
        self.nameWin.l_item.setText("Identifier:")
        self.nameWin.buttonBox.buttons()[0].setText("Ok")
        self.nameWin.e_item.selectAll()
        result = self.nameWin.exec_()

        if result == 1:
            self.setTaskname(self.nameWin.e_item.text())
            self.nameChanged(self.e_name.text())
            self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def presetOverrideChanged(self, checked):
        self.cb_renderPreset.setEnabled(checked)
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def resOverrideChanged(self, checked):
        self.sp_resWidth.setEnabled(checked)
        self.sp_resHeight.setEnabled(checked)
        self.b_resPresets.setEnabled(checked)

        self.updateUi()

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def showResPresets(self):
        pmenu = QMenu(self)

        for preset in self.resolutionPresets:
            pAct = QAction(preset, self)
            res = self.getResolution(preset)
            if not res:
                continue

            pwidth, pheight = res

            pAct.triggered.connect(
                lambda x=None, v=pwidth: self.sp_resWidth.setValue(v)
            )
            pAct.triggered.connect(
                lambda x=None, v=pheight: self.sp_resHeight.setValue(v)
            )
            pAct.triggered.connect(lambda: self.stateManager.saveStatesToScene())
            pmenu.addAction(pAct)

        pmenu.exec_(QCursor.pos())


    @err_catcher(name=__name__)
    def getRangeType(self):
        return self.cb_rangeType.currentText()


    @err_catcher(name=__name__)
    def setRangeType(self, rangeType):
        idx = self.cb_rangeType.findText(rangeType)
        if idx != -1:
            self.cb_rangeType.setCurrentIndex(idx)
            self.updateRange()
            return True

        return False


    @err_catcher(name=__name__)
    def getResolution(self, resolution):
        res = None
        if resolution == "Get from rendersettings":
            if hasattr(self.core.appPlugin, "getResolution"):
                res = self.core.appPlugin.getResolution()
            else:
                res = [1920, 1080]
        elif resolution.startswith("Project ("):
            res = resolution[9:-1].split("x")
            res = [int(r) for r in res]
        else:
            try:
                pwidth = int(resolution.split("x")[0])
                pheight = int(resolution.split("x")[1])
                res = [pwidth, pheight]
            except:
                res = getattr(
                    self.core.appPlugin, "evaluateResolution", lambda x: None
                )(resolution)

        return res
    

    @err_catcher(name=__name__)                                 
    def rezScaleCalc(self, index):
        if hasattr(self.core.appPlugin, "getResolution"):
            rez = self.core.appPlugin.getResolution()

        scale = int(self.cb_scaling.currentText()) / 100

        xRezScaled = round(rez[0] * scale)
        self.e_xRez.setText(str(xRezScaled))

        yRezScaled = round(rez[1] * scale)
        self.e_yRez.setText(str(yRezScaled))

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def getMasterVersion(self):
        return self.cb_master.currentText()


    @err_catcher(name=__name__)
    def setMasterVersion(self, master):
        idx = self.cb_master.findText(master)
        if idx != -1:
            self.cb_master.setCurrentIndex(idx)
            self.stateManager.saveStatesToScene()
            return True

        return False
    

    @err_catcher(name=__name__)                             
    def getRenderSamples(self, command, samples=None):
        if command == "Status":
            isChecked = self.core.appPlugin.getRenderSamples(command="Status")

            return isChecked
        
        elif command == "Set":
            self.core.appPlugin.getRenderSamples(command="Set", samples=samples)


    @err_catcher(name=__name__)                             
    def useCompositor(self, command, useComp=False):
        if command == "Status":
            isChecked = self.core.appPlugin.useCompositor(command="Status")

            return isChecked
        
        elif command == "Set":
            self.core.appPlugin.useCompositor(command="Set", useComp=useComp)


    @err_catcher(name=__name__)                             
    def getPersistantData (self, command, usePD=False):
        if command == "Status":
            isChecked = self.core.appPlugin.getPersistantData(command="Status")

            return isChecked
        
        elif command == "Set":
            self.core.appPlugin.getPersistantData(command="Set", usePD=usePD)


    @err_catcher(name=__name__)                             
    def getColorSpaces(self, command):
        colorOverride, currSpace, spaceList = self.core.appPlugin.getColorSpaces()

        if command == "isOverride":
            return colorOverride
        
        if command == "current":
            return currSpace
        
        if command == "load":
            self.cb_colorSpace.addItems(spaceList)


    @err_catcher(name=__name__)
    def getLocation(self):
        return self.cb_outPath.currentText()


    @err_catcher(name=__name__)
    def setLocation(self, location):
        idx = self.cb_outPath.findText(location)
        if idx != -1:
            self.cb_outPath.setCurrentIndex(idx)
            self.stateManager.saveStatesToScene()
            return True

        return False
    

    @err_catcher(name=__name__)                         
    def getRenderLayers(self, command="current"):
        renderLayers, currentLayer = self.core.appPlugin.getRenderLayers()

        if command == "current":
            return currentLayer
        elif command == "all":
            return renderLayers
        elif command == "load":
            self.cb_renderLayer.addItems(renderLayers)


    @err_catcher(name=__name__)
    def refreshContext(self):
        context = self.getCurrentContext()
        contextStr = self.getContextStrFromEntity(context)
        self.l_context.setText(contextStr)


    @err_catcher(name=__name__)
    def getCurrentContext(self):
        context = None
        if self.allowCustomContext:
            ctype = self.getContextType()
            if ctype == "Custom":
                context = self.customContext

        if not context:
            fileName = self.core.getCurrentFileName()
            context = self.core.getScenefileData(fileName)
        
        if "username" in context:
            del context["username"]

        if "user" in context:
            del context["user"]

        return context


    @err_catcher(name=__name__)
    def refreshSubmitUi(self):
        if not self.gb_submit.isHidden():
            if not self.gb_submit.isCheckable():
                return

            submitChecked = self.gb_submit.isChecked()
            for idx in reversed(range(self.gb_submit.layout().count())):
                self.gb_submit.layout().itemAt(idx).widget().setHidden(not submitChecked)

            if submitChecked:
                self.core.plugins.getRenderfarmPlugin(self.cb_manager.currentText()).sm_render_updateUI(self)


    @err_catcher(name=__name__)
    def updateRange(self):
        rangeType = self.cb_rangeType.currentText()
        isCustom = rangeType == "Custom"
        isExp = rangeType == "Expression"
        isFML = rangeType in ["FML", "FMMML"]

        self.l_rangeStart.setVisible(not isCustom and not isExp and not isFML)
        self.l_rangeEnd.setVisible(not isCustom and not isExp and not isFML)
        self.sp_rangeStart.setVisible(isCustom)
        self.sp_rangeEnd.setVisible(isCustom)
        self.l_rangeStartInfo.setVisible(not isFML)
        self.l_rangeEndInfo.setVisible(not isFML)
        self.w_frameRangeValues.setVisible(not isExp and not isFML)
        self.w_frameExpression.setVisible(isExp)
        self.w_fml.setVisible(isFML)

        if not isCustom and not isExp and not isFML:
            frange = self.getFrameRange(rangeType=rangeType)
            start = str(int(frange[0])) if frange[0] is not None else "-"
            end = str(int(frange[1])) if frange[1] is not None else "-"
            self.l_rangeStart.setText(start)
            self.l_rangeEnd.setText(end)

        if rangeType in ["FML", "FMMML"]:                                                      
            self.fmlRange(rangeType)                                                         


    @err_catcher(name=__name__)
    def fmlRange(self, rangeType):
        startFrame, endFrame = self.getFrameRange(rangeType="Shot")
        middleFrame = round((startFrame + endFrame) / 2)

        if rangeType == "FML":
            middleFrame = round((startFrame + endFrame) / 2)
            fmlString = f"{startFrame}, {middleFrame}, {endFrame}"
        else:
            step = (endFrame - startFrame) / 4
            mdlFirst, mdlSecond, mdlThrird = round(startFrame + step), round(startFrame + 2 * step), round(startFrame + 3 * step)
            fmlString = f"{startFrame}, {mdlFirst}, {mdlSecond}, {mdlThrird}, {endFrame}"

        self.e_fml.setText(fmlString)


    @err_catcher(name=__name__)
    def getFrameRange(self, rangeType):
        startFrame = None
        endFrame = None
        if rangeType == "Scene":
            if hasattr(self.core.appPlugin, "getFrameRange"):
                startFrame, endFrame = self.core.appPlugin.getFrameRange(self)
                startFrame = int(startFrame)
                endFrame = int(endFrame)
            else:
                startFrame = 1001
                endFrame = 1100
        elif rangeType == "Shot":
            context = self.getCurrentContext()
            if context.get("type") == "shot" and "sequence" in context:
                frange = self.core.entities.getShotRange(context)
                if frange:
                    startFrame, endFrame = frange
        elif rangeType == "Single Frame":
            if hasattr(self.core.appPlugin, "getCurrentFrame"):
                startFrame = int(self.core.appPlugin.getCurrentFrame())
            else:
                startFrame = 1001
        elif rangeType == "Custom":
            startFrame = self.sp_rangeStart.value()
            endFrame = self.sp_rangeEnd.value()
        elif rangeType == "Expression":
            return self.core.resolveFrameExpression(self.le_frameExpression.text())

        elif rangeType in ["FML", "FMMML"]:
            return self.core.resolveFrameExpression(self.e_fml.text())
        
        if startFrame == "":
            startFrame = None

        if endFrame == "":
            endFrame = None

        if startFrame is not None:
            startFrame = int(startFrame)

        if endFrame is not None:
            endFrame = int(endFrame)

        return startFrame, endFrame


    @err_catcher(name=__name__)
    def openSlaves(self):
        if eval(os.getenv("PRISM_DEBUG", "False")):
            try:
                del sys.modules["SlaveAssignment"]
            except:
                pass

        import SlaveAssignment

        self.sa = SlaveAssignment.SlaveAssignment(
            core=self.core, curSlaves=self.e_osSlaves.text()
            )
        result = self.sa.exec_()

        if result == 1:
            selSlaves = ""
            if self.sa.rb_exclude.isChecked():
                selSlaves = "exclude "
            if self.sa.rb_all.isChecked():
                selSlaves += "All"
            elif self.sa.rb_group.isChecked():
                selSlaves += "groups: "
                for i in self.sa.activeGroups:
                    selSlaves += i + ", "

                if selSlaves.endswith(", "):
                    selSlaves = selSlaves[:-2]

            elif self.sa.rb_custom.isChecked():
                slavesList = [x.text() for x in self.sa.lw_slaves.selectedItems()]
                for i in slavesList:
                    selSlaves += i + ", "

                if selSlaves.endswith(", "):
                    selSlaves = selSlaves[:-2]

            self.e_osSlaves.setText(selSlaves)
            self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def gpuPtChanged(self):
        self.w_dlGPUdevices.setEnabled(self.sp_dlGPUpt.value() == 0)
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def gpuDevicesChanged(self):
        self.w_dlGPUpt.setEnabled(self.le_dlGPUdevices.text() == "")
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def curOverrideLayer(self):
        return self.cb_renderLayer.currentText()


    @err_catcher(name=__name__)
    def refreshPasses(self, index=None):
        renderlayer = self.curOverrideLayer()

        self.core.appPlugin.sm_render_refreshPasses(self, renderlayer)


    @err_catcher(name=__name__)
    def showPasses(self):
        curRenderLayer = self.curOverrideLayer()
        renderLayers =  self.getRenderLayers("all")

        steps = getattr(
            self.core.appPlugin, "sm_render_getRenderPasses", lambda x: None
            )(self, curRenderLayer)

        if steps is None or len(steps) == 0:
            return False

        if self.core.isStr(steps):
            steps = eval(steps)

        if eval(os.getenv("PRISM_DEBUG", "False")):
            try:
                del sys.modules["ItemList"]
            except:
                pass

        import ItemList

        self.il = ItemList.ItemList(core=self.core)
        self.il.setWindowTitle("Select Passes")
        self.core.parentWindow(self.il)
        self.il.tw_steps.doubleClicked.connect(self.il.accept)
        self.il.tw_steps.horizontalHeaderItem(0).setText("Name")
        self.il.tw_steps.setColumnHidden(1, True)
        for i in sorted(steps, key=lambda s: s.lower()):
            rc = self.il.tw_steps.rowCount()
            self.il.tw_steps.insertRow(rc)
            item1 = QTableWidgetItem(i)
            self.il.tw_steps.setItem(rc, 0, item1)

        result = self.il.exec_()

        if result != 1:
            return False

        if self.chb_overrideLayers.isChecked():

            for i in self.il.tw_steps.selectedItems():
                if i.column() == 0:
                    self.core.appPlugin.sm_render_addRenderPass(
                        self, passName=i.text(), steps=steps, renderLayer=curRenderLayer
                    )
        else:
            for layer in renderLayers:

                for i in self.il.tw_steps.selectedItems():
                    if i.column() == 0:
                        self.core.appPlugin.sm_render_addRenderPass(
                            self, passName=i.text(), steps=steps, renderLayer=layer)



        self.updateUi()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def rclickPasses(self, pos):
        if self.lw_passes.currentItem() is None or not getattr(
            self.core.appPlugin, "canDeleteRenderPasses", True
            ):
            return

        rcmenu = QMenu()

        delAct = QAction("Delete", self)
        delAct.triggered.connect(self.deleteAOVs)
        rcmenu.addAction(delAct)

        rcmenu.exec_(QCursor.pos())


    @err_catcher(name=__name__)
    def deleteAOVs(self):
        renderLayer = self.curOverrideLayer()
        renderLayers = self.getRenderLayers("all")

        if self.chb_overrideLayers.isChecked():

            items = self.lw_passes.selectedItems()
            for i in items:
                self.core.appPlugin.removeAOV(i.text(), renderLayer)

        else:
            for layer in renderLayers:
                items = self.lw_passes.selectedItems()
                for i in items:
                    self.core.appPlugin.removeAOV(i.text(), layer)
                    
        self.updateUi()


    @err_catcher(name=__name__)
    def rjToggled(self, checked):
        self.refreshSubmitUi()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def managerChanged(self, text=None):
        if getattr(self.cb_manager, "prevManager", None):
            self.cb_manager.prevManager.unsetManager(self)

        plugin = self.core.plugins.getRenderfarmPlugin(self.cb_manager.currentText())
        if plugin:
            plugin.sm_render_managerChanged(self)

        self.cb_manager.prevManager = plugin
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def getContextStrFromEntity(self, entity):
        if not entity:
            return ""

        entityType = entity.get("type", "")
        if entityType == "asset":
            entityName = entity.get("asset_path").replace("\\", "/")
        elif entityType == "shot":
            entityName = self.core.entities.getShotName(entity)
        else:
            return ""

        context = "%s - %s" % (entityType.capitalize(), entityName)
        return context


    @err_catcher(name=__name__)
    def preExecuteState(self):
        warnings = []

        self.updateUi()

        if self.tasknameRequired and not self.getTaskname():
            warnings.append(["No identifier is given.", "", 3])

        if self.curCam is None or (
            self.curCam != "Current View"
            and not self.core.appPlugin.isNodeValid(self, self.curCam)
            ):
            warnings.append(["No camera is selected.", "", 3])
        elif self.curCam == "Current View":
            warnings.append(["No camera is selected.", "", 2])

        rangeType = self.cb_rangeType.currentText()
        frames = self.getFrameRange(rangeType)

        if rangeType not in ["Expression", "FML", "FMMML"]:
            frames = frames[0]

        if frames is None or frames == []:
            warnings.append(["Framerange is invalid.", "", 3])

        if not self.gb_submit.isHidden() and self.gb_submit.isChecked():
            plugin = self.core.plugins.getRenderfarmPlugin(self.cb_manager.currentText())
            warnings += plugin.sm_render_preExecute(self)

        warnings += self.core.appPlugin.sm_render_preExecute(self)

        return [self.state.text(0), warnings]


    @err_catcher(name=__name__)
    def getOutputName(self, useVersion="next"):
        if self.tasknameRequired and not self.getTaskname():
            return

        task = self.getTaskname()
        extension = self.cb_format.currentText()
        context = self.getCurrentContext()
        framePadding = ""

        if "type" not in context:
            return

        singleFrame = self.cb_rangeType.currentText() == "Single Frame"
        location = self.cb_outPath.currentText()
        outputPathData = self.core.mediaProducts.generateMediaProductPath(
            entity=context,
            task=task,
            extension=extension,
            framePadding=framePadding,
            comment=self.stateManager.publishComment,
            version=useVersion if useVersion != "next" else None,
            location=location,
            singleFrame=singleFrame,
            returnDetails=True,
            mediaType=self.mediaType,
            )

        outputFolder = os.path.dirname(outputPathData["path"])
        hVersion = outputPathData["version"]

        return outputPathData["path"], outputFolder, hVersion


    @err_catcher(name=__name__)
    def executeState(self, parent, useVersion="next"):
        rangeType = self.cb_rangeType.currentText()
        frames = self.getFrameRange(rangeType)

        if rangeType not in ["Expression", "FML", "FMMML"]:
            startFrame = frames[0]
            endFrame = frames[1]
        else:
            startFrame = None
            endFrame = None

        if frames is None or frames == [] or frames[0] is None:
            return [self.state.text(0) + ": error - Framerange is invalid"]

        if rangeType == "Single Frame":
            endFrame = startFrame

        updateMaster = True
        fileName = self.core.getCurrentFileName()
        context = self.getCurrentContext()
        if not self.renderingStarted:
            if self.tasknameRequired and not self.getTaskname():
                return [
                    self.state.text(0)
                    + ": error - no identifier is given. Skipped the activation of this state."
                ]

            if self.curCam is None or (
                self.curCam != "Current View"
                and not self.core.appPlugin.isNodeValid(self, self.curCam)
            ):
                return [
                    self.state.text(0)
                    + ": error - no camera is selected. Skipping activation of this state."
                ]

            outputName, outputPath, hVersion = self.getOutputName(useVersion=useVersion)

            outLength = len(outputName)
            if platform.system() == "Windows" and os.getenv("PRISM_IGNORE_PATH_LENGTH") != "1" and outLength > 255:
                return [
                    self.state.text(0)
                    + " - error - The outputpath is longer than 255 characters (%s), which is not supported on Windows. Please shorten the outputpath by changing the comment, taskname or projectpath."
                    % outLength
                ]

            if not os.path.exists(os.path.dirname(outputPath)):
                os.makedirs(os.path.dirname(outputPath))

            details = context.copy()
            if "filename" in details:
                del details["filename"]

            if "extension" in details:
                del details["extension"]

            details["version"] = hVersion
            details["sourceScene"] = fileName
            details["identifier"] = self.getTaskname()
            details["comment"] = self.stateManager.publishComment

            if self.mediaType == "3drenders":
                infopath = os.path.dirname(outputPath)
            else:
                infopath = outputPath

            self.core.saveVersionInfo(
                filepath=infopath, details=details
            )

            aovName = self.currentAOVname()        

            passList = []

            # Iterate through each item in the QListWidget
            for row in range(self.lw_passes.count()):
                passItem = self.lw_passes.item(row)
                if passItem is not None:
                    passList.append(passItem.text())                       

            self.l_pathLast.setText(outputName)
            self.l_pathLast.setToolTip(outputName)
            self.stateManager.saveStatesToScene()

            rSettings = {
                "aovName": aovName,                                         
                "outputName": outputName,
                "startFrame": startFrame,
                "endFrame": endFrame,
                "frames": frames,
                "rangeType": rangeType,
                "overrideLayers": self.chb_overrideLayers.isChecked(),      
                "renderLayer": self.cb_renderLayer.currentText(),           
                "renderSamples": self.e_samples.text(),                     
                "imageFormat": self.cb_format.currentText(),                
                "exrCodec": self.cb_exrCodec.currentText(),                 
                "exrBitDepth": self.cb_exrBitDepth.currentText(),           
                "pngBitDepth": self.cb_pngBitDepth.currentText(),           
                "pngCompress": self.sp_pngCompress.value(),                 
                "jpegQual": self.sp_jpegQual.value(),                       
                "useAlpha": self.chb_alpha.isChecked(),                     
                "useComp": self.chb_compositor.isChecked(),                 
                "persData": self.chb_persData.isChecked(),
                "ovrColorspace": self.chb_colorSpace.isChecked(),
                "colorSpace": self.cb_colorSpace.currentText(),
                "aovPasses": passList                   
                }

            if (
                self.chb_renderPreset.isChecked()
                and "RenderSettings" in self.stateManager.stateTypes
                ):
                rSettings["renderSettings"] = getattr(
                    self.core.appPlugin,
                    "sm_renderSettings_getCurrentSettings",
                    lambda x: {},
                    )(self)
                self.stateManager.stateTypes["RenderSettings"].applyPreset(
                    self.core, self.renderPresets[self.cb_renderPreset.currentText()]
                    )

            self.core.appPlugin.sm_render_preSubmit(self, rSettings)

            kwargs = {
                "state": self,
                "scenefile": fileName,
                "settings": rSettings,
                }

            result = self.core.callback("preRender", **kwargs)
            for res in result:
                if isinstance(res, dict) and res.get("cancel", False):
                    return [
                        self.state.text(0)
                        + " - error - %s" % res.get("details", "preRender hook returned False")
                        ]

            if not os.path.exists(os.path.dirname(rSettings["outputName"])):
                os.makedirs(os.path.dirname(rSettings["outputName"]))

            self.core.saveScene(versionUp=False, prismReq=False)

            if not self.gb_submit.isHidden() and self.gb_submit.isChecked():
                handleMaster = "media" if self.isUsingMasterVersion() else False
                farmPlugin = self.core.plugins.getRenderfarmPlugin(self.cb_manager.currentText())
                if hasattr(self, "chb_redshift") and self.chb_redshift.isChecked() and not self.w_redshift.isHidden():
                    sceneDescription = "redshift"
                else:
                    sceneDescription = None

                result = farmPlugin.sm_render_submitJob(
                    self,
                    rSettings["outputName"],
                    parent,
                    handleMaster=handleMaster,
                    details=details,
                    sceneDescription=sceneDescription
                    )
                updateMaster = False
            else:
                result = self.core.appPlugin.sm_render_startLocalRender(
                    self, rSettings["outputName"], rSettings
                    )
        else:
            rSettings = self.LastRSettings
            result = self.core.appPlugin.sm_render_startLocalRender(
                self, rSettings["outputName"], rSettings
                )
            outputName = rSettings["outputName"]

        if not self.renderingStarted:
            self.core.appPlugin.sm_render_undoRenderSettings(self, rSettings)
            self.core.saveScene(versionUp=False, prismReq=False)                        

        if result == "publish paused":
            return [self.state.text(0) + " - publish paused"]
        else:
            if updateMaster:
                self.handleMasterVersion(outputName)

            kwargs = {
                "state": self,
                "scenefile": fileName,
                "settings": rSettings,
                "result": result,
                }

            self.core.callback("postRender", **kwargs)

            if "Result=Success" in result:
                return [self.state.text(0) + " - success"]
            else:
                erStr = "%s ERROR - sm_BlenderRenderPublish %s:\n%s" % (
                    time.strftime("%d/%m/%y %X"),
                    self.core.version,
                    result,
                    )
                if not result.startswith("Execute Canceled: "):
                    if result == "unknown error (files do not exist)":
                        QMessageBox.warning(
                            self.core.messageParent,
                            "Warning",
                            "No files were created during the rendering. If you think this is a Prism bug please report it in the forum:\nwww.prism-pipeline.com/forum/\nor write a mail to contact@prism-pipeline.com",
                            )
                    else:
                        self.core.writeErrorLog(erStr)
                return [self.state.text(0) + " - error - " + result]


    @err_catcher(name=__name__)
    def isUsingMasterVersion(self):
        useMaster = self.core.mediaProducts.getUseMaster()
        if not useMaster:
            return False

        masterAction = self.cb_master.currentText()
        if masterAction == "Don't update master":
            return False

        return True


    @err_catcher(name=__name__)
    def handleMasterVersion(self, outputName):
        if not self.isUsingMasterVersion():
            return

        masterAction = self.cb_master.currentText()
        if masterAction == "Set as master":
            self.core.mediaProducts.updateMasterVersion(outputName)
        elif masterAction == "Add to master":
            self.core.mediaProducts.addToMasterVersion(outputName)


    @err_catcher(name=__name__)
    def setTaskWarn(self, warn):
        useSS = getattr(self.core.appPlugin, "colorButtonWithStyleSheet", False)
        if warn:
            if useSS:
                self.b_changeTask.setStyleSheet(
                    "QPushButton { background-color: rgb(200,0,0); }"
                )
            else:
                self.b_changeTask.setPalette(self.warnPalette)
        else:
            if useSS:
                self.b_changeTask.setStyleSheet("")
            else:
                self.b_changeTask.setPalette(self.oldPalette)


    @err_catcher(name=__name__)
    def getStateProps(self):

        stateProps = {
            "stateName": self.e_name.text(),
            "contextType": self.getContextType(),
            "customContext": self.customContext,
            "useCustomAOV": self.chb_customAOV.isChecked(),
            "aovNameCustom": self.e_aovNameCustom.text(),
            "taskname": self.getTaskname(),
            "rezScale": str(self.cb_scaling.currentText()),                     
            "renderpresetoverride": str(self.chb_renderPreset.isChecked()),
            "currentrenderpreset": self.cb_renderPreset.currentText(),
            "rangeType": str(self.cb_rangeType.currentText()),
            "startframe": self.sp_rangeStart.value(),
            "endframe": self.sp_rangeEnd.value(),
            "frameExpression": self.le_frameExpression.text(),
            "currentcam": str(self.curCam),
            "resoverride": str(
                [
                    self.chb_resOverride.isChecked(),
                    self.sp_resWidth.value(),
                    self.sp_resHeight.value(),
                ]
                ),
            "masterVersion": self.cb_master.currentText(),
            "renderSamples": self.e_samples.text(),                             
            "curoutputpath": self.cb_outPath.currentText(),
            "overrideLayers": self.chb_overrideLayers.isChecked(),              
            "renderlayer": str(self.cb_renderLayer.currentText()),
            "useComp": self.chb_compositor.isChecked(),                         
            "persData": self.chb_persData.isChecked(),                          
            "outputFormat": str(self.cb_format.currentText()),
            "codec": self.cb_exrCodec.currentText(),                            
            "exrBitDepth": self.cb_exrBitDepth.currentText(),                   
            "pngBitDepth": self.cb_pngBitDepth.currentText(),                   
            "pngComp": self.sp_pngCompress.value(),                             
            "jpegQual": self.sp_jpegQual.value(),                               
            "useAlpha": self.chb_alpha.isChecked(),
            "ovrColorSpace": self.chb_colorSpace.isChecked(),
            "currColorSpace": self.cb_colorSpace.currentText(),
            "submitrender": str(self.gb_submit.isChecked()),
            "rjmanager": str(self.cb_manager.currentText()),
            "rjprio": self.sp_rjPrio.value(),
            "rjframespertask": self.sp_rjFramesPerTask.value(),
            "rjtimeout": self.sp_rjTimeout.value(),
            "rjsuspended": str(self.chb_rjSuspended.isChecked()),
            "osdependencies": str(self.chb_osDependencies.isChecked()),
            "osupload": str(self.chb_osUpload.isChecked()),
            "ospassets": str(self.chb_osPAssets.isChecked()),
            "osslaves": self.e_osSlaves.text(),
            "dlconcurrent": self.sp_dlConcurrentTasks.value(),
            "dlgpupt": self.sp_dlGPUpt.value(),
            "dlgpudevices": self.le_dlGPUdevices.text(),
            "lastexportpath": self.l_pathLast.text().replace("\\", "/"),
            "enablepasses": str(self.gb_passes.isChecked()),
            "stateenabled": self.core.getCheckStateValue(self.state.checkState(0)),
            }
        self.core.callback("onStateGetSettings", self, stateProps)
        return stateProps
