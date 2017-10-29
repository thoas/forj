from collections import OrderedDict

import multiform


class MultiModelForm(multiform.MultiModelForm):
    def get_base_forms(self):
        return OrderedDict(self.base_forms)
