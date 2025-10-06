// import { useState } from 'react'
import {Routes, Route} from "react-router"
import { HomePage } from "./components/HomePage"
import { HistoryPanel } from "./components/History"
import './App.css'
import { LoginPage } from "./components/LoginPage"

function App() {
  // const [count, setCount] = useState(0)

  return (
    <Routes>
      <Route index element={<HomePage/>}/>
      <Route path='/login' element={<LoginPage/>}/>
      <Route path="history" element={<HistoryPanel />}/>
    </Routes>
  
  )
}

export default App
