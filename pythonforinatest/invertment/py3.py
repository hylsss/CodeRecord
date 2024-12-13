import os
import re
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt


# 获取基金历史数据
def fetch_fund_data(code, start_date, end_date):
    return ak.fund_etf_fund_info_em(fund=code, start_date=start_date, end_date=end_date)


# 清洗数据并保存为Excel
def clean_and_save_data(fund_etf_fund_info_em_df, code):
    try:
        # 删除不需要的列
        fund_etf_hist_em_df = fund_etf_fund_info_em_df.drop(columns=['累计净值', '申购状态', '赎回状态', '日增长率'],
                                                            errors='ignore')

        # 检查是否存在"净值日期"列
        if '净值日期' in fund_etf_hist_em_df.columns:
            # 转换日期格式
            fund_etf_hist_em_df['净值日期'] = pd.to_datetime(fund_etf_hist_em_df['净值日期'], errors='coerce')

            # 确保日期格式化无误
            fund_etf_hist_em_df['净值日期'] = fund_etf_hist_em_df['净值日期'].dt.strftime('%Y-%m-%d')

            # 保存为Excel文件
            output_file_path = f"fund_etf_{code}.xlsx"

            if os.path.exists(output_file_path):
                os.remove(output_file_path)
                print(f"文件 {output_file_path} 已存在，已删除原文件。")

            fund_etf_hist_em_df.to_excel(output_file_path, index=False)

            print(f"数据已保存到 {output_file_path}")
        else:
            print("数据中没有'净值日期'列，无法进行日期转换。")

        return fund_etf_hist_em_df

    except Exception as e:
        print(f"发生错误: {e}")
        return pd.DataFrame()  # 返回一个空的DataFrame以便后续处理


# 加载基金数据
def load_fund_data(file_path):
    # 加载数据时，确保 '净值日期' 列被转换为 datetime 类型
    df = pd.read_excel(file_path, parse_dates=['净值日期'])
    df.set_index('净值日期', inplace=True)
    return df


def calculate_investment_return(df, start_date, end_date, weekly_day):
    # 确保 start_date 和 end_date 转换为 datetime 类型
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # 根据传入的日期和定投的星期几筛选数据
    df_filtered = df[(df.index >= start_date) & (df.index <= end_date)]
    df_filtered = df_filtered[df_filtered.index.weekday == weekly_day]

    # 每次定投的金额为1元
    total_units = 0

    # 累积定投获得的基金单位数
    for idx, row in df_filtered.iterrows():
        total_units += 200 / row['单位净值']  # 若每次定投金额是200元，这里可以根据实际需求调整

    # 最终回报计算
    final_value = df_filtered.iloc[-1]['单位净值']
    total_investment = len(df_filtered)  # 投入的次数，即定投的份数
    total_investment_value = total_investment  # 每次投入1元
    total_final_value = total_units * final_value

    return total_final_value - total_investment_value  # 回报 = 最终净值 - 投入的金额


# 分析每周定投效果
def analyze_weekly_investment(df, start_date, end_date):
    results = {}

    for weekday in range(5):  # 0=Monday, 1=Tuesday, ..., 6=Sunday
        investment_return = calculate_investment_return(df, start_date, end_date, weekday)
        results[weekday] = investment_return
        # print("log值", results)

    # 输出不同星期几定投的回报结果
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for weekday, return_value in results.items():
        print(f"{weekday_names[weekday]}: {return_value:.2f}")

    # 找到回报最高的星期几
    best_weekday = max(results, key=results.get)
    print(f"\n最划算的定投星期是: {weekday_names[best_weekday]}")

    return results  # 返回分析结果以便可视化


# 可视化分析结果
def plot_investment_results(results):
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    values = list(results.values())

    plt.bar(weekday_names, values)
    plt.title('Weekday Investment Returns')
    plt.xlabel('Day of the Week')
    plt.ylabel('Return (元)')
    plt.show()


def parse_weekly_returns(log_data):
    # 用正则表达式提取每周回报数据
    results = {}
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # 修改正则表达式，去掉了 "Total return =" 和 "元" 部分
    pattern = r'(\w+): (\d+\.\d+)'  # 只匹配星期和数字

    # 使用正则表达式查找所有匹配项
    matches = re.findall(pattern, log_data)
    print(matches)

    # 填充字典
    for i, match in enumerate(matches):
        weekday, return_value = match
        results[weekday] = float(return_value)

    return results

def fill_excel_with_weekly_returns(file_path, fund_code, log_data, start_date, end_date):
    # 解析控制台日志数据
    weekly_returns = parse_weekly_returns(log_data)
    print('asd',weekly_returns)

    # 创建一个新的数据字典
    new_data = {
        '基金代码': fund_code,
        'start_date': start_date,
        'end_date': end_date
    }

    # 填充每周回报数据
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for weekday in weekday_names:
        new_data[weekday] = weekly_returns.get(weekday, 0.0)  # 如果没找到该星期，默认为 0.0

    # 创建 DataFrame
    new_row_df = pd.DataFrame([new_data])

    # 检查 Excel 文件是否存在
    if os.path.exists(file_path):
        # 如果文件存在，读取它
        df = pd.read_excel(file_path)

        # 如果基金代码已经存在，更新对应的行；否则，添加新的行
        if fund_code in df['基金代码'].values:
            row_index = df[df['基金代码'] == fund_code].index[0]
            for weekday in weekday_names + ['start_date', 'end_date']:
                df.at[row_index, weekday] = new_data[weekday]
        else:
            # 如果基金代码不存在，则追加新行
            df = pd.concat([df, new_row_df], ignore_index=True)
    else:
        # 如果文件不存在，直接创建 DataFrame
        df = new_row_df

    # 保存更新后的数据回 Excel 文件
    df.to_excel(file_path, index=False)

    print(f"数据已成功插入或更新至 {file_path} 中！")



if __name__ == "__main__":
    # 输入基金代码和数据日期范围
    code = "000965"
    start_date = '2020-01-04'
    end_date = '2024-12-10'

    # 获取基金历史数据
    fund_data = fetch_fund_data(code, start_date, end_date)

    # 清洗数据并保存
    fund_data_cleaned = clean_and_save_data(fund_data, code)

    # 检查是否清洗后的数据为空
    if fund_data_cleaned.empty:
        print("清洗后的数据为空，请检查数据处理流程。")
        exit()

    # 加载清洗后的数据
    output_file_path = f"fund_etf_{code}.xlsx"
    df = load_fund_data(output_file_path)

    # 分析每周不同定投日期的效果
    results = analyze_weekly_investment(df, start_date, end_date)

    log_data = str(results)
    # 可视化定投效果
    plot_investment_results(results)

    fill_excel_with_weekly_returns('py_fund.xlsx', code, log_data, start_date, end_date)
