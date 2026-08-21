import { useState } from "react";
import { useNavigate } from "react-router";

import "./LoginInput.css"

export default function LoginInput() {
    const [loginData, setLoginData] = useState({
        username: '',
        password: ''
    });
    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setLoginData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };

    const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:8000/api/auth/login", {
                method: "POST",
                headers: {
                    "Accept": "application/json"
                },
                // using URLSearchParams instead of JSON.stringify() due to FastAPI and pydantic validation
                body: new URLSearchParams({
                    username: loginData.username, password: loginData.password
                })
            });

            if (response.ok) {
                // Redirect to user page once it is created. Redirect to the home page for now.
                navigate("/", { replace: true });
                
            } else if (response.status === 422) {
                const errorData = await response.json();
                console.log("Validation Failed:", errorData);
            } else {
                console.log("Something went wrong...");
                console.log(response);
            }

        } catch (error) {
            console.log("Error sending data:", error);
        }

    };

    return (
        <div>
            <form className="login-form" onSubmit={handleSubmit}>
                <label className="login-label" htmlFor="username">
                    Username
                    <input
                        type="username"
                        name="username"
                        value={loginData.username}
                        onChange={handleChange}
                        placeholder="Username"
                        className="login-input"
                        id="username"
                    />
                </label>

                <label className="login-label" htmlFor="password">
                    Password
                    <input 
                        type="password"
                        name="password"
                        value={loginData.password}
                        onChange={handleChange}
                        placeholder="Password"
                        className="login-input"
                        id="password"
                    />
                </label>

                <button className="login-info-submit-button" type="submit">
                    Login
                </button>
            </form>
        </div>
    )
}