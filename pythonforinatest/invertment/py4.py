import pandas as pd
from openpyxl import load_workbook

# 假设你已经有一个results字典，包含每周的投资回报
results = {
    0: 49304.23,  # Monday
    1: 51027.01,  # Tuesday
    2: 51714.86,  # Wednesday
    3: 51875.18,  # Thursday
    4: 50314.66,  # Friday
    5: 199.00,  # Saturday
    6: 199.00  # Sunday
}

weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

# 读取现有的Excel文件
file_path = 'fund_returns.xlsx'

# 如果文件不存在，你可以创建一个初始的Excel文件
# 这里假设我们已有一个表头为：基金代码, Monday, Tuesday, Wednesday, Thursday, Friday 的Excel文件
df = pd.read_excel(file_path)

# 假设基金代码已经存在，我们直接更新这些周的回报数据
# 检查是否已有表头（基金代码, Monday, Tuesday, ...）
if '基金代码' in df.columns and all(weekday in df.columns for weekday in weekday_names):
    # 找到基金代码所在行，假设我们要更新的基金代码是 "510310"
    fund_code = '510310'  # 示例基金代码
    if fund_code in df['基金代码'].values:
        # 定位到对应的基金代码行
        row_index = df[df['基金代码'] == fund_code].index[0]

        # 更新对应的每个星期的回报数据
        for i, weekday in enumerate(weekday_names):
            df.at[row_index, weekday] = results[i]
    else:
        # 如果没有该基金代码，新增一行
        new_row = {'基金代码': fund_code}
        for i, weekday in enumerate(weekday_names):
            new_row[weekday] = results[i]

        # 使用pd.concat来替代df.append
        new_row_df = pd.DataFrame([new_row])

        # 清理掉所有全NA或空列
        new_row_df = new_row_df.dropna(axis=1, how='all')

        # 合并新行
        df = pd.concat([df, new_row_df], ignore_index=True)
else:
    print("Excel文件缺少基金代码或者星期几的列，无法更新数据。")

# 保存修改后的数据回Excel文件
df.to_excel(file_path, index=False)

print(f"数据已成功插入至基金代码 {fund_code} 对应的行！")
