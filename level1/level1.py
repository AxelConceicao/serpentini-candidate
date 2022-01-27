import os
import sys
import json
import errno
import json
import argparse


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
        self._deals = [deal for deal in deals
                       if deal['user'] == user['id']]

    def get_user_id(self):
        return self._id

    def get_commissions(self):
        if not len(self._deals):
            return 0
        commissions = 0
        _sum = sum(deal['amount'] for deal in self._deals)
        if len(self._deals) < 3:
            commissions = _sum * 0.10
        else:
            commissions = _sum * 0.20
        if _sum > 2000:
            commissions += 500
        return commissions


def main(args):
    with open(args.input_file, 'r') as json_file:
        try:
            data = json.load(json_file)
        except:
            print("Cannot parse json file", file=sys.stderr)

    commissions = []
    for user in data['users']:
        _user = User(user, data['deals'])
        commissions.append({
            'user_id': _user.get_user_id(),
            'commission': _user.get_commissions(),
        })

    with open('data/output.json', 'w') as output_file:
        json.dump({'commissions': commissions}, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file", type=is_file_exist)
    main(parser.parse_args())
    exit(0)
