from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class AuditLoadAreaForm(forms.Form):
    WorkOrderNumber = forms.CharField(widget = forms.HiddenInput(),max_length=200, required=True)
    LoadArea = forms.CharField(widget = forms.HiddenInput(),max_length=200, required=True)
    ID = forms.CharField(label="ID", max_length=200, required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
        # Row('AssignedWorkOrderNumbers','AllWorkOrderNumbers','LoadArea','ID','Role', css_class='form-row'),
        Row('WorkOrderNumber','LoadArea','ID', css_class='form-row'),
        Submit('submit', 'Submit', css_class='btn btn-secondary SubmitButtonModal'))
