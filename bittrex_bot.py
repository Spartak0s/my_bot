from bittrex.bittrex import Bittrex

key_file_name = '../bittrex.keys'
with open(key_file_name) as key_file:
	line_num = 0;
	for line in key_file:
		if(line_num==0):
			pub_key = line.rstrip('\n');
		elif(line_num==1):
			priv_key = line.rstrip('\n');
		line_num += 1

max_port_cur = 10;
portfolio = [dict() for x in range(max_port_cur)]

#init
my_bittrex = Bittrex(pub_key,priv_key)

#main loop for reading-values
#--------------------------------------------------------------------------------------
market_list = my_bittrex.get_markets()['result']
coin_list = my_bittrex.get_currencies()['result']
market_summaries = my_bittrex.get_market_summaries()['result']

#print available coins
for i in range(len(coin_list)):
	print(coin_list[i]['Currency'])

#print available market-trades
for i in range(len(market_list)):
	print(market_list[i]['MarketName'])

#vailable portfolio currencies
#--------------------------------------------------------------------------------------
#choice 1 slower
#port_index = 0;
#for i in range(len(coin_list)):
#	balance = my_bittrex.get_balance(coin_list[i]['Currency'])['result']['Balance']
#	#check if there is any balance and save it to portfolio dict
#	if((balance is None) or (balance == 0.0)):
#		balance_str = '0.000000'
#	else:
#		balance_str = '%.6f' % balance
#		portfolio[port_index]['name'] = coin_list[i]['Currency']
#		portfolio[port_index]['balance'] = balance;
#		print(coin_list[i]['Currency']+' '+ balance_str)
#		port_index += 1

#choice 2 faster (prefetch)
available_balances = my_bittrex.get_balances()['result']
port_index = 0;
for i in range(len(available_balances)):
	balance = available_balances[i]['Balance']
	if((balance is None) or (balance == 0.0)):
		balance_str = '0.000000'
	else:
		balance_str = '%.6f' % balance
		portfolio[port_index]['name'] = available_balances[i]['Currency']
		portfolio[port_index]['balance'] = balance;
		print(coin_list[i]['Currency']+' '+ balance_str)
		port_index += 1

#get information about each portfolio-market
#--------------------------------------------------------------------------------------
for i in range(port_index-1):
	tmp_name = portfolio[i]['name']
	my_bittrex.get_ticker(tmp_name)
	market_sum = my_bittrex.get_marketsummary(tmp_name)
	order_book = my_bittrex.get_orderbook(tmp_name)
	market_history = my_bittrex.get_market_history(tmp_name)

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

#market-list by currency
btc_markets = my_bittrex.list_markets_by_currency('ZCL')
btc_markets = my_bittrex.list_markets_by_currency('XRP')
