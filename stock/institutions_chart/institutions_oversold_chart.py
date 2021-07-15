from .institutions_chart import InstitutionsChart


class InstitutionsOverSoldChart(InstitutionsChart):

    def __init__(self):
        super().__init__(type='sell')
