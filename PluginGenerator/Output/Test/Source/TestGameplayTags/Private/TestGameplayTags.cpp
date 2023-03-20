// Fill out your copyright notice in the Description page of Project Settings.

#include "TestGameplayTags.h"
#include "GameplayTagsManager.h"

// Convert VariableName to TagName
// ex) Item_Equipment_Weapon_Sword > "Item.Equipment.Weapon.Sword"
#define ADD_TAG(VariableName, TagComment) AddTag(VariableName, TCHAR_TO_ANSI(*FString(# VariableName).Replace(TEXT("_"), TEXT("."))), TagComment)

FTestGameplayTags FTestGameplayTags::GameplayTags;

// It should be called in StartupModule()
// Module's loading phase should be PostSplashScreen or PreEarlyLoadingScreen for using even in CDO Constructor
void FTestGameplayTags::InitializeNativeTags()
{
	UGameplayTagsManager& GameplayTagsManager = UGameplayTagsManager::Get();

	GameplayTags.AddAllTags(GameplayTagsManager);

	GameplayTagsManager.DoneAddingNativeTags();
}

void FTestGameplayTags::AddAllTags(UGameplayTagsManager& Manager)
{
	// ex) ADD_TAG(Item_Equipment_Weapon_Sword, "Native Tag for Sword");
}

void FTestGameplayTags::AddTag(FGameplayTag& OutTag, const ANSICHAR* TagName, const ANSICHAR* TagComment)
{
	OutTag = UGameplayTagsManager::Get().AddNativeGameplayTag(FName(TagName), FString(TEXT("(Native) ")) + FString(TagComment));
}
