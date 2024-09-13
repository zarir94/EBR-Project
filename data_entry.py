from app import app, SSCResult, db

all_boards = [
    "BARISHAL",
    "CHATTOGRAM",
    "CUMILLA",
    "DHAKA",
    "DINAJPUR",
    "JASHORE",
    "MADRASAH",
    "RAJSHAHI",
    "SYLHET",
    "MYMENSINGH",
    "TECHNICAL"
]

with open('log.txt') as f: d=f.read()

f = open('log.txt', 'w')
f.write(d)

with app.app_context():
    for year in range(2015, 2024 + 1):
        for board in all_boards:
            slug = f'{year}-{board}'
            if slug in d: continue
            f.write(slug + '\n')
            print('Adding Entries for', board, year, flush=True)
            for roll in range(100000, 999999 + 1):
                db.session.add(SSCResult(roll=roll, year=year, board=board))
            db.session.commit()
            print('Done!', flush=True)




print('All Done', flush=True)