from django.shortcuts import render
from Forms import AssignLoadArea, AuditLoadArea
from django.db import connection
import datetime
# Create your views here.
def ScanAndAssignPageFunction(request):
    ############################### Get All Unassigned Work Order Numbers ###############################################################
    cursor = connection.cursor()
    curr_query = "select work_order_number from public.scan_table st where is_assigned='N' and moved_to_paint_line='N'"
    cursor.execute(curr_query)
    res = cursor.fetchall()
    ExistingUnassignedWorkOrderList = []
    for item in res:
        ExistingUnassignedWorkOrderList.append(item[0])
    ############################### Get All Assigned Work Order Numbers ###############################################################
    cursor = connection.cursor()
    curr_query = "select work_order_number from public.scan_table st where is_assigned='Y' and moved_to_paint_line='N'"
    cursor.execute(curr_query)
    res = cursor.fetchall()
    ExistingAssignedWorkOrderList = []
    for item in res:
        ExistingAssignedWorkOrderList.append(item[0])
    ################################################## Check For Post Request ############################################################
    if request.method == "POST":
        assign_form = AssignLoadArea.AssignLoadAreaForm(request.POST)
        if assign_form.is_valid():
            today_date = str(datetime.datetime.now().date())
            ########################################## Get Current Data Submitted by User ###################################################
            CurrentWorkOrderNumbers = assign_form.cleaned_data.get('AllWorkOrderNumbers')
            CurrentAssignedWorkOrderNumbers = assign_form.cleaned_data.get('AssignedWorkOrderNumbers')
            CurrentLoadArea = assign_form.cleaned_data.get('LoadArea')
            CurrentID = assign_form.cleaned_data.get('ID')
            CurrentAllWorkOrderNumbers = [item for item in CurrentWorkOrderNumbers.split("||") if item.strip() != ""]
            CurrentAssignedWorkOrderNumbers = [item for item in CurrentAssignedWorkOrderNumbers.split("||") if item.strip() != ""]
            CurrentUnassignedWorkOrderNumbers = [item for item in CurrentAllWorkOrderNumbers if not(item in CurrentAssignedWorkOrderNumbers)]
            print("CurrentAllWorkOrderNumbers:",CurrentAllWorkOrderNumbers)
            print("CurrentAssignedWorkOrderNumbers:",CurrentAssignedWorkOrderNumbers)
            print("CurrentUnassignedWorkOrderNumbers:",CurrentUnassignedWorkOrderNumbers)
            #################### Add Current Unassigned Work Order Numbers not present in Database ###########################################
            CurrentUnassignedWorkOrderNumbersNotPresentInDatabase = [item for item in CurrentUnassignedWorkOrderNumbers if not(item in ExistingUnassignedWorkOrderList+ExistingAssignedWorkOrderList)]
            for item in CurrentUnassignedWorkOrderNumbersNotPresentInDatabase:
                curr_query = "insert into public.scan_table (work_order_number,entry_date) values ('"+str(item)+"','"+today_date+"')"
                cursor.execute(curr_query)
            #################### Add Current Assigned Work Order Numbers not present in Database ###########################################
            CurrentAssignedWorkOrderNumbersNotPresentInDatabase = [item for item in CurrentAssignedWorkOrderNumbers if not(item in ExistingUnassignedWorkOrderList+ExistingAssignedWorkOrderList)]
            for item in CurrentAssignedWorkOrderNumbersNotPresentInDatabase:
                curr_query = "insert into public.scan_table (work_order_number,entry_date,is_assigned,assign_date,assign_area,assign_operator_id) values ('"+str(item)+"','"+today_date+"','Y','"+today_date+"','"+CurrentLoadArea+"','"+str(CurrentID)+"')"
                cursor.execute(curr_query)
            #################### Add Current Assigned Work Order Numbers present in Database ###########################################
            CurrentAssignedWorkOrderNumbersPresentInDatabase = [item for item in CurrentAssignedWorkOrderNumbers if ((item in ExistingAssignedWorkOrderList) and not(item in ExistingUnassignedWorkOrderList))]
            for item in CurrentAssignedWorkOrderNumbersPresentInDatabase:
                curr_query = "update public.scan_table set assign_date='"+today_date+"',"+"assign_area='"+CurrentLoadArea+"',assign_operator_id='"+str(CurrentID)+"' where work_order_number='"+str(item)+"'"
                cursor.execute(curr_query)
            #################### Add Current Assigned Work Order Numbers present in Database as Unassigned ###########################################
            CurrentAssignedWorkOrderNumbersPresentInDatabaseAsUnassigned = [item for item in CurrentAssignedWorkOrderNumbers if (not(item in ExistingAssignedWorkOrderList) and (item in ExistingUnassignedWorkOrderList))]
            for item in CurrentAssignedWorkOrderNumbersPresentInDatabaseAsUnassigned:
                curr_query = "update public.scan_table set is_assigned='Y',assign_date='"+today_date+"',"+"assign_area='"+CurrentLoadArea+"',assign_operator_id='"+str(CurrentID)+"' where work_order_number='"+str(item)+"'"
                cursor.execute(curr_query)
            ######################################## Get unassigned Work Order Numbers after all DB operations #########################################
            curr_query = "select work_order_number from public.scan_table st where is_assigned='N' and moved_to_paint_line='N'"
            cursor.execute(curr_query)
            res = cursor.fetchall()
            ExistingUnassignedWorkOrderList = []
            for item in res:
                ExistingUnassignedWorkOrderList.append(item[0])
            all_unassigned_wons = "||".join(ExistingUnassignedWorkOrderList)
            assign_form = AssignLoadArea.AssignLoadAreaForm()
            context = {"unassigned_id":ExistingUnassignedWorkOrderList,"employee_id":CurrentID,"assign_form":assign_form,"all_unassigned_wons":all_unassigned_wons}
            return render(request, "HTML/ScanAndAssignPage.html", context=context)
    else:
        all_unassigned_wons = "||".join(ExistingUnassignedWorkOrderList)
        assign_form = AssignLoadArea.AssignLoadAreaForm()
        context = {"unassigned_id":ExistingUnassignedWorkOrderList,"assign_form":assign_form,"all_unassigned_wons":all_unassigned_wons}
        return render(request, "HTML/ScanAndAssignPage.html", context=context)
def ScanAndAuditPageFunction(request):
    ############################### Get All Assigned Work Order Numbers ###############################################################
    cursor = connection.cursor()
    curr_query = "select work_order_number,assign_area,moved_to_paint_line from public.scan_table st"
    cursor.execute(curr_query)
    res = cursor.fetchall()
    ExistingWorkOrderLoadAreaDict = {}
    ExistingWorkOrderPaintStatusDict = {}
    for item in res:
        ExistingWorkOrderLoadAreaDict[item[0]]=item[1]
        ExistingWorkOrderPaintStatusDict[item[0]]=item[2]
    print("ExistingWorkOrderLoadAreaDict:",ExistingWorkOrderLoadAreaDict)
    print("ExistingWorkOrderPaintStatusDict:",ExistingWorkOrderPaintStatusDict)
    NonPaintedExistingWorkOrderList = []
    PaintedExistingWorkOrderList = []
    for key,val in ExistingWorkOrderPaintStatusDict.items():
        if val == "N":
            print(key)
            curr_load_ar = ExistingWorkOrderLoadAreaDict[key]
            if curr_load_ar is None:
                NonPaintedExistingWorkOrderList.append(key+"-"+"N")
            else:
                NonPaintedExistingWorkOrderList.append(key+"-"+curr_load_ar)
        else:
            PaintedExistingWorkOrderList.append(key)
    NonPaintedExistingWorkOrder = "||".join([item for item in NonPaintedExistingWorkOrderList if item.strip() != ""])
    PaintedExistingWorkOrder = "||".join(PaintedExistingWorkOrderList)
    if request.method == "POST":
        audit_form = AuditLoadArea.AuditLoadAreaForm(request.POST)
        if audit_form.is_valid():
            today_date = str(datetime.datetime.now().date())
            CurrentWorkOrderNumber = audit_form.cleaned_data.get('WorkOrderNumber')
            CurrentLoadArea = audit_form.cleaned_data.get('LoadArea')
            CurrentID = audit_form.cleaned_data.get('ID')
            if CurrentWorkOrderNumber in ExistingWorkOrderPaintStatusDict:
                if ExistingWorkOrderPaintStatusDict[CurrentWorkOrderNumber] == "N":
                    existing_load_area = ExistingWorkOrderLoadAreaDict[CurrentWorkOrderNumber]
                    if (existing_load_area == "") or (existing_load_area is None):
                        curr_query = "update public.scan_table set is_assigned='Y', assign_date='"+today_date+"',"+"assign_area='"+CurrentLoadArea+"',is_audited='Y',audit_date='"+today_date+"',audit_operator_id='"+str(CurrentID)+"' where work_order_number='"+str(CurrentWorkOrderNumber)+"'"
                        cursor.execute(curr_query)
                    else:
                        if existing_load_area != CurrentLoadArea:
                            curr_query = "update public.scan_table set assign_area='"+CurrentLoadArea+"',is_audited='Y',audit_date='"+today_date+"',previous_assign_area='"+existing_load_area+"',audit_operator_id='"+str(CurrentID)+"' where work_order_number='"+str(CurrentWorkOrderNumber)+"'"
                            cursor.execute(curr_query)
            else:
                if not(CurrentWorkOrderNumber in PaintedExistingWorkOrderList):
                    curr_query = "insert into public.scan_table (work_order_number,entry_date,is_assigned,assign_date,assign_area,is_audited,audit_date,audit_operator_id) values ('"+str(CurrentWorkOrderNumber)+"','"+today_date+"','Y','"+today_date+"','"+CurrentLoadArea+"','Y','"+today_date+"','"+str(CurrentID)+"')"
                    cursor.execute(curr_query)
        audit_form = AuditLoadArea.AuditLoadAreaForm()
        context = {"non_painted_wons":NonPaintedExistingWorkOrder,"painted_wons":PaintedExistingWorkOrder,"audit_form":audit_form,"employee_id":CurrentID}
        return render(request, "HTML/ScanAndAuditPage.html",context=context)
    else:
        audit_form = AuditLoadArea.AuditLoadAreaForm()
        context = {"non_painted_wons":NonPaintedExistingWorkOrder,"painted_wons":PaintedExistingWorkOrder,"audit_form":audit_form}
        return render(request, "HTML/ScanAndAuditPage.html",context=context)
