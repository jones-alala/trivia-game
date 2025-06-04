import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL =
  "https://opentdb.com/api.php?amount=1&category=32&type=multiple";

function TriviaGame() {
  const [question, setQuestion] = useState(null);
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState("");
  const [answered, setAnswered] = useState(false);

  useEffect(() => {
    fetchQuestion();
  }, []);

  const fetchQuestion = async () => {
    const response = await axios.get(API_URL);
    const data = response.data.results[0];
    const answers = [...data.incorrect_answers, data.correct_answer].sort();

    setQuestion({
      question: data.question,
      correct_answer: data.correct_answer,
      answers,
    });

    setFeedback("");
    setAnswered(false);
  };

  const handleAnswer = (answer) => {
    const isCorrect = answer === question.correct_answer;
    if (isCorrect) setScore(score + 1);
    setFeedback(
      isCorrect
        ? "✅ Correct!"
        : `❌ Wrong! Correct: ${question.correct_answer}`
    );
    setAnswered(true);
  };

  const handleFeedback = (type) => {
    alert(`You ${type}d the question!`);
  };

  if (!question) return <p>Loading...</p>;

  return (
    <div>
      <h2 dangerouslySetInnerHTML={{ __html: question.question }} />
      {question.answers.map((ans, i) => (
        <button
          key={i}
          onClick={() => handleAnswer(ans)}
          disabled={answered}
          dangerouslySetInnerHTML={{ __html: ans }}
        />
      ))}

      {feedback && (
        <>
          <p>{feedback}</p>
          <button onClick={() => handleFeedback("like")}>👍 Like</button>
          <button onClick={() => handleFeedback("dislike")}>👎 Dislike</button>
          <br />
          <button onClick={fetchQuestion}>Next Question</button>
        </>
      )}

      <p>
        <strong>Score:</strong> {score}
      </p>
    </div>
  );
}

export default TriviaGame;
