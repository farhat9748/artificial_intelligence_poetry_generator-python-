
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    save_poem as save_poem_to_db,
    get_all_poems,
    get_connection
)


# ---------------------------------
# FLASK CONFIGURATION
# ---------------------------------

app = Flask(
    __name__,
    template_folder="template"
)

app.secret_key = "ai-poetry-secret-key-2026"


# ---------------------------------
# POETRY GENERATOR
# ---------------------------------

def generate_poem_text(topic, mood):

    poems = {

        "romantic": f"""
In the quiet whispers of the night,
Your smile becomes a gentle light.
The stars above begin to shine,
As dreams of you become mine.

{topic} blooms within my heart,
A beautiful tale, a work of art.
Through every season, come what may,
Your love brings sunshine every day.
""",

        "sad": f"""
Beneath the clouds of fading grey,
Memories softly drift away.
The silence speaks of yesterday,
And broken dreams refuse to stay.

{topic} echoes through the rain,
A gentle reminder of the pain.
Yet somewhere deep, a hope remains,
Like sunlight dancing after rains.
""",

        "nature": f"""
The morning breeze begins to sing,
And flowers wake to greet the spring.
The rivers dance beneath the sun,
A peaceful day has just begun.

{topic} paints the world in green,
The loveliest sight I have ever seen.
Through whispered leaves and skies so blue,
Nature reveals a world anew.
""",

        "motivational": f"""
Rise with courage, face the day,
Let every fear dissolve away.
Though roads may twist and mountains stand,
Believe in strength within your hand.

{topic} is a dream worth chasing,
Every step is progress you are making.
Keep your spirit strong and bright,
And turn your darkness into light.
"""
    }

    return poems.get(
        mood.lower(),
        f"""
A poem begins with a simple thought,
A dream discovered, a lesson taught.

{topic} inspires words to flow,
Like gentle rivers as they go.

With every line and every rhyme,
A little magic grows with time.
"""
    )


# ---------------------------------
# HOME PAGE
# ---------------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    poem = None
    topic = ""
    mood = "romantic"

    if request.method == "POST":

        topic = request.form.get(
            "topic",
            ""
        ).strip()

        mood = request.form.get(
            "mood",
            "romantic"
        )

        if not topic:

            flash("Please enter a topic.")

            return render_template(
                "index.html",
                poem=None,
                topic=topic,
                mood=mood
            )

        poem = generate_poem_text(
            topic,
            mood
        )

        success = save_poem_to_db(
            topic,
            mood,
            poem
        )

        if success:

            flash(
                "Poem generated and saved successfully!"
            )

        else:

            flash(
                "Poem generated, but database saving failed."
            )

    return render_template(
        "index.html",
        poem=poem,
        topic=topic,
        mood=mood
    )


# ---------------------------------
# POEMS PAGE
# ---------------------------------

@app.route("/poems")
def poems():

    all_poems = get_all_poems()

    return render_template(
        "poems.html",
        poems=all_poems
    )


@app.route("/saved-poems")
def saved_poems():
    return poems()


# ---------------------------------
# DASHBOARD
# ---------------------------------

@app.route("/dashboard")
def dashboard():

    total_poems = 0

    connection = get_connection()

    if connection:

        try:

            cursor = connection.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM poems"
            )

            total_poems = cursor.fetchone()[0]

            cursor.close()
            connection.close()

        except Exception as e:

            print("Dashboard error:", e)

    return render_template(
        "dashboard.html",
        total_poems=total_poems,
        saved_poems_count=total_poems
    )


# ---------------------------------
# GENERATE POEM PAGE
# ---------------------------------

@app.route("/generate-poem", methods=["GET", "POST"])
def generate_poem():

    if request.method == "POST":

        topic = request.form.get(
            "topic",
            ""
        ).strip()

        mood = request.form.get(
            "mood",
            "romantic"
        )

        style = request.form.get(
            "style",
            "Free Verse"
        )

        if not topic:

            flash("Please enter a topic.")

            return redirect(
                url_for("generate_poem")
            )

        poem = generate_poem_text(
            topic,
            mood
        )

        return render_template(
            "poem_result.html",
            topic=topic,
            mood=mood,
            style=style,
            poem=poem
        )

    return render_template(
        "poem.html"
    )


# ---------------------------------
# SAVE POEM
# ---------------------------------

@app.route("/save-poem", methods=["POST"])
def save_poem():

    topic = request.form.get(
        "topic",
        ""
    ).strip()

    mood = request.form.get(
        "mood",
        ""
    )

    poem = request.form.get(
        "poem",
        ""
    )

    if not topic or not poem:

        flash("Topic and poem are required.")

        return redirect(
            url_for("generate_poem")
        )

    success = save_poem_to_db(
        topic,
        mood,
        poem
    )

    if success:

        flash("Poem saved successfully!")

    else:

        flash("Error saving poem.")

    return redirect(
        url_for("poems")
    )


# ---------------------------------
# DELETE POEM
# ---------------------------------

@app.route(
    "/delete-poem/<int:poem_id>",
    methods=["GET", "POST"]
)
def delete_poem(poem_id):

    connection = get_connection()

    if connection:

        try:

            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM poems WHERE id = %s",
                (poem_id,)
            )

            connection.commit()

            cursor.close()
            connection.close()

            flash("Poem deleted successfully!")

        except Exception as e:

            print("Delete error:", e)

    else:

        flash("Database connection failed.")

    return redirect(
        url_for("poems")
    )


# ---------------------------------
# LOGIN
# ---------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not email or not password:

            flash(
                "Please enter your email and password."
            )

        else:

            flash("Login functionality is ready.")

            return redirect(
                url_for("index")
            )

    return render_template(
        "login.html"
    )


# ---------------------------------
# REGISTER
# ---------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not name or not email or not password:

            flash("Please fill in all fields.")

        elif password != confirm_password:

            flash("Passwords do not match.")

        else:

            flash(
                "Registration form submitted successfully."
            )

            return redirect(
                url_for("login")
            )

    return render_template(
        "register.html"
    )


# ---------------------------------
# RUN APPLICATION
# ---------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )