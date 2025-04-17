import React, { useState, useRef } from 'react'
import './App.css'

function App() {
  // const [isOpen, setIsOpen] = useState(false);
  const [userName, setUserName] = useState('');
  const [birthday, setBirthday] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const dialogRef = useRef(null);

  const changeBtn = async () => {
    const response = await fetch("http://localhost:8000/user/", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "Authorization": accessToken,
      },
      body: JSON.stringify({ username: userName, birthday: birthday}),
    });
    console.log(response);
  }

  const deleteBtn = async () => {
    const response = await fetch("http://localhost:8000/user/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": accessToken,
      },
      // body: JSON.stringify({ username: userName, birthday: birthday}),
    });
    console.log(response);
    // const result = await response.json();
    // setAccessToken(result.access_token);
  };

  const loginBtn = async () => {
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: userName }),
    });
    const result = await response.json();
    setAccessToken(result.access_token);
  };

  const createBtn = async () => {
    const response = await fetch("http://localhost:8000/user/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: userName, birthday: birthday }),
    });
    console.log(response);
    // const result = await response.json();
    // setAccessToken(result.access_token);
  };

  React.useEffect(() => {
    if(accessToken !== ''){
      console.log(accessToken);
    }
  }, [accessToken]);
  
  return (
    <>
      <div id="user_dialog">
        User Name<br />
        <input 
            type="text" 
            id="user_name_box" 
            className="user_input"
            name="user_name_box" 
            placeholder="Name" 
            size="10" 
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
        />
        Birthday<br />
        <input 
            type="date" 
            id="birthday_box" 
            className="user_input" 
            name="birthday_box"  
            value={birthday}
            onChange={(e) => setBirthday(e.target.value)}
        />
        {/* change user data */}
        <button onClick={changeBtn}>Change</button>
        {/* delete user */}
        <button onClick={deleteBtn}>Delete</button>
        <button onClick={loginBtn}>Login</button>
        <button onClick={createBtn}>CreateUser</button>
    </div>
    </>
  )
}

export default App
