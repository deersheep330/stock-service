from .institutions_chart import InstitutionsChart


class InstitutionsOverBoughtChart(InstitutionsChart):

    def __init__(self):
        super().__init__(type='buy')
