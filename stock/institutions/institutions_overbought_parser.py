from .institutions_parser import InstitutionsParser


class InstitutionsOverboughtParser(InstitutionsParser):

    def __init__(self):
        super().__init__()
        self.model = 'twse_over_bought'
