// Function to open the popup model
function openPopupModel() {
    const popup = document.getElementById('popup-model');
    popup.style.display = 'block';
}

// Function to close the popup model
function closePopupModel() {
    const popup = document.getElementById('popup-model');
    popup.style.display = 'none';
}
function savePopupModel(data,token,path_model){
    var result_list = data;
    
    
    
    const updatedOrder = [...sortableList.querySelectorAll(".item")].map(item => item.querySelector("span").textContent);
    for(let i=0;i<updatedOrder.length;i++){
        const index = result_list.findIndex(obj => obj.column_name === updatedOrder[i]);
        if (index !== -1) {
            // Modify the properties of the object
            if ($('#chk'+updatedOrder[i]).prop('checked')) {
                result_list[index].visible = true;
              } 
            else{
                result_list[index].visible = false;
            }
            result_list[index].sort_order = i+1;
            // ... update other properties as needed
        }
    }
    
    // Send the AJAX request
    $.ajax({
        url: '/nucleus/save_prefrences/',
        method: 'POST',
        data: {
            updatedPrefrences: JSON.stringify(result_list),
            path_model:path_model,
            // Include any other data needed for the AJAX request
            csrfmiddlewaretoken: token
        },
        success: function(response) {
            // Handle the AJAX response
            if (response.success) {
                location.reload(true);
            }
        },
        error: function(error) {
            // Handle AJAX error
        }
    }); 
    
    // e.preventDefault();
    
  
    
}
