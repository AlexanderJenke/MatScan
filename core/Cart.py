class Item:
    def __init__(self, pzn: int, name: str, exp_year: int, exp_month: int, count: int = 1):
        self.pzn = pzn
        self.name = name
        self.exp = (exp_year, exp_month)
        self.count = count
        self.mid = f"{pzn}_{str(exp_month).zfill(2)}.{exp_year}"

    def json(self):
        return {'name': self.name,
                'id': self.mid,
                'count': self.count,
                'exp': f"{str(self.exp[1]).zfill(2)}.{self.exp[0]}",
                }


class Cart:
    def __init__(self):
        self.items = {}

    def add(self, pzn, exp=None, count=1):
        from core import core

        if pzn not in self.items:
            name, exps = core.storage[pzn]
            self.items[pzn] = {'name': name,
                               'exps': {exp: {'count': 0, 'max': exps[exp]} for exp in exps}}

        if exp is None:
            exp = min([exp for exp in self.items[pzn]['exps']
                       if self.items[pzn]['exps'][exp]['count'] < self.items[pzn]['exps'][exp]['max']])

        if exp not in self.items[pzn]['exps']:
            raise IndexError(f"Exp. date for {self.items[pzn]['name']} doesn't exist.")

        self.items[pzn]['exps'][exp]['count'] += count

        if self.items[pzn]['exps'][exp]['count'] > self.items[pzn]['exps'][exp]['max']:
            self.items[pzn]['exps'][exp]['count'] = self.items[pzn]['exps'][exp]['max']
            raise OverflowError(
                f"Only {self.items[pzn]['exps'][exp]['max']} exist for exp. date for {self.items[pzn]['name']}.")

    def clear(self):
        self.items = {}

    def get_item(self, mid):
        pzn, exp = mid.split('_')
        return {'name': self.items[pzn]['name'],
                'count': self.items[pzn]['exps'][int(exp)],
                'pzn': pzn,
                'exp': exp,
                'mid': mid}

    def increase(self, mid):
        pzn, exp = mid.split('_')
        self.add(pzn, int(exp))

    def decrease(self, mid):
        pzn, exp = mid.split('_')
        self.items[pzn]['exps'][int(exp)]['count'] -= 1

    def set_count(self, mid, count):
        pzn, exp = mid.split('_')
        self.items[pzn]['exps'][int(exp)]['count'] = min(max(count, 0), self.items[pzn]['exps'][int(exp)]['max'])

    def del_item(self, mid):
        pzn, exp = mid.split('_')
        self.items[pzn]['exps'][int(exp)]['count'] = 0

    def get_dates(self, pzn):
        rows = []
        for exp in sorted(self.items[pzn]['exps']):
            rows.append({'name': "",
                         'id': f"{pzn}_{exp}",
                         'count': self.items[pzn]['exps'][exp]['count'],
                         'exp': f"{str(exp % 100).zfill(2)}.{int(exp / 100)}",
                         'increasable': self.items[pzn]['exps'][exp]['count'] < self.items[pzn]['exps'][exp]['max']
                         })
        return rows

    def get_rows(self):
        rows = []
        for pzn in self.items:
            count_bigger_one = [self.items[pzn]['exps'][exp]['count'] > 0 for exp in self.items[pzn]['exps']]
            if sum(count_bigger_one) > 1:
                rows.append({'name': self.items[pzn]['name'],
                             'superrow': True,
                             'id': f"{pzn}_{sorted(self.items[pzn]['exps'])[0]}",
                             })

                for exp in sorted(self.items[pzn]['exps']):
                    if self.items[pzn]['exps'][exp]['count'] == 0:
                        continue
                    rows.append({'name': "",
                                 'subrow': True,
                                 'id': f"{pzn}_{exp}",
                                 'count': self.items[pzn]['exps'][exp]['count'],
                                 'exp': f"{str(exp % 100).zfill(2)}.{int(exp / 100)}",
                                 'increasable': self.items[pzn]['exps'][exp]['count'] < self.items[pzn]['exps'][exp][
                                     'max']
                                 })

                rows.append({'seperator': True})
            else:
                for exp in self.items[pzn]['exps']:
                    if self.items[pzn]['exps'][exp]['count'] == 0:
                        continue
                    rows.append({'name': self.items[pzn]['name'],
                                 'id': f"{pzn}_{exp}",
                                 'count': self.items[pzn]['exps'][exp]['count'],
                                 'exp': f"{str(exp % 100).zfill(2)}.{int(exp / 100)}",
                                 'increasable': self.items[pzn]['exps'][exp]['count'] <
                                                self.items[pzn]['exps'][exp]['max']
                                 })

        return rows
