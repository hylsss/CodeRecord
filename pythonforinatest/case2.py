import akshare as ak
import pandas as pd

# 获取基金排名数据
fund_open_fund_rank_em_df = ak.fund_open_fund_rank_em(symbol="股票型")
print(fund_open_fund_rank_em_df)

# 确保日期列是datetime类型
if '日期' in fund_open_fund_rank_em_df.columns:
    # 将字符串类型的日期转换为datetime类型，并格式化为'YYYY-MM-DD'格式的字符串
    fund_open_fund_rank_em_df['日期'] = pd.to_datetime(fund_open_fund_rank_em_df['日期']).dt.strftime('%Y-%m-%d')

output_file_path = "fund_rank.xlsx"  # 指定输出文件的路径和文件名
fund_open_fund_rank_em_df.to_excel(output_file_path, index=False)

print(f"基金排名数据已保存到 {output_file_path}")