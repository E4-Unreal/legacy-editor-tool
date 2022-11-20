import unreal
import json

# 커스텀 모듈
import unreal_functions as uf
import AnimSequence_functions as asf

# 커스텀 모듈이 수정되어도 실시간 반영을 위한 reload
from importlib import *
reload(uf)
reload(asf)

# 원본 시퀀스 경로
base_asset_path = ""

# JSON 파일 경로
folder_path = ""
file_name = ""
file_path = folder_path + file_name

# 시퀀스 복제본이 저장될 경로
base_path = '' # "콘텐츠 브라우저 > All > 콘텐츠 > E4 > Test" 폴더
name = '' # 에셋 이름

# JSON 파일에서 커브 데이터 읽어오기
try:
    with open(file_path, 'r') as f:
        tracks = json.load(f)
except:
    print(file_path + "에서 json 로드에 실패하였습니다")

# 원본 시퀀스 로드
asset = uf.get_asset(base_asset_path)

# 시퀀스 샘플링 프레임 수 체크
sampled_frames = asset.get_editor_property('number_of_sampled_frames')

for track in tracks:
    if track['frames'][-1] > sampled_frames:
        print(track['bone'] + " 트랙의 목표 프레임이 시퀀스 샘플링 프레임 수 보다 큽니다")
        quit()

# 시퀀스 복제
duplicated_asset = uf.duplicate_asset(name, base_path, asset)

# 시퀀스 복제본에 커브 데이터 추가
for track in tracks:
    unreal.AnimationLibrary.add_curve(duplicated_asset, track['bone'], unreal.RawCurveTrackTypes.RCT_TRANSFORM)

    # 수동으로 Json 작성할 경우 프레임을 기준으로 키를 설정하기 때문에 time으로 계산 필요
    if len(track['times']) == 0:
        for frame in track['frames']:
            track['times'].append(unreal.AnimationLibrary.get_time_at_frame(duplicated_asset, frame))

    track['transforms'] = []
    for i in range(0, len(track['times'])):
        track['transforms'].append(uf.compose_transform(track['locations'][i], track['rotations'][i], track['scales'][i]))
    unreal.AnimationLibrary.add_transformation_curve_keys(duplicated_asset, track['bone'], track['times'],track['transforms'])