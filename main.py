from BoursiereObj import Boursiere

b = Boursiere()

#b.load()

"""
b.add_beer('Bush', 96, 1.9, 0.08, 0.05, 2.5)
b.add_beer('Orval', 96, 1.5, 0.08, 0.05, 2.5)
b.update_prices(do_round=True)
b.add_conso('Orval', 1)
b.add_conso('Orval', 1)
b.add_conso('Orval', 1)
b.add_conso('Orval', 1)
b.add_conso('Orval', 1)

b.add_conso('Bush', 13)
b.update_prices(do_round=True)
b.add_conso('Orval', 7)
b.update_prices(do_round=True)
b.add_conso('Orval', 5)
b.update_prices(do_round=True)
b.add_conso('Orval', 10)
b.update_prices(do_round=True)
b.add_conso('Orval', 2)
b.update_prices(do_round=True)
b.update_prices(do_round=True)
b.add_conso('Orval', 3)
b.update_prices(do_round=True)
b.add_conso('Orval', 4)
b.update_prices(do_round=True)
b.update_prices(do_round=True)
b.update_prices(do_round=True)
b.add_conso('Orval', 14)
b.update_prices(do_round=True)
b.add_conso('Orval', 20)
b.update_prices(do_round=True)
"""


# -- end the stock of Orval --

#b.add_conso('Orval', 26)
#b.update_prices(do_round=True)

#  -- raise Error because beer is out of stock --

#b.add_conso('Orval', 27)
# (b.update_prices(do_round=True))

#print(b.to_json())

# -- save data in 'data.json' --
b.save()
