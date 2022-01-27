import os
import json

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

    def get_user_id(self):
        return self._id

    def get_commissions(self):
        commissions = 0
        # sum of all deals amount
        _sum = sum(deal['amount'] for deal in self._deals)
        # determine the commission in relation to the objective
        if _sum > self._objective * 0.00:
            commissions += self._objective * 0.50 * 0.05
        if _sum > self._objective * 0.50:
            commissions += self._objective * 0.50 * 0.10
        if _sum > self._objective * 1.00:
            commissions += (_sum - self._objective) * 0.15
        return commissions


if __name__ == "__main__":
    with open(INPUT_FILE, 'r') as json_file:
        data = json.load(json_file)

    commissions = []
    for user in data['users']:
        _user = User(user, data['deals'])
        commissions.append({
            'user_id': _user.get_user_id(),
            'commission': _user.get_commissions(),
        })

    with open(OUTPUT_FILE, 'w') as output_file:
        json.dump({'commissions': commissions}, output_file)

    exit(0)
