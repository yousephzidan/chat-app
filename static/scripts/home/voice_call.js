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
const remoteVideo =document.querySelector(".remoteVideo")

document.addEventListener('keydown', (e) => {
  if (e.altKey && e.key === "m") {
    let t = localStream.getAudioTracks()[0];
    t.enabled = !t.enabled;}
  if (e.altKey && e.key === "v") {
    let t = localStream.getVideoTracks()[0];
    t.enabled = !t.enabled;}
});

peerConnection.ontrack = event => {
  remoteAudio.srcObject = event.streams[0];
  remoteAudio.play();
  remoteVideo.srcObject = event.streams[0];
//remoteAudio.muted = true;

};

async function StartAudioCall() {
  localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
  localStream.getTracks().forEach(t => peerConnection.addTrack(t, localStream));

  const offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);

  socket.emit("send_call_offer", { offer, to: otherFriendId });
}

socket.on("receive_call_offer", async ({ offer, from }) => {

  localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
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

