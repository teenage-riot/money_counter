def make_category(cat, cat_cont): 
    with open(cat, 'r') as f:
        cat_cont[cat] = [word.strip() for word in f.read().split('\n')]

exp_cat = ['alco', 'debts', 'donation', 'drugs', 'everyday_life', 'food', 'smoking', 'transport']
exp_cat_content = {k: [] for k in exp_cat}

inc_cat = ['got_debt', 'job']
inc_cat_content = {k: [] for k in inc_cat}

# for c in inc_cat:
#     print(f'\'{c}\': \'\',')

rus_cat = {
    'alco': 'Алкоголь',
    'debts': 'Возврат долгов',
    'donation': 'Пожертвования',
    'drugs': 'Лекарства',
    'everyday_life': 'Быт',
    'food': 'Пища',
    'smoking': 'Курение',
    'transport': 'Транспорт',
    'got_debt': 'Взял в долг',
    'job': 'Работа',
    'exp_other': 'Прочие расходы',
    'inc_other': 'Прочие доходы',
}

for cat in exp_cat:
    make_category(cat, exp_cat_content)

for cat in inc_cat:
    make_category(cat, inc_cat_content)

expences = {k: 0 for k in exp_cat}
expences['exp_other'] = 0

incomes = {k: 0 for k in inc_cat}
incomes['inc_other'] = 0

incomes_sum, expences_sum = 0, 0

lines = {k: [] for k in exp_cat}
for k in inc_cat:
    lines[k] = []
lines['exp_other'], lines['inc_other'] = [], []

with open('money', 'r') as f:
    txt = f.read()


for line in txt.split('\n'):
    if line:
        try:
            num = int(line.split()[0])
            if line[0] == '+':
                incomes_sum += num
                name = ' '.join(line.split()[1:])

                found = False
                for cat in inc_cat:
                    if name in inc_cat_content[cat]:
                        incomes[cat] += num
                        lines[cat].append(line)
                        found = True
                        break
                if not found:
                    incomes['inc_other'] += num
                    lines['inc_other'].append(line)
            else:
                expences_sum += num
                name = ' '.join(line.split()[1:])

                found = False
                for cat in exp_cat:
                    if name in exp_cat_content[cat]:
                        expences[cat] += num
                        lines[cat].append(line)
                        found = True
                        break
                if not found:
                    expences['exp_other'] += num
                    lines['exp_other'].append(line)
        except ValueError:
            pass

print(f'Расоходы: {expences_sum}')
print(f'Доходы: {incomes_sum}')

def write_dict(d, file):
    i = 1
    for k, v in d.items():
        file.write(f'{i}. {rus_cat[k]}: {v}\n')
        i += 1
        for line in lines[k]:
            file.write(f'{line}\n')
        file.write('\n')

with open('result', 'w') as f:
    f.write(f'--- Расоходы: {expences_sum} ---\n\n')
    write_dict(expences, f)
    f.write('\n')
    f.write(f'--- Доходы: {incomes_sum} ---\n\n')
    write_dict(incomes, f)


