## Problem statemt 
Financial markets often react to economic stress after it has already started. The objective of the Economic Earthquake Detector is to identify periods of systemic risk by combining macroeconomic indicators and cross-asset market behavior into a unified Economic Earthquake Index (EEI).

##Term i used :
1. ###Economic earthquake :- Its basically a period where multiple asset classes simultaneously exhibit abnormal behavior due to underlying macroeconomic stress. like The Covid crash , banking stress of 2023.

##Assets i used :
I used yfinance to collect given data of past 10 years containing around 32k rows.
| Asset Class      | Asset        |
| ---------------- | ------------ |
| Equity           | S&P500       |
| Volatility       | VIX          |
| Interest Rates   | TNX          |
| Bonds            | TLT          |
| Commodities      | Gold, Oil    |
| Forex            | EUR/USD, JPY |
| Crypto           | BTC, ETH     |
| Technology       | SOXX         |
| Emerging Markets | EEM          |

##Economic indiators
I used FRED's API to collect these data which is for around 70 years.
| Indicator | Purpose         |
| --------- | --------------- |
| CPI       | Inflation       |
| UNRATE    | Labor Stress    |
| FEDFUNDS  | Monetary Policy |
| GDP       | Economic Growth |
| USREC     | Recession Label |

##Feature categories
I made 4 stages or classes of features to tackle all the required components i needed,
1. Trend features usinG exponential moving average of past 7 , 30 and 90 days
2. Risk features like daily return, rolling volatility , drawdown 
3. Macro features like inflation shock,yield shock 
4. My features that designed to capture my goal like Flight To Safety Index, Contagion Index, Correlation Breakdown
5. My MVP :
     Cross-Asset Contagion Index (CACI) : the idea behind this is for everyday, it will count for how many assest classes are behaving abnormally and will give score , i use simple fraction to give score.

