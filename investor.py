import requests
import logging
from time import gmtime, strftime, sleep
import sys
secret = 'dasfasdfasdf'
LOG_FILENAME = 'history.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)


class Investor:

    def __init__(self, secret):
        self.secret = secret

    def list():
        '''
        Listing own investments (may be slow due to no api for that)
        '''
        # Query list of investments where investor invested
        pass

    def details():
        '''
        Details on given investment
        '''
        pass

    def create(self, lid, amount):
        '''
        Investing in given loans

        '''
        url = "https://api.loanbase.com/api/investment"
        params = {'loan_id': lid, 'amount': amount}
        headers = {
            'Authorization': 'Bearer ' + self.secret,
            'Accept': 'application/vnd.blc.v1+json',
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        resp = requests.post(url, data=params, headers=headers)
        info = "Investing LID: {0}, Amount: {1}"\
            .format(lid, amount)
        logging.info(strftime("%Y-%m-%d %H:%M:%S", gmtime())+info)
        print(resp.text)

    def modify():
        '''
        Modify investment (have to know id)
        '''
        pass

    def delete(self,id):
        '''
        To delete investment
        '''

        url = "https://api.loanbase.com/api/investment/"+str(id)
        params = {'id': id}
        headers = {
            'Authorization': 'Bearer ' + self.secret,
            'Accept': 'application/vnd.blc.v1+json',
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        resp = requests.delete(url, data=params, headers=headers)
        info = "Deleting ID: {0}"\
            .format(id)
        logging.info(strftime("%Y-%m-%d %H:%M:%S", gmtime())+info)
        print(resp.text)


def brfl(lid):
    r = requests.get("https://api.loanbase.com/api/investments/"+str(lid))
    raw = requests.get("https://api.loanbase.com/api/loan/"+str(lid))
    solist = sorted(r.json()['investments'], key=lambda x: float(x['rate']))
    max_rate = 1.0
    investments = 0.0
    requested = float(raw.json()['loans'][0]['amount'])
    for idx, i in enumerate(solist):
        investments = investments + float(solist[idx]['amount'])
        if investments >= requested:
            max_rate = float(solist[idx-1]['rate'])
            return max_rate

def return_reputation_loan_ids():
    rep_url = 'https://api.loanbase.com/api/loans?type=reputation&term=1,7,14,30'
    response = requests.get(rep_url)
    lid_list = []
    for i in response.json()['loans']:
        lid_list.append(i['id'])
    return lid_list

def main(amount):
    watch_url = 'https://api.loanbase.com/api/loans?type=reputation&term=1,7,14,30&status=funding'
    sess = requests.Session()

    while True:
        try:
            sleep(15)
            response = sess.get(watch_url)
            
            print response.json()
            if len(response.json()['loans']) > 0:
                check_lid = response.json()['loans']['id']

                I = Investor(token)
                I.create(check_lid, amount)
            
        except Exception, e:
            print e
        
if __name__ == '__main__':
    amount = str(sys.argv[1])
    main(amount)


    
