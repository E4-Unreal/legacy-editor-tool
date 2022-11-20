import unreal
import json

# 커스텀 모듈
import unreal_functions as uf
import AnimSequence_functions as asf

# 커스텀 모듈이 수정되어도 실시간 반영을 위한 reload
from importlib import *
reload(uf)
reload(asf)

# 커브 데이터를 읽어올 시퀀스 경로
asset_path = ""

# JSON 파일 경로
folder_path = ""
file_name = ""
file_path = folder_path + file_name

# 시퀀스 로드
asset = uf.get_asset(asset_path)

if asset == None:
    print(asset_path + "는 존재하지 않습니다")
    quit()

# 시퀀스에서 커브 데이터 읽어오기
tracks = asf.GetCurveData(asset)

# 커브 데이터를 JSON 파일로 저장
try:
    with open(file_path, 'w') as f:
        json.dump(tracks, f)
except:
    print("json 저장 실패")