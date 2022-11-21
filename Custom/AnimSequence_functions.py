import unreal
import json

import unreal_functions as uf
from importlib import *
reload(uf)

def GetCurveData(AnimSequence):
    tracks = []
    # skeletal bone names
    curve_names = unreal.AnimationLibrary.get_animation_curve_names(AnimSequence, unreal.RawCurveTrackTypes.RCT_TRANSFORM)

    for curve_name in curve_names:
        transformation_keys = unreal.AnimationLibrary.get_transformation_keys(AnimSequence, curve_name)

        track = {}
        track['bone'] = str(curve_name)
        track['times'] = list(transformation_keys[0])
        track['frames'] = []
        track['locations'] = []
        track['rotations'] = []
        track['scales'] = []

        # Convert times to frames
        for time in track['times']:
            track['frames'].append(unreal.AnimationLibrary.get_frame_at_time(AnimSequence, time))

        # ReCalculate times from frames
        track['times'] = []
        for frame in track['frames']:
            track['times'].append(unreal.AnimationLibrary.get_time_at_frame(AnimSequence, frame))

        for transform in transformation_keys[1]:
            location, rotation, scale = uf.decompose_transform(transform)
            track['locations'].append(location)
            track['rotations'].append(rotation)
            track['scales'].append(scale)


        tracks.append(track)
    
    return tracks

class AnimSequence:
    # asset_path, json_path, result_path: 레퍼런스 경로
    def __init__(self, asset_path = "", json_path = "", json_name = "", result_path = "", result_name = ""):
        self.asset_path = asset_path
        self.json_path = json_path
        self.json_name = json_name
        self.result_path = result_path
        self.result_name = result_name

    def CheckNone(self, option = 0):

        if option == 0:
            if self.asset_path == "":
                print("asset_path is None")
                quit()
            
            if self.json_path == "":
                self.json_path = unreal.Paths.get_path(self.asset_path)

            if self.json_name == "":
                self.json_name = unreal.Paths.get_base_filename(self.asset_path) + ".json"

        else:
            if self.asset_path == "" or self.json_path == "" or self.json_name == "":
                print("One of asset_path/json_path/json_name is None")

            if self.result_path == "":
                self.result_path = unreal.Paths.get_path(self.asset_path)
            
            if self.result_name == "":
                self.result_name = self.json_name
            
    def ConvertJsonPath(self):
        json_path = self.json_path.replace("/Game/", unreal.Paths.project_content_dir())
        json_file_path = json_path + "/" + self.json_name + ".json"
        return json_file_path

    def CurvesToJson(self):
        self.CheckNone()
        json_file_path = self.ConvertJsonPath()

        # 시퀀스 로드
        asset = uf.get_asset(self.asset_path)

        if asset == None:
            print(self.asset_path + "는 존재하지 않습니다")
            quit()

        # 시퀀스에서 커브 데이터 읽어오기
        tracks = GetCurveData(asset)

        # 커브 데이터를 JSON 파일로 저장
        try:
            with open(json_file_path, 'w') as f:
                json.dump(tracks, f)
        except:
            print("json 저장 실패")

    def JsonToCurves(self):
        self.CheckNone(option=1)
        json_file_path = self.ConvertJsonPath()

        # JSON 파일에서 커브 데이터 읽어오기
        try:
            with open(json_file_path, 'r') as f:
                tracks = json.load(f)
        except:
            print(json_file_path + "에서 json 로드에 실패하였습니다")
            quit()

        # 원본 시퀀스 로드
        asset = uf.get_asset(self.asset_path)

        # 시퀀스 샘플링 프레임 수 체크
        sampled_frames = asset.get_editor_property('number_of_sampled_frames')

        for track in tracks:
            if track['frames'][-1] > sampled_frames:
                print(track['bone'] + " 트랙의 목표 프레임이 시퀀스 샘플링 프레임 수 보다 큽니다")
                quit()

        # 시퀀스 복제
        duplicated_asset = uf.duplicate_asset(self.result_name, self.result_path, asset)

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