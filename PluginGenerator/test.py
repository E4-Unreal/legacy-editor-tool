import os
from classes import *

moduleDescriptors = [
    {
    'templateName': "SimpleModuleWithLog",
    'moduleName': "PLUGIN_NAMEGame"
    },

    {
    'templateName': "SimpleModuleWithLog",
    'moduleName': "PLUGIN_NAMEEditor",
    'type': 'Editor'
    },

    {
    'templateName': "NativeGameplayTags",
    'moduleName': "PLUGIN_NAMEGameplayTags",
    'loadingPhase': "PostSplashScreen"
    }
]

pluginDescriptor = {
	"FileVersion": 3,
	"Version": 1,
	"VersionName": "0.1",
	"FriendlyName": "PLUGIN_NAME",
	"Description": "",
	"Category": "New",
	"CreatedBy": "",
	"CreatedByURL": "",
	"DocsURL": "",
	"MarketplaceURL": "",
	"SupportURL": "",
	"EngineVersion": "5.1.0",
	"EnabledByDefault": True,
	"CanContainContent": True,
	"IsBetaVersion": False,
	"IsExperimentalVersion": True,
	"Installed": False,
	"Modules": [
	]
}

curDir = os.path.curdir

PG = PluginGenerator("./Templates", "BasePlugin", os.path.join(curDir, "Output"), "Test", moduleDescriptors, pluginDescriptor)
PG.generate()
