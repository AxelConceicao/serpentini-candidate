import os
import sys
import json
import errno
import json
import argparse
from datetime import datetime


def is_file_exist(filename):
    if os.path.isfile(filename):
        return filename
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), filename)


class User:
    def __init__(self, user, deals):
        self._id = user['id']
        self._name = user['name']
        self._objective = user['objective']
        self._deals = [deal for deal in deals
                       if deal['user'] == user['id']]
        self._commissions = []

    def get_user_id(self):
        return self._id

    def get_payed_deals(self, deal):
        close_date = datetime.strptime(deal['close_date'], '%Y-%m-%d')
        return [_deal for _deal in self._deals
                if datetime.strptime(_deal['payment_date'], '%Y-%m-%d') <= close_date]

    def get_commission_by_rate_of(self, rate, deal_amount, commissions, dealted_amount):
        if deal_amount > self._objective * 0.50:
            commissions += self._objective * 0.50 * rate
            deal_amount -= self._objective * 0.50
            dealted_amount += self._objective * 0.50
        else:
            commissions += deal_amount * rate
            deal_amount -= deal_amount
            dealted_amount += deal_amount
        return deal_amount, commissions, dealted_amount

    def calcul_commissions(self):
        for deal in self._deals:
            commission = 0
            dealted_amount = 0
            deal_amount = deal['amount']
            payed_deals = sum(deal['amount']
                              for deal in self.get_payed_deals(deal))

            if payed_deals <= self._objective * 1.00 and deal_amount > self._objective * 0.00:
                deal_amount, commission, dealted_amount = self.get_commission_by_rate_of(
                    0.05, deal_amount, commission, deal_amount)
            if payed_deals <= self._objective * 1.00 and deal_amount + dealted_amount > self._objective * 0.50:
                deal_amount, commission, dealted_amount = self.get_commission_by_rate_of(
                    0.10, deal_amount, commission, deal_amount)
            if payed_deals > self._objective * 1.00 or deal_amount + dealted_amount > self._objective * 1.00:
                commission += deal_amount * 0.15
            self._commissions.append(
                {'id': deal['id'], 'commission': commission, 'close_date': deal['close_date'], 'payment_date': deal['payment_date']})

    def get_commissions_by_month(self):
        commission = {}
        months = []
        for deal in self._commissions:
            months.append('-'.join(deal['payment_date'].split('-')[:-1]))
        months = sorted(list(set(months)))
        for month in months:
            commission[month] = sum(deal['commission'] for deal in self._commissions
                                    if deal['payment_date'].startswith(month))
        return commission


def main(args):
    with open(args.input_file, 'r') as json_file:
        try:
            data = json.load(json_file)
        except:
            print("Cannot parse json file", file=sys.stderr)

    commissions = []
    deals = []
    for user in data['users']:
        _user = User(user, data['deals'])
        _user.calcul_commissions()
        commissions.append({
            'user_id': _user.get_user_id(),
            'commission': _user.get_commissions_by_month(),
        })
        deals += _user._commissions

    # deals.sort(key=lambda x: x['close_date'])
    output = {
        'commissions': commissions,
        'deals': [{'id': deal['id'], 'commission': deal['commission']} for deal in deals]

    }
    with open('data/output.json', 'w') as output_file:
        json.dump(output, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file", type=is_file_exist)
    main(parser.parse_args())
    exit(0)
