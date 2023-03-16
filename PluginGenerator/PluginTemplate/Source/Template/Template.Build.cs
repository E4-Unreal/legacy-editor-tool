using UnrealBuildTool; 

public class Template: ModuleRules 
{ 
	public Template(ReadOnlyTargetRules Target) : base(Target) 
	{
		// Default Modules
		PrivateDependencyModuleNames.AddRange(new string[] {"Core", "CoreUObject", "Engine"});
		
		// Additional Modules
		PrivateDependencyModuleNames.AddRange(new string[] {});
	} 
}