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

const IceServers = {
  iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
};

peerConnection = new RTCPeerConnection(IceServers);
async function StartAudioCall() {
  console.log("[Frontend] Starting audio call to", otherFriendId);

  localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  console.log("[Frontend] Local audio stream obtained");

  
  localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

  peerConnection.onicecandidate = event => {
    if (event.candidate) {
      console.log("[Frontend] Sending ICE candidate:", event.candidate);
      socket.emit("send_ice_candidate", { candidate: event.candidate, to: otherFriendId });
    }
  };

  peerConnection.ontrack = event => {
    console.log("[Frontend] Received remote track");
    const remoteAudio = document.querySelector(".remoteAudio");
    remoteAudio.srcObject = event.streams[0];
  };

  const offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);
  console.log("[Frontend] Sending offer:", offer);

  socket.emit("send_call_offer", { offer, to: otherFriendId });

}

socket.on("receive_call_offer", async ({offer, from}) => {
  console.log("[Frontend] Received call offer from:", from);

  localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  console.log("[Frontend] Local audio stream obtained for answer");

  peerConnection = new RTCPeerConnection(IceServers);
  localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

  peerConnection.onicecandidate = event => {
    if (event.candidate) {
      console.log("[Frontend] Sending ICE candidate for answer:", event.candidate);

      socket.emit("send_ice_candidate", { candidate: event.candidate, to: from });
    }
  };

  peerConnection.ontrack = event => {
    console.log("[Frontend] Received remote track for answer");

    document.getElementById("remoteAudio").srcObject = event.streams[0];
  };

  await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
  console.log("[Frontend] Remote description set from offer");

  const answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);
  socket.emit("send_call_answer", { answer, to: from });


})

socket.on("receive_call_answer", async ({ answer, from }) => {
  console.log("[Frontend] receive answer:", answer);

  await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
});

socket.on("receive_ice_candidate", async ({ candidate }) => {
   try {
        await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    } catch(err) {
        console.error("Error adding ICE candidate", err);
    } 
});
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

