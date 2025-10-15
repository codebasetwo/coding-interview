import { Routes, Route } from "react-router"
import { LoginPage } from "./pages/login/LoginPage"
import { HomePage } from "./pages/home/HomePage"
import { SignupPage } from "./pages/signup/SignupPage"
import { HistoryPanel } from "./pages/history/History"
import './App.css'

function App() {
  return (
    <>
      <Routes>
        <Route index element={<HomePage />}/>
        <Route path="login" element={<LoginPage />} />
        <Route path='signup' element={<SignupPage />}/>
        <Route path='history' element={<HistoryPanel/>}/>
      </Routes>
    </>
  )
}

export default App
