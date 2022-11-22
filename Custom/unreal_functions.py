import unreal

def get_asset(asset_path):
    browser = unreal.EditorAssetLibrary()
    if browser.does_asset_exist(asset_path):
        asset_data = browser.find_asset_data(asset_path)
        return asset_data.get_asset()

def duplicate_asset(name, base_path, asset):
    if get_asset(base_path + '/' + name) == None:
        return unreal.AssetToolsHelpers.get_asset_tools().duplicate_asset(name, base_path, asset)
    else:
        print(base_path + '/' + name + "은 이미 존재합니다")
        quit()

def decompose_transform(transform):
    location = list(transform.translation.to_tuple())
    rotation = list(transform.rotation.euler().to_tuple())
    scale = list(transform.scale3d.to_tuple())

    return location, rotation, scale

def compose_transform(location, rotation, scale):
    rotation = convert_rotation_for_transform(rotation)
    return unreal.Transform(location, rotation, scale)

# unreal.Transform.rotation.euler() = unreal.Vector(x,y,z)
# unreal.Transform(location, rotation, scale)에서 rotation = unreal.Rotator = [y, z, x] 
# 이를 보정하기 위해 JSON의 rotation을 [x, y, z] => [y, z, x] 로 변환하기 위한 함수
def convert_rotation_for_transform(rotation):
    if len(rotation) == 3:
        tem = rotation[0]
        rotation[0] = rotation[1]
        rotation[1] = rotation[2]
        rotation[2] = tem

        return rotation
    else:
        print("convert_rotation_for_transform(rotation): rotation의 길이가 3이 아닙니다")
        quit()

def round_list(list, DecimalPlace):
    new_list = []
    for e in list:
        new_list.append(round(e, DecimalPlace))
    return new_list