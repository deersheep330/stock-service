from .institutions_parser import InstitutionsParser


class InstitutionsOversoldParser(InstitutionsParser):

    def __init__(self):
        super().__init__()
        self.symbol_xpath = "//*[contains(@class, 'fRtBx')]//tbody//tr//td[1]//a"
        self.foreign_xpath = "//*[contains(@class, 'fRtBx')]//tbody//tr//td[3]"
        self.quantity_xpath = "//*[contains(@class, 'fRtBx')]//tbody//tr//td[6]"
        self.model = 'twse_over_sold'

    def exclude_condition(self, input):
        if input >= 0:
            return True
        else:
            return False
