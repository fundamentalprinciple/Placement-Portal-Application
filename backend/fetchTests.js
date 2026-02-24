let p1 = fetch("http://localhost:3000/login?include_auth_token", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
                email: "princedixit931@gmail.com",
                password: "12345678"
            })
})

p1.then((response)=>{return response.json()}).then((response)=>{console.log(response)})

