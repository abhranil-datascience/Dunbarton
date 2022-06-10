function set_focus(){
  text_area = document.getElementById('AuditScanInput')
  text_area.focus()
}
function GetWorkOrderNumber(e){
  if (e.keyCode == 13) {
    document.getElementById('WorkOrderNumberAuditTable').innerHTML = ""
    document.getElementById('id_WorkOrderNumber').value = ""
    document.getElementById('LoadAreaCell').innerHTML = ""
    var scanned_won = document.getElementById('AuditScanInput').value
    document.getElementById('AuditScanInput').value = ""
    console.log(scanned_won)
    var mod_won = "_"+scanned_won
    var non_painted_wons = document.getElementsByName('non_painted_wons')[0].getAttribute('content')
    var non_painted_wons_array = non_painted_wons.split("||")
    var painted_wons = document.getElementsByName('painted_wons')[0].getAttribute('content')
    var painted_wons_array = painted_wons.split("||")
    var found = false
    for (let i=0; i<non_painted_wons_array.length; i++){
      var curr_comb = non_painted_wons_array[i]
      var curr_comb_array = curr_comb.split("-")
      var curr_won = curr_comb_array[0]
      var curr_ar = curr_comb_array[1]
      if (curr_won == mod_won){
        if (!painted_wons_array.includes(mod_won)){
          if (curr_ar!="N")
          {
            document.getElementById('LoadAreaCell').innerHTML = curr_ar
          }
          document.getElementById('WorkOrderNumberAuditTable').innerHTML = scanned_won
          document.getElementById('id_WorkOrderNumber').value = mod_won
          break
        }
        else{
          alert("Work Order Number "+scanned_won+"is already in paint line")
          break
        }
      }
    }
    if (!found){
      if (painted_wons_array.includes(mod_won)){
        document.getElementById('WorkOrderNumberAuditTable').innerHTML = ""
        document.getElementById('id_WorkOrderNumber').value = ""
        document.getElementById('LoadAreaCell').innerHTML = ""
        alert("Work Order Number "+scanned_won+"is already in paint line")
      }
      else{
        document.getElementById('WorkOrderNumberAuditTable').innerHTML = scanned_won
        document.getElementById('id_WorkOrderNumber').value = mod_won
      }
    }
    text_area = document.getElementById('AuditScanInput')
    text_area.focus()
  }
}
function AddWonManually(){
  document.getElementById('WorkOrderNumberAuditTable').innerHTML = ""
  document.getElementById('id_WorkOrderNumber').value = ""
  document.getElementById('LoadAreaCell').innerHTML = ""
  var scanned_won = document.getElementById('AuditAddManualWONInput').value
  document.getElementById('AuditAddManualWONInput').value = ""
  console.log(scanned_won)
  if (scanned_won != ""){
    var mod_won = "_"+scanned_won
    var non_painted_wons = document.getElementsByName('non_painted_wons')[0].getAttribute('content')
    var non_painted_wons_array = non_painted_wons.split("||")
    var painted_wons = document.getElementsByName('painted_wons')[0].getAttribute('content')
    var painted_wons_array = painted_wons.split("||")
    var found = false
    for (let i=0; i<non_painted_wons_array.length; i++){
      var curr_comb = non_painted_wons_array[i]
      var curr_comb_array = curr_comb.split("-")
      var curr_won = curr_comb_array[0]
      var curr_ar = curr_comb_array[1]
      if (curr_won == mod_won){
        if (!painted_wons_array.includes(mod_won)){
          console.log("this")
          if (curr_ar!="N")
          {
            console.log("here")
            document.getElementById('LoadAreaCell').innerHTML = curr_ar
          }
          document.getElementById('WorkOrderNumberAuditTable').innerHTML = scanned_won
          document.getElementById('id_WorkOrderNumber').value = mod_won
          break
        }
        else{
          alert("Work Order Number "+scanned_won+"is already in paint line")
          break
        }
      }
    }
    if (!found){
      if (painted_wons_array.includes(mod_won)){
        document.getElementById('WorkOrderNumberAuditTable').innerHTML = ""
        document.getElementById('id_WorkOrderNumber').value = ""
        document.getElementById('LoadAreaCell').innerHTML = ""
        alert("Work Order Number "+scanned_won+"is already in paint line")
      }
      else{
        document.getElementById('WorkOrderNumberAuditTable').innerHTML = scanned_won
        document.getElementById('id_WorkOrderNumber').value = mod_won
      }
    }
  }
  text_area = document.getElementById('AuditScanInput')
  text_area.focus()
}
function AuditAddLoadAreaFunction(LA){
  if (document.getElementById('WorkOrderNumberAuditTable').innerHTML.trim() != ""){
    console.log("I am here")
    document.getElementById('submit-id-submit').disabled = false
    document.getElementById('id_LoadArea').value = LA
  }
  else{
    document.getElementById('submit-id-submit').disabled = true
  }
  text_area = document.getElementById('AuditScanInput')
  text_area.focus()
}
