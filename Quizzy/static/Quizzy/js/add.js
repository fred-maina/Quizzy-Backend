let questionCount = 1;

document.getElementById('addQuestion').addEventListener('click', () => {
    questionCount++;
    const questionItem = document.createElement('div');
    questionItem.classList.add('question-item');
    questionItem.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <label class="form-label">Question ${questionCount}</label>
            <button type="button" class="delete-btn delete-question" style="max-height: 36px; max-width: fit-content; background-color: brown;">delete question &times; </button>
        </div>
        <input type="text" class="form-control mb-2 question-text" placeholder="Enter question text" required>
        <div class="choices-container">
            <div class="input-group mb-2 choice-item">
                <input type="text" class="form-control" placeholder="Enter choice text" required>
                <div class="input-group-text">
                    <input type="radio" name="question-${questionCount - 1}-choice" aria-label="Correct choice" required>
                </div>
                <button type="button" class="delete-btn delete-choice" style="max-height: 36px; max-width: 10px; background-color: red;"> &times;</button>
            </div>
            <div class="input-group mb-2 choice-item">
                <input type="text" class="form-control" placeholder="Enter choice text" required>
                <div class="input-group-text">
                    <input type="radio" name="question-${questionCount - 1}-choice" aria-label="Correct choice" required>
                </div>
                <button type="button" class="delete-btn delete-choice" style="max-height: 36px; max-width: 10px; background-color: red;"> &times;</button>
            </div>
        </div>
        <button type="button" class="btn btn-secondary add-choice">Add another choice</button>
    `;
    document.getElementById('questionsContainer').appendChild(questionItem);
});

document.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('add-choice')) {
        const choicesContainer = e.target.previousElementSibling;
        const choiceCount = choicesContainer.querySelectorAll('.input-group').length;
        const questionIndex = Array.from(choicesContainer.parentNode.parentNode.children).indexOf(choicesContainer.parentNode);
        const newChoice = document.createElement('div');
        newChoice.classList.add('input-group', 'mb-2', 'choice-item');
        newChoice.innerHTML = `
            <input type="text" class="form-control" placeholder="Enter choice text" required>
            <div class="input-group-text">
                <input type="radio" name="question-${questionIndex}-choice" aria-label="Correct choice" required>
            </div>
            <button type="button" class="delete-btn delete-choice" style="max-height: 36px; max-width: 10px; background-color: red;"> &times;</button>
        `;
        choicesContainer.appendChild(newChoice);
    }

    if (e.target && e.target.classList.contains('delete-choice')) {
        e.target.closest('.choice-item').remove();
    }

    if (e.target && e.target.classList.contains('delete-question')) {
        e.target.closest('.question-item').remove();
    }
});


