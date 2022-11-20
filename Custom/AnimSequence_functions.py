import unreal

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