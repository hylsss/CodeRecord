class FundInvestment:
    def __init__(self, buy_cost, current_value, fund_share):
        ###buy_cost:买入的价格
        ###current_value:当前价格
        ###fund_share:买入份额
        self.buy_cost = buy_cost
        self.current_value = current_value
        self.fund_share = fund_share

    # 计算总成本
    def total_cost(self):
        return self.buy_cost * self.fund_share


    def current_fund_total_value(self):
        return self.current_value * self.fund_share

    ###计算总收益
    def current_fund_value(self):
        total_value = self.current_fund_total_value() - self.total_cost()
        return total_value

    ###计算买入后的涨幅
    def percentage_change(self):
        # return ((self.current_value - self.buy_cost) / self.buy_cost) * 100
        return f"{((self.current_value - self.buy_cost) / self.buy_cost) * 100:.2f}%"
    def display_results(self) -> object:
        """
        显示收益和涨幅

        :param current_nav: 当前基金的净值
        """
        print(f"买入成本总额: {self.total_cost():.2f} 元")
        print(f"当前基金市值: {self.current_value:.2f} 元")
        print(f"收益: {self.current_fund_value():.2f} 元")
        print(f"涨幅: {self.percentage_change():.2f} %")
