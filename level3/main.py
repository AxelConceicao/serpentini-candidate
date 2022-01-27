import os
import json
from datetime import datetime

INPUT_FILE = os.path.dirname(__file__) + '/data/input.json'
OUTPUT_FILE = os.path.dirname(__file__) + '/data/output.json'


class User:
    def __init__(self, user, deals):
        self._id = user['id']
        self._name = user['name']
        self._objective = user['objective']
        # filter user deals
        self._deals = [deal for deal in deals
                       if deal['user'] == user['id']]
        self._commissions = []

    def get_user_id(self):
        return self._id

    # return all payed deals at the time of the selected deal close date
    def get_payed_deals(self, deal):
        close_date = datetime.strptime(deal['close_date'], '%Y-%m-%d')
        return [_deal for _deal in self._deals
                if datetime.strptime(_deal['payment_date'], '%Y-%m-%d') <= close_date]

    def get_commission_by_rate_of(self, rate, deal_amount, commission, dealted_amount):
        # if the deal amount is greater than the objective the rest of the amount deal will be commissioned in the next tier
        if deal_amount > self._objective * 0.50:
            commission += self._objective * 0.50 * rate
            deal_amount -= self._objective * 0.50
            dealted_amount += self._objective * 0.50
        # otherwise the current tier will be filled in the next deal
        else:
            commission += deal_amount * rate
            deal_amount -= deal_amount
            dealted_amount += deal_amount
        return deal_amount, commission, dealted_amount

    def calcul_commissions(self):
        for deal in self._deals:
            commission = 0
            dealted_amount = 0
            deal_amount = deal['amount']
            payed_deals = sum(deal['amount']
                              for deal in self.get_payed_deals(deal))
            # tier 1 only if the sum of the payed deals amount is lower than the objective and if the deal amount matches perfectly the [0% - 50%] interval
            if payed_deals <= self._objective * 1.00 and deal_amount > self._objective * 0.00:
                deal_amount, commission, dealted_amount = self.get_commission_by_rate_of(
                    0.05, deal_amount, commission, dealted_amount)
            # tier 2 only if the sum of the payed deals amount is lower than the objective and if the deal amount matches perfectly the [50% - 100%] interval
            if payed_deals <= self._objective * 1.00 and deal_amount + dealted_amount > self._objective * 0.50:
                deal_amount, commission, dealted_amount = self.get_commission_by_rate_of(
                    0.10, deal_amount, commission, dealted_amount)
            # tier 3 if the sum of the payed deals amount is greater than the objective OR if the current deal amount already filled the tier 1 and tier 2
            if payed_deals > self._objective * 1.00 or deal_amount + dealted_amount > self._objective * 1.00:
                commission += deal_amount * 0.15
            self._commissions.append(
                {'id': deal['id'], 'commission': commission, 'close_date': deal['close_date'], 'payment_date': deal['payment_date']})

    def get_commissions_by_month(self):
        commission = {}
        months = []
        # get all deals payment date by month
        for deal in self._commissions:
            months.append('-'.join(deal['payment_date'].split('-')[:-1]))
        # erase duplicate months
        months = sorted(list(set(months)))
        # and get the sum of deals amount for each month
        for month in months:
            commission[month] = sum(deal['commission'] for deal in self._commissions
                                    if deal['payment_date'].startswith(month))
        return commission


if __name__ == "__main__":
    with open(INPUT_FILE, 'r') as json_file:
        data = json.load(json_file)

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

    output = {
        'commissions': commissions,
        # erase the payment_date and the close_date of each deals
        'deals': [{'id': deal['id'], 'commission': deal['commission']} for deal in deals]

    }
    with open(OUTPUT_FILE, 'w') as output_file:
        json.dump(output, output_file)

    exit(0)
