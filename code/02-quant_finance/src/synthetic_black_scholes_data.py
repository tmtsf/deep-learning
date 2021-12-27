import scipy.stats
import math
import csv
import random

def value_call_option(strike, spot, maturity, dividend, discount, volatility):
  forward = spot * math.exp((discount - dividend) * maturity)
  moneyness = math.log(forward / strike)
  var = volatility * math.sqrt(maturity)
  d1 = moneyness / var + .5 * var
  d2 = d1 - var

  discounting = math.exp(- discount * maturity)
  return discounting * (forward * scipy.stats.norm.cdf(d1)
                       - strike * scipy.stats.norm.cdf(d2))

def synthetic_data():
  random.seed(42)
  with open('../data/black_scholes.csv', 'w', newline='\n') as csvfile:
    saver = csv.writer(csvfile)
    for i in range(10000):
      strike = random.uniform(7, 650)
      spot = random.uniform(10, 500)
      maturity = random.randint(1, 1095) / 365.
      dividend = random.uniform(.0,  .03)
      discount = random.uniform(.01, .03)
      volatility = random.uniform(.05, .9)

      price = value_call_option(strike, spot, maturity, dividend, discount, volatility) / strike
      saver.writerow([spot / strike, maturity, dividend, discount, volatility, price])

if __name__ == '__main__':
  synthetic_data()
