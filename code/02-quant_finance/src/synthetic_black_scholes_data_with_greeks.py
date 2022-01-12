import scipy.stats
import math
import csv
import random

def value_call_option(strike, spot, maturity, dividend, discount, volatility):
  discounting = math.exp(- discount * maturity)
  div_yield = math.exp(- dividend * maturity)

  forward = spot * div_yield / discounting
  moneyness = math.log(forward / strike)
  var = volatility * math.sqrt(maturity)
  d1 = moneyness / var + .5 * var
  d2 = d1 - var

  price = discounting * (forward * scipy.stats.norm.cdf(d1)
                       - strike * scipy.stats.norm.cdf(d2))
  dCalldStrike = - discounting * scipy.stats.norm.cdf(d2)
  delta = div_yield * scipy.stats.norm.cdf(d1)
  theta = div_yield * spot * volatility * scipy.stats.norm.pdf(d1) * .5 / math.sqrt(maturity) \
        - discount * strike * dCalldStrike - dividend * spot * delta
  dCalldQ = - spot * maturity * delta
  dCalldR = - strike * maturity * dCalldStrike
  vega = spot * div_yield * scipy.stats.norm.pdf(d1) * math.sqrt(maturity)
  return price / strike, delta, theta / strike, dCalldQ / strike, dCalldR / strike, vega / strike

def synthetic_data(size=10000):
  random.seed(42)
  with open('../data/black_scholes_with_greeks.csv', 'w', newline='\n') as csvfile:
    saver = csv.writer(csvfile)
    for i in range(size):
      strike = random.uniform(7, 650)
      spot = random.uniform(10, 500)
      maturity = random.randint(1, 1095) / 365.
      dividend = random.uniform(.0,  .03)
      discount = random.uniform(.01, .03)
      volatility = random.uniform(.05, .9)

      price, delta, theta, epsilon, rho, vega = value_call_option(strike, spot, maturity, dividend, discount, volatility)
      saver.writerow([spot / strike, maturity, dividend, discount, volatility, price, delta, theta, epsilon, rho, vega])

if __name__ == '__main__':
  synthetic_data()
