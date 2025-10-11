console.log("Sanity Check! | Friends.js");

const add_friend_btn = document.querySelector(".add_friend");
const add_friends_popup = document.querySelector(".add_friends_popup");

const add_friend_username = document.querySelector(".add_username_input")
const add_friend_submit_btn = document.querySelector(".add_friend_submit_btn")
const add_friend_error = document.querySelector(".add_friend_error")

add_friend_btn.addEventListener("click", () => {
    add_friends_popup.classList.toggle("dnone")
});


add_friend_submit_btn.addEventListener("click", async () => {
    const username = add_friend_username.value.trim();

    if (!username) return;

    try {
        const response = await fetch(`/friends/add/${username}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "same-origin",
        });

        const data = await response.json();

        if (!response.ok) {
            add_friend_error.textContent = data.error || "Something went wrong..";
        } else {
            add_friend_error.textContent = data.message;
        }

    } catch (error) {
        add_friend_error.textContent = "Network Error";
        console.log(error)
    }


    console.log(username);
})


const profile_btn = document.querySelector(".profile");
const profile_popup = document.querySelector(".profile_popup");



profile_btn.addEventListener("click", () => {
    profile_popup.classList.toggle("dnone")
});

