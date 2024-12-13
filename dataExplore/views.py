import json
import pandas as pd
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
from uploadFile.models import NBA
import seaborn as sns
from django.db import models
from django.db.models import Count, F, Value as V
from django.db.models.functions import Cast, Replace
from django.db.models.fields import IntegerField


# Create your views here.
def data_explore(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        return HttpResponse(json.dumps({'result': explore(data)}), content_type='application/json')


def explore(data):
    match (data['text']):
        case '前10名球员':
            return function1(1)
        case '工资分布':
            return function2(2)
        case '球队排名':
            return function3(3)
        case '各国在NBA的参与度':
            return function4(4)
        case '球员的排名和工资的关系':
            return function5(5)
        case '球员身高和体重的分布':
            return function6(6)
        case '各球员的评分分布情况':
            return function7(7)
        case '各队伍人数情况':
            return function8(8)
        case '各球员身高分布':
            return function9(9)
        case '各球员体重分布':
            return function10(10)
        case '各球员工资区间分布情况':
            return function11(11)
        case '各球员选秀年份分布':
            return function12(12)
        case '各球员评分和工资的关系':
            return function13(13)
        case '工资排名':
            return function14(14)


# 前10名球员
def function1(id):
    # 获取评分最高的前10名球员
    top_players = NBA.objects.order_by('-rating')[:10]
    # 将数据转换为DataFrame
    top_players_df = pd.DataFrame.from_records(top_players.values())
    # 选择要显示的列
    columns_to_display = ['full_name', 'rating', 'jersey', 'country']
    # 筛选DataFrame以只包含所选列
    top_players_selected_df = top_players_df[columns_to_display]
    # 创建一个表格图来显示这些数据
    fig, ax = plt.subplots(figsize=(8, 5))  # 设置图片大小
    ax.axis('tight')
    ax.axis('off')
    # 创建表格，只显示选定的列
    ax.table(cellText=top_players_selected_df.values,
             colLabels=top_players_selected_df.columns,
             cellLoc='center', loc='center')
    plt.title('Top 10 NBA Players by Rating (Selected Data)')
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close(fig)
    return id


# 工资/工资分布
def function2(id):
    # 获取所有球员的工资数据
    salaries = NBA.objects.values_list('salary', flat=True)
    salaries_df = pd.DataFrame(salaries, columns=['salary'])
    # 将工资转换为数值型，以便分析
    salaries_df['salary'] = salaries_df['salary'].replace('[\$,]', '', regex=True).astype(float)
    # 绘制工资分布图
    plt.hist(salaries_df['salary'], bins=50)
    plt.title('Salary Distribution')
    plt.xlabel('Salary ($)')
    plt.ylabel('Number of Players')
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 球队排名
def function3(id):
    # 获取每个球队的评级平均值并按评级降序排列
    team_rankings = NBA.objects.values('team').annotate(team_rating_avg=models.Avg('rating')).order_by(
        '-team_rating_avg')
    # 将数据转换为DataFrame
    team_rankings_df = pd.DataFrame(team_rankings)
    # 创建颜色列表
    colors = plt.cm.tab20(np.linspace(0, 1, len(team_rankings_df)))
    # 创建条形图
    plt.figure(figsize=(16, 10))  # 设置图片大小
    plt.barh(team_rankings_df['team'], team_rankings_df['team_rating_avg'], color=colors)
    plt.xlabel('Average Rating')
    plt.ylabel('Team')
    plt.title('NBA Teams Average Rating')
    plt.gca().invert_yaxis()  # 反转y轴，使得顶部的条形图代表评级最高的球队
    plt.subplots_adjust(left=0.2)
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 各国在NBA的参与度
def function4(id):
    # 获取每个国家的球员数量
    country_participation = NBA.objects.values('country').annotate(player_count=models.Count('id'))
    # 将数据转换为DataFrame
    country_participation_df = pd.DataFrame(country_participation)
    # 创建颜色列表
    colors = plt.cm.tab20(np.linspace(0, 1, len(country_participation_df)))
    # 创建饼图
    plt.figure(figsize=(8, 8))  # 设置图片大小
    plt.pie(country_participation_df['player_count'],
            colors=colors,
            startangle=90)  # 移除了 autopct 参数
    # 计算每个国家的占比并格式化为两位小数
    percentages = country_participation_df['player_count'] / country_participation_df['player_count'].sum() * 100
    percentages_str = percentages.apply(lambda x: f"{x:.2f}%")
    # 创建颜色图例，并包含国家名称和占比
    labels_with_percentage = [f"{country} ({percentages_str.iloc[i]})"
                              for i, country in enumerate(country_participation_df['country'])]
    patches = [plt.plot([], [], marker="s", ls="", mec=None, color=colors[i],
                        markersize=10, label=labels_with_percentage[i])[0] for i in
               range(len(country_participation_df))]
    plt.legend(handles=patches, bbox_to_anchor=(0.95, 0.5), loc='center left', title="Countries")
    plt.title('NBA Players Country Participation')
    plt.axis('equal')  # 确保饼图是圆的
    plt.subplots_adjust(right=0.7)
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 球员的排名和工资的关系
def function5(id):
    # 获取评分最高的前10名球员
    top_players = NBA.objects.order_by('-rating')[:10]
    # 将数据转换为DataFrame
    top_players_df = pd.DataFrame.from_records(top_players.values())
    # 绘制排名与工资的关系图
    plt.scatter(top_players_df['rating'], top_players_df['salary'].replace('[\$,]', '', regex=True).astype(float))
    plt.title('Player Rating vs Salary')
    plt.xlabel('Rating')
    plt.ylabel('Salary ($)')
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 球员身高和体重的分布
def function6(id):
    # 获取所有NBA球员的数据
    players = NBA.objects.all()
    # 将数据转换为DataFrame
    df = pd.DataFrame(players.values())
    # 清洗身高数据，转换为英寸
    def clean_height(height_str):
        if pd.isnull(height_str):
            return None
        feet, inches = height_str.split('/')[0].split('-')
        return int(feet) * 12 + int(inches)

    df['height_in'] = df['height'].apply(clean_height)

    # 清洗体重数据，转换为磅
    def clean_weight(weight_str):
        if pd.isnull(weight_str):
            return None
        # 尝试提取磅数
        if 'lbs' in weight_str:
            pounds = weight_str.split(' ')[0]
            return float(pounds)
        # 如果没有磅数，尝试提取公斤数并转换为磅
        elif 'kg' in weight_str:
            kg = weight_str.split(' ')[0]
            return float(kg) * 2.20462
        return None
    df['weight_lbs'] = df['weight'].apply(clean_weight)
    # 过滤掉清洗后仍然为空的记录
    df = df.dropna(subset=['height_in', 'weight_lbs'])
    # 绘制身高和体重的散点图
    plt.figure(figsize=(16, 10))
    sns.scatterplot(x='height_in', y='weight_lbs', data=df)
    plt.title('Height vs Weight of NBA Players')
    plt.xlabel('Height (inches)')
    plt.ylabel('Weight (pounds)')
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 各球员的评分分布情况
def function7(id):
    rating_distribution = NBA.objects.values('rating').annotate(count=models.Count('rating')).order_by('rating')
    rating_distribution_df = pd.DataFrame(rating_distribution)
    # 绘制条形图
    rating_distribution_df.plot(kind='bar', x='rating', y='count', color='skyblue')
    plt.title('NBA Players Rating Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Number of Players')
    plt.xticks(rotation=45)  # 如果rating值较多，可以考虑旋转x轴标签以便阅读
    plt.grid(axis='y')
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 各队伍人数情况
def function8(id):
    team_distribution = NBA.objects.values('team').annotate(count=models.Count('id')).order_by('team')
    team_distribution_df = pd.DataFrame(team_distribution)
    # 绘制条形图
    team_distribution_df.plot(kind='bar', x='team', y='count', color='lightgreen')
    plt.title('NBA Teams Player Distribution')
    plt.xlabel('Team')
    plt.ylabel('Number of Players')
    plt.xticks(rotation=45, ha='right')  # 如果队伍名称较长，可以考虑旋转x轴标签以便阅读
    plt.tight_layout()  # 调整布局以适应x轴标签
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 各球员身高分布
def function9(id):
    df = pd.DataFrame(NBA.objects.all().values())

    # 清洗身高数据，转换为英寸
    def clean_height(height_str):
        if pd.isnull(height_str):
            return None
        feet, inches = height_str.split('/')[0].split('-')
        return int(feet) * 12 + int(inches)

    df['height_in'] = df['height'].apply(clean_height)
    # 过滤掉清洗后仍然为空的记录
    df = df.dropna(subset=['height_in'])
    # 绘制身高分布图
    sns.histplot(df['height_in'], bins=50, kde=True)
    plt.title('Height Distribution of NBA Players')
    plt.xlabel('Height (inches)')
    plt.ylabel('Frequency')
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 各球员体重分布
def function10(id):
    # 将数据转换为DataFrame
    df = pd.DataFrame(NBA.objects.all().values())

    # 清洗体重数据，转换为磅
    def clean_weight(weight_str):
        if pd.isnull(weight_str):
            return None
        # 尝试提取磅数
        if 'lbs' in weight_str:
            pounds = weight_str.split(' ')[0]
            return float(pounds)
        # 如果没有磅数，尝试提取公斤数并转换为磅
        elif 'kg' in weight_str:
            kg = weight_str.split(' ')[0]
            return float(kg) * 2.20462
        return None

    df['weight_lbs'] = df['weight'].apply(clean_weight)
    # 过滤掉清洗后仍然为空的记录
    df = df.dropna(subset=['weight_lbs'])
    # 绘制体重分布图
    sns.histplot(df['weight_lbs'], bins=50, kde=True)
    plt.title('Weight Distribution of NBA Players')
    plt.xlabel('Weight (pounds)')
    plt.ylabel('Frequency')
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 各球员工资区间分布情况
def function11(id):
    # 定义工资区间
    salary_ranges = [
        (0, 100000),
        (100001, 1000000),
        (1000001, 2500000),
        (2500001, 5000000),
        (7500001, 10000000),
        (10000001, 100000000),
    ]
    # 准备查询结果列表，用于存储每个区间的球员数量
    salary_counts = []
    # 查询数据库并统计每个工资区间的球员数量
    for lower, upper in salary_ranges:
        # 使用annotate来创建一个转换后的salary字段
        count = NBA.objects.annotate(
            salary_numeric=Cast(
                Replace(
                    Replace(F('salary'), V('$'), V('')),
                    V(','), V('')
                ),
                output_field=IntegerField()
            )
        ).filter(
            salary_numeric__gte=lower,
            salary_numeric__lt=upper if upper is not None else float('inf')
        ).count()
        salary_counts.append(count)
    # 创建饼图
    labels = [f'${lower}-{upper}' if upper is not None else f'$5000001 and above' for lower, upper in salary_ranges]
    plt.title('Player salary range distribution')
    plt.pie(salary_counts, labels=labels, autopct=lambda p: f'{p:.1f}%' if p > 0 else '', startangle=140)
    plt.axis('equal')  # 确保饼图是圆的
    plt.subplots_adjust(right=0.82)
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 各球员选秀年份分布
def function12(id):
    # 聚合查询，计算每个选秀年份的球员数量
    draft_year_counts = NBA.objects.values('draft_year').annotate(count=Count('id')).order_by('draft_year')
    # 准备数据用于绘图
    years = [entry['draft_year'] for entry in draft_year_counts if entry['draft_year'] is not None]
    counts = [entry['count'] for entry in draft_year_counts if entry['draft_year'] is not None]
    # 绘制条形图
    plt.bar(years, counts)
    # 设置图表标题和轴标签
    plt.title('NBA Players Draft Year Distribution')
    plt.xlabel('Draft Year')
    plt.ylabel('Number of Players')
    # 设置 x 轴刻度，如果年份跨度较大，可以调整刻度间隔
    plt.xticks(years)
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id


# 各球员评分和工资的关系
def function13(id):
    # 定义一个函数，将工资字符串转换为整数
    def parse_salary(salary_str):
        try:
            return int(salary_str.replace('$', ''))
        except (ValueError, TypeError):
            return None
    # 获取所有球员的评分和工资，并转换工资为整数
    players = NBA.objects.all().values_list('rating', 'salary')
    players_with_numbers = [(rating, parse_salary(salary)) for rating, salary in players if
                            rating is not None and parse_salary(salary) is not None]
    # 分离出评分和工资的数值列表
    ratings = [player[0] for player in players_with_numbers]
    salaries = [player[1] for player in players_with_numbers]
    # 绘制散点图
    plt.scatter(ratings, salaries)
    # 设置图表标题和轴标签
    plt.title('NBA Players Rating vs Salary')
    plt.xlabel('Rating')
    plt.ylabel('Salary')
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id

# 工资排名
def function14(id):
    # 定义一个函数，将工资字符串转换为整数
    def parse_salary(salary_str):
        try:
            return int(salary_str.replace('$', ''))
        except (ValueError, TypeError):
            return None
    # 获取所有球员的工资，并转换工资为整数，同时获取球员的全名
    players = NBA.objects.all().values_list('full_name', 'salary')
    players_with_numbers = [(name, parse_salary(salary)) for name, salary in players if
                            parse_salary(salary) is not None]
    # 按工资对球员进行排序（降序）
    sorted_players = sorted(players_with_numbers, key=lambda x: x[1], reverse=True)
    # 提取前N名球员的数据进行可视化（例如前10名）
    N = 10
    top_players = sorted_players[:N]
    # 分离出球员名称和工资的数值列表
    names = [player[0] for player in top_players]
    salaries = [player[1] for player in top_players]
    # 绘制条形图
    plt.barh(names, salaries)
    # 设置图表标题和轴标签
    plt.title('NBA Players Salary Ranking')
    plt.xlabel('Salary')
    plt.ylabel('Player Name')
    # 设置图表的y轴标签字体方向，使得标签可以垂直显示
    plt.yticks(rotation=0)
    plt.savefig('./vue-demo\src/assets\static/' +str(id) + '.png')
    plt.close()
    return id