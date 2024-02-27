# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BlenderRenderhqdkzs.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_wg_BlenderRender(object):
    def setupUi(self, wg_BlenderRender):
        if not wg_BlenderRender.objectName():
            wg_BlenderRender.setObjectName(u"wg_BlenderRender")
        wg_BlenderRender.resize(505, 1184)
        self.verticalLayout = QVBoxLayout(wg_BlenderRender)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.f_name = QWidget(wg_BlenderRender)
        self.f_name.setObjectName(u"f_name")
        self.horizontalLayout_4 = QHBoxLayout(self.f_name)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(9, 0, 18, 0)
        self.l_name = QLabel(self.f_name)
        self.l_name.setObjectName(u"l_name")

        self.horizontalLayout_4.addWidget(self.l_name)

        self.e_name = QLineEdit(self.f_name)
        self.e_name.setObjectName(u"e_name")

        self.horizontalLayout_4.addWidget(self.e_name)

        self.l_class = QLabel(self.f_name)
        self.l_class.setObjectName(u"l_class")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_class.setFont(font)

        self.horizontalLayout_4.addWidget(self.l_class)


        self.verticalLayout.addWidget(self.f_name)

        self.gb_BlenderRender = QGroupBox(wg_BlenderRender)
        self.gb_BlenderRender.setObjectName(u"gb_BlenderRender")
        self.verticalLayout_2 = QVBoxLayout(self.gb_BlenderRender)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.f_AOV = QHBoxLayout()
        self.f_AOV.setObjectName(u"f_AOV")
        self.f_AOV.setContentsMargins(9, -1, 9, -1)
        self.l_AOV = QLabel(self.gb_BlenderRender)
        self.l_AOV.setObjectName(u"l_AOV")

        self.f_AOV.addWidget(self.l_AOV)

        self.e_aovNameCustom = QLineEdit(self.gb_BlenderRender)
        self.e_aovNameCustom.setObjectName(u"e_aovNameCustom")

        self.f_AOV.addWidget(self.e_aovNameCustom)

        self.e_aovNameAuto = QLineEdit(self.gb_BlenderRender)
        self.e_aovNameAuto.setObjectName(u"e_aovNameAuto")
        self.e_aovNameAuto.setReadOnly(True)

        self.f_AOV.addWidget(self.e_aovNameAuto)

        self.chb_customAOV = QCheckBox(self.gb_BlenderRender)
        self.chb_customAOV.setObjectName(u"chb_customAOV")

        self.f_AOV.addWidget(self.chb_customAOV)


        self.verticalLayout_2.addLayout(self.f_AOV)

        self.w_context = QWidget(self.gb_BlenderRender)
        self.w_context.setObjectName(u"w_context")
        self.horizontalLayout_11 = QHBoxLayout(self.w_context)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(9, 0, 9, 0)
        self.label_7 = QLabel(self.w_context)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_11.addWidget(self.label_7)

        self.horizontalSpacer_5 = QSpacerItem(37, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)

        self.l_context = QLabel(self.w_context)
        self.l_context.setObjectName(u"l_context")

        self.horizontalLayout_11.addWidget(self.l_context)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_3)

        self.b_context = QPushButton(self.w_context)
        self.b_context.setObjectName(u"b_context")

        self.horizontalLayout_11.addWidget(self.b_context)

        self.cb_context = QComboBox(self.w_context)
        self.cb_context.setObjectName(u"cb_context")

        self.horizontalLayout_11.addWidget(self.cb_context)


        self.verticalLayout_2.addWidget(self.w_context)

        self.f_taskname = QWidget(self.gb_BlenderRender)
        self.f_taskname.setObjectName(u"f_taskname")
        self.horizontalLayout_10 = QHBoxLayout(self.f_taskname)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(9, 0, 9, 0)
        self.label_2 = QLabel(self.f_taskname)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_10.addWidget(self.label_2)

        self.l_taskName = QLineEdit(self.f_taskname)
        self.l_taskName.setObjectName(u"l_taskName")

        self.horizontalLayout_10.addWidget(self.l_taskName)

        self.b_changeTask = QPushButton(self.f_taskname)
        self.b_changeTask.setObjectName(u"b_changeTask")
        self.b_changeTask.setEnabled(True)
        self.b_changeTask.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_10.addWidget(self.b_changeTask)


        self.verticalLayout_2.addWidget(self.f_taskname)

        self.f_range = QWidget(self.gb_BlenderRender)
        self.f_range.setObjectName(u"f_range")
        self.horizontalLayout = QHBoxLayout(self.f_range)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.label_3 = QLabel(self.f_range)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.cb_rangeType = QComboBox(self.f_range)
        self.cb_rangeType.setObjectName(u"cb_rangeType")
        self.cb_rangeType.setMinimumSize(QSize(150, 0))

        self.horizontalLayout.addWidget(self.cb_rangeType)


        self.verticalLayout_2.addWidget(self.f_range)

        self.w_frameRangeValues = QWidget(self.gb_BlenderRender)
        self.w_frameRangeValues.setObjectName(u"w_frameRangeValues")
        self.gridLayout = QGridLayout(self.w_frameRangeValues)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 0, 9, 0)
        self.l_rangeStart = QLabel(self.w_frameRangeValues)
        self.l_rangeStart.setObjectName(u"l_rangeStart")
        self.l_rangeStart.setMinimumSize(QSize(30, 0))
        self.l_rangeStart.setFrameShape(QFrame.NoFrame)
        self.l_rangeStart.setFrameShadow(QFrame.Plain)
        self.l_rangeStart.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.l_rangeStart, 0, 5, 1, 1)

        self.sp_rangeStart = QSpinBox(self.w_frameRangeValues)
        self.sp_rangeStart.setObjectName(u"sp_rangeStart")
        self.sp_rangeStart.setMaximumSize(QSize(55, 16777215))
        self.sp_rangeStart.setMaximum(99999)
        self.sp_rangeStart.setValue(1001)

        self.gridLayout.addWidget(self.sp_rangeStart, 0, 6, 1, 1)

        self.horizontalSpacer_44 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_44, 0, 13, 1, 1)

        self.l_rangeEndInfo = QLabel(self.w_frameRangeValues)
        self.l_rangeEndInfo.setObjectName(u"l_rangeEndInfo")

        self.gridLayout.addWidget(self.l_rangeEndInfo, 0, 8, 1, 1)

        self.sp_rangeEnd = QSpinBox(self.w_frameRangeValues)
        self.sp_rangeEnd.setObjectName(u"sp_rangeEnd")
        self.sp_rangeEnd.setMaximumSize(QSize(55, 16777215))
        self.sp_rangeEnd.setMaximum(99999)
        self.sp_rangeEnd.setValue(1100)

        self.gridLayout.addWidget(self.sp_rangeEnd, 0, 10, 1, 1)

        self.horizontalSpacer_43 = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_43, 0, 0, 1, 1)

        self.l_rangeEnd = QLabel(self.w_frameRangeValues)
        self.l_rangeEnd.setObjectName(u"l_rangeEnd")
        self.l_rangeEnd.setMinimumSize(QSize(30, 0))
        self.l_rangeEnd.setFrameShape(QFrame.NoFrame)
        self.l_rangeEnd.setFrameShadow(QFrame.Plain)
        self.l_rangeEnd.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.l_rangeEnd, 0, 9, 1, 1)

        self.l_rangeStartInfo = QLabel(self.w_frameRangeValues)
        self.l_rangeStartInfo.setObjectName(u"l_rangeStartInfo")

        self.gridLayout.addWidget(self.l_rangeStartInfo, 0, 1, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_13, 0, 7, 1, 1)


        self.verticalLayout_2.addWidget(self.w_frameRangeValues)

        self.w_fml = QFrame(self.gb_BlenderRender)
        self.w_fml.setObjectName(u"w_fml")
        self.f_fml = QHBoxLayout(self.w_fml)
        self.f_fml.setObjectName(u"f_fml")
        self.f_fml.setContentsMargins(9, 0, 9, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_fml.addItem(self.horizontalSpacer_4)

        self.l_fml = QLabel(self.w_fml)
        self.l_fml.setObjectName(u"l_fml")

        self.f_fml.addWidget(self.l_fml)

        self.e_fml = QLineEdit(self.w_fml)
        self.e_fml.setObjectName(u"e_fml")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.e_fml.sizePolicy().hasHeightForWidth())
        self.e_fml.setSizePolicy(sizePolicy)
        self.e_fml.setMinimumSize(QSize(200, 0))
        self.e_fml.setMaximumSize(QSize(500, 16777215))
        self.e_fml.setReadOnly(True)

        self.f_fml.addWidget(self.e_fml)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_fml.addItem(self.horizontalSpacer_10)


        self.verticalLayout_2.addWidget(self.w_fml)

        self.w_frameExpression = QWidget(self.gb_BlenderRender)
        self.w_frameExpression.setObjectName(u"w_frameExpression")
        self.horizontalLayout_15 = QHBoxLayout(self.w_frameExpression)
        self.horizontalLayout_15.setSpacing(6)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(9, 0, 9, 0)
        self.l_frameExpression = QLabel(self.w_frameExpression)
        self.l_frameExpression.setObjectName(u"l_frameExpression")

        self.horizontalLayout_15.addWidget(self.l_frameExpression)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_14)

        self.le_frameExpression = QLineEdit(self.w_frameExpression)
        self.le_frameExpression.setObjectName(u"le_frameExpression")
        self.le_frameExpression.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_15.addWidget(self.le_frameExpression)


        self.verticalLayout_2.addWidget(self.w_frameExpression)

        self.f_cam = QWidget(self.gb_BlenderRender)
        self.f_cam.setObjectName(u"f_cam")
        self.horizontalLayout_2 = QHBoxLayout(self.f_cam)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.label = QLabel(self.f_cam)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(60, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.cb_cam = QComboBox(self.f_cam)
        self.cb_cam.setObjectName(u"cb_cam")
        self.cb_cam.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_2.addWidget(self.cb_cam)


        self.verticalLayout_2.addWidget(self.f_cam)

        self.f_resScaling = QWidget(self.gb_BlenderRender)
        self.f_resScaling.setObjectName(u"f_resScaling")
        self.horizontalLayout_38 = QHBoxLayout(self.f_resScaling)
        self.horizontalLayout_38.setSpacing(6)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(9, 0, 9, 0)
        self.l_scaling = QLabel(self.f_resScaling)
        self.l_scaling.setObjectName(u"l_scaling")
        self.l_scaling.setEnabled(True)

        self.horizontalLayout_38.addWidget(self.l_scaling)

        self.cb_scaling = QComboBox(self.f_resScaling)
        self.cb_scaling.setObjectName(u"cb_scaling")

        self.horizontalLayout_38.addWidget(self.cb_scaling)

        self.horizontalSpacer_39 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_39)

        self.e_xRez = QLineEdit(self.f_resScaling)
        self.e_xRez.setObjectName(u"e_xRez")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.e_xRez.sizePolicy().hasHeightForWidth())
        self.e_xRez.setSizePolicy(sizePolicy1)
        self.e_xRez.setMinimumSize(QSize(50, 0))
        self.e_xRez.setFocusPolicy(Qt.NoFocus)
        self.e_xRez.setAcceptDrops(False)
        self.e_xRez.setAlignment(Qt.AlignCenter)
        self.e_xRez.setReadOnly(True)

        self.horizontalLayout_38.addWidget(self.e_xRez)

        self.l_Xtext = QLabel(self.f_resScaling)
        self.l_Xtext.setObjectName(u"l_Xtext")

        self.horizontalLayout_38.addWidget(self.l_Xtext)

        self.e_yRez = QLineEdit(self.f_resScaling)
        self.e_yRez.setObjectName(u"e_yRez")
        sizePolicy1.setHeightForWidth(self.e_yRez.sizePolicy().hasHeightForWidth())
        self.e_yRez.setSizePolicy(sizePolicy1)
        self.e_yRez.setMinimumSize(QSize(50, 0))
        self.e_yRez.setFocusPolicy(Qt.NoFocus)
        self.e_yRez.setAcceptDrops(False)
        self.e_yRez.setAlignment(Qt.AlignCenter)
        self.e_yRez.setReadOnly(True)

        self.horizontalLayout_38.addWidget(self.e_yRez)


        self.verticalLayout_2.addWidget(self.f_resScaling)

        self.f_resolution = QWidget(self.gb_BlenderRender)
        self.f_resolution.setObjectName(u"f_resolution")
        self.horizontalLayout_9 = QHBoxLayout(self.f_resolution)
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(9, 0, 9, 0)
        self.label_4 = QLabel(self.f_resolution)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(True)

        self.horizontalLayout_9.addWidget(self.label_4)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)

        self.chb_resOverride = QCheckBox(self.f_resolution)
        self.chb_resOverride.setObjectName(u"chb_resOverride")

        self.horizontalLayout_9.addWidget(self.chb_resOverride)

        self.sp_resWidth = QSpinBox(self.f_resolution)
        self.sp_resWidth.setObjectName(u"sp_resWidth")
        self.sp_resWidth.setEnabled(False)
        self.sp_resWidth.setMinimum(1)
        self.sp_resWidth.setMaximum(99999)
        self.sp_resWidth.setValue(1280)

        self.horizontalLayout_9.addWidget(self.sp_resWidth)

        self.sp_resHeight = QSpinBox(self.f_resolution)
        self.sp_resHeight.setObjectName(u"sp_resHeight")
        self.sp_resHeight.setEnabled(False)
        self.sp_resHeight.setMinimum(1)
        self.sp_resHeight.setMaximum(99999)
        self.sp_resHeight.setValue(720)

        self.horizontalLayout_9.addWidget(self.sp_resHeight)

        self.b_resPresets = QPushButton(self.f_resolution)
        self.b_resPresets.setObjectName(u"b_resPresets")
        self.b_resPresets.setEnabled(False)
        self.b_resPresets.setMinimumSize(QSize(23, 23))
        self.b_resPresets.setMaximumSize(QSize(23, 23))
        self.b_resPresets.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_9.addWidget(self.b_resPresets)


        self.verticalLayout_2.addWidget(self.f_resolution)

        self.w_renderPreset = QWidget(self.gb_BlenderRender)
        self.w_renderPreset.setObjectName(u"w_renderPreset")
        self.horizontalLayout_14 = QHBoxLayout(self.w_renderPreset)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, -1, 0)
        self.l_renderPreset = QLabel(self.w_renderPreset)
        self.l_renderPreset.setObjectName(u"l_renderPreset")

        self.horizontalLayout_14.addWidget(self.l_renderPreset)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_7)

        self.chb_renderPreset = QCheckBox(self.w_renderPreset)
        self.chb_renderPreset.setObjectName(u"chb_renderPreset")

        self.horizontalLayout_14.addWidget(self.chb_renderPreset)

        self.cb_renderPreset = QComboBox(self.w_renderPreset)
        self.cb_renderPreset.setObjectName(u"cb_renderPreset")
        self.cb_renderPreset.setEnabled(False)
        self.cb_renderPreset.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_14.addWidget(self.cb_renderPreset)


        self.verticalLayout_2.addWidget(self.w_renderPreset)

        self.w_master = QWidget(self.gb_BlenderRender)
        self.w_master.setObjectName(u"w_master")
        self.horizontalLayout_17 = QHBoxLayout(self.w_master)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(9, 0, 9, 0)
        self.l_outPath_2 = QLabel(self.w_master)
        self.l_outPath_2.setObjectName(u"l_outPath_2")

        self.horizontalLayout_17.addWidget(self.l_outPath_2)

        self.horizontalSpacer_28 = QSpacerItem(113, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_28)

        self.cb_master = QComboBox(self.w_master)
        self.cb_master.setObjectName(u"cb_master")
        self.cb_master.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_17.addWidget(self.cb_master)


        self.verticalLayout_2.addWidget(self.w_master)

        self.f_renderLayer = QWidget(self.gb_BlenderRender)
        self.f_renderLayer.setObjectName(u"f_renderLayer")
        self.horizontalLayout_5 = QHBoxLayout(self.f_renderLayer)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(9, 0, 9, 0)
        self.label_5 = QLabel(self.f_renderLayer)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.chb_overrideLayers = QCheckBox(self.f_renderLayer)
        self.chb_overrideLayers.setObjectName(u"chb_overrideLayers")
        self.chb_overrideLayers.setChecked(True)

        self.horizontalLayout_5.addWidget(self.chb_overrideLayers)

        self.cb_renderLayer = QComboBox(self.f_renderLayer)
        self.cb_renderLayer.setObjectName(u"cb_renderLayer")
        self.cb_renderLayer.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cb_renderLayer.sizePolicy().hasHeightForWidth())
        self.cb_renderLayer.setSizePolicy(sizePolicy2)
        self.cb_renderLayer.setMinimumSize(QSize(250, 0))

        self.horizontalLayout_5.addWidget(self.cb_renderLayer)


        self.verticalLayout_2.addWidget(self.f_renderLayer)

        self.w_outPath = QWidget(self.gb_BlenderRender)
        self.w_outPath.setObjectName(u"w_outPath")
        self.horizontalLayout_16 = QHBoxLayout(self.w_outPath)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(9, 0, 9, 0)
        self.l_samples = QLabel(self.w_outPath)
        self.l_samples.setObjectName(u"l_samples")

        self.horizontalLayout_16.addWidget(self.l_samples)

        self.e_samples = QLineEdit(self.w_outPath)
        self.e_samples.setObjectName(u"e_samples")
        sizePolicy1.setHeightForWidth(self.e_samples.sizePolicy().hasHeightForWidth())
        self.e_samples.setSizePolicy(sizePolicy1)
        self.e_samples.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_16.addWidget(self.e_samples)

        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_27)

        self.l_outPath = QLabel(self.w_outPath)
        self.l_outPath.setObjectName(u"l_outPath")

        self.horizontalLayout_16.addWidget(self.l_outPath)

        self.cb_outPath = QComboBox(self.w_outPath)
        self.cb_outPath.setObjectName(u"cb_outPath")
        self.cb_outPath.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_16.addWidget(self.cb_outPath)


        self.verticalLayout_2.addWidget(self.w_outPath)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.f_midPanelUpr = QHBoxLayout()
        self.f_midPanelUpr.setObjectName(u"f_midPanelUpr")
        self.f_midPanelUpr.setContentsMargins(9, -1, -1, -1)
        self.f_midUprLt = QVBoxLayout()
        self.f_midUprLt.setObjectName(u"f_midUprLt")
        self.f_midUprLt.setContentsMargins(-1, -1, 30, -1)
        self.f_midUprLt_2 = QHBoxLayout()
        self.f_midUprLt_2.setObjectName(u"f_midUprLt_2")
        self.l_format = QLabel(self.gb_BlenderRender)
        self.l_format.setObjectName(u"l_format")

        self.f_midUprLt_2.addWidget(self.l_format)

        self.cb_format = QComboBox(self.gb_BlenderRender)
        self.cb_format.setObjectName(u"cb_format")
        self.cb_format.setMinimumSize(QSize(50, 0))

        self.f_midUprLt_2.addWidget(self.cb_format)


        self.f_midUprLt.addLayout(self.f_midUprLt_2)


        self.f_midPanelUpr.addLayout(self.f_midUprLt)

        self.f_midUprRt = QVBoxLayout()
        self.f_midUprRt.setObjectName(u"f_midUprRt")
        self.f_midUprRt_2 = QHBoxLayout()
        self.f_midUprRt_2.setObjectName(u"f_midUprRt_2")
        self.chb_compositor = QCheckBox(self.gb_BlenderRender)
        self.chb_compositor.setObjectName(u"chb_compositor")
        self.chb_compositor.setLayoutDirection(Qt.RightToLeft)

        self.f_midUprRt_2.addWidget(self.chb_compositor)

        self.horizontalSpacer_41 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_midUprRt_2.addItem(self.horizontalSpacer_41)


        self.f_midUprRt.addLayout(self.f_midUprRt_2)


        self.f_midPanelUpr.addLayout(self.f_midUprRt)


        self.verticalLayout_2.addLayout(self.f_midPanelUpr)

        self.f_midPanelMid = QHBoxLayout()
        self.f_midPanelMid.setObjectName(u"f_midPanelMid")
        self.f_midPanelMid.setContentsMargins(9, -1, -1, -1)
        self.f_midMidLt = QVBoxLayout()
        self.f_midMidLt.setObjectName(u"f_midMidLt")
        self.f_midMidLt_2 = QHBoxLayout()
        self.f_midMidLt_2.setObjectName(u"f_midMidLt_2")
        self.f_midMidLt_2.setContentsMargins(-1, -1, 30, -1)
        self.l_fileCompress = QLabel(self.gb_BlenderRender)
        self.l_fileCompress.setObjectName(u"l_fileCompress")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.l_fileCompress.sizePolicy().hasHeightForWidth())
        self.l_fileCompress.setSizePolicy(sizePolicy3)
        self.l_fileCompress.setMinimumSize(QSize(40, 0))

        self.f_midMidLt_2.addWidget(self.l_fileCompress)

        self.cb_exrCodec = QComboBox(self.gb_BlenderRender)
        self.cb_exrCodec.setObjectName(u"cb_exrCodec")
        self.cb_exrCodec.setMinimumSize(QSize(50, 0))

        self.f_midMidLt_2.addWidget(self.cb_exrCodec)

        self.sp_pngCompress = QSpinBox(self.gb_BlenderRender)
        self.sp_pngCompress.setObjectName(u"sp_pngCompress")
        self.sp_pngCompress.setMaximum(100)
        self.sp_pngCompress.setSingleStep(10)
        self.sp_pngCompress.setValue(50)

        self.f_midMidLt_2.addWidget(self.sp_pngCompress)

        self.sp_jpegQual = QSpinBox(self.gb_BlenderRender)
        self.sp_jpegQual.setObjectName(u"sp_jpegQual")
        self.sp_jpegQual.setMaximum(100)
        self.sp_jpegQual.setSingleStep(10)
        self.sp_jpegQual.setValue(50)

        self.f_midMidLt_2.addWidget(self.sp_jpegQual)


        self.f_midMidLt.addLayout(self.f_midMidLt_2)


        self.f_midPanelMid.addLayout(self.f_midMidLt)

        self.f_midMidRt = QVBoxLayout()
        self.f_midMidRt.setObjectName(u"f_midMidRt")
        self.f_midMidRt_2 = QHBoxLayout()
        self.f_midMidRt_2.setObjectName(u"f_midMidRt_2")
        self.chb_persData = QCheckBox(self.gb_BlenderRender)
        self.chb_persData.setObjectName(u"chb_persData")
        self.chb_persData.setLayoutDirection(Qt.RightToLeft)

        self.f_midMidRt_2.addWidget(self.chb_persData)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_midMidRt_2.addItem(self.horizontalSpacer_15)


        self.f_midMidRt.addLayout(self.f_midMidRt_2)


        self.f_midPanelMid.addLayout(self.f_midMidRt)


        self.verticalLayout_2.addLayout(self.f_midPanelMid)

        self.f_midPanelLwr = QHBoxLayout()
        self.f_midPanelLwr.setObjectName(u"f_midPanelLwr")
        self.f_midPanelLwr.setContentsMargins(9, -1, -1, -1)
        self.f_midLwrLt = QVBoxLayout()
        self.f_midLwrLt.setObjectName(u"f_midLwrLt")
        self.f_midLwrLt_2 = QHBoxLayout()
        self.f_midLwrLt_2.setObjectName(u"f_midLwrLt_2")
        self.f_midLwrLt_2.setContentsMargins(-1, -1, 30, -1)
        self.l_bitDepth = QLabel(self.gb_BlenderRender)
        self.l_bitDepth.setObjectName(u"l_bitDepth")

        self.f_midLwrLt_2.addWidget(self.l_bitDepth)

        self.cb_exrBitDepth = QComboBox(self.gb_BlenderRender)
        self.cb_exrBitDepth.setObjectName(u"cb_exrBitDepth")
        self.cb_exrBitDepth.setMinimumSize(QSize(50, 0))

        self.f_midLwrLt_2.addWidget(self.cb_exrBitDepth)

        self.cb_pngBitDepth = QComboBox(self.gb_BlenderRender)
        self.cb_pngBitDepth.setObjectName(u"cb_pngBitDepth")
        self.cb_pngBitDepth.setMinimumSize(QSize(50, 0))

        self.f_midLwrLt_2.addWidget(self.cb_pngBitDepth)


        self.f_midLwrLt.addLayout(self.f_midLwrLt_2)


        self.f_midPanelLwr.addLayout(self.f_midLwrLt)

        self.f_midLwrRt = QVBoxLayout()
        self.f_midLwrRt.setObjectName(u"f_midLwrRt")
        self.f_midLwrRt_2 = QHBoxLayout()
        self.f_midLwrRt_2.setObjectName(u"f_midLwrRt_2")
        self.chb_alpha = QCheckBox(self.gb_BlenderRender)
        self.chb_alpha.setObjectName(u"chb_alpha")
        self.chb_alpha.setLayoutDirection(Qt.RightToLeft)

        self.f_midLwrRt_2.addWidget(self.chb_alpha)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_midLwrRt_2.addItem(self.horizontalSpacer_8)


        self.f_midLwrRt.addLayout(self.f_midLwrRt_2)


        self.f_midPanelLwr.addLayout(self.f_midLwrRt)


        self.verticalLayout_2.addLayout(self.f_midPanelLwr)


        self.verticalLayout.addWidget(self.gb_BlenderRender)

        self.gb_submit = QGroupBox(wg_BlenderRender)
        self.gb_submit.setObjectName(u"gb_submit")
        self.gb_submit.setCheckable(True)
        self.gb_submit.setChecked(True)
        self.verticalLayout_8 = QVBoxLayout(self.gb_submit)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(-1, 15, -1, -1)
        self.f_manager = QWidget(self.gb_submit)
        self.f_manager.setObjectName(u"f_manager")
        self.horizontalLayout_13 = QHBoxLayout(self.f_manager)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(9, 0, 9, 0)
        self.l_manager = QLabel(self.f_manager)
        self.l_manager.setObjectName(u"l_manager")

        self.horizontalLayout_13.addWidget(self.l_manager)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_19)

        self.cb_manager = QComboBox(self.f_manager)
        self.cb_manager.setObjectName(u"cb_manager")
        self.cb_manager.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_13.addWidget(self.cb_manager)


        self.verticalLayout_8.addWidget(self.f_manager)

        self.f_rjSuspended = QWidget(self.gb_submit)
        self.f_rjSuspended.setObjectName(u"f_rjSuspended")
        self.horizontalLayout_26 = QHBoxLayout(self.f_rjSuspended)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(9, 0, 9, 0)
        self.label_18 = QLabel(self.f_rjSuspended)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_26.addWidget(self.label_18)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_20)

        self.chb_rjSuspended = QCheckBox(self.f_rjSuspended)
        self.chb_rjSuspended.setObjectName(u"chb_rjSuspended")
        self.chb_rjSuspended.setChecked(False)

        self.horizontalLayout_26.addWidget(self.chb_rjSuspended)


        self.verticalLayout_8.addWidget(self.f_rjSuspended)

        self.f_osDependencies = QWidget(self.gb_submit)
        self.f_osDependencies.setObjectName(u"f_osDependencies")
        self.horizontalLayout_27 = QHBoxLayout(self.f_osDependencies)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(9, 0, 9, 0)
        self.label_19 = QLabel(self.f_osDependencies)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_27.addWidget(self.label_19)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_22)

        self.chb_osDependencies = QCheckBox(self.f_osDependencies)
        self.chb_osDependencies.setObjectName(u"chb_osDependencies")
        self.chb_osDependencies.setChecked(True)

        self.horizontalLayout_27.addWidget(self.chb_osDependencies)


        self.verticalLayout_8.addWidget(self.f_osDependencies)

        self.f_osUpload = QWidget(self.gb_submit)
        self.f_osUpload.setObjectName(u"f_osUpload")
        self.horizontalLayout_23 = QHBoxLayout(self.f_osUpload)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, 0, -1, 0)
        self.label_16 = QLabel(self.f_osUpload)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_23.addWidget(self.label_16)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_18)

        self.chb_osUpload = QCheckBox(self.f_osUpload)
        self.chb_osUpload.setObjectName(u"chb_osUpload")
        self.chb_osUpload.setChecked(True)

        self.horizontalLayout_23.addWidget(self.chb_osUpload)


        self.verticalLayout_8.addWidget(self.f_osUpload)

        self.f_osPAssets = QWidget(self.gb_submit)
        self.f_osPAssets.setObjectName(u"f_osPAssets")
        self.horizontalLayout_24 = QHBoxLayout(self.f_osPAssets)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, 0, -1, 0)
        self.label_17 = QLabel(self.f_osPAssets)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_24.addWidget(self.label_17)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_21)

        self.chb_osPAssets = QCheckBox(self.f_osPAssets)
        self.chb_osPAssets.setObjectName(u"chb_osPAssets")
        self.chb_osPAssets.setChecked(True)

        self.horizontalLayout_24.addWidget(self.chb_osPAssets)


        self.verticalLayout_8.addWidget(self.f_osPAssets)

        self.f_rjPrio = QWidget(self.gb_submit)
        self.f_rjPrio.setObjectName(u"f_rjPrio")
        self.horizontalLayout_21 = QHBoxLayout(self.f_rjPrio)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(9, 0, 9, 0)
        self.l_rjPrio = QLabel(self.f_rjPrio)
        self.l_rjPrio.setObjectName(u"l_rjPrio")

        self.horizontalLayout_21.addWidget(self.l_rjPrio)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_16)

        self.sp_rjPrio = QSpinBox(self.f_rjPrio)
        self.sp_rjPrio.setObjectName(u"sp_rjPrio")
        self.sp_rjPrio.setMaximum(100)
        self.sp_rjPrio.setValue(50)

        self.horizontalLayout_21.addWidget(self.sp_rjPrio)


        self.verticalLayout_8.addWidget(self.f_rjPrio)

        self.f_rjWidgetsPerTask = QWidget(self.gb_submit)
        self.f_rjWidgetsPerTask.setObjectName(u"f_rjWidgetsPerTask")
        self.horizontalLayout_22 = QHBoxLayout(self.f_rjWidgetsPerTask)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(9, 0, 9, 0)
        self.label_15 = QLabel(self.f_rjWidgetsPerTask)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_22.addWidget(self.label_15)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_17)

        self.sp_rjFramesPerTask = QSpinBox(self.f_rjWidgetsPerTask)
        self.sp_rjFramesPerTask.setObjectName(u"sp_rjFramesPerTask")
        self.sp_rjFramesPerTask.setMaximum(9999)
        self.sp_rjFramesPerTask.setValue(5)

        self.horizontalLayout_22.addWidget(self.sp_rjFramesPerTask)


        self.verticalLayout_8.addWidget(self.f_rjWidgetsPerTask)

        self.f_rjTimeout = QWidget(self.gb_submit)
        self.f_rjTimeout.setObjectName(u"f_rjTimeout")
        self.horizontalLayout_28 = QHBoxLayout(self.f_rjTimeout)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(9, 0, 9, 0)
        self.l_rjTimeout = QLabel(self.f_rjTimeout)
        self.l_rjTimeout.setObjectName(u"l_rjTimeout")

        self.horizontalLayout_28.addWidget(self.l_rjTimeout)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_23)

        self.sp_rjTimeout = QSpinBox(self.f_rjTimeout)
        self.sp_rjTimeout.setObjectName(u"sp_rjTimeout")
        self.sp_rjTimeout.setMinimum(1)
        self.sp_rjTimeout.setMaximum(9999)
        self.sp_rjTimeout.setValue(180)

        self.horizontalLayout_28.addWidget(self.sp_rjTimeout)


        self.verticalLayout_8.addWidget(self.f_rjTimeout)

        self.gb_osSlaves = QGroupBox(self.gb_submit)
        self.gb_osSlaves.setObjectName(u"gb_osSlaves")
        self.horizontalLayout_25 = QHBoxLayout(self.gb_osSlaves)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(9, 3, 9, 3)
        self.e_osSlaves = QLineEdit(self.gb_osSlaves)
        self.e_osSlaves.setObjectName(u"e_osSlaves")

        self.horizontalLayout_25.addWidget(self.e_osSlaves)

        self.b_osSlaves = QPushButton(self.gb_osSlaves)
        self.b_osSlaves.setObjectName(u"b_osSlaves")
        self.b_osSlaves.setMaximumSize(QSize(25, 16777215))
        self.b_osSlaves.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_25.addWidget(self.b_osSlaves)


        self.verticalLayout_8.addWidget(self.gb_osSlaves)

        self.w_dlConcurrentTasks = QWidget(self.gb_submit)
        self.w_dlConcurrentTasks.setObjectName(u"w_dlConcurrentTasks")
        self.horizontalLayout_29 = QHBoxLayout(self.w_dlConcurrentTasks)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(9, 0, 9, 0)
        self.l_dlConcurrentTasks = QLabel(self.w_dlConcurrentTasks)
        self.l_dlConcurrentTasks.setObjectName(u"l_dlConcurrentTasks")

        self.horizontalLayout_29.addWidget(self.l_dlConcurrentTasks)

        self.horizontalSpacer_24 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_24)

        self.sp_dlConcurrentTasks = QSpinBox(self.w_dlConcurrentTasks)
        self.sp_dlConcurrentTasks.setObjectName(u"sp_dlConcurrentTasks")
        self.sp_dlConcurrentTasks.setMinimum(1)
        self.sp_dlConcurrentTasks.setMaximum(99)
        self.sp_dlConcurrentTasks.setValue(1)

        self.horizontalLayout_29.addWidget(self.sp_dlConcurrentTasks)


        self.verticalLayout_8.addWidget(self.w_dlConcurrentTasks)

        self.w_dlGPUpt = QWidget(self.gb_submit)
        self.w_dlGPUpt.setObjectName(u"w_dlGPUpt")
        self.horizontalLayout_30 = QHBoxLayout(self.w_dlGPUpt)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(9, 0, 9, 0)
        self.l_dlGPUpt = QLabel(self.w_dlGPUpt)
        self.l_dlGPUpt.setObjectName(u"l_dlGPUpt")

        self.horizontalLayout_30.addWidget(self.l_dlGPUpt)

        self.horizontalSpacer_25 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_25)

        self.sp_dlGPUpt = QSpinBox(self.w_dlGPUpt)
        self.sp_dlGPUpt.setObjectName(u"sp_dlGPUpt")
        self.sp_dlGPUpt.setMinimum(0)
        self.sp_dlGPUpt.setMaximum(99)
        self.sp_dlGPUpt.setValue(0)

        self.horizontalLayout_30.addWidget(self.sp_dlGPUpt)


        self.verticalLayout_8.addWidget(self.w_dlGPUpt)

        self.w_dlGPUdevices = QWidget(self.gb_submit)
        self.w_dlGPUdevices.setObjectName(u"w_dlGPUdevices")
        self.horizontalLayout_31 = QHBoxLayout(self.w_dlGPUdevices)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(9, 0, 9, 0)
        self.l_dlGPUdevices = QLabel(self.w_dlGPUdevices)
        self.l_dlGPUdevices.setObjectName(u"l_dlGPUdevices")

        self.horizontalLayout_31.addWidget(self.l_dlGPUdevices)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_26)

        self.le_dlGPUdevices = QLineEdit(self.w_dlGPUdevices)
        self.le_dlGPUdevices.setObjectName(u"le_dlGPUdevices")
        self.le_dlGPUdevices.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_31.addWidget(self.le_dlGPUdevices)


        self.verticalLayout_8.addWidget(self.w_dlGPUdevices)


        self.verticalLayout.addWidget(self.gb_submit)

        self.gb_passes = QGroupBox(wg_BlenderRender)
        self.gb_passes.setObjectName(u"gb_passes")
        self.gb_passes.setCheckable(True)
        self.verticalLayout_5 = QVBoxLayout(self.gb_passes)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 9, 9, 9)
        self.lw_passes = QListWidget(self.gb_passes)
        self.lw_passes.setObjectName(u"lw_passes")
        self.lw_passes.setMaximumSize(QSize(16777215, 500))
        self.lw_passes.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lw_passes.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_5.addWidget(self.lw_passes)

        self.b_addPasses = QPushButton(self.gb_passes)
        self.b_addPasses.setObjectName(u"b_addPasses")
        self.b_addPasses.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout_5.addWidget(self.b_addPasses)


        self.verticalLayout.addWidget(self.gb_passes)

        self.gb_previous = QGroupBox(wg_BlenderRender)
        self.gb_previous.setObjectName(u"gb_previous")
        self.gb_previous.setCheckable(False)
        self.gb_previous.setChecked(False)
        self.horizontalLayout_18 = QHBoxLayout(self.gb_previous)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(9, 9, 9, 9)
        self.scrollArea = QScrollArea(self.gb_previous)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 454, 69))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.l_pathLast = QLabel(self.scrollAreaWidgetContents)
        self.l_pathLast.setObjectName(u"l_pathLast")

        self.verticalLayout_3.addWidget(self.l_pathLast)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_18.addWidget(self.scrollArea)

        self.b_pathLast = QToolButton(self.gb_previous)
        self.b_pathLast.setObjectName(u"b_pathLast")
        self.b_pathLast.setEnabled(True)
        self.b_pathLast.setArrowType(Qt.DownArrow)

        self.horizontalLayout_18.addWidget(self.b_pathLast)


        self.verticalLayout.addWidget(self.gb_previous)

        QWidget.setTabOrder(self.e_name, self.b_context)
        QWidget.setTabOrder(self.b_context, self.cb_context)
        QWidget.setTabOrder(self.cb_context, self.cb_rangeType)
        QWidget.setTabOrder(self.cb_rangeType, self.sp_rangeStart)
        QWidget.setTabOrder(self.sp_rangeStart, self.le_frameExpression)
        QWidget.setTabOrder(self.le_frameExpression, self.cb_cam)
        QWidget.setTabOrder(self.cb_cam, self.chb_resOverride)
        QWidget.setTabOrder(self.chb_resOverride, self.sp_resWidth)
        QWidget.setTabOrder(self.sp_resWidth, self.sp_resHeight)
        QWidget.setTabOrder(self.sp_resHeight, self.chb_renderPreset)
        QWidget.setTabOrder(self.chb_renderPreset, self.cb_renderPreset)
        QWidget.setTabOrder(self.cb_renderPreset, self.cb_master)
        QWidget.setTabOrder(self.cb_master, self.cb_outPath)
        QWidget.setTabOrder(self.cb_outPath, self.cb_renderLayer)
        QWidget.setTabOrder(self.cb_renderLayer, self.gb_submit)
        QWidget.setTabOrder(self.gb_submit, self.cb_manager)
        QWidget.setTabOrder(self.cb_manager, self.sp_rjPrio)
        QWidget.setTabOrder(self.sp_rjPrio, self.sp_rjFramesPerTask)
        QWidget.setTabOrder(self.sp_rjFramesPerTask, self.sp_rjTimeout)
        QWidget.setTabOrder(self.sp_rjTimeout, self.chb_rjSuspended)
        QWidget.setTabOrder(self.chb_rjSuspended, self.chb_osDependencies)
        QWidget.setTabOrder(self.chb_osDependencies, self.chb_osUpload)
        QWidget.setTabOrder(self.chb_osUpload, self.chb_osPAssets)
        QWidget.setTabOrder(self.chb_osPAssets, self.e_osSlaves)
        QWidget.setTabOrder(self.e_osSlaves, self.sp_dlConcurrentTasks)
        QWidget.setTabOrder(self.sp_dlConcurrentTasks, self.sp_dlGPUpt)
        QWidget.setTabOrder(self.sp_dlGPUpt, self.le_dlGPUdevices)
        QWidget.setTabOrder(self.le_dlGPUdevices, self.gb_passes)
        QWidget.setTabOrder(self.gb_passes, self.lw_passes)
        QWidget.setTabOrder(self.lw_passes, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.b_pathLast)

        self.retranslateUi(wg_BlenderRender)
        self.chb_overrideLayers.toggled.connect(self.cb_renderLayer.setEnabled)
        self.chb_resOverride.toggled.connect(self.cb_scaling.setDisabled)
        self.chb_resOverride.toggled.connect(self.e_xRez.setDisabled)
        self.chb_resOverride.toggled.connect(self.e_yRez.setDisabled)

        QMetaObject.connectSlotsByName(wg_BlenderRender)
    # setupUi

    def retranslateUi(self, wg_BlenderRender):
        wg_BlenderRender.setWindowTitle(QCoreApplication.translate("wg_BlenderRender", u"Image Render", None))
        self.l_name.setText(QCoreApplication.translate("wg_BlenderRender", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_BlenderRender", u"Blender Render", None))
        self.gb_BlenderRender.setTitle(QCoreApplication.translate("wg_BlenderRender", u"General", None))
        self.l_AOV.setText(QCoreApplication.translate("wg_BlenderRender", u"AOV Name:     ", None))
        self.chb_customAOV.setText(QCoreApplication.translate("wg_BlenderRender", u"Custom", None))
        self.label_7.setText(QCoreApplication.translate("wg_BlenderRender", u"Context:", None))
        self.l_context.setText("")
        self.b_context.setText(QCoreApplication.translate("wg_BlenderRender", u"Select", None))
        self.label_2.setText(QCoreApplication.translate("wg_BlenderRender", u"Identifier:       ", None))
        self.b_changeTask.setText(QCoreApplication.translate("wg_BlenderRender", u"change", None))
        self.label_3.setText(QCoreApplication.translate("wg_BlenderRender", u"Framerange:", None))
        self.l_rangeStart.setText(QCoreApplication.translate("wg_BlenderRender", u"1001", None))
        self.l_rangeEndInfo.setText(QCoreApplication.translate("wg_BlenderRender", u"End:", None))
        self.l_rangeEnd.setText(QCoreApplication.translate("wg_BlenderRender", u"1100", None))
        self.l_rangeStartInfo.setText(QCoreApplication.translate("wg_BlenderRender", u"Start:", None))
        self.l_fml.setText(QCoreApplication.translate("wg_BlenderRender", u"Frames:  ", None))
        self.l_frameExpression.setText(QCoreApplication.translate("wg_BlenderRender", u"Frame expression:", None))
        self.label.setText(QCoreApplication.translate("wg_BlenderRender", u"Camera:", None))
        self.l_scaling.setText(QCoreApplication.translate("wg_BlenderRender", u"Scaling %:  ", None))
        self.l_Xtext.setText(QCoreApplication.translate("wg_BlenderRender", u" x ", None))
        self.label_4.setText(QCoreApplication.translate("wg_BlenderRender", u"Resolution override:", None))
        self.chb_resOverride.setText("")
        self.b_resPresets.setText(QCoreApplication.translate("wg_BlenderRender", u"\u25bc", None))
        self.l_renderPreset.setText(QCoreApplication.translate("wg_BlenderRender", u"Rendersettings preset:", None))
        self.chb_renderPreset.setText("")
        self.l_outPath_2.setText(QCoreApplication.translate("wg_BlenderRender", u"Master Version:", None))
        self.label_5.setText(QCoreApplication.translate("wg_BlenderRender", u"Render layer:", None))
        self.chb_overrideLayers.setText(QCoreApplication.translate("wg_BlenderRender", u"override", None))
        self.l_samples.setText(QCoreApplication.translate("wg_BlenderRender", u"Samples:  ", None))
        self.l_outPath.setText(QCoreApplication.translate("wg_BlenderRender", u"Location:  ", None))
        self.l_format.setText(QCoreApplication.translate("wg_BlenderRender", u"Format:  ", None))
        self.chb_compositor.setText(QCoreApplication.translate("wg_BlenderRender", u"Compositor:  ", None))
        self.l_fileCompress.setText(QCoreApplication.translate("wg_BlenderRender", u"Codec:     ", None))
        self.chb_persData.setText(QCoreApplication.translate("wg_BlenderRender", u"Persitent Data:", None))
        self.l_bitDepth.setText(QCoreApplication.translate("wg_BlenderRender", u"Bit Depth:  ", None))
        self.chb_alpha.setText(QCoreApplication.translate("wg_BlenderRender", u"Alpha:  ", None))
        self.gb_submit.setTitle(QCoreApplication.translate("wg_BlenderRender", u"Submit Render Job", None))
        self.l_manager.setText(QCoreApplication.translate("wg_BlenderRender", u"Manager:", None))
        self.label_18.setText(QCoreApplication.translate("wg_BlenderRender", u"Submit suspended:", None))
        self.chb_rjSuspended.setText("")
        self.label_19.setText(QCoreApplication.translate("wg_BlenderRender", u"Submit dependent files:", None))
        self.chb_osDependencies.setText("")
        self.label_16.setText(QCoreApplication.translate("wg_BlenderRender", u"Upload output:", None))
        self.chb_osUpload.setText("")
        self.label_17.setText(QCoreApplication.translate("wg_BlenderRender", u"Use Project Assets", None))
        self.chb_osPAssets.setText("")
        self.l_rjPrio.setText(QCoreApplication.translate("wg_BlenderRender", u"Priority:", None))
        self.label_15.setText(QCoreApplication.translate("wg_BlenderRender", u"Frames per Task:", None))
        self.l_rjTimeout.setText(QCoreApplication.translate("wg_BlenderRender", u"Task Timeout (min)", None))
        self.gb_osSlaves.setTitle(QCoreApplication.translate("wg_BlenderRender", u"Assign to slaves:", None))
        self.b_osSlaves.setText(QCoreApplication.translate("wg_BlenderRender", u"...", None))
        self.l_dlConcurrentTasks.setText(QCoreApplication.translate("wg_BlenderRender", u"Concurrent Tasks:", None))
        self.l_dlGPUpt.setText(QCoreApplication.translate("wg_BlenderRender", u"GPUs Per Task:", None))
        self.l_dlGPUdevices.setText(QCoreApplication.translate("wg_BlenderRender", u"Select GPU Devices:", None))
        self.le_dlGPUdevices.setPlaceholderText(QCoreApplication.translate("wg_BlenderRender", u"Enter Valid GPU Device Id(s)", None))
        self.gb_passes.setTitle(QCoreApplication.translate("wg_BlenderRender", u"Render Passes", None))
        self.b_addPasses.setText(QCoreApplication.translate("wg_BlenderRender", u"Add Passes", None))
        self.gb_previous.setTitle(QCoreApplication.translate("wg_BlenderRender", u"Previous render", None))
        self.l_pathLast.setText(QCoreApplication.translate("wg_BlenderRender", u"None", None))
        self.b_pathLast.setText(QCoreApplication.translate("wg_BlenderRender", u"...", None))
    # retranslateUi

