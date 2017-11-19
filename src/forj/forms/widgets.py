from django.forms.widgets import ChoiceWidget


class Radio(ChoiceWidget):
    input_type = 'radio'
    template_name = 'forj/forms/widgets/radio.html'
    option_template_name = 'forj/forms/widgets/radio_option.html'
