from stock.institutions import InstitutionsOverboughtParser, InstitutionsOversoldParser

if __name__ == '__main__':

    print('==> institutions_entry')

    overbought_parser = InstitutionsOverboughtParser()
    overbought_parser.parse().save_to_db()

    oversold_parser = InstitutionsOversoldParser()
    oversold_parser.parse().save_to_db()
