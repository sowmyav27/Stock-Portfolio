from __future__ import unicode_literals
import json
from pytz import timezone
from django.template import loader
import plotly.offline as opy
import plotly.graph_objs as go
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
from django.views.generic import TemplateView
import matplotlib.pyplot as plt 

#global variables declared to be used accross functions
stock_names=[]
stock_closings = []
stock_openPrice = []
stock_divs = []
stock_names = []
stock_symbols = []
stock_weights = []
stock_details = []
count = 0
types = []
stock_values = []

#function to map the symbols and the stock names from two different APIs - alphavantage API and TRADIER API
#function also returns a json format data with the symbol name, closing price, value 
def getDetailsOfStock(symbol):
    url = "https://www.alphavantage.co/query?apikey=96QILYKIW036UJW9&function=TIME_SERIES_DAILY&symbol="+symbol
    response = requests.get(url)
    body = response.json()
    d = body['Time Series (Daily)']
    data_temp = []
    n=0

    headr = {"Accept":"application/json", "Authorization":"Bearer JIhRpxG1YcwcUZlK6hR5wtsEAvjI"}
    url = "https://sandbox.tradier.com/v1/markets/quotes?symbols=" + symbol
    name_response = requests.get(url, headers=headr)
    name = name_response.json()['quotes']['quote']['description']
    
    keys = []
    values = []
    for k,v in d.items():
        temp = json.dumps(v)
        data_temp.append(temp)
        keys.append(k)
        values.append(json.loads(temp)['4. close'])
        n = n+1
        if n>31:
            break

    todayData = json.loads(data_temp[0])
    today_close = todayData['4. close']
    today_open = todayData['1. open']
    detailsJson = {'symbol':symbol,'name' : name,'openPrice' : f"{float(today_open):.2f}",'closePrice' : f"{float(today_close):.2f}",'currency' : 'USD','keys':keys,'value':values}
    return detailsJson

#function which generates the graph plot for a symbol given the x axis and y axis values.
def get_plot(x_val,y_val,symb,name):
    
    trace1 = go.Scatter(x=x_val,y=y_val,fill='tonexty')
    data=go.Data([trace1])
    layout=go.Layout(title="Weekly Stats of "+symb,xaxis={'title':'Date'},yaxis={'title':'Closing Value of the stock'},width=380,height=340)
    figure=go.Figure(data=data,layout=layout)
    div_graph = opy.plot(figure, auto_open=False, output_type='div')
    return div_graph

#Views/templates
#index view or the main page view.
@csrf_exempt
def index_view(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

#details view, which lists out the stocks/ symbols and the amount to invest in each of them
@csrf_exempt
def details_view(request):
    global stock_names
    stock_names=[]
    global stock_closings 
    stock_closings = []
    global stock_openPrice 
    stock_openPrice = []
    global stock_divs 
    stock_divs = []
    global stock_symbols
    stock_symbols = []
    global stock_weights
    stock_weights = []
    global stock_details
    stock_details = []
    global count 
    count = 1
    global types
    types = []
    global stock_values 
    stock_values = []
    if request.method == 'POST':
        isEthical = request.POST.get('ethicalInvesting')
        isGrowth = request.POST.get('growthInvesting')
        isIndex = request.POST.get('indexInvesting')
        jsonCompanies = '{"strategy":{"Ethical Investing":[{"name":"AAPL","percentage_Symbol":"55"},{"name":"GOOG","percentage_Symbol":"25"},{"name":"NSRGY","percentage_Symbol":"5"},{"name":"SBUX","percentage_Symbol":"15"}],"Growth Investing":[{"name":"QCOM","percentage_Symbol":"10"},{"name":"ADBE","percentage_Symbol":"30"},{"name":"GOOG","percentage_Symbol":"45"},{"name":"CSCO","percentage_Symbol":"15"}],"Index Investing":[{"name":"VFINX","percentage_Symbol":"50"},{"name":"SWPPX","percentage_Symbol":"25"},{"name":"PREIX","percentage_Symbol":"15"},{"name":"IUSV","percentage_Symbol":"10"}]}}'
        companies = json.loads(jsonCompanies)
        
        if isEthical == 'Ethical Investing':
            types.append(isEthical)
            companies = companies['strategy']['Ethical Investing']
            for comp in companies:
                stock_symbols.append(comp['name'])
                stock_weights.append(comp['percentage_Symbol'])
        
        if isGrowth == 'Growth Investing':
            types.append(isGrowth)
            companies = companies['strategy']['Growth Investing']
            for comp in companies:
                stock_symbols.append(comp['name'])
                stock_weights.append(comp['percentage_Symbol'])

        if isIndex == 'Index Investing':
            types.append(isIndex)
            companies = companies['strategy']['Index Investing']
            for comp in companies:
                stock_symbols.append(comp['name'])
                stock_weights.append(comp['percentage_Symbol'])

        amount = request.POST.get('amount')
        totalAmount = float(amount)
        for stock_weight in stock_weights:
            temp = float(totalAmount)*float(stock_weight)/100
            stock_values.append(temp/count)

        for stock_symbol in stock_symbols:
            stock_details.append(getDetailsOfStock(stock_symbol))

        for stock_detail in stock_details:
            stock_names.append(stock_detail['name'])
            stock_closings.append(stock_detail['closePrice'])
            stock_openPrice.append(stock_detail['openPrice'])

        whole_data = zip(stock_names,stock_closings,stock_openPrice,stock_symbols,stock_values)
        whole_data2 = zip(stock_names,stock_closings,stock_openPrice,stock_symbols,stock_values)
        context = {
            "whole_data" : whole_data,
            "types" : types,
            "whole_data2" : whole_data2,
        } 
        return render(request, "details.html", context)

#function which sends the graph to the appropriate page to be displayed to the users.
@csrf_exempt
def details_graphs(request):
    stock_graph_details = []
    if request.method == 'POST':
        print(len(stock_details))
        for stock_detail in stock_details:
            stock_graph_details.append(get_plot(stock_detail['keys'], stock_detail['value'],stock_detail['symbol'],stock_detail['name']))
        context_for_graphs = {
            "graphs" : stock_graph_details
        } 
        return render(request, "details_graphs.html", context_for_graphs)
