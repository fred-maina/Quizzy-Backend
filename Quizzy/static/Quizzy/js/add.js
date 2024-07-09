let questionCounter = 0;

const addChoice = (choicesContainer, questionId) => {
    const choiceItem = document.createElement('div');
    choiceItem.classList.add('input-group', 'mb-2', 'choice-item');
    const choiceId = `${Date.now()}`; // Unique ID for each choice
    choiceItem.innerHTML = `
        <input type="text" class="form-control" name="question-${questionId}-choice-${choiceId}-text" placeholder="Enter choice text" required>
        <div class="input-group-text">
            <input type="radio" name="question-${questionId}-correct-choice" value="${choiceId}" aria-label="Correct choice" required>
        </div>
        <button type="button" class="delete-btn delete-choice" style="max-height: 36px; max-width: 10px; background-color: red;">&times;</button>
    `;
    choicesContainer.appendChild(choiceItem);

    // Event listener for deleting choice
    choiceItem.querySelector('.delete-choice').addEventListener('click', () => {
        choiceItem.remove();
    });
};

const loadQuestion = () => {
    const questionId = `q${Date.now()}`; // Generate unique question ID using Date.now()
    const questionItem = document.createElement('div');
    questionItem.classList.add('question-item');
    questionItem.dataset.questionId = questionId; // Store question ID as data attribute
    questionItem.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <label class="form-label">Question</label>
            <button type="button" class="delete-btn delete-question" style="max-height: 36px; max-width: fit-content; background-color: brown;">delete question &times;</button>
        </div>
        <input type="text" class="form-control mb-2 question-text" name="question-${questionId}-text" placeholder="Enter question text" required>
        <div class="choices-container"></div>
        <button type="button" class="btn btn-secondary add-choice">Add another choice</button>
    `;
    const choicesContainer = questionItem.querySelector('.choices-container');

    // Add two choices by default
    for (let i = 0; i < 2; i++) {
        addChoice(choicesContainer, questionId);
    }

    // Event listener to add new choices
    questionItem.querySelector('.add-choice').addEventListener('click', () => {
        addChoice(choicesContainer, questionId);
    });

    // Event listener to delete question
    questionItem.querySelector('.delete-question').addEventListener('click', () => {
        questionItem.remove();
    });

    // Append question to the container
    document.getElementById('questionsContainer').appendChild(questionItem);
};

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('addQuestion').addEventListener('click', loadQuestion);

    // Initial setup: Load the first question on page load
    loadQuestion();
});
