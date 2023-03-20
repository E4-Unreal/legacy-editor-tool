// Copyright Epic Games, Inc. All Rights Reserved.

#include "MODULE_NAMEModule.h"
#include "MODULE_NAME.h"

#define LOCTEXT_NAMESPACE "FMODULE_NAMEModule"

void FMODULE_NAMEModule::StartupModule()
{
	// This code will execute after your module is loaded into memory;
	// the exact timing is specified in the .uplugin file per-module

	//Load Native Tags
	FMODULE_NAME::InitializeNativeTags();
}

void FMODULE_NAMEModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.
	// For modules that support dynamic reloading, we call this function before unloading the module.
	// we call this function before unloading the module.
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FMODULE_NAMEModule, MODULE_NAME)
