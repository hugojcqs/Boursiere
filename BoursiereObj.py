class Boursiere:
    def __init__(self):
        self.db = {}
        self.current_qarder = 0
        self.out_of_stock = {}  # beer qu'on a plus en stock (on move les beer de db dans out_of_stock

    def add_beer(self, beer_name, stock, buy_price, coef_down, coef_up, coef_max):
        self.db[beer_name] = {'stock': stock, 'buy_price': buy_price, 'price': buy_price, 'coef_down': coef_down,
                              'coef_up': coef_up, 'coef_max': coef_max, 'q_qarder': 0, 'q_current_qarder': 0, 'history': []}

    def change_coef_down(self, beer_name, coef_down):
        self._verify_beer_exists(beer_name)
        self.db[beer_name]['coef_down'] = coef_down

    def change_coef_up(self, beer_name, coef_up):
        self._verify_beer_exists(beer_name)
        self.db[beer_name]['coef_up'] = coef_up

    def change_coef_max(self, beer_name, coef_max):
        self._verify_beer_exists(beer_name)
        self.db[beer_name]['coef_max'] = coef_max

    def add_conso(self, beer_name, number):
        self._verify_beer_exists(beer_name)
        self.db[beer_name]['q_current_qarder'] += number

    @staticmethod
    def _compute_price(q_current_beer, q_last_beer, coef_down, coef_up, price):
        if q_current_beer > q_last_beer:
            return price + coef_up * (q_current_beer - q_last_beer)
        else:
            return price + coef_down * (q_current_beer - q_last_beer)

    def update_prices(self, do_round=True):
        self.current_qarder += 1
        for beer_name in self.db:

            q_current_beer = self.db[beer_name]['q_current_qarder']
            q_last_beer = self.db[beer_name]['q_qarder']
            coef_max = self.db[beer_name]['coef_max']
            coef_down = self.db[beer_name]['coef_up']
            coef_up = self.db[beer_name]['coef_down']
            price = self.db[beer_name]['price']
            buy_price = self.db[beer_name]['buy_price']

            self.db[beer_name]['history'].append((self.current_qarder-1, q_current_beer, price))
            new_price = self._compute_price(q_current_beer, q_last_beer, coef_down, coef_up, price)
            self.db[beer_name]['stock'] -= q_current_beer

            # TODO : Cas stock est vide? Bouger le dict de la beer vers un autre dict pour plus qu'il ne soit utilisé ?



            if self.db[beer_name]['stock'] <= 0: # check if the stock is empty
                self.out_of_stock[beer_name] = self.db[beer_name] # add the db part of beer to out_of_stock (line:70)
                continue

            self.db[beer_name]['q_qarder'] = q_current_beer
            self.db[beer_name]['q_current_qarder'] = 0


            if new_price > (coef_max * buy_price):  # check for avoid too many growth in the price
                self.db[beer_name]['price'] = coef_max * buy_price
                return coef_max * buy_price
            if do_round:
                self.db[beer_name]['price'] = round(new_price, 1)
                return round(new_price, 1)
            else:
                self.db[beer_name]['price'] = new_price
                return new_price

        for beer_name in self.out_of_stock: #
            del(self.db[beer_name])         # del from db all the beer out of stocks

        return -1                           #  add default return value for out_of_stock case

    def _verify_beer_exists(self, beer_name):
        if beer_name not in self.db:
            raise Exception('Beer does not exists in the database')

    def to_json(self):
        pass  # used to transform de db to json for frontend processing
