from BoursiereObj import Boursiere

b = Boursiere()
b.add_beer('Orval', 96, 1.5, 0.08, 0.05, 2.5)
print(b.update_prices(do_round=False))
b.add_conso('Orval', 5)
print(b.update_prices(do_round=False))
b.add_conso('Orval', 7)
print(b.update_prices(do_round=False))
b.add_conso('Orval', 5)
print(b.update_prices(do_round=False))
b.add_conso('Orval', 10)
print(b.update_prices(do_round=False))
b.add_conso('Orval', 2)
print(b.update_prices(do_round=False))
