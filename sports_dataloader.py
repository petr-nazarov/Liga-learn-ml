import os 
import numpy as np 
import cv2
import random
from typing import List, Dict, Tuple


def create_random_color(existing_colors : List[Tuple[int]]) -> Tuple[int, int, int]: 
    # color in rgb format
    new_color = (
            int(np.random.randint(0, 256)),
            int(np.random.randint(0, 256)),
            int(np.random.randint(0, 256)),
        )
    if new_color in existing_colors: 
        return create_random_color(existing_colors)
    return new_color
def load_gt(dataset_path: str): 
    gt_path = None
    gt_data= None
    gt_objects = {}
    for root, dirs, files in os.walk(dataset_path):
        for file_name in files:
            if 'gt.txt' == file_name: 
                gt_path = os.path.join(root, file_name)
    if not gt_path: 
        return None
    with open(gt_path, 'r') as f:
        gt_data = f.readlines()
    for gt_object in gt_data: 
        gt_object = gt_object.replace('\n', '').split(', ')
        for i in range(len(gt_object)):
            gt_object[i] = int(gt_object[i])
        frame_number, player_id, top_left_x, top_left_y, width, height, _, _, _ = gt_object 
        if frame_number not in gt_objects.keys(): 
            gt_objects[frame_number] = {}
        gt_objects[frame_number][player_id] = (top_left_x, top_left_y, width, height)
    return gt_objects

def load_img_paths(dataset_path: str) -> Dict[int, str]: 
    img_paths = {}
    for root, dirs, files in os.walk(dataset_path):
        for file_name in files:
            if '.jpg' in file_name and len(file_name) == 10: 
                frame_number = int(file_name[:-4])
                img_paths[frame_number] = os.path.join(root, file_name)
    return img_paths;


def run_dataset(dataset_path:str , outdir: str): 
    img_paths = load_img_paths(dataset_path)
    gt_objects = load_gt(dataset_path)
    colots_list = []
    for _ in range(12):
        colots_list.append(create_random_color(colots_list))
    for frame_number, frame_objects in gt_objects.items():
        try: 
            img_path = img_paths[frame_number]
        except KeyError:
            continue
        img = cv2.imread(img_path)
        img2draw = img.copy() 
        for player_id, player_bbox in frame_objects.items():
            color = colots_list[player_id]
            cv_bbox = xywh2x1y1x2y2(player_bbox)
            cv2.putText(
                img2draw, 
                text = str(player_id), 
                # bottom left corner of the text
                org = (
                    #x1 + half of width of bbox
                    cv_bbox[0] + int( (cv_bbox[2] - cv_bbox[-0]) /2) - 5, 
                    # y1 - 2px
                    cv_bbox[1]-5), 
                fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale = 1, 
                color = color, 
                thickness = 2, 
                lineType = cv2.LINE_AA)
            cv2.rectangle(
                    img2draw, 
                    #top left 
                    pt1=(cv_bbox[0], cv_bbox[1]),
                    #bottom rigth
                    pt2=(cv_bbox[2], cv_bbox[3]),
                    color=color,
                    thickness=2)

        os.makedirs(outdir, exist_ok=True)
        img_out_path = os.path.join(outdir, os.path.basename(img_path))
        cv2.imwrite(img_out_path, img2draw)
        print('out written to', os.path.abspath(img_out_path))



def xywh2x1y1x2y2(xywh_bbox: tuple):
    return (
            xywh_bbox[0],
            xywh_bbox[1],
            xywh_bbox[0] + xywh_bbox[2],
            xywh_bbox[1] + xywh_bbox[3]
        )
if __name__ == '__main__' :
    outdir = 'output'
    run_dataset('datasets/sportsMOT', outdir);
