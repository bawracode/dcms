from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

class CustomToggleSwitchWidget(DjangoToggleSwitchWidget):
    template_name = "widgets/toggle_switch.html"
