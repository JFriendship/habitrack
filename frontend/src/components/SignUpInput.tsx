import { useState } from "react";
import { useNavigate } from "react-router";

import "./SignUpInput.css"

export default function SignUpInput() {
    const [signUpData, setSignUpData] = useState({
        email: '',
        username: '',
        password: ''
    });
    const navigate = useNavigate();


    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setSignUpData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    }


    const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:8000/api/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email: signUpData.email, username: signUpData.username, password: signUpData.password}),
            });

            if (response.ok) {
                // Redirect to login page
                navigate("/", { replace: true })
            } else {
                console.log("Something went wrong...")
            }

        } catch (error) {
            console.log("Error sending data:", error);
        }
    };

    return (
        <div>
            <form className="sign-up-form" onSubmit={handleSubmit}>
                <label className="input-label" htmlFor="email"> 
                    Email 
                    <input 
                        type="email"
                        name="email"
                        value={signUpData.email}
                        onChange={handleChange}
                        placeholder="Email"
                        className="user-info-input"
                        id="email"
                    />
                </label>
                <label className="input-label" htmlFor="username"> 
                    Username 
                    <input 
                        type="text"
                        name="username"
                        value={signUpData.username}
                        onChange={handleChange}
                        placeholder="Username"
                        className="user-info-input"
                        id="username"
                    />
                </label>

                <label className="input-label" htmlFor="password"> 
                    Password 
                    <input 
                        type="password"
                        name="password"
                        value={signUpData.password}
                        onChange={handleChange}
                        placeholder="Password"
                        className="user-info-input"
                        id="password"
                    />
                </label>

                <button className="user-info-submit-button" type="submit">
                    Sign Up
                </button>

            </form>
        </div>
    );
}