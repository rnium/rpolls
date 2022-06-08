// copy to clipboard
let poll_link = document.getElementById('poll-link');
let ctc_btn = document.getElementById('ctc');

ctc_btn.onclick = function() {
  navigator.clipboard.writeText(poll_link.innerText);
  alert("link copied to clipboard");
}