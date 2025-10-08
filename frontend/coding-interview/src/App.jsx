
import { Routes, Route } from "react-router"
import { SignoutPage } from "./components/Signout"
import { HomePage } from "./components/HomePage"
import './App.css'

function App() {
  return (
    <>
      <Routes>
        <Route index element={<HomePage />}/>
        <Route path="login" element={<SignoutPage />} />
      </Routes>
    </>
  )
}

export default App
