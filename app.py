from flask import Flask, render_template, request, url_for, flash, redirect ,abort
import datetime
import sqlite3
import os


app = Flask(__name__)



app.config['SECRET_KEY'] = '3f83a7d3d2818bd6dd156b56408c53a6b9aa97c386255f50'
messages=[]
blog1=[    {"title": "This is the first blog.", "body": 'Blog 1'},
    {"title": "This is the second blog.", "body": 'Blog 2'},
    {"title": "This is the third blog.", "body": 'Blog 3'}
]

@app.route('/')
@app.route('/blogs/')
def blogs():
    try:
        current_directory = os.getcwd()
        database_path = os.path.join(current_directory, 'database.db')
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content FROM posts")
        posts = cursor.fetchall()

    except sqlite3.Error as e:
        flash(f'Database error: {e}', 'error')
    finally:
        if conn:
            conn.close()

    print(posts)
    return render_template('blogs.html', posts=posts)

@app.route('/index')
def index():
    heading =["Understanding AI:","Applications in Everyday Life:","The Impact on Industries:","Ethical Considerations:"]
    content = [ "At its core, AI refers to the development of computer systems that can perform tasks that typically require human intelligence. These tasks include learning, reasoning, problem-solving, perception, and language understanding. It's like giving machines the ability to think and make decisions, much like we do","AI has already woven itself into the fabric of our daily routines. From virtual assistants like Siri and Alexa to personalized recommendations on streaming platforms, AI enhances user experiences. It powers autonomous vehicles, predicts weather patterns, and even aids in medical diagnoses. The possibilities seem limitless.","Industries across the board are embracing AI to enhance efficiency and productivity. In healthcare, AI assists in analyzing medical images and predicting disease outcomes. Businesses use AI for data analysis, improving decision-making processes. AI-driven algorithms are transforming the way we shop, from personalized product recommendations to efficient supply chain management.","As we marvel at the capabilities of AI, it's crucial to address ethical concerns. Questions about privacy, bias in algorithms, and the potential for job displacement arise. Striking a balance between technological advancement and ethical responsibility is a challenge that society must grapple with as AI continues to advance."]
    return render_template('index.html',time=datetime.datetime.utcnow(),hed1=heading[0],hed2=heading[1],hed3=heading[2],con1=content[0],con2=content[1],con3=content[2])
@app.route('/about/')
def about():
    return render_template('about.html')
@app.route('/hello/')
def hello():
    return render_template('hello.html')
@app.route('/comments/')
def comments():
   comments = ['This is the first comment.',
               'This is the second comment.',
               'This is the third comment.',
               'This is the fourth comment.'
               ]
   return render_template('comments.html', comments=comments)
@app.route('/comments1/')
def comments1():
   comments = ['This is the first comment.',
               'This is the second comment.',
               'This is the third comment.',
               'This is the fourth comment.'
               ]
   return render_template('comments1.html',comments=comments)
@app.route('/comments2/')
def comment():
   comments = ['This is the first comment.',
               'This is the second comment.',
               'This is the third comment.',
               'This is the fourth comment.'
               ]
   return render_template('comments2.html',comments=comments)


@app.route('/blog/<int:blog_id>/')
def blog(blog_id):
    post = get_post(blog_id)
    return render_template('blog.html', blog=post)


'''dwf  create():
    posts = []  # Initialize posts with a default value

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = None  # Initialize conn outside the try block

            try:
                
                current_directory = os.getcwd()

# Construct the database file path using os.path.join
                database_path=os.path.join(current_directory, 'database.db')
                conn = sqlite3.connect(database_path)
# Connect to the database
                

                cursor = conn.cursor()

                # Insert new post
                cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))

                # Fetch all posts after insertion
                cursor.execute("SELECT * FROM posts")
                posts = cursor.fetchall()

                conn.commit()
                return render_template("index.html", posts=posts)
            except sqlite3.Error as e:
                flash(f'Database error: {e}')
            finally:
                if conn:
                    conn.close()
    return render_template("create.html")
if __name__ == '__main__':
    app.run(debug=True)
'''



@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
           
        if not title:
            flash('Title is required!', 'error')
        elif not content:
            flash('Content is required!', 'error')
        else:
            conn = None
            try:
                current_directory = os.getcwd()
                database_path = os.path.join(current_directory, 'database.db')
                conn = sqlite3.connect(database_path)
                cursor = conn.cursor()

                cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))

                conn.commit()

                return redirect(url_for('blogs'))
            except sqlite3.Error as e:
                flash(f'Database error: {e}', 'error')
            finally:
                if conn:
                    conn.close()

    return render_template("create.html")

if __name__ == '__main__':
    app.run(debug=True)


def get_post(post_id):
    current_directory = os.getcwd()
    database_path = os.path.join(current_directory, 'database.db')
    conn = sqlite3.connect(database_path)
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    
    if post is None:
        return None
    
    return post



@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        
        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            current_directory = os.getcwd()
            database_path = os.path.join(current_directory, 'database.db')
            conn = sqlite3.connect(database_path)

            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('blogs'))

    return render_template('edit.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)



from flask import abort

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    
    if post is None:
        flash('Post not found!', 'error')
        return redirect(url_for('blogs'))

    current_directory = os.getcwd()
    database_path = os.path.join(current_directory, 'database.db')
    conn = sqlite3.connect(database_path)

    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('"{}" was successfully deleted!'.format(post[2]))
    return redirect(url_for('blogs'))


