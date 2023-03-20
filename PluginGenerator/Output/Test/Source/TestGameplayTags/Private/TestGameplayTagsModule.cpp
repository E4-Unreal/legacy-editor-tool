// Copyright Epic Games, Inc. All Rights Reserved.

#include "TestGameplayTagsModule.h"
#include "TestGameplayTags.h"

#define LOCTEXT_NAMESPACE "FTestGameplayTagsModule"

void FTestGameplayTagsModule::StartupModule()
{
	// This code will execute after your module is loaded into memory;
	// the exact timing is specified in the .uplugin file per-module

	//Load Native Tags
	FTestGameplayTags::InitializeNativeTags();
}

void FTestGameplayTagsModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.
	// For modules that support dynamic reloading, we call this function before unloading the module.
	// we call this function before unloading the module.
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FTestGameplayTagsModule, TestGameplayTags)
