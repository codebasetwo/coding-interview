
import { Routes, Route } from "react-router"
import { LoginPage } from "./components/LoginPage"
import { HomePage } from "./components/HomePage"
import { SignupPage } from "./components/SignupPage"
import './App.css'

function App() {
  return (
    <>
      <Routes>
        <Route index element={<HomePage />}/>
        <Route path="login" element={<LoginPage />} />
        <Route path='signup' element={<SignupPage />}/>
      </Routes>
    </>
  )
}

export default App
