from flask import Flask, render_template, request
import requests
from datetime import datetime
import json
from converter import get_rates, get_best_rate

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    date = datetime.today().strftime('%Y-%m-%d')
    get_date = date

    if request.method == 'POST':
        get_date = request.form['date']
    trDate = datetime.strptime(get_date, '%Y-%m-%d').strftime('%d-%m-%Y')  # For TR based urls

    url = 'https://evds2.tcmb.gov.tr/service/evds/series=TP.DK.USD.A-TP.DK.EUR.A&startDate={0}&endDate={0}&type=json&key=QxNuloYOMu'
    url1 = 'http://api.currencylayer.com/historical?access_key=e6617c13a8cde01cfaeb62cd8605ec09&date={}&currencies=EUR,TRY&format=1'

    """
    jsonLocation for rates location in json files
    Since date formats differ, they must be defined by the user.(date_obj)
    """
    rates = get_rates(source_url=url, date_obj=trDate, jsonLocation='items')
    rates1 = get_rates(source_url=url1, date_obj=get_date, jsonLocation="quotes")

    data = get_best_rate(rates1, rates[0])

    return render_template('layout.html', data=list(data), current_date=date, date=trDate)


if __name__ == '__main__':
    app.run()
