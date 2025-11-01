console.log("Sanity Check! | Voice Call.js");

const iceServers = [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "stun:stun.l.google.com:5349" },
    { urls: "stun:stun1.l.google.com:3478" },
    { urls: "stun:stun1.l.google.com:5349" },
    { urls: "stun:stun2.l.google.com:19302" },
    { urls: "stun:stun2.l.google.com:5349" },
    { urls: "stun:stun3.l.google.com:3478" },
    { urls: "stun:stun3.l.google.com:5349" },
    { urls: "stun:stun4.l.google.com:19302" },
    { urls: "stun:stun4.l.google.com:5349" }
];

let pendingCandidates = [];
let localStream = null;

const peerConnection = new RTCPeerConnection({ iceServers });

peerConnection.onicecandidate = event => {
  if (event.candidate) {
    socket.emit("send_ice_candidate", { candidate: event.candidate, to: otherFriendId });
  }
};

const remoteAudio =document.querySelector(".remoteAudio")
peerConnection.ontrack = event => {
  remoteAudio.srcObject = event.streams[0];
//  remoteAudio.play();
  remoteAudio.muted = true;

};

async function StartAudioCall() {
  localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  localStream.getTracks().forEach(t => peerConnection.addTrack(t, localStream));

  const offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);

  socket.emit("send_call_offer", { offer, to: otherFriendId });
}

socket.on("receive_call_offer", async ({ offer, from }) => {

  localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  localStream.getTracks().forEach(t => peerConnection.addTrack(t, localStream));

  await peerConnection.setRemoteDescription(offer);

  for (const c of pendingCandidates) await peerConnection.addIceCandidate(c);
  pendingCandidates = [];

  const answer = await peerConnection.createAnswer();
  await peerConnection.setLocalDescription(answer);

  socket.emit("send_call_answer", { answer, to: from });
});

socket.on("receive_call_answer", async ({ answer, from }) => {

  await peerConnection.setRemoteDescription(answer);

  for (const c of pendingCandidates) await peerConnection.addIceCandidate(c);
  pendingCandidates = [];
});

socket.on("receive_ice_candidate", async ({ candidate }) => {
  if (peerConnection.remoteDescription) {
    await peerConnection.addIceCandidate(candidate);
  } else {
    pendingCandidates.push(candidate);
  }
});

