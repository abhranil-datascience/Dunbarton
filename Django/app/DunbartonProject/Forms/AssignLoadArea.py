from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class AssignLoadAreaForm(forms.Form):
    AssignedWorkOrderNumbers = forms.CharField(widget = forms.HiddenInput(),max_length=9000, required=False)
    # AssignedWorkOrderNumbers = forms.CharField(max_length=9000, required=True)
    AllWorkOrderNumbers = forms.CharField(widget = forms.HiddenInput(),max_length=9000, required=True)
    # AllWorkOrderNumbers = forms.CharField(max_length=9000, required=True)
    LoadArea = forms.CharField(widget = forms.HiddenInput(),max_length=200, required=True)
    # LoadArea = forms.CharField(max_length=200, required=True)
    ID = forms.CharField(label="ID", max_length=200, required=True)
    Role = forms.ChoiceField(label='Role', choices = (("E","Employee"),("A","Auditor")), required=True, initial="Employee")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
        Row('AssignedWorkOrderNumbers','AllWorkOrderNumbers','LoadArea','ID','Role', css_class='form-row'),
        Submit('submit', 'Submit', css_class='btn btn-secondary SubmitButtonModal'))
