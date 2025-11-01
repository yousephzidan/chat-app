console.log("Sanity Check! | Chat.js");

const input_btn = document.querySelector(".input_btn");
const send_btn = document.querySelector(".send_btn");
const msg_screen = document.querySelector(".msg_screen");
const friend_chat = document.querySelector(".friend");  
const ChatWith = document.querySelector(".ChatWith");  

var otherFriendId;
var otherFriendUsername;

let contactId;

send_btn.addEventListener("click", () => {
  const msg_val = input_btn.value;
})

const socket = io();

async function chat(receiver_id, username) {
  msg_screen.textContent = ''; 
  
  
  ChatWith.textContent = `Chat with ${username}`;
  const data = await fetch(`/chat/${receiver_id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "same-origin",

  }) 

  otherFriendId = receiver_id;
  otherFriendUsername = username;

  const info = await data.json();
  info.forEach(data => {

    const newMessage = document.createElement('div');
    const msg_content = document.createElement('p'); 

    msg_content.textContent = data.msg;
    newMessage.classList.add('msg');

    if (data.id == current_user_id) newMessage.classList.add("sender");

    newMessage.appendChild(msg_content);

    msg_screen.appendChild(newMessage);

  })

  console.log(info)
  contactId = receiver_id;

  socket.emit("join_dm", {
    dm_contact_id: contactId
  })
  msg_screen.scrollTop = msg_screen.scrollHeight;

}

function send_msg() {
  const msg_val = input_btn.value;

  socket.emit("send_dm", {
    dm_contact_id: contactId,
    msg: msg_val
  })

}

socket.on('receive_msg', data => {
  console.log(data);

  const newMessage = document.createElement('div');
  const msg_content = document.createElement('p'); 

  msg_content.textContent = data.msg;
  newMessage.classList.add('msg');
  
  console.log(current_user_id)
  if (data.sender_id == current_user_id) newMessage.classList.add("sender");

  newMessage.appendChild(msg_content);

  msg_screen.appendChild(newMessage);
  msg_screen.scrollTop = msg_screen.scrollHeight;

  input_btn.value = '';

})

