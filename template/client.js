const socket = io("http://127.0.0.1:5000", {
    query: 1
});

// 🔹 Message de confirmation de connexion
socket.on(`user_connected_${user_id}`, (data) => {
    console.log("✅ Connexion WebSocket réussie :", data);
});

socket.on(`new_entry_${user_id}`, (signatures) => {
    console.log("📢 Liste mise à jour des signatures :", signatures);
});