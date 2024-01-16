from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', youtube_url=None)

@app.route('/process-video', methods=['GET', 'POST'])
def process_video():
    if request.method == 'POST':
        # Process POST request
        youtube_url = request.form['url']
    else:
        # Only for testing with GET
        youtube_url = request.args.get('url', 'DefaultURL')

    # Your processing code
    return render_template('index.html', youtube_url=youtube_url)

if __name__ == '__main__':
    app.run(debug=True)