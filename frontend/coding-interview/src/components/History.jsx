import {useState, useEffect} from "react"
import {ChallengeQuestions} from "./ChallengeQuestions.jsx"
import { getRequest } from "../utils/apiRequests.js"

export function HistoryPanel() {
    const [history, setHistory] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        let mounted = true

        async function fetchData () {
            setIsLoading(true)
            setError(null)

            try {
                const historyData = await getRequest('my-history')
                console.log(historyData)
                if (mounted) {
                    setHistory(historyData.challenges)
                }
            } catch (err) {
                if (mounted) {
                    setError(err.message || "Failed to load history.")
                }
            } finally {
                if (mounted) {
                    setIsLoading(false)
                }
            }
        }

        fetchData();

        return () => { mounted = false }

    }, [])

    const fetchHistory = async () => {
        setIsLoading(true)
        setError(null)

        try {
            const historyData = await getRequest('my-history')
            console.log(historyData)
            setHistory(historyData.challenges)
        } catch (err) {
            setError(err.message || "Failed to load history.")
        } finally {
                setIsLoading(false)
        }
    }

    if (isLoading) {
        return <div className="loading">Loading history...</div>
    }

    if (error) {
        return <div className="error-message">
            <p>{error}</p>
            <button onClick={fetchHistory}>Retry</button>
        </div>
    }

    return <div className="history-panel">
        <h2>History</h2>
        {history.length === 0 ? <p>No challenge history</p> :
            <div className="history-list">
                {history.map((challenge) => {
                    return <ChallengeQuestions
                                challenge={challenge}
                                key={challenge.id}
                                showExplanation
                            />
                })}
            </div>
        }
    </div>
}