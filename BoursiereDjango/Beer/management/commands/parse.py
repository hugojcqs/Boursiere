from django.core.management.base import BaseCommand
from Beer.models import *
import xlrd
import json



class Command(BaseCommand):
    def handle(self, *args, **options):

        print("+===========================================================================+")
        print("  ____                       _                 _____  ")                       
        print(" |  _ \                     (_)               |  __ \ ")                      
        print(" | |_) | ___  _   _ _ __ ___ _  ___ _ __ ___  | |__) |_ _ _ __ ___  ___ _ __ ")
        print(" |  _ < / _ \| | | | '__/ __| |/ _ \ '__/ _ \ |  ___/ _` | '__/ __|/ _ \ '__|")
        print(" | |_) | (_) | |_| | |  \__ \ |  __/ | |  __/ | |  | (_| | |  \__ \  __/ |   ")
        print(" |____/ \___/ \__,_|_|  |___/_|\___|_|  \___| |_|   \__,_|_|  |___/\___|_|   \n")
        print("+===========================================================================+ \n")

        # get the name of the xls file                                                                     
        file_name = str(input(".xlsx file name: "))  

        #init the book and sheet variable
        book = None
        sheet = None


        # try to open the .xls file else catch an exeption ..
        try:

            # open the .xls file
            book = xlrd.open_workbook(file_name)

        except:
            print("File (%s) not found or invalid." % file_name)

        if book is not None:

            print('\n --- %s opened with %d sheets --- \n' %(file_name, book.nsheets))

            # get the sheet name
            sheet_name = str(input("beer sheet name: "))

            # try to open the correct sheet or catch exception
            try:

                # open the correct sheet for parse them.
                sheet = book.sheet_by_name(sheet_name)

            except:
                print("Sheet (%s) not found." % sheet_name)

            if sheet is not None:
                with open('beer.json', 'w') as outfile:
                    #json.dump(self.read_beers(book,sheet), outfile)

                    beers_db = self.read_beers(book,sheet)

                #create all dumped beers

                for beer in beers_db:

                    if beer.upper() in [bear.beer_name.upper() for bear in Beer.objects.all()]:
                        print(' [x] %s is already registered'%beer)
                        continue
                    Beer.objects.create(beer_name=beer,
                                     price=beers_db[beer]['price'],
                                     buy_price=beers_db[beer]['price'],
                                     coef_down=beers_db[beer]['coef_down'],
                                     coef_up=beers_db[beer]['coef_up'],
                                     stock=beers_db[beer]['stock'],
                                     static_stock=beers_db[beer]['stock'],
                                     coef_max=beers_db[beer]['coef_max'],
                                     coef_min=beers_db[beer]['coef_min'],
                                     alcohol_percentage=beers_db[beer]['alcohol_percentage'],
                                     bar=beers_db[beer]['bar']
                                     )
                    print(' [v] -> %s beer has been dumped..'%beer)
                    
                print('\n--- All valid beer has been dumped... ---\n')

    def read_beers(self,book,sheet):

        dumped = {}

        for row in range(sheet.nrows):

            #data = []
            beer = sheet.cell(row, 0).value

            if beer == '' or '#' in beer:
                continue

            dumped[beer] = {}

            for col in range(1, sheet.ncols):

                # get the cell in .xlsx
                cell = sheet.cell(row,col)

                #get LIBELLE
                libelle = sheet.cell(0,col).value
                
                #get Beer Model field_names
                fields_names = [f.name for f in Beer._meta.fields]
                
                # add only fields name valued into data
                if libelle in fields_names:
                    dumped[beer][libelle] = cell.value
        
        return dumped


