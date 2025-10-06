import { useState, useEffect } from 'react'
import { getNextResetTime } from '../utils/resetTime.js'
import { callApi } from '../utils/API.js';
import './Body.css'
import { ChallengeQuestion } from './ChallengeQuestionBody.jsx';

export function Body(){
    const [challenge, setChallenge] = useState(null)
    const [difficulty, setDifficulty] = useState('Easy');
    const [quota, setQuota] = useState(null);
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)
    const {makeRequest} = callApi()

    const fetchQuota = async () => {
        try {
            const data = await makeRequest("quota")
            setQuota(data)
        } catch (err) {
            console.log(err)
        }
    }

    useEffect(() => {
        fetchQuota()
    }, )

    

    const generateChallenge = async () => {
        setIsLoading(true)
        setError(null)

        try {
            const data = await makeRequest("generate-challenge", {
                method: "POST",
                body: JSON.stringify({difficulty})
                }
            )
            setChallenge(data)
            fetchQuota()
        } catch (err) {
            setError(err.message || "Failed to generate challenge.")
        } finally {
            setIsLoading(false)
        }
    }


    return (
        <main>
            <div className='challenge-container'>
                <h2>
                    Coding Challenge Generator
                </h2>
                <div className="quota-display">
                    <p>Challenges remaining today: {quota?.quota_remaining || 0}</p>
                    {quota?.quota_remaining === 0 && (
                        <p>Next reset: {getNextResetTime(quota)?.toLocaleString()}</p>
                    )}
                </div>
                <div className='difficulty-selector'>
                    <label  htmlfor="difficulty">Select Difficulty</label>
                    <select
                        id="difficulty"
                        value={difficulty}
                        onChange={(e) => setDifficulty(e.target.value)}
                        disabled={isLoading}
                    >
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                    </select>
                </div>
                
                <button 
                    className='generate-button'
                    onClick={generateChallenge}
                    disabled={isLoading || quota?.quota_remaining === 0}
                >
                   {isLoading ? "Generating..." : "Generate Challenge"}
                </button>

                {error && 
                <div className="error-message">
                    <p>{error}</p>
                </div>}

                {challenge && <ChallengeQuestion challenge={challenge}/>}
            </div>
            </main>
    )
}