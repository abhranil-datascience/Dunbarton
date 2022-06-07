from django.shortcuts import render
from Forms import AssignLoadArea
# Create your views here.
def ScanPageFunction(request):
    if request.method == "POST":
        assign_form = AssignLoadArea.AssignLoadAreaForm(request.POST)
        if assign_form.is_valid():
            AllWorkOrderNumbers = assign_form.cleaned_data.get('AllWorkOrderNumbers')
            AssignedWorkOrderNumbers = assign_form.cleaned_data.get('AssignedWorkOrderNumbers')
            LoadArea = assign_form.cleaned_data.get('LoadArea')
            ID = assign_form.cleaned_data.get('ID')
            print("AllWorkOrderNumbers:",AllWorkOrderNumbers)
            print("AssignedWorkOrderNumbers:",AssignedWorkOrderNumbers)
            print("LoadArea:",LoadArea)
            print("ID:",ID)
            NotAssignedWorkOrderNumbersList=[]
            AllWorkOrderNumbersSplitted = AllWorkOrderNumbers.split("||")
            AssignedWorkOrderNumbersSplitted = AssignedWorkOrderNumbers.split("||")
            for item in AllWorkOrderNumbersSplitted:
                if not(str(item) in AssignedWorkOrderNumbersSplitted):
                    NotAssignedWorkOrderNumbersList.append(str(item))
            NotAssignedWorkOrderNumbers = "||".join(NotAssignedWorkOrderNumbersList)
            print("NotAssignedWorkOrderNumbers:",NotAssignedWorkOrderNumbers)
            assign_form = AssignLoadArea.AssignLoadAreaForm()
            context = {"unassigned_id":NotAssignedWorkOrderNumbersList,"new_wons":NotAssignedWorkOrderNumbers,"employee_id":ID,"assign_form":assign_form}
            print(context)
            return render(request, "HTML/ScanPage.html", context=context)
        else:
            ID = assign_form.cleaned_data.get('ID')
            assign_form = AssignLoadArea.AssignLoadAreaForm()
            context = {"employee_id":ID,"assign_form":assign_form}
            return render(request, "HTML/ScanPage.html", context=context)
    else:
        assign_form = AssignLoadArea.AssignLoadAreaForm()
        context = {"assign_form":assign_form}
        return render(request, "HTML/ScanPage.html", context=context)
