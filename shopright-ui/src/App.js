import React, { useState, useEffect } from "react";
import SlotTable from './SlotTable.js'
import socketIOClient from "socket.io-client";

const ENDPOINT = "";

function App() {
  const [response, setResponse] = useState("");
  
  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);
    socket.on("my_response", response => {
      var slots_json = JSON.parse(response.data);
      var slot_array = Object.entries(slots_json)
      setResponse(slot_array);
    });
    socket.on("connect", data => {
      console.log("connected");
    });
  }, []);

  return (
    <div style={{width : '50%', margin: '0 auto', paddingTop: "50px"}}>
      <h2 style={{textAlign: 'center', paddingBottom: '10px'}}>ShopRite Pickup Slots</h2>
      <SlotTable slot={response}></SlotTable>
    </div>
  );
}

export default App;
