from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        current_question_id = 0

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not answer:
        return False, "Answer cannot be empty."

    # Initialize the answers list if not present
    if "answers" not in session:
        session["answers"] = []

    # Store the answer
    session["answers"].append({
        "question_id": current_question_id,
        "answer": answer
    })

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]
        return next_question, next_question_id
    else:
        return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    answers = session.get("answers", [])

    for answer in answers:
        question_id = answer["question_id"]
        user_answer = answer["answer"]

        if question_id < len(PYTHON_QUESTION_LIST):
            correct_answer = PYTHON_QUESTION_LIST[question_id]["correct_answer"]
            if user_answer == correct_answer:
                score += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    result_message = f"Your score is {score} out of {total_questions}."

    return result_message
