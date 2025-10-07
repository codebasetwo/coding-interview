import './Body.css'
export function Body(){
    return (
        <>
            <main>
                <div className="app-main">
                    <h2>Coding Challenge Generator</h2>
                    <div className="quota-display">
                        <p>Challenges remaining today: 0</p>
                    </div>
                    <div className='difficulty-selector'>
                        <label  htmlfor="difficulty">Select Difficulty</label>
                        <select
                            id="difficulty"
                        >
                            <option value="easy">Easy</option>
                            <option value="medium">Medium</option>
                            <option value="hard">Hard</option>
                        </select>
                    </div>
                    <button
                    className='generate-button'
                    >
                        Generate Challenge
                    </button>
                </div>
              
            </main>
        
        </>
    )
}