import os 
import numpy as np 
import cv2
from typing import List, Dict, Tuple
from sports_dataloader import  load_gt, load_img_paths, xywh2x1y1x2y2
from varname.helpers import debug

start_frame = 21
end_frame = 30

def square_from_rectangle(player_bbox: tuple):
    x, y, w, h = player_bbox
    centr = [int(x+w/2), int(y+h/2)]
    square_side = max(w, h)
    x1y1x2y2 = [
        int(centr[0] - square_side/2), 
        int(centr[1] - square_side/2),
        int(centr[0] + square_side/2), 
        int(centr[1] + square_side/2)             
    ]
    x1y1x2y2_to_return = []
    for value in x1y1x2y2:
        if value < 0:
            value = 0
        x1y1x2y2_to_return.append(value)
    return x1y1x2y2_to_return


def crop_snippet(match_path:str , outdir: str, square: bool = False, is_square: bool = False): 
    match_name = os.path.basename(os.path.normpath(match_path))
    img_paths = load_img_paths(match_path)
    gt_objects = load_gt(match_path)
    os.makedirs(outdir, exist_ok=True)
    match_outdir = os.path.join(outdir, match_name)
    os.makedirs(match_outdir, exist_ok=True)
    for frame_number, frame_objects in gt_objects.items():
        if (frame_number < start_frame) or (frame_number > end_frame): 
            continue
        try: 
            img_path = img_paths[frame_number]
        except KeyError:
            continue
        img = cv2.imread(img_path)
        # ext = img_path.split('.')[-1]
        ext = os.path.splitext(img_path)[-1].split('.')[-1]
        img2draw = img.copy() 
        for player_id, player_bbox in frame_objects.items():
            player_out_dir = os.path.join(match_outdir, 'player_{}'.format(str(player_id)))
            os.makedirs(player_out_dir, exist_ok=True)
            cv_bbox = xywh2x1y1x2y2(player_bbox) if is_square else square_from_rectangle(player_bbox)
            player_snippet = img2draw[cv_bbox[1]:cv_bbox[3], cv_bbox[0]:cv_bbox[2], :]

            snippet_name = '{}_{:02d}_{:06d}_x1_{}_y1_{}_x2_{}_y2_{}.{}'.format(
                    match_name,
                    player_id,
                    frame_number,
                    cv_bbox[0], cv_bbox[1], cv_bbox[2], cv_bbox[3],
                    #*cv_bbox,
                    ext)
            snippet_path = os.path.join(player_out_dir, snippet_name)
            # debug(snippet_path)
            cv2.imwrite(snippet_path, player_snippet)
            #print('out written to', os.path.abspath(snippet_path))


if __name__ == '__main__' :
    outdir = 'output/snippets'
    match_path = 'datasets/sportsMOT_volley_starter_pack.002/sportsMOT_volley_light_dataset/match_001_short'
    crop_snippet(match_path, outdir, True);
