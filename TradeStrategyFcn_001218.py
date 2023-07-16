import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import figure
def TradeStrategyFcn_001218(data  ,BuyRepeatDays,SellRepeatDays,EnterCommission,ExitCommission ,PlotIndex  ):
    data['RecomV'] = 0
    RecomIndex = 0
    InDaysNo = 0
    Efficiency = 1
    index=list(data.index)
    EnterClosePrice=data.at[index[0],'close']
    TotalTransactionsNo = 0
    PositiveTransactionsNo = 0
    EnterDay = 0

    sum_TransactionEfficiency = 0
    sum_disAdvantage_Efficiency = 0
    NegativeTransactionsNo = 0
    for j in range(data.shape[0]-600,data.shape[0]):
        if   j>BuyRepeatDays and data.at[index[j]-2,'Label']==1 and data.at[index[j]-1,'Label']==1 and data.at[index[j],'Tag']==1 and  (data.at[index[j],'close']/data.at[index[j]-2,'close'])>1.03 and RecomIndex == 0:
            data.at[index[j],'RecomV']=  1
            RecomIndex = 1
            EnterDay = j
            EnterClosePrice = data.at[index[j],'close']
        else:
            if ( j>SellRepeatDays and (((data.at[index[j]-2,'Label']==-1 and data.at[index[j]-1,'Label']==-1 and data.at[index[j],'Tag']==-1) and  (data.at[index[j],'close']/data.at[index[j]-2,'close'])<0.97 and ((j - EnterDay) > 3)) or ((data.at[index[j],'close'] / EnterClosePrice) < 0.9) )and RecomIndex == 1):
                data.at[index[j],'RecomV']= - 1
                RecomIndex = 0
                ExitDay = j
                InDaysNo = InDaysNo + (ExitDay - EnterDay)
                ExitClosePrice =  data.at[index[j],'close']
                TransactionEfficiency = (((1 - ExitCommission) * ExitClosePrice) / ((1 + EnterCommission) * EnterClosePrice))
                Efficiency = Efficiency * TransactionEfficiency
                TotalTransactionsNo = TotalTransactionsNo + 1
                if TransactionEfficiency > 1:
                    PositiveTransactionsNo = PositiveTransactionsNo + 1
                else:
                    sum_TransactionEfficiency = sum_TransactionEfficiency + TransactionEfficiency
                    sum_disAdvantage_Efficiency = sum_disAdvantage_Efficiency + Efficiency
                    NegativeTransactionsNo = NegativeTransactionsNo + 1
    
    BaseEfficiency=data['close'].tail(1).item()/data['close'].head(1).item()
    TestDays = data.shape[0]
    DaysV = list(range(1, data.shape[0]+1))
    data['DaysV'] = pd.Series(DaysV).values
    if PlotIndex == 1:
         fig=figure()
         # dataB=data.loc[data['RecomV']==1,['DaysV','close']]
         plt.plot(data['DaysV'], data['close'],color='blue')
         plt.scatter(data.loc[data['RecomV']==1,['DaysV']],data.loc[data['RecomV']==1,['close']],edgecolor ="green")
         dataS = data.loc[data['RecomV'] == -1, ['DaysV', 'close']]
         plt.scatter(data.loc[data['RecomV'] == -1, ['DaysV']],data.loc[data['RecomV'] == -1, [ 'close']],edgecolor ="red")
         plt.legend(['Close Price','Buy','Sell'])
         plt.xlim(DaysV[0],DaysV[-1])
         plt.xlabel(' Live Test Days No.')
         plt.ylabel(' Price ')


    return fig,Efficiency,BaseEfficiency,InDaysNo,TestDays,TotalTransactionsNo,PositiveTransactionsNo