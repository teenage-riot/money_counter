import os

def make_category(cat, cat_cont, path): 
    with open(path + cat, 'r') as f:
        cat_cont[cat] = [word.strip() for word in f.read().split('\n')]

exp_cat = os.listdir('exp_cat')
exp_cat_content = {k: [] for k in exp_cat}

inc_cat = os.listdir('inc_cat')
inc_cat_content = {k: [] for k in inc_cat}

# for c in exp_cat:
#     print(f'\'{c}\': \'\',')

rus_cat = {
    'alco': 'Алкоголь',
    'connection': 'Связь',
    'clothes': 'Одежда',
    'debts': 'Возврат долгов',
    'donation': 'Пожертвования',
    'drugs': 'Лекарства',
    'energetics': 'Энергетики',
    'enjoy': 'Развлечения',
    'everyday_life': 'Быт',
    'food': 'Пища',    
    'gave_a_loan': 'Дал в долг',
    'housing': 'Жильё',
    'presents': 'Подарки',
    'smoking': 'Курение',
    'sweet': 'Сладкое',
    'tech': 'Техника',
    'transport': 'Транспорт',
    'unalco': 'Безалкоголка',
    'exp_other': 'Прочие расходы',

    'got_debt': 'Взял в долг',
    'job': 'Работа',
    'loan_returns': 'Вернули долги',
    'inc_other': 'Прочие доходы',
}

for cat in exp_cat:
    make_category(cat, exp_cat_content, 'exp_cat\\')

for cat in inc_cat:
    make_category(cat, inc_cat_content, 'inc_cat\\')

expences = {k: 0 for k in exp_cat}
expences['exp_other'] = 0

incomes = {k: 0 for k in inc_cat}
incomes['inc_other'] = 0

incomes_sum, expences_sum = 0, 0

lines = {k: [] for k in exp_cat}
for k in inc_cat:
    lines[k] = []
lines['exp_other'], lines['inc_other'] = [], []

with open('source', 'r') as f:
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
print(f'Разница: {incomes_sum - expences_sum}')


def write_lines(cat, file):
    for line in lines[cat]:
        file.write(f'{line}\n')
    file.write('\n')


def write_dict(d, file, sum):
    i = 1
    for k, v in d.items():
        file.write(f'{i}. {rus_cat[k]}: {v} ({round(v / sum * 100, 2)}%)\n')
        i += 1
        write_lines(k, file)


def write_diff(a, b, file):
    diff = a - b
    file.write(f'Разница: {diff} ')
    if diff < 0:
        file.write('(отдал больше)')  
    elif diff > 0:
        file.write('(взял больше)')  
    else:
        file.write('(вышел в ноль)') 


with open('result', 'w') as f:
    f.write(f'--- Расоходы: {expences_sum} ---\n\n')
    write_dict(expences, f, expences_sum)
    f.write('\n')
    f.write(f'--- Доходы: {incomes_sum} ---\n\n')
    write_dict(incomes, f, incomes_sum)
    
    f.write('\n-----------------\n')
    f.write(f'Взял в долг: {incomes['got_debt']}\n')
    write_lines('got_debt', f)
    f.write(f'Вернул долгов: {expences['debts']}\n')
    write_lines('debts', f)
    write_diff(incomes['got_debt'], expences['debts'], f)

    f.write('\n\n-----------------\n')
    f.write(f'Одолжил: {expences['gave_a_loan']}\n')
    write_lines('gave_a_loan', f)
    f.write(f'Вернули: {incomes['loan_returns']}\n')
    write_lines('loan_returns', f)
    write_diff(incomes['loan_returns'], expences['gave_a_loan'], f)
    


