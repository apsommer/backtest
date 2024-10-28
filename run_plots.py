import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# initialize plots
sns.set_style('darkgrid')
plt.rcParams['figure.figsize'] = [20, 12]

# example data
data = (yf.Ticker('AAPL').history(
    start='2007-12-01',
    end='2009-12-31',
    interval='1d'))

close = data.Close
close.plot()
plt.show()