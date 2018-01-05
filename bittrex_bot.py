from bittrex.bittrex import Bittrex
from time import gmtime, strftime

# import keys from bittrex.keys file
key_file_name = '../bittrex.keys'
with open(key_file_name) as key_file:
	line_num = 0;
	for line in key_file:
		if(line_num==0):
			pub_key = line.rstrip('\n')
		elif(line_num==1):
			priv_key = line.rstrip('\n')
		line_num += 1

# constants
debug = 1
max_port_cur = 15
portfolio = [dict() for x in range(max_port_cur)]
# bitcoin momentum constants
btc_gain_check = 1+ 0.02
btc_prices_length = 50
btc_prices = [0] * btc_prices_length
btc_index = 0

#init
my_bittrex = Bittrex(pub_key,priv_key)

#wait for bitcoin-prices initialization
for i in range(btc_prices_length):
	btc_tmp = my_bittrex.get_ticker('USDT-BTC')['result']
	btc_prices[btc_index] = btc_tmp['Last']
	btc_index = (btc_index + 1) % btc_prices_length
print(btc_prices)

#main loop for reading-values
#--------------------------------------------------------------------------------------
market_list = my_bittrex.get_markets()['result']
coin_list = my_bittrex.get_currencies()['result']
market_summaries = my_bittrex.get_market_summaries()['result']

if(debug):
	#print available coins
	for i in range(len(coin_list)):
		print(coin_list[i]['Currency'])

	#print available market-trades
	for i in range(len(market_list)):
		print(market_list[i]['MarketName'])

#available portfolio currencies
#--------------------------------------------------------------------------------------
available_balances = my_bittrex.get_balances()['result']
port_index = 0;
for i in range(len(available_balances)):
	balance = available_balances[i]['Balance']
	if(not((balance is None) or (balance == 0.0))):
		balance_str = '%.6f' % balance
		portfolio[port_index]['name'] = available_balances[i]['Currency']
		portfolio[port_index]['Balance'] = balance;
		print(available_balances[i]['Currency']+' '+ balance_str)
		port_index += 1
portfolio_currencies = port_index -1

#market-list by portfolio-currencies
for i in range(portfolio_currencies):
	portfolio[i]['Markets'] = my_bittrex.list_markets_by_currency(portfolio[i]['name'])
	print(portfolio[i]['name'] + ':' + str(portfolio[i]['Balance']))
	print(portfolio[i]['Markets'])
	print('\n')

#get information about each portfolio-market
#--------------------------------------------------------------------------------------
while(1):
	#1st logic: check for bitcoin movement constantly
	btc_tmp = my_bittrex.get_ticker('USDT-BTC')['result']
	btc_prices[btc_index] = btc_tmp['Last']
	btc_index_last = btc_index;
	btc_index = (btc_index + 1) % btc_prices_length
	if((btc_gain_check* btc_prices[(btc_index_last-5) % btc_prices_length]) <= (btc_prices[btc_index_last])):
		if(debug):
			print(btc_prices)
			print((btc_prices[(btc_index_last-5) % btc_prices_length]))
			print((btc_prices[btc_index_last]))
		print('Pump BUY signal' + strftime("%Y-%m-%d %H:%M:%S",gmtime()) )
	elif((btc_prices[(btc_index_last-5) % btc_prices_length]) >= (btc_gain_check * btc_prices[btc_index_last])):
		if(debug):
			print(btc_prices)
			print((btc_prices[(btc_index_last-5) % btc_prices_length]))
			print((btc_prices[btc_index_last]))
		print('Dump SELL signal' + strftime("%Y-%m-%d %H:%M:%S",gmtime()) )
	#2nd logic
	for i in range(portfolio_currencies):
		tmp_name = portfolio[i]['name']
		if(tmp_name == 'BTC'):
			tmp_name = 'USDT-BTC'
		elif(tmp_name != 'USDT'):
			tmp_name = 'BTC-'+tmp_name
		else:
			continue
		tmp_msg = my_bittrex.get_ticker(tmp_name)
		if(tmp_msg['success'] == True):
			if(debug):
				print(my_bittrex.get_market_history(tmp_name))
			portfolio[i]['Bid'] = tmp_msg['result']['Bid']
			portfolio[i]['Ask'] = tmp_msg['result']['Ask']
			#draft check of calling
			market_sum = my_bittrex.get_marketsummary(tmp_name)
			order_book = my_bittrex.get_orderbook(tmp_name)
			# Task 1.2: insert logic here which checks ids that are not in db
			# and inserts them correctly
			portfolio[i]['transactions'] = my_bittrex.get_market_history(tmp_name)
		

#buy-order example
#tmp_name = portfolio[1]['name']
#quantity = 1
#rate = 0.2
#my_bittrex.buy_limit(tmp_name,quantity,rate)

#sell-order example
#tmp_name = portfolio[1]['name']
#quantity = 1
#rate = 0.2
#my_bittrex.sell_limit(tmp_name,quantity,rate)

#cancel order
#uuid = 1
#my_bittrex.cancel(uuid)
	
#get open orders
open_orders = my_bittrex.get_open_orders()['result']
#or specific coin
tmp_open_order = my_bittrex.get_open_orders('BTC-ETH')

#order history
order_history = my_bittrex.get_order_history()['result']
