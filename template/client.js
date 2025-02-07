const user_id = 1

const socket = io("https://pi-project-i6z7.onrender.com", {
    query: { user_id }
});

// 🔹 Message de confirmation de connexion
socket.on(`user_connected_${user_id}`, (data) => {
    console.log("✅ Connexion WebSocket réussie :", data);
});

socket.on(`new_entry_${user_id}`, (signatures) => {
    console.log("📢 Liste mise à jour des signatures :", signatures);
});