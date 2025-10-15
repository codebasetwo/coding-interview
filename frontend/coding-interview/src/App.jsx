import { Routes, Route } from "react-router"
import { LoginPage } from "./components/LoginPage"
import { HomePage } from "./components/HomePage"
import { SignupPage } from "./components/SignupPage"
import { HistoryPanel } from "./components/History"
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
