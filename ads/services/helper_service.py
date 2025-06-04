from ..models import *


class HelperService:
    def __init__(self):
        self.Ad = Ad.objects
        self.Category = Category.objects
        self.Condition = Condition.objects
        self.User = User.objects

    def get_categories(self):
        return self.Category.all()

    def get_conditions(self):
        return self.Condition.all()
