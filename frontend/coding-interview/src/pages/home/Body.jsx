import { useState, useEffect } from "react";
import { getRequest, postRequest } from "../../utils/apiRequests";
import { ChallengeQuestions } from "../../components/ChallengeQuestions.jsx";
import { getNextResetTime } from "../../utils/resetTime.js";
import "./Body.css";

export function Body() {
  const [challenge, setChallenge] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [difficulty, setDifficulty] = useState("easy");
  const [quota, setQuota] = useState(null);

  useEffect(() => {
    fetchQuota();
  }, []);

  const generateChallenge = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await postRequest("generate-challenge", difficulty)
      console.log('generateChallenge response:', data)
      // Basic validation: require an id and title
      if (!data || !data.id || !data.title) {
        throw new Error('Invalid challenge returned from server')
      }
      // ensure options is an array
      if (typeof data.options === "string") data.options = JSON.parse(data.options)
      // ensure correct_answer_id is a number (some backends return it as string)
      if (data.correct_answer_id !== undefined) {
        data.correct_answer_id = Number(data.correct_answer_id)
      }
      setChallenge(data);
      fetchQuota();
    } catch (err) {
      setError(err.message || "Failed to generate challenge.");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchQuota = async () => {
    try {
      const data = await getRequest("quota");
      setQuota(data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
      <main>
        <div className="app-main">
          <h2>Coding Challenge Generator</h2>
          <div className="quota-display">
            <p>Challenges remaining today: {quota?.quota_remaining || 0}</p>
            {quota?.quota_remaining === 0 && (
              <p>Next reset: {getNextResetTime(quota)?.toLocaleString()}</p>
            )}
          </div>
          <div className="difficulty-selector">
            <label htmlFor="difficulty">Select Difficulty</label>
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
            onClick={generateChallenge}
            className="generate-button"
            disabled={isLoading || quota?.quota_remaining === 0}
          >
            {isLoading ? "Generating..." : "Generate Challenge"}
          </button>
          {error && (
            <div className="error-message">
              <p>{error}</p>
            </div>
          )}
          {challenge && <ChallengeQuestions challenge={challenge} />}
        </div>
      </main>
    </>
  );
}
