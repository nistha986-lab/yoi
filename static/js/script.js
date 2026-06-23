async function sendMessage() {

let message =
document.getElementById("message").value;

if(message===""){
return;
}

let chatBox =
document.getElementById("chat-box");

chatBox.innerHTML +=
`
<div class="user">
🧑 ${message}
</div>
`;

document.getElementById("message").value="";

let response = await fetch("/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
message:message
})
});

let data = await response.json();

chatBox.innerHTML +=
`
<div class="bot">
🦋 YOI: ${data.reply}
</div>
`;

chatBox.scrollTop =
chatBox.scrollHeight;
}