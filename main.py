import math
import os
import pathlib

from PIL import Image


# 855 - 846 - signal line
# 250 line start information
# 530 line of graphic

class ChartFile:
    def __init__(self, full_path, name:str):
        self.full_path = full_path
        self.name = name
        self.id = name.split(".")[0]

chart_list_path = []
base_chart_path = None
cur_path = str(pathlib.Path().resolve())
path_folder = cur_path + "\\Pic\\"

for k in os.listdir(path_folder):
    if k.startswith('00.png'):
        base_chart_path = path_folder + k
    else:
        if k.endswith('.png'):
            if k.find('compare') == -1:
                chart_list_path.append(ChartFile(path_folder + k, k))

band_list = [5785, 5787, 5789, 5791, 5793, 5795, 5797, 5799, 5801, 5803, 5805, 5807, 5809, 5811, 5813, 5815]
# band_list = [5795, 5797, 5799, 5801, 5803]


def my_min(sequence):
    low = sequence[0]  # need to start with some value
    for i in sequence:
        if low is None or i < low:
            low = i

    class cor:
        def __init__(self, a, b, va, vb):
            self.a = a
            self.b = b
            self.va = va
            self.vb = vb

    min_dict = {}
    for i in range(len(sequence)):
        for ii in range(len(sequence)):
            if i != ii:
                # new_dict = {'a': i, 'b': ii}
                if sequence[i] is not None and sequence[ii] is not None:
                    min_dict[cor(i, ii, sequence[i], sequence[ii])] = abs(sequence[i] - sequence[ii])

    min = None
    min_dict_key = None
    error = False

    # for key, value in min_dict.items():
    #     if value > 50:
    #         min = value
    #         min_dict_key = key
    #         error = True
    #         break

    if error is False:
        for key, value in min_dict.items():
            if min == None or value < min:
                min = value
                min_dict_key = key

    if len(min_dict) == 0:
        return low
    else:
        return math.trunc((min_dict_key.va + min_dict_key.vb) / 2)

def get_chart_structure(band_list, full_path):
    with Image.open(full_path) as image:
        pixels = image.load()
        image_processed = Image.new('RGB', (image.size[0], image.size[1]))
        pixels_processed = image_processed.load()

        image_cursor = Image.new('RGB', (image.size[0], image.size[1]))
        pixels_cursor = image_cursor.load()

        pi = 0
        min = 2000

        # band_list = [5785, 5787, 5789, 5791, 5793, 5795, 5797, 5799, 5801, 5803, 5805, 5807, 5809, 5811, 5813, 5815]
        # band_list = [5805]
        band_value = {}

        def its_info(r, g, b):
            if r > 70 and g > 70 and b < 10:
                return True
            else:
                return False

        for cur_band in band_list:
            x_start = (math.trunc(cur_band / 2) - 2902) * 12 + 1001
            # x_end = x_start + 10

            for i in range(0, 4, 1):
                x_cur = x_start + i * 3

                minimum_position = 500
                min_y = [None, None, None]
                round = 1
                for x in range(x_cur, x_cur + 3, 1):  # image.size[0],100,1):
                    for y in range(image.size[1] - 1, minimum_position, -1):
                        pixel = pixels[x, y]
                        (r, g, b) = pixel[0], pixel[1], pixel[2]

                        if y <= 900:
                            if its_info(r, g, b):
                                if min_y[round - 1] == None or min_y[round - 1] > y:
                                    min_y[round - 1] = y

                    round += 1
                # print(min_y)
                try:
                    mx = my_min(min_y)
                except Exception as e:
                    mx = minimum_position

                band_value[cur_band + 0.5 * i] = mx - minimum_position
                for x in range(x_cur, x_cur + 3, 1):
                    for y in range(image.size[1] - 1, minimum_position, -1):
                        if y <= 900 and y >= mx:
                            pixels_processed[x, y] = pix_col = (255, 255, 0)

        # print(band_value)
        # for cur in band_value.items():
        #     print(cur)

        # print("min: " + str(min))
        # image_processed.show()
        return band_value

max_y = 400
base_chart_data = get_chart_structure(band_list, base_chart_path)
for cur_chart_path in chart_list_path:
    cur_chart_data = get_chart_structure(band_list, cur_chart_path.full_path)

    image_delta = Image.new('RGB', (len(band_list)*20, max_y))
    pixels_delts = image_delta.load()
    lines = 0
    rvalue_sum = 0
    rbase_value_sum = 0
    for key, value in cur_chart_data.items():
        base_value = base_chart_data[key]
        for xi in range(1, 4, 1):
            x = lines*4 + xi
            for yi in range(0, max_y, 1):
                if yi >= value:
                    if yi < base_value:
                        pixels_delts[x, yi] = (0, 0, 255)
                    else:
                        pixels_delts[x, yi] = (0, 255, 0)
                elif yi >= base_value:
                    pixels_delts[x, yi] = (255, 0, 0)
                else:
                    pixels_delts[x, yi] = (0, 0, 0)
        lines += 1
        rvalue = max_y - value
        rbase_value = max_y - base_value

        if rvalue <= rbase_value:
            rvalue_sum = rvalue_sum + rvalue
            rbase_value_sum = rbase_value_sum + rbase_value

    delta = (rbase_value_sum - rvalue_sum) / rbase_value_sum * 100
    print("" + cur_chart_path.name + " procent: " + str(round(delta,1)))


    image_delta.show()
    image_delta.save(path_folder + cur_chart_path.id + "-compare" + ".png")

    pass


# with Image.open(r"D:\FILES\Bukovel\OneDrive\Projects\DroneAge\Projects\FShield\Interpriter\Pic\00.png") as image:
#     pixels = image.load()
#     image_processed = Image.new('RGB', (image.size[0], image.size[1]))
#     pixels_processed = image_processed.load()
#
#     image_cursor = Image.new('RGB', (image.size[0], image.size[1]))
#     pixels_cursor = image_cursor.load()
#
#     pi = 0
#     min = 2000
#
#     # band_list = [5785, 5787, 5789, 5791, 5793, 5795, 5797, 5799, 5801, 5803, 5805, 5807, 5809, 5811, 5813, 5815]
#     # band_list = [5805]
#     band_value = {}
#
#     def its_info(r, g, b):
#         if r > 70 and g > 70 and b < 10:
#             return True
#         else:
#             return False
#
#
#     for cur_band in band_list:
#         x_start = (math.trunc(cur_band/2)-2902) * 12 + 1001
#         # x_end = x_start + 10
#
#         for i in range(0, 4, 1):
#             x_cur = x_start+i*3
#
#             minimum_position = 500
#             min_y = [None, None, None]
#             round = 1
#             for x in range(x_cur, x_cur+3, 1):  # image.size[0],100,1):
#                 for y in range(image.size[1]-1, minimum_position ,-1):
#                     pixel = pixels[x, y]
#                     (r, g, b) = pixel[0] , pixel[1], pixel[2]
#
#                     if y <= 900:
#                         if its_info(r,g,b):
#                             if min_y[round - 1] == None or min_y[round - 1] > y:
#                                 min_y[round - 1] = y
#
#                 round += 1
#             # print(min_y)
#             try:
#                 mx = my_min(min_y)
#             except Exception as e:
#                 mx = minimum_position
#
#             band_value[cur_band+0.5*i] = mx-minimum_position
#             for x in range(x_cur, x_cur + 3, 1):
#                 for y in range(image.size[1] - 1, minimum_position, -1):
#                     if y <= 900 and y >= mx:
#                         pixels_processed[x, y] = pix_col = (255, 255, 0)
#
#
#     # print(band_value)
#     for cur in band_value.items():
#         print(cur)
#
#     # print("min: " + str(min))
#     image_processed.show()
#     # image_cursor.show()
#     # print("test 11")
#
#
# print("test")
#
#
