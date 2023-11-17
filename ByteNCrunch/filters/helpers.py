'''
Byte&Crunch Commission Rates
	Less than 200 - 250
	Between 200 and 800 - 300
	Between 800 and 1500 - 400
	Between 1500 and 3000 - 500
	Above 3000 - 700   


'''


def compute_rates(price):
    rate = 0
    if price < 200:
        rate = 250
    elif price in range(200-1,800):
        rate = 300
    elif price in range(800-1,1500):
        rate = 400
    elif price in range(1500-1,3000):
        rate = 500
    elif price >= 3000:
        rate = 700

    return rate
    