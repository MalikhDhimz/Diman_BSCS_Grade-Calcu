from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  #For flashing error messages

@app.route('/', methods=['GET', 'POST'])
def index():
    # Route for home page and grade input form
    if request.method == 'POST':
        try:
             # Retrieve and validate Prelim grade input
            prelim_grade = float(request.form['prelim_grade'])
            if prelim_grade < 0 or prelim_grade > 100:
                flash("Please enter a valid grade between 0 and 100.")
                return redirect(url_for('index'))

            # Check if passing is possible
            max_midterm_and_final = 0.3 * 100 + 0.5 * 100  # Max possible from midterm and final
            current_score = 0.20 * prelim_grade

            if current_score + max_midterm_and_final < 75:
                flash("It's not possible to pass the subject with the current Prelim grade.")
                return redirect(url_for('index'))

            # If passing is possible, calculate the required grades
            required_midterm = (75 - current_score - 0.5 * 100) / 0.30
            required_final = (75 - current_score - 0.3 * 100) / 0.50

            return render_template('result.html', prelim=prelim_grade,
                                   required_midterm=max(0, required_midterm),
                                   required_final=max(0, required_final))

        except ValueError:
            flash("Please enter a valid numerical grade.")
            return redirect(url_for('index'))

    return render_template('index.html')

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)
