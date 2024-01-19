# -*- coding: utf-8 -*-
"""
Created on Thu May  4 17:22:55 2023

@author: Jialin Ye
@institution: SIAT

"""

import os 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats
from scipy.interpolate import make_interp_spline
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import matplotlib.patheffects as pe




def get_path(file_dir,content):
    file_path_dict = {}
    for file_name in os.listdir(file_dir):
        if (file_name.startswith('rec-'))&(file_name.endswith(content)):
            USN = int(file_name.split('-')[1])            
            file_path_dict.setdefault(USN,file_dir+'\\'+file_name)
    return(file_path_dict)

def get_path2(file_dir,content):
    file_path_dict = {}
    for file_name in os.listdir(file_dir):
        if file_name.startswith('rec'):
            if file_name.endswith(content):
                USN = file_name.split('_')[0]
                #date = i.split('-')[3][0:8]
                #file_name = 'rec-{0}-G1-{1}'.format(USN,date)
                file_path_dict.setdefault(USN,file_dir+'\\'+file_name)
    return(file_path_dict)




animal_info_csv = r"G:/Arousal/Data analysis & graph/3D/Animal_information/CM_optogenetics_info1.csv"
#animal_info_csv = r"I:/3D/3D_Analysis/Sp_arousal_info.csv" #r"I:/3D/3D_Analysis/Sponteneous_wakefulness_arousal_info.csv"
animal_info = pd.read_csv(animal_info_csv)

Feature_space_dir_CM = r'G:/Arousal/Data analysis & graph/3D/Second round/CM_optogenetics/Analysis/Revised_BeAOutputs_v3'
#Feature_space_dir_Sp = r'I:/3D/3D_Analysis/Arousal_second_round/Spontenous arousal/Results_new/SP_Revised_data'

Feature_space_path = get_path2(Feature_space_dir_CM,'new_Feature_Space.csv')
movemment_label_path = get_path2(Feature_space_dir_CM,'Movement_Labels.csv')


movement_label_order = ['Running','Trotting','Walking','Stepping','Right_turning','Left_turning',
                        'Rising','Rearing','Climbing','Sniffing',
                        'Grooming',
                        'Immobility',
                        'Paralysis','Twitching',
                        'LORR']



def calculate_entroy(df):
    
    count_df = df['origin_label'].value_counts()
    mv_entroy = pd.DataFrame()
    #for mv in movement_label_order:
    for mv in range(1,41):   
        if mv in count_df.index:
            mv_count = count_df[mv]

        else:
            mv_count = 0
        mv_entroy.loc[mv,'count'] = mv_count
    
    #print(mv_entroy)
    entroy = scipy.stats.entropy(mv_entroy,base=2)
    #print(entroy)
    return(entroy)


 
def add_category(df):
    df_copy = df.copy()
    big_category_dict6 = {'locomotion':['running','trotting','walking','left_turning','right_turning','stepping'],
                     'exploration':['climbing','rearing','rising','sniffing'],
                     'maintenance':['grooming'],
                     'nap':['immobility'],
                     'post-anesthetix_ataxia':['paralysis','twitching'],
                     'anesthetic_posture':['LORR'],
                     }


    df_copy.loc[df_copy['movement_label'].isin(big_category_dict4['locomotion']),'category6'] = 'locomotion'
    df_copy.loc[df_copy['movement_label'].isin(big_category_dict4['exploration']),'category6'] = 'exploration'
    df_copy.loc[df_copy['movement_label'].isin(big_category_dict4['maintenance']),'category4'] = 'maintenance' 
    df_copy.loc[df_copy['movement_label'].isin(big_category_dict4['nap']),'category6'] = 'nap'
    df_copy.loc[df_copy['movement_label'].isin(big_category_dict4['post-anesthetix_ataxia']),'category6'] = 'post-anesthetix_ataxia'
    df_copy.loc[df_copy['movement_label'].isin(big_category_dict4['anesthetic_posture']),'category6'] = 'anesthetic_posture'
    return(df_copy)

     

df_trans_speed = pd.DataFrame()

step = 10

start = 0
end = 0
num = 0
for i in range(step,61,step):
      end = i *30*60
#movement_frequency_each_mice = []
      for index in animal_info.index:
          file_name = animal_info.loc[index,'video_index']
          group = animal_info.loc[index,'group']
   
     # for key in Feature_space_path_day.keys():
          FeA_data = pd.read_csv(Feature_space_path[file_name])
          Mov_data = pd.read_csv(movemment_label_path[file_name])
          #FeA_data = pd.read_csv(Feature_space_path2[file_name])
          #Mov_data = pd.read_csv(movemment_label_path2[file_name])        
        
          temp_df = FeA_data[(FeA_data['segBoundary_start']>start) & (FeA_data['segBoundary_end']<end)]
          Mov_data = Mov_data.iloc[start:end,:]
          #Mov_data = add_movement_label(Mov_data)
        
          #if  len(temp_df) == 0:
          #    print(start,end,file_name,temp_df)
          entropy = calculate_entroy(Mov_data)
          df_trans_speed.loc[num,'video_index'] = file_name
          df_trans_speed.loc[num,'group'] = group
          df_trans_speed.loc[num,'time_tag'] = i
          if  len(temp_df) == 0:
              df_trans_speed.loc[num,'trans_speed'] = len(temp_df) +1  # (len(temp_df) /1) * entroy
          else:
              df_trans_speed.loc[num,'trans_speed'] = len(temp_df) 
          df_trans_speed.loc[num,'entropy'] = entropy
          num += 1

      start = end        


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))



average_df = pd.DataFrame()
num = 0   
for i in range(step,61,step):
    for k in ['mCherry','ChR2']:
    #for k in ['Wakefulness','Post-anesthesia','ChR2','mCherry']:
        temp_df = df_trans_speed[(df_trans_speed['time_tag']==i) &(df_trans_speed['group']==k) ]
        average_trans_speed = np.mean(temp_df['trans_speed'])
        average_entropy = np.mean(temp_df['entropy'])
        average_df.loc[num,'time_tag'] = i
        average_df.loc[num,'group'] = k
        average_df.loc[num,'average_trans_speed'] = average_trans_speed
        average_df.loc[num,'average_entropy'] = average_entropy
        num += 1

        
color_list = {'mCherry':'#2a52be', 'ChR2':'#9f0000'}
#color_list = {'Wakefulness':'#000000', 'Post-anesthesia':'#9f0000', 'ChR2':'#9f0000', 'mCherry':'#2a52be'}
    

fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,5),dpi=300)
for k in  ['mCherry','ChR2']:
 #for k in  ['Wakefulness','Post-anesthesia','ChR2','mCherry']:
      ExperimentTime_df = average_df[average_df['group']==k]
      
      x = ExperimentTime_df['time_tag']
      y = ExperimentTime_df['average_entropy']
      x_smooth = np.linspace(x.min(), x.max(), 300)  # np.linspace 等差数列,从x.min()到x.max()生成300个数，便于后续插值
      y_smooth = make_interp_spline(x, y)(x_smooth)
      #min_max_scaler = preprocessing.MinMaxScaler()
      #normalized_y_smooth = NormalizeData(y_smooth)
      #ax.set_ylim(0,1)
      #ax.set_yticks([0.2,0.4,0.6,0.8,1.0])
      color = color_list[k]
      plt.plot(x_smooth, y_smooth, color = color, lw=3, path_effects=[pe.Stroke(linewidth=6, foreground=color,alpha=0.6), pe.Normal()])
 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)    

        
        
        
        
        
        
        
        
        
        