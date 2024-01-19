# -*- coding:utf-8 -*-
# @FileName  :Arousal_correlation_matrix.py
# @Time      :2021/9/11 20:01
# @Author    :Yang Xu
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')

color_list = ['#845EC2', '#B39CD0', '#D65DB1', '#4FFBDF', '#FFC75F',
              '#D5CABD', '#B0A8B9', '#FF6F91', '#F9F871', '#D7E8F0',
              '#60DB73', '#E8575A', '#008B74', '#00C0A3', '#FF9671',
              '#93DEB1']


def search_csv(path=".", name=""):
    result = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search_csv(item_path, name)
        elif os.path.isfile(item_path):
            if name + ".csv" == item:
                # global csv_result
                # csv_result.append(name)
                result.append(item_path)
                # print(csv_result)
                # print(item_path + ";", end="")
                # result = item
    return result


def read_csv(path='.', name="", column="", element="", state_name=""):
    item_path = os.path.join(path, name)
    with open(item_path, 'rb') as f:
        csv_data = pd.read_excel(f, sheet_name=state_name)

    return csv_data


def pre_data(file_path, dataframe, num, state=""): # data prepocessing
    df1 = pd.read_csv(file_path)
    looming_time = int(dataframe.at[num, state])
    data = df1.iloc[looming_time - 5*30:looming_time+115*30, 1:2] 

    data1 = data.iloc[:, 0].tolist()

    class_type = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                  11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
    for line in data1:
        if line not in class_type:
            class_type[line] = 0

        else:
            class_type[line] += 1

    list_1 = list(class_type.values())

    return list_1


def sort_data(list_1):
    male_std = []
    for i in range(len(list_1)):
        male_1 = np.std(list_1[i])
        male_std.append(male_1)
    sort_list = []
    dictlist = list(dictionary.keys())
    dictlist.sort()

    # Print the corresponding key and value by traversing this list
    for key in dictlist:
        sort_list.append(dictionary[key])
    return sort_list


if __name__ == '__main__':

    """
        Loading Wakefulness data
    """
    a = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_Wakefulness")  # Male_Wakefulness

    file_list_1 = []
    for item in a['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_1.append(file_list1)
    file_list_1 = list(np.ravel(file_list_1))

    b = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx",
                 column="looming_time1", state_name="Female_Wakefulness")  # Female_Wakefulness

    file_list_2 = []
    for item in b['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list1 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_2.append(file_list1)
    file_list_2 = list(np.ravel(file_list_2))

    Male_list = []
    for i in range(len(file_list_1)):
        sub_list1 = pre_data(file_list_1[i], a, i, state="looming_time1")
        # print(sub_list1)
        Male_list.append(sub_list1)
    Male_list = sort_data(Male_list)

    Female_list = []
    for i in range(len(file_list_2)):
        sub_list2 = pre_data(file_list_2[i], b, i, state="looming_time1")
        # print(sub_list2)
        Female_list.append(sub_list2)
    Female_list = sorted(Female_list)

    Wake = Male_list + Female_list

    """
        Loading RORR data
    """
    c = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx", column="looming_time1", state_name="Male_RoRR")  # Male_Wakefulness

    file_list_3 = []
    for item in c['Video_name'][0:5]:
        item = item.replace("-camera-0", "")
        file_list3 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_3.append(file_list3)
    file_list_3 = list(np.ravel(file_list_3))

    d = read_csv(path=r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new',
                 name="video_info.xlsx",
                 column="looming_time1", state_name="Female_RoRR")  # Female_Wakefulness

    file_list_4 = []
    for item in d['Video_name'][0:6]:
        item = item.replace("-camera-0", "")
        file_list4 = search_csv(
            path=r"D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Arousal_result_final\looming_new\BeAOutputs\csv_file_output_new",
            name="{}_Movement_Labels".format(item))
        file_list_4.append(file_list4)
    file_list_4 = list(np.ravel(file_list_4))

    for j in range(1, 5, 1):
        RORR = []
        state = 'looming_time{}'.format(j)

        Male_RORR = []
        for i in range(len(file_list_3)):
            sub_list3 = pre_data(file_list_3[i], c, i, state=state)
            Male_RORR.append(sub_list3)

        Female_RORR = []
        for i in range(len(file_list_4)):
            sub_list4 = pre_data(file_list_4[i], d, i, state=state)
            Female_RORR.append(sub_list4)

        RORR = Male_RORR + Female_RORR

        all_list = Wake + RORR
    
        """
            heatmap plot
        """
        X = np.corrcoef(all_list)
        fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

        ax = sns.heatmap(X, center=0, cmap="vlag", yticklabels=False, xticklabels=False, vmin=-1, vmax=1)
        cbar = ax.collections[0].colorbar

        # here set the labelsize by 20
        cbar.ax.tick_params(labelsize=25)
        plt.tight_layout()
        plt.show()

        plt.savefig(r'D:\3D_behavior\Arousal_behavior\Arousal_analysis_new\Analysis\corr_matrix\looming'
                    '/Wake_RORR_looming_time{}_v23.tiff'.format(j), dpi=300, transparent=True)
        plt.close()
