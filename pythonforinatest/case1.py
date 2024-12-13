import akshare as ak
import pandas as pd
# 导入FundInvestment类
from utils import FundInvestment


def get_fund_net_value(fund_code):
    """
    获取基金净值数据

    :param fund_code: 基金代码
    :return: 返回基金的净值数据
    """
    # 使用 akshare 提供的 fund_net_value 函数获取基金净值数据
    fund_data = ak.fund_net_value(fund_code=fund_code)
    # 数据清洗，确保日期是升序的
    fund_data = fund_data[['date', 'netValue']]
    fund_data['date'] = pd.to_datetime(fund_data['date'])
    fund_data = fund_data.sort_values(by='date', ascending=True)
    return fund_data


def main():
    # 基金代码：007539
    fund_code = "007539"

    # 获取基金007539的净值数据
    fund_data = get_fund_net_value(fund_code)

    # 获取2024/09/12的净值（假设2024/09/12的数据存在）
    start_date = pd.to_datetime("2024-09-12")
    start_data = fund_data[fund_data['date'] == start_date]

    if start_data.empty:
        print(f"未能找到2024/09/12的数据，请检查基金代码或日期范围。")
        return

    # 获取基金开始时的净值和当前净值
    start_nav = start_data.iloc[0]['netValue']
    current_nav = fund_data.iloc[-1]['netValue']  # 取最新的净值

    print(f"2024/09/12的净值: {start_nav}")
    print(f"当前的净值: {current_nav}")

    # 设置买入成本和份额
    buy_cost = 1.1138
    fund_share = 448.91

    # 创建FundInvestment对象
    investment = FundInvestment(buy_cost=buy_cost, current_value=current_nav, fund_share=fund_share)

    # 显示结果
    investment.display_results()


if __name__ == "__main__":
    main()
