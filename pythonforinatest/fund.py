import os
import akshare as ak
import pandas as pd
from datetime import datetime
from utils import FundInvestment

today = datetime.today().strftime('%Y%m%d')
print(today)

# 假设你有这些投资参数
funds = [
    {"code": "018897", "start_date": "20241120", "end_date": "20241202", "buy_cost": 1.2574, "fund_share": 397.65},
    {"code": "007539", "start_date": "20241119", "end_date": "20241202", "buy_cost": 1.1895, "fund_share": 420.34},
    {"code": "014678", "start_date": "20241112", "end_date": "20241202", "buy_cost": 1.0941, "fund_share": 1827.95},
    # 可以继续添加更多基金
]

# 遍历每只基金
for fund in funds:
    code = fund["code"]
    start_date = fund["start_date"]
    end_date = today
    buy_cost = fund["buy_cost"]
    fund_share = fund["fund_share"]

    # 获取基金数据
    fund_etf_hist_em_df = ak.fund_etf_fund_info_em(fund=code, start_date=start_date, end_date=end_date)

    # 插入基金代码列
    fund_etf_hist_em_df.insert(1, '基金代码', code)

    # 删除不需要的列
    fund_etf_hist_em_df = fund_etf_hist_em_df.drop(columns=['申购状态', '赎回状态', '日增长率'], errors='ignore')

    # 输出数据（检查列名）
    # print(fund_etf_hist_em_df.head())  # 查看前几行数据，检查列名
    print(fund_etf_hist_em_df)


    def calculate_daily_return(row, buy_cost, fund_share):
        # 获取当前的单位净值
        current_value = row['单位净值']

        # 创建 FundInvestment 实例，计算收益率
        investment = FundInvestment(buy_cost=buy_cost, current_value=current_value, fund_share=fund_share)

        # 获取百分比变化，即收益率
        total_money = investment.percentage_change()

        return total_money

    def calculate_daily_income(row, buy_cost, fund_share):
        # 获取当前的单位净值
        current_value = row['单位净值']

        # 创建 FundInvestment 实例，计算收益率
        investment = FundInvestment(buy_cost=buy_cost, current_value=current_value, fund_share=fund_share)

        # 获取百分比变化，即收益率
        total_income = investment.current_fund_value()

        return total_income


    # 确保基金数据中有 '净值日期' 列
    if '净值日期' in fund_etf_hist_em_df.columns:
        # 转换日期格式
        fund_etf_hist_em_df['净值日期'] = pd.to_datetime(fund_etf_hist_em_df['净值日期'], errors='coerce')
        fund_etf_hist_em_df['净值日期'] = fund_etf_hist_em_df['净值日期'].dt.strftime('%Y-%m-%d')

    # 计算每日收益率
    fund_etf_hist_em_df['每日收益率'] = fund_etf_hist_em_df.apply(calculate_daily_return, axis=1, args=(buy_cost, fund_share))
    # 计算总收益金额
    fund_etf_hist_em_df['总收益金额'] = fund_etf_hist_em_df.apply(calculate_daily_income, axis=1, args=(buy_cost, fund_share))

    # 保存到 Excel
    output_file_path = f"fund_etf_{code}.xlsx"

    if os.path.exists(output_file_path):
        os.remove(output_file_path)
        print(f"文件 {output_file_path} 已存在，已删除原文件。")

    fund_etf_hist_em_df.to_excel(output_file_path, index=False)

    print(f"数据已保存到 {output_file_path}")

    # 读取保存的 Excel 文件
    df = pd.read_excel(output_file_path)

    # 打印列名，确保引用正确
    print("Excel列名：", df.columns)
