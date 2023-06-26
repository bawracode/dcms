

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
  
  const csrftoken = getCookie('csrftoken');



async function render_sub_section(data) {
const configLink = document.querySelector('.config_link2');
configLink.innerHTML = '';

for (let i = 0; i < Object.keys(data).length - 1; i++) {
  const sectionData = data["sub_section"];
  
  const div = document.createElement('div');
  div.id = 'menu';
  div.classList.add('sub_section');
  
  const a = document.createElement('a');
  a.classList.add('subsection_menu');
  a.textContent = sectionData[i].section;
  
  
  const innerDiv = document.createElement('div');
  innerDiv.style.display = 'none';

  for(let i=0; i < sectionData.length;i++){
    let temp1 = sectionData[i]
    for (let j = 0; j < temp1.fields.length; j++) {
        const field = temp1.fields[j]
                  

        let element;
        if (field.type === 'varchar') {
        element = createTextField(field.label, field.default, field.key);
        } else if (field.type === 'text') {
        element = createTextArea(field.label, field.default, field.key);
        } else if (field.type === 'single_select') {
        all_options = await fetch_option(field.key)
        element = createSingleSelectField(field.label, all_options,field.default, field.key);
        } else if (field.type === 'switch') {
        element = createToggleButton(field.label, field.default);
        }
        
        if (element) {
        innerDiv.appendChild(element);
        }

        
        
      }
  }
  
  div.appendChild(a);
  div.appendChild(document.createElement('br'));
  div.appendChild(innerDiv);
  

  configLink.appendChild(div);
  logInputOnBlur();
  $('#menu > a').click(function(){
    $(this).next().next().slideToggle();
    return false;
});
}
}

function createToggleButton(label, defaultValue) {
const lebal = document.createElement('label');
lebal.textContent = label;


const fieldLabel = document.createElement('label');

fieldLabel.classList.add('switch');

const input = document.createElement('input');
input.type = 'checkbox';
input.name = label;
input.checked = defaultValue || false;

const span = document.createElement('span');
span.classList.add('slider');
span.classList.add('round');

fieldLabel.appendChild(input);
fieldLabel.appendChild(span);

const container = document.createElement('div');
container.appendChild(lebal);
container.appendChild(fieldLabel);

return container;
}


function createSingleSelectField(label, all_options, defaultValue, key) {
const fieldLabel = document.createElement('label');
fieldLabel.textContent = label;

const select = document.createElement('select');
select.name = label;
select.id = key;


for (let i = 0; i < all_options.length; i++) {
  const option = document.createElement('option');
  option.value = all_options[i];
  option.textContent = all_options[i];
  select.appendChild(option);
}

const br = document.createElement('br');

const container = document.createElement('div');
container.appendChild(fieldLabel);
container.appendChild(br);
container.appendChild(select);

return container;
}

function createTextField(label, defaultValue, key) {
const fieldLabel = document.createElement('label');
fieldLabel.textContent = label;

const input = document.createElement('input');
input.type = 'text';
input.name = label;
input.id = key;
input.value = defaultValue || '';

const br = document.createElement('br');

const container = document.createElement('div');
container.appendChild(fieldLabel);
container.appendChild(br);
container.appendChild(input);

return container;
}

function createTextArea(label, defaultValue, key) {
const fieldLabel = document.createElement('label');
fieldLabel.textContent = label;

const textarea = document.createElement('textarea');
textarea.name = label;
textarea.id = key;
textarea.rows = '4';
textarea.cols = '50';
textarea.textContent = defaultValue || '';

const br = document.createElement('br');

const container = document.createElement('div');
container.appendChild(fieldLabel);
container.appendChild(br);
container.appendChild(textarea);

return container;
}

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
      render_sub_section(responseData)
      
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function logInputOnBlur() {
const inputs = document.querySelectorAll('input, textarea, select');

for (let i = 0; i < inputs.length; i++) {
  inputs[i].addEventListener('blur', function(event) {

    save_change_value(event.target.id,event.target.value)
  });
}
}

function save_change_value(key,value){
fetch('/app_config/save_change_value/', {
    method: 'POST',
    headers: {
      'Content-Type': "application/json",
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      'key': key,
      'value': value
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
