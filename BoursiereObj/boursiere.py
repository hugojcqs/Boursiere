"""

Prémice de code :

reflexion algo:
---------------

p + , si q vendu au qarder1 est < q vendu au qarder 2
p -, si q vendu qu qarder 1 est >= q vendu au qarder 2

n_p = old_p + 0.1 * ((q qarder 2 - qarder 1))



"""

boursier = {}
current_qarder = 0                                                      # ATTENTION : NEED TO START AT 0


def add_beer(dico, beer_name, stock, buy_price, coef_down, coef_up, coef_max):
    dico[beer_name] = {'stock':stock, 'buy_price':buy_price, 'price':buy_price, 'coef_down':coef_down, 'coef_up':coef_up, 'coef_max':coef_max, 'q_qarder':[], 'q_current_qarder':0}


#def compute_new_price(buy_price,current_price,q_last_qarder , q_current_qarder ,coef_up,coef_down, coef_max, do_round=True):

    if q_current_qarder > q_last_qarder:                                # check if the actual qarder quantity sold is upper than the last
        new_price = current_price + coef_up*(q_current_qarder-q_last_qarder)
    else:
        new_price = current_price + coef_down*(q_current_qarder-q_last_qarder)

    if new_price > (coef_max * buy_price):                            # check for avoid too many growth in the price
        new_price = coef_max * buy_price
    if do_round:
        new_price = round(new_price, 1)                                 # arround new price for 1 virgule

    return new_price


def update(dico, beer_name):
    if beer_name in dico.keys():                                        #check if the beer is listed
        beer = dico[beer_name]                                          # get the dico of the beer
        if beer['q_qarder'] != []:                                      # check if the list of quantity by for each qarder is not empty
            q_last_qarder = beer['q_qarder'][current_qarder-1]          # current qarder -1 because we start qarder at 1
            beer['price'] = compute_new_price(beer['buy_price'], beer['price'], q_last_qarder, beer['q_current_qarder'], beer['coef_up'], beer['coef_down'], beer['coef_max'])

        beer['q_qarder'].append(beer['q_current_qarder'])          # add current qarder buy quantity to the list of quantity for each qarder
        beer['q_current_qarder'] = 0                               # reset to 0 the current qarder buy quantity
        current_qarder += 1
    else:
        print('--- beer not found. ---')                               # beer is not in the dico
