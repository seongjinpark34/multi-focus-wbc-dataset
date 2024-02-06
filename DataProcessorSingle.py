# data processor for single test
import os
import json
import pandas as pd
import glob
import shutil
from PIL import Image

# reads csv file.

MILAB_RESULT_FILE = 'analyze_result.json'
EXCLUDE_CLS = [0, 1]  # for 0 and 1 are rbcs and platelets
IMG_SIZE = [1920, 1200]


class DataProcessorSingle():
    def __init__(self, test_dir, img_size=[1920, 1200], crop_size=200):
        self.test_dir = test_dir
        self.df = None
        self._get_target_df()
        self.milab_result = None
        self._get_milab_result()
        self.img_size = img_size
        self.crop_size = crop_size

    def process_for_label_images(self, output_dir='./label'):
        # returns target image stacked and corresponding pre-classification label.
        target_folder = os.path.join(output_dir, os.path.basename(self.test_dir))
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        else:
            shutil.rmtree(target_folder)
            os.makedirs(target_folder)
        crop_index = 0
        target_img_nums = self._get_target_img_nums()
        label_info = []
        for target_img_num in target_img_nums:
            temp_dict = self.milab_result[str(target_img_num - 1)]["cell_prediction"]
            target_locations = self._get_target_cell_locations(temp_dict)
            for crop_bbox in target_locations:
                target_img_list = self._get_img_list(
                    self.df.loc[self.df['img_num'] == target_img_num].sort_values(by=['stack_num'], axis=0)[
                        'img_name'].to_list())
                result_img = crop_and_concat(target_img_list, crop_bbox, self.crop_size, self.img_size)
                result_img.save(os.path.join(target_folder, f'{crop_index}.jpg'))
                temp_info = [crop_index, os.path.basename(self.test_dir), target_img_num, crop_bbox]
                label_info.append(temp_info)
                crop_index += 1

        result_pd = pd.DataFrame(label_info)
        result_pd.columns = ['crop_index', 'test_id', 'img_num', 'cell_location']
        result_pd.to_csv(os.path.join(target_folder, 'label.csv'))

    def _get_img_list(self, img_list):
        return_list = []
        for img in img_list:
            return_list.append(Image.open(os.path.join(self.test_dir, img)))
        return return_list

    def _get_target_cell_locations(self, cell_prediction_dict):
        target_cell_locations = []
        for items in cell_prediction_dict.items():
            if items[1]['prediction'] in EXCLUDE_CLS:
                continue
            else:
                target_cell_locations.append(items[1]['location'])
        return target_cell_locations

    def _identify_target_images(self):
        # identify available image stacks.
        # only jpg images are expected

        images = [os.path.basename(x) for x in glob.glob(os.path.join(self.test_dir, "*.jpg"))]
        return images

    def _get_target_df(self):
        target_images = self._identify_target_images()
        self.df = extract_img_info(target_images)

    def _get_target_img_nums(self):
        ## identify available images
        available_img_nums = self.df['img_num'].unique()
        return available_img_nums

    def _get_milab_result(self):
        try:
            with open(os.path.join(self.test_dir, MILAB_RESULT_FILE)) as f:
                self.milab_result = json.load(f)
        except Exception as e:
            raise e

    def _process_milab_result():
        milab_result_path = os.path.join(self.test_dir, MILAB_RESULT_FILE)
        if not os.path.exists(milab_result_path):
            raise Exception('No result presents... please check the test folder')

        with open(milab_result_path, 'r') as file:
            self.milab_result = json.load(file)

    # def _get_bboxes(self, img_idx):
    # def _concatenate():

    # def save()


def extract_info(image_name):
    img_num, x_value, y_value, stack_num, fm_value = image_name.split('_')
    return [img_num, x_value, y_value, stack_num, fm_value.split('.')[0]]


def extract_img_info(fovs):
    result_list = []

    for fov in fovs:
        info = list(map(int, extract_info(fov)))
        info.append(fov)
        result_list.append(info)

    result_df = pd.DataFrame(result_list,
                             columns=['img_num', 'x_value', 'y_value', 'stack_num', 'fm_value', 'img_name'], dtype=int)
    return result_df


def crop_and_concat(img_list, crop_location, size=200, max_size=[1920, 1200]):
    cropped_images = []
    new_width = len(img_list) * size
    new_height = size
    concatenated_img = Image.new('RGB', (new_width, new_height))
    x_offset = 0

    crop_coord = get_crop_coord(crop_location, size, max_size)
    for img in img_list:
        concatenated_img.paste(img.crop(crop_coord), (x_offset, 0))
        x_offset += size
    return concatenated_img


def get_crop_coord(pos_cord, size=200, max_size=[1920, 1200]):
    # pos_cord in x,y,w,h
    x, y, w, h = pos_cord
    x = (x + w // 2)
    y = (y + h // 2)
    half_size = size // 2
    x_0 = max(0, x - half_size)
    y_0 = max(0, y - half_size)
    x_1 = min(x_0 + size, 1920)
    if x_1 == max_size[0]:
        x_0 = max_size[0] - size
    y_1 = min(y_0 + size, max_size[1])
    if y_1 == max_size[1]:
        y_0 = max_size[1] - size
    return x_0, y_0, x_1, y_1
