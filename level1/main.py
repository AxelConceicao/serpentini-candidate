import os
import json

INPUT_FILE = os.path.dirname(__file__) + '/data/input.json'
OUTPUT_FILE = os.path.dirname(__file__) + '/data/output.json'


class User:
    def __init__(self, user, deals):
        self._id = user['id']
        self._name = user['name']
        # filter user deals
        self._deals = [deal for deal in deals
                       if deal['user'] == user['id']]

    def get_user_id(self):
        return self._id

    def get_commissions(self):
        commissions = 0
        # sum of all deals amount
        _sum = sum(deal['amount'] for deal in self._deals)
        # determine the commission in relation to the number of deals
        if len(self._deals) < 3:
            commissions = _sum * 0.10
        else:
            commissions = _sum * 0.20
        if _sum > 2000:
            commissions += 500
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
