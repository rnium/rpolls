let inputsdiv = document.getElementById('choices');
let add_choice_btn = document.getElementById('add-choice');
let remove_choice_btn = document.getElementById('remove-choice');
let choicecount = 3;

add_choice_btn.onclick = function() {
    let new_input = document.createElement('input');
    new_input.setAttribute('type', 'text');
    new_input.setAttribute('class', 'textinput choiceinput');
    new_input.setAttribute('placeholder', `choice ${choicecount}`);
    new_input.setAttribute('name', `choice${choicecount}`);
    new_input.setAttribute('required', "");
    inputsdiv.appendChild(new_input);
    choicecount += 1;
};

remove_choice_btn.onclick = function() {
    let inputs = document.getElementsByClassName('choiceinput')
    if (inputs.length > 2) {
        inputsdiv.removeChild(inputs[inputs.length - 1]);
        choicecount -= 1;
    };
};