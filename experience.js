function submitAnswer() {
  let radios = document.getElementsByName("choice");
  let i = 0, len = radios.length;
  let checked = false;
  let userAnswer;
  
  for( i = 0; i < len; i++ ) {
     if(radios[i].checked) {
       checked = true;
       userAnswer = radios[i].value;
     }
  } 
  // if user click submit button without selecting any option, alert box should be say "please select choice answer".
  if(!checked) {
    alert("Please choose an Experience Type.");
    return;
  }
  
}