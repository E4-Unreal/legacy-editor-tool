// Fill out your copyright notice in the Description page of Project Settings.

#include "MODULE_NAME.h"
#include "GameplayTagsManager.h"

// Convert VariableName to TagName
// ex) Item_Equipment_Weapon_Sword > "Item.Equipment.Weapon.Sword"
#define ADD_TAG(VariableName, TagComment) AddTag(VariableName, TCHAR_TO_ANSI(*FString(# VariableName).Replace(TEXT("_"), TEXT("."))), TagComment)

FMODULE_NAME FMODULE_NAME::GameplayTags;

// It should be called in StartupModule()
// Module's loading phase should be PostSplashScreen or PreEarlyLoadingScreen for using even in CDO Constructor
void FMODULE_NAME::InitializeNativeTags()
{
	UGameplayTagsManager& GameplayTagsManager = UGameplayTagsManager::Get();

	GameplayTags.AddAllTags(GameplayTagsManager);

	GameplayTagsManager.DoneAddingNativeTags();
}

void FMODULE_NAME::AddAllTags(UGameplayTagsManager& Manager)
{
	// ex) ADD_TAG(Item_Equipment_Weapon_Sword, "Native Tag for Sword");
}

void FMODULE_NAME::AddTag(FGameplayTag& OutTag, const ANSICHAR* TagName, const ANSICHAR* TagComment)
{
	OutTag = UGameplayTagsManager::Get().AddNativeGameplayTag(FName(TagName), FString(TEXT("(Native) ")) + FString(TagComment));
}
