function addWonManually()
{
  // Get the Manually Entered Won and Clear the Manually Entered Won Field
  var Won = document.getElementById('AddManualWONInput').value
  var mod_won = "_"+Won
  document.getElementById("AddManualWONInput").value = ""
  if (Won == "")
  {
    alert("Please enter a valid Work Order Number")
  }
  else{
    // On new entry add it Work Order Numbers Div
    var CurrentWonDiv = document.getElementById('WorkOrderTableDiv').innerHTML
    CurrentWonDiv = CurrentWonDiv+'<div class="form-check"><input class="form-check-input" type="checkbox" value="" id='+mod_won+' onclick="AddWonToAssignedWorkOrderNumbers('+mod_won+')"><label class="form-check-label" for='+mod_won+'>'+Won+'</label></div>'
    document.getElementById('WorkOrderTableDiv').innerHTML = CurrentWonDiv

    // Add each Won to modal form
    var AllWons = document.getElementById('id_AllWorkOrderNumbers').value
    if (AllWons==""){
      AllWons = mod_won
    }
    else{
      AllWons = AllWons+"||"+mod_won
    }
    document.getElementById('id_AllWorkOrderNumbers').value = AllWons

    // Copy state from meta variable
    var MetaWon = document.getElementsByName('MetaWon')[0].getAttribute('content')
    if (!MetaWon==""){
      MetaWonArray = MetaWon.split('||')
      for(var i = 0; i < MetaWonArray.length; i++){
        curr_won = MetaWonArray[i]
        curr_checkbox = document.getElementById(curr_won)
        curr_checkbox.checked = true
      }
    }
  }
}
function AddWonToAssignedWorkOrderNumbers(CurrentWon){
  CurrentWon = CurrentWon.id
  console.log(CurrentWon)
  // Grab id of calling Won
  curr_checkbox = document.getElementById(CurrentWon)
  // Find if checkbox is checked or not

  var IsChecked = false
  if (curr_checkbox.checked){
    IsChecked = true
  }
  // Grab AssignedWorkOrderNumbers field in Modal form
  var AssignedWons = document.getElementById('id_AssignedWorkOrderNumbers').value

  // Grab meta variable to identify state
  var MetaWon = document.getElementsByName('MetaWon')[0].getAttribute('content')

  if (IsChecked) {
    // Add wons to AssignedWorkOrderNumbers in Modal form
    if (!AssignedWons.includes(CurrentWon)){
      if (AssignedWons == ""){
        AssignedWons = CurrentWon
      }
      else{
        AssignedWons = AssignedWons+"||"+CurrentWon
      }
      document.getElementById('id_AssignedWorkOrderNumbers').value = AssignedWons
    }
    // Add wons to Meta Variable
    if (!MetaWon.includes(CurrentWon)){
      if (MetaWon == ""){
        MetaWon = CurrentWon
      }
      else{
        MetaWon = MetaWon+"||"+CurrentWon
      }
      document.getElementsByName('MetaWon')[0].setAttribute('content',MetaWon)
    }

  }
  else{
    // Remove wons from AssignedWorkOrderNumbers in Modal form
    if(AssignedWons.includes(CurrentWon))
    {
      if(AssignedWons.endsWith("||"+CurrentWon)){
        AssignedWons = AssignedWons.replace("||"+CurrentWon,"")
      }
      else if (AssignedWons.startsWith(CurrentWon+"||")) {
        AssignedWons = AssignedWons.replace(CurrentWon+"||","")
      }
      else if (AssignedWons.includes("||"+CurrentWon+"||")){
        AssignedWons = AssignedWons.replace(CurrentWon+"||","")
      }
      else{
        AssignedWons = AssignedWons.replace(CurrentWon,"")
      }
      document.getElementById('id_AssignedWorkOrderNumbers').value = AssignedWons
    }
    // Remove wons from Meta Variable
    if(MetaWon.includes(CurrentWon))
    {
      if(MetaWon.endsWith("||"+CurrentWon)){
        MetaWon = MetaWon.replace("||"+CurrentWon,"")
      }
      else if (MetaWon.startsWith(CurrentWon+"||")) {
        MetaWon = MetaWon.replace(CurrentWon+"||","")
      }
      else if (MetaWon.includes("||"+CurrentWon+"||")){
        MetaWon = MetaWon.replace(CurrentWon+"||","")
      }
      else{
        MetaWon = MetaWon.replace(CurrentWon,"")
      }
      document.getElementsByName('MetaWon')[0].setAttribute('content',MetaWon)
    }
  }
}
function AddLoadAreaFunction(LoadArea){
  // Set LoadArea field in Modal form
  document.getElementById('id_LoadArea').value = LoadArea
}
function addAllWon(){
  ModalAllWonFieldValues = document.getElementById('id_AllWorkOrderNumbers').value
  ModalAssignedFieldValues = document.getElementById('id_AssignedWorkOrderNumbers').value
  ModalAllWonFieldValuesArray = ModalAllWonFieldValues.split('||')
  for(var i = 0; i < ModalAllWonFieldValuesArray.length; i++){
    curr_won = ModalAllWonFieldValuesArray[i]
    curr_checkbox = document.getElementById(curr_won)
    curr_checkbox.checked = true
    if (!ModalAssignedFieldValues.includes(curr_won)){
      if (ModalAssignedFieldValues == ""){
        ModalAssignedFieldValues = curr_won
      }
      else{
        ModalAssignedFieldValues = ModalAssignedFieldValues + "||" +curr_won
      }
    }
  }
  document.getElementById('id_AssignedWorkOrderNumbers').value = ModalAssignedFieldValues
}
