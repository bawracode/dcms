
// getCookie function: fetch cookie from browser
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}



// csrf token for ajax request
const csrftoken = getCookie('csrftoken');


default_section = sessionStorage.getItem("section_name");
if(default_section != null){
  render_section(default_section);

}else{
  render_section('Settings');
}


// get all the sections, sub-sections and fields
async function render_sub_section(section_name,data) {
  const configLink = document.querySelector('.config_link2');

  toggleVisibility(convertToClassName(section_name));

  if(checkSectionExistence(convertToClassName(section_name)) == 0){
    console.log()

    for (let i = 0; i < Object.keys(data).length - 1; i++) {
      const sectionData = data["sub_section"];
  
      const div = document.createElement('div');
      div.id = 'menu';
      div.classList.add(convertToClassName(section_name));
  
      const anchor_tag = document.createElement('a');
      anchor_tag.classList.add('subsection_menu');
      anchor_tag.classList.add(convertToClassName(sectionData[i].section));
      anchor_tag.textContent = sectionData[i].section;
  
      const innerDiv = document.createElement('div');
      innerDiv.style.display = 'none';
      innerDiv.classList.add(`${convertToClassName(sectionData[i].section)}_div`)
  
      for (let i = 0; i < sectionData.length; i++) {
        let temp1 = sectionData[i];
        for (let j = 0; j < temp1.fields.length; j++) {
          const field = temp1.fields[j];
  
          let element;
          if (field.type === 'varchar') {
            element = createTextField(field.label, field.default, field.key);
          } else if (field.type === 'text') {
            element = createTextArea(field.label, field.default, field.key);
          } else if (field.type === 'single_select') {
            all_options = await fetch_option(field.key);
            console.log(field.default)
            element = createSingleSelectField(
              field.label,
              all_options,
              field.default,
              field.key
            );
          } else if (field.type === 'switch') {
            element = createToggleButton(field.label, eval(field.default), field.key);
          } else if (field.type === 'multiple_select') {
            console.log(field.default)
            all_options = await fetch_option(field.key);
            
            element = createMultipleSelectField(
              field.label,
              all_options,
              field.default,
              field.key
            );
          }
  
          if (element) {
            innerDiv.appendChild(element);
          }
        }
      }
  
      div.appendChild(anchor_tag);
      div.appendChild(document.createElement('br'));
      div.appendChild(innerDiv);
  
      const saveButton = document.createElement('button');
      saveButton.textContent = 'Save';


      anchor_tag.addEventListener('click', function () {
      if(innerDiv.style.display == 'none'){
      
        sessionStorage.setItem("sub_section",`${convertToClassName(sectionData[i].  section)}_div`);
      }else{
        sessionStorage.removeItem("sub_section");
      }

      
      });
  
      saveButton.addEventListener('click', async function () {
        const inputs = innerDiv.querySelectorAll('input, select, textarea');
      
        const formData = {};
  
        for (let i = 0; i < inputs.length; i++) {
          const input = inputs[i];
  
          if (input.type === 'checkbox') {
            formData[input.classList[0]] = getCheckboxValues(input.classList[0]);
          }
          else{
            formData[input.classList[0]] = input.value;
          }
        }
        save_change_value(formData);
      });
  
      innerDiv.appendChild(saveButton);
      configLink.appendChild(div);

      default_sub_section = sessionStorage.getItem("sub_section");
      if(default_sub_section != null){
        let temp = document.getElementsByClassName(default_sub_section);
        if(temp.length > 0){
          temp[0].style.display = "block";
        }
      } 
    }
  
    $(`#menu > a`).click(function () {
      $(this).next().next().slideToggle();
      return false;
    });
  }
  // configLink.innerHTML = '';
  
}


// create multiple select field
function createMultipleSelectField(label, all_options, defaultValues, key) {
  const fieldLabel = document.createElement('label');
  fieldLabel.textContent = label;

  const container = document.createElement('div');

  for (let i = 0; i < all_options.length; i++) {
    const option = document.createElement('div');
    option.classList.add('checkbox-option');

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.name = label;
    checkbox.value = all_options[i];
    checkbox.id = key + i;
    checkbox.classList.add(key);

    if (defaultValues.includes(all_options[i])) {
      checkbox.checked = true; 
    }

    const checkboxLabel = document.createElement('label');
    checkboxLabel.textContent = all_options[i];
    checkboxLabel.setAttribute('for', key + i);

    option.appendChild(checkbox);
    option.appendChild(checkboxLabel);
    container.appendChild(option);
  }

  const br = document.createElement('br');
  container.appendChild(br);

  const fieldContainer = document.createElement('div');
  fieldContainer.appendChild(fieldLabel);
  fieldContainer.appendChild(container);

  return fieldContainer;
}



// create toggle button
function createToggleButton(label, defaultValue, key) {
  const fieldLabel = document.createElement('label');
  fieldLabel.classList.add('switch');

  const input = document.createElement('input');
  input.type = 'checkbox';
  input.name = label;
  input.checked = defaultValue;
  input.id = key;
  input.classList.add(key);

  input.addEventListener('change', function () {
    const isChecked = input.checked;
    console.log(isChecked)
    input.value = isChecked;
  });

  const span = document.createElement('span');
  span.classList.add('slider');
  span.classList.add('round');

  fieldLabel.appendChild(input);
  fieldLabel.appendChild(span);

  const container = document.createElement('div');
  container.appendChild(document.createTextNode(label));
  container.appendChild(fieldLabel);

  return container;
}


// create single select field
function createSingleSelectField(label, all_options, defaultValue, key) {
  const fieldLabel = document.createElement('label');
  fieldLabel.textContent = label;

  const select = document.createElement('select');
  select.name = label;
  select.id = key;
  select.classList.add(key);


  for (let i = 0; i < all_options.length; i++) {
    const option = document.createElement('option');
    option.value = all_options[i];
    option.textContent = all_options[i];

    if (all_options[i] === defaultValue) {
      option.selected = true; // Set the default option as selected
    }

    select.appendChild(option);
  }

  const br = document.createElement('br');

  const container = document.createElement('div');
  container.appendChild(fieldLabel);
  container.appendChild(br);
  container.appendChild(select);

  return container;
}



// create text field
function createTextField(label, defaultValue, key) {
const fieldLabel = document.createElement('label');
fieldLabel.textContent = label;

const input = document.createElement('input');
input.type = 'text';
input.name = label;
input.id = key;
input.value = defaultValue || '';
input.classList.add(key);

const br = document.createElement('br');

const container = document.createElement('div');
container.appendChild(fieldLabel);
container.appendChild(br);
container.appendChild(input);

return container;
}


// create text area
function createTextArea(label, defaultValue, key) {
const fieldLabel = document.createElement('label');
fieldLabel.textContent = label;

const textarea = document.createElement('textarea');
textarea.name = label;
textarea.id = key;
textarea.rows = '4';
textarea.cols = '50';
textarea.textContent = defaultValue || '';
textarea.classList.add(key);


const br = document.createElement('br');

const container = document.createElement('div');
container.appendChild(fieldLabel);
container.appendChild(br);
container.appendChild(textarea);

return container;
}


// fetch options for single select field
async function fetch_option(key) {

const url = `/app_config/return_option/`;

try {
const response = await fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': "application/json",
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({
    'key': key
  })
});

if (!response.ok) {
  throw new Error('Error: ' + response.status);
}
const responseData = await response.json();

return responseData["options"];
} catch (error) {
console.error('Error:', error);
}
}





// render sub section
function render_section(section_name){

const url = `/app_config/return_sub_section/`;

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': "application/json",
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({
    'section_name': section_name
  })
})
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Error: ' + response.status);
  })
  .then(responseData => {
    sessionStorage.setItem("section_name", section_name);
    render_sub_section(section_name,responseData)
    
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


// log input on blur
// cancel this idea
function logInputOnBlur() {

const inputs = document.querySelectorAll('input, textarea, select');

for (let i = 0; i < inputs.length; i++) {
inputs[i].addEventListener('blur', function(event) {

  save_change_value(event.target.id,event.target.value)
});
}
}


// save_change_value function
function save_change_value(form_field){
fetch('/app_config/save_change_value/', {
  method: 'POST',
  headers: {
    'Content-Type': "application/json",
    'X-Requested-With': 'XMLHttpRequest',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({
    'form_field': form_field
  })
})
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Error: ' + response.status);
  })
  .then(responseData => {
    console.log(responseData)
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


// make array of checked checkboxes
function getCheckboxValues(className) {
  var checkboxValues = [];
  var checkboxes = document.querySelectorAll('.' + className);
  if (checkboxes.length === 1) {
    var checkbox = checkboxes[0];
    var checkboxValue = checkbox.checked;
    return checkboxValue;
  } else {
    for (var i = 0; i < checkboxes.length; i++) {
      var checkbox = checkboxes[i];
      if (checkbox.checked)
      {
        checkboxValues.push(checkbox.value);
      }
    }
    return checkboxValues;
  }
}

function convertToClassName(str) {
  return str.replace(/\s+/g, '_');
}


function toggleVisibility(className) {
  var parentContainer = document.querySelector('.config_link2');
  var childElements = parentContainer.children;
  for (var i = 0; i < childElements.length; i++) {
    var child = childElements[i];
    if (child.classList.contains(className)) {
      child.style.display = 'block';
    } else {
      child.style.display = 'none';
    }
  }
}

function checkSectionExistence(className) {
  var parentContainer = document.querySelector('.config_link2');
  var section = parentContainer.querySelector('.' + className);
  if (section) {
    return 1;
  } else {
    return 0;
  }
}
