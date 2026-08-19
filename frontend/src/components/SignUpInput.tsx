import { useState } from "react";
import { useNavigate } from "react-router";

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
                body: JSON.stringify({ username: signUpData.username, email: signUpData.email, password: signUpData.password}),
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
            <form onSubmit={handleSubmit}>
                <input 
                    type="text"
                    name="email"
                    value={signUpData.email}
                    onChange={handleChange}
                    placeholder="Email"

                />

                <input 
                    type="text"
                    name="username"
                    value={signUpData.username}
                    onChange={handleChange}
                    placeholder="Username"
                />

                <input 
                    type="password"
                    name="password"
                    value={signUpData.password}
                    onChange={handleChange}
                    placeholder="Password"
                />

                <button type="submit">
                    Sign Up
                </button>

            </form>
        </div>
    );
}