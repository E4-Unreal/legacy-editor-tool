// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameplayTagContainer.h"

class UGameplayTagsManager;

/**
 *
 *	Singleton containing native gameplay tags.
 */
 // TODO Add *GAMEPLAYTAGS_API to use FTestGameplayTags in other modules
struct TESTGAMEPLAYTAGS_API FTestGameplayTags
{
public:
	static const FTestGameplayTags& Get() { return GameplayTags; }

	static void InitializeNativeTags();

	// Add Native Gameplay Tags
	// ex) FGameplayTag Item_Equipment_Weapon_Sword;

protected:
	//Registers all of the tags with the GameplayTags Manager
	void AddAllTags(UGameplayTagsManager& Manager);

	//Helper function used by AddAllTags to register a single tag with the GameplayTags Manager
	void AddTag(FGameplayTag& OutTag, const ANSICHAR* TagName, const ANSICHAR* TagComment);

private:

	static FTestGameplayTags GameplayTags;
};