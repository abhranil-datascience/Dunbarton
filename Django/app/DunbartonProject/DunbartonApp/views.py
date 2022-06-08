from django.shortcuts import render
from Forms import AssignLoadArea
from django.db import connection
import datetime
# Create your views here.
def ScanPageFunction(request):
    if request.method == "POST":
        assign_form = AssignLoadArea.AssignLoadAreaForm(request.POST)
        if assign_form.is_valid():
            today_date = str(datetime.datetime.now().date())

            AllWorkOrderNumbers = assign_form.cleaned_data.get('AllWorkOrderNumbers')
            AssignedWorkOrderNumbers = assign_form.cleaned_data.get('AssignedWorkOrderNumbers')
            LoadArea = assign_form.cleaned_data.get('LoadArea')
            ID = assign_form.cleaned_data.get('ID')
            Role = assign_form.cleaned_data.get('Role')
            # print("Role:",Role)
            CurrentAllWorkOrderNumbers = [item for item in AllWorkOrderNumbers.split("||") if item.strip() != ""]
            CurrentAssignedWorkOrderNumbers = [item for item in AssignedWorkOrderNumbers.split("||") if item.strip() != ""]
            CurrentUnassignedWorkOrderNumbers = [item for item in CurrentAllWorkOrderNumbers if not(item in CurrentAssignedWorkOrderNumbers)]

            ######################################### SQL Queries ########################################################################
            cursor = connection.cursor()
            curr_query = "select work_order_number from public.scan_table st where is_assigned='N' and moved_to_paint_line='N'"
            cursor.execute(curr_query)
            res = cursor.fetchall()
            ExistingUnassignedWorkOrderList = []
            for item in res:
                ExistingUnassignedWorkOrderList.append(item[0])

            curr_query = "select work_order_number from public.scan_table st where is_assigned='Y' and moved_to_paint_line='N'"
            cursor.execute(curr_query)
            res = cursor.fetchall()
            ExistingAssignedWorkOrderList = []
            for item in res:
                ExistingAssignedWorkOrderList.append(item[0])

            ####################################### Get new unassigned WONs to be inserted into DB #######################################
            NewUnassignedWorkOrderList = [item for item in CurrentUnassignedWorkOrderNumbers if not(item in ExistingUnassignedWorkOrderList+ExistingAssignedWorkOrderList)]
            print("NewUnassignedWorkOrderList:",NewUnassignedWorkOrderList)
            for item in NewUnassignedWorkOrderList:
                curr_query = "insert into public.scan_table (work_order_number,entry_date) values ('"+str(item)+"','"+today_date+"')"
                cursor.execute(curr_query)

            ####################################### Get new assigned WONs to be inserted into DB #######################################
            NewAssignedWorkOrderList = [item for item in CurrentAssignedWorkOrderNumbers if not(item in ExistingUnassignedWorkOrderList+ExistingAssignedWorkOrderList)]
            print("NewAssignedWorkOrderList:",NewAssignedWorkOrderList)
            for item in NewAssignedWorkOrderList:
                if Role == "E":
                    curr_query = "insert into public.scan_table (work_order_number,entry_date,is_assigned,assign_date,assign_area,assign_operator_id) values ('"+str(item)+"','"+today_date+"','Y','"+today_date+"','"+LoadArea+"','"+str(ID)+"')"
                else:
                    curr_query = "insert into public.scan_table (work_order_number,entry_date,is_assigned,assign_date,assign_area,is_audited,audit_date,audit_operator_id) values ('"+str(item)+"','"+today_date+"','Y','"+today_date+"','"+LoadArea+"','Y','"+today_date+"','"+str(ID)+"')"
                cursor.execute(curr_query)
            ####################################### Get existing assigned WONs with new assign to be updated into DB #######################################
            ExistingAssignedWorkOrderList = [item for item in CurrentAssignedWorkOrderNumbers if (item in ExistingAssignedWorkOrderList)]
            print("ExistingAssignedWorkOrderList:",ExistingAssignedWorkOrderList)
            for item in ExistingAssignedWorkOrderList:
                print("Role",Role)
                if Role == "E":
                    curr_query = "update public.scan_table set is_assigned='Y',assign_date='"+today_date+"',"+"assign_area='"+LoadArea+"',assign_operator_id='"+str(ID)+"' where work_order_number='"+str(item)+"'"
                    # print("curr_query:",curr_query)
                else:
                    curr_query = "select assign_area from public.scan_table where work_order_number='"+str(item)+"'"
                    cursor.execute(curr_query)
                    res = cursor.fetchall()
                    previous_assign_area = res[0][0]
                    curr_query = "update public.scan_table set is_assigned='Y', assign_date='"+today_date+"',"+"assign_area='"+LoadArea+"',is_audited='Y',audit_date='"+today_date+"',previous_assign_area='"+previous_assign_area+"',audit_operator_id='"+str(ID)+"' where work_order_number='"+str(item)+"'"
                cursor.execute(curr_query)
            ####################################### Get existing unassigned WONs with assign to be updated into DB #######################################
            ExistingUnAssignedWorkOrderList = [item for item in CurrentAssignedWorkOrderNumbers if (not(item in ExistingAssignedWorkOrderList) and (item in ExistingUnassignedWorkOrderList))]
            print("ExistingUnAssignedWorkOrderList:",ExistingUnAssignedWorkOrderList)
            for item in ExistingUnAssignedWorkOrderList:
                if Role == "E":
                    curr_query = "update public.scan_table set is_assigned='Y',assign_date='"+today_date+"',"+"assign_area='"+LoadArea+"',assign_operator_id='"+str(ID)+"' where work_order_number='"+str(item)+"'"
                    # print("curr_query:",curr_query)
                else:
                    curr_query = "update public.scan_table set is_assigned='Y', assign_date='"+today_date+"',"+"assign_area='"+LoadArea+"',is_audited='Y',audit_date='"+today_date+"',audit_operator_id='"+str(ID)+"' where work_order_number='"+str(item)+"'"
                cursor.execute(curr_query)
            ############################################ Return Items ########################################################################
            cursor = connection.cursor()
            curr_query = "select work_order_number from public.scan_table st where is_audited='N' and moved_to_paint_line='N'"
            cursor.execute(curr_query)
            res = cursor.fetchall()
            ExistingUnassignedWorkOrderList = []
            for item in res:
                ExistingUnassignedWorkOrderList.append(item[0])
            all_unassigned_wons = "||".join(ExistingUnassignedWorkOrderList)
            assign_form = AssignLoadArea.AssignLoadAreaForm()
            context = {"unassigned_id":ExistingUnassignedWorkOrderList,"employee_id":ID,"role":Role,"assign_form":assign_form,"all_unassigned_wons":all_unassigned_wons}
            return render(request, "HTML/ScanPage.html", context=context)
    else:
        cursor = connection.cursor()
        curr_query = "select work_order_number from public.scan_table st where is_audited='N' and moved_to_paint_line='N'"
        cursor.execute(curr_query)
        res = cursor.fetchall()
        NotAssignedWorkOrderNumbersList = []
        for item in res:
            NotAssignedWorkOrderNumbersList.append(item[0])
        all_unassigned_wons = "||".join(NotAssignedWorkOrderNumbersList)
        assign_form = AssignLoadArea.AssignLoadAreaForm()
        context = {"unassigned_id":NotAssignedWorkOrderNumbersList,"assign_form":assign_form,"all_unassigned_wons":all_unassigned_wons}
        return render(request, "HTML/ScanPage.html", context=context)
