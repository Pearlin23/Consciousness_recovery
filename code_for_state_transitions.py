# -*- coding:utf-8 -*-
# @FileName  :Arousal_state_convert_plot.py
# @Time      :2022/5/10 11:23
# @Author    :Yang Xu
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_chord_diagram import chord_diagram
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib

matplotlib.use('Qt5Agg')
sys.path.append(os.path.abspath(".."))

def search_csv(path=".", name=""): 
    result = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search_csv(item_path, name)
        elif os.path.isfile(item_path):
            if name + ".csv" == item:
                result.append(item_path)

    return result


def read_csv(path='.', name="", column="", element="", state_name=""):
    """
        column[0]: file_name      column[1]:first looming time
        sheet1：Fwake state       sheet2： Frorr state
    """
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        csv_data = pd.read_excel(f, sheet_name=state_name)

    return csv_data


def pre_data(file_path, dataframe, num, state=""):
    # j = 0
    A = np.zeros((16, 16))

    fre_list = []
    looming_time = int(dataframe.at[num, state])
    start = looming_time - 600 * 30  # start time
    end = looming_time + 0 * 30  # end time

    df2 = pd.read_csv(file_path)

    data = df2.iloc[start:end, 1:2]
    for i in range(1, len(data)):
        if data.iloc[i, 0] != data.iloc[i - 1, 0]:
            a = data.iloc[i, 0] - 1
            b = data.iloc[i - 1, 0] - 1
            A[a, b] = A[a, b] + 1

    class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,
                  9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}

    for line in data.iloc[:, 0]:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    class_type = dict(sorted(class_type.items(), key=lambda item: item[0]))  # sort dict

    behavior_fre = list(class_type.values())

    A = normalize_2d(A)

    behavior_fre_norm = behavior_fre / np.linalg.norm(behavior_fre)
    for j in range(len(behavior_fre_norm)):
        # A[j, j] = behavior_fre_norm[j]
        A[j, j] = 0

    return A


def del_pre_data(data_list): # data pre-processing
    del_index = []
    del_data = data_list
    t = 0
    for i in range(len(del_data)):
        if np.any(del_data[:, [i]]) == 0 and np.any(del_data[[i], :]) == 0:
            # print(i, t, i - t)
            del_index.append(i - t)
            t = t + 1

    for item in del_index:
        del_data = np.delete(del_data, item, 1)
        del_data = np.delete(del_data, item, 0)

    names = ['Right turning', 'Left turning', 'Sniffing', 'Walking', 'Trembling', 'Climbing', 'Falling',
             'Immobility', 'Paralysis', 'Standing', 'Trotting', 'Grooming', 'Flight', 'Running', 'LORR', 'Stepping']

    color_list = ['#A86A74', '#CB4042', '#FF6E00', '#EF8C92', '#89BDDE',
                  '#FFB67F', '#FFC408', '#937DAD', '#478FB1', '#FFE2CC',
                  '#EFB4C5', '#1d953f', '#B34C5A', '#D35889', '#A8DBD9',
                  '#EACAC9']

    for item in del_index:
        del names[item]
        del color_list[item]

    return del_data, names, color_list


# explicit function to normalize array
def normalize_2d(matrix):
    norm = np.linalg.norm(matrix)
    matrix = matrix / norm  # normalized matrix
    return matrix


if __name__ == '__main__':

    # data loading

    a = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time1", state_name="Female_RoRR")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
                 r"/BeAMapping_correct",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_RoRR")  # Female_Wakefulness

    file_list_2 = []
    for item in b['Video_name'][0:10]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:/3D_behavior/Arousal_behavior/Arousal_result_all/Spontaneous_arousal/SP_Arousal_result_add2"
                 r"/BeAMapping_correct",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))
    
    file_list = file_list_2
    dataframe = b
    mouse_state = 'RORR'
    looming_time = 14
    Male_data = np.zeros((16, 16))
    Female_data = np.zeros((16, 16))
    for x in range(2, looming_time, 2):  # Adjusting time window
        state = "looming_time{}".format(x)
        for num in range(len(file_list)):  # Accessing individual mice
            sub_list1 = pre_data(file_list[num], dataframe, num, state=state)
            Male_data = Male_data + sub_list1

        for num in range(len(file_list_1)):
            sub_list2 = pre_data(file_list_1[num], a, num, state=state)
            Female_data = Female_data + sub_list2

        all_data = Male_data + Female_data

        del_data, names, colors = del_pre_data(all_data)
        all_data = np.zeros((16, 16))
        color = ListedColormap(colors)
        fig = plt.figure(figsize=(5, 5), dpi=300)
        ax = fig.add_subplot(111)
        chord_diagram(del_data, gap=0.03, use_gradient=True, sort='distance', cmap=color,
                      chord_colors=colors, fontcolor="grey", ax=ax, fontsize=10)

        # str_grd = "_gradient" if grads[0] else ""
        plt.xlabel('Time (s)', fontsize=15)
        plt.ylabel('Fraction', fontsize=15)
        plt.tight_layout()
        plt.show()
        plt.savefig('D:/3D_behavior/Arousal_behavior/Arousal_result_all/Analysis_result/State_convert/SP_Arousal_add'
                    '/all_v5/All_{}{}_10min_v9.tiff'.format(mouse_state, int(x / 2)), dpi=300)
        plt.close()
