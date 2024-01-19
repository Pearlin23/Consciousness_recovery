# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 10:16:58 2023

@author: zyl
"""



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取Excel文件
df = pd.read_excel('G:/Arousal/Data_analysis_graph/EEGEMG/v29/EEG_withlooming/20200926_M1/20200926_M1_EEG1_Post-RORR15_1min_cFFT.xlsx')

# 转置DataFrame以便横纵坐标交换
df_t = df.T

# 删除第一列
data = df_t.iloc[1:,:]

# 将字符串转换为浮点数
data = data.astype(float)

# 反转DataFrame的行名
data = data.reindex(index=data.index[::-1])

# 自定义热力图参数
cmap = plt.cm.get_cmap('RdBu_r')  # 颜色映射
vmin = 0.0  # 颜色映射最小值（默认为数据集中的最小值）
vmax = 60.0  # 颜色映射最大值（默认为数据集中的最大值）
figsize = (0.2, 1.5)  # 图片大小（宽度，高度）
cbar_kws = {'label': 'Power', 'orientation': 'vertical'}  # 颜色条参数


# 绘制热力图
sns.set_style('whitegrid')  # 设置背景样式
ax = sns.heatmap(data, cmap=cmap, xticklabels=data.columns, yticklabels=data.index, vmin=vmin, vmax=vmax, cbar_kws=cbar_kws)
ax.set_xlabel('')  # 去掉x轴标签
ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)  # 去掉x轴标尺
# 设置纵轴上的刻度位置和标签
yticks = list(range(0, len(data), 5))
yticklabels = data.index[::5]
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)


plt.gcf().set_size_inches(figsize)  # 设置画布大小
plt.gcf().set_dpi(300)  # 设置分辨率
#plt.subplots_adjust(bottom=0.2)  # 调整主图和scale bar之间的距离

plt.show()



