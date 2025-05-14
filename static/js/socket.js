const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const host = window.location.host;
const socket = new WebSocket(`${protocol}//${host}/ws`);

socket.onopen = () => {
    console.log("connected to server")
}

socket.onmessage = async (event) => {
    const message = event.data
    console.log(`Message received: ${message}`)
    await reloadMap()
}

socket.onerror = (error) => {
    console.error(`Websocket error: ${error}`)
}

socket.onclose = () => {
    console.log("connection closed")
}