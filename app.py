from flask import Flask, request, render_template, Response, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "fg7sf98udsfgds9fys8dgfsdfdf67s89fy98ug98"  # Required for flashing messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-m3u', methods=['POST'])
def download_m3u():
    url = request.form.get('url')
    headers = {
        'User-Agent': 'OTT Navigator/1.7.1.4 (Linux;Android 7.1.2; en; cvhrc6)'
    }

    try:
        # Fetch the M3U playlist
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Extract content starting from #EXTM3U
        content = response.text
        start_index = content.find("#EXTM3U")
        if start_index == -1:
            flash("Error: The response does not contain a valid M3U playlist.", "error")
            return redirect(url_for('index'))
        
        # Cleaned content starts from #EXTM3U
        cleaned_content = content[start_index:]

        # Ensure there is data to return
        if not cleaned_content.strip():
            flash("Error: The M3U playlist content is empty.", "error")
            return redirect(url_for('index'))

        # Create a response to send as a downloadable file
        return Response(
            cleaned_content,
            mimetype='audio/x-mpegurl',
            headers={"Content-Disposition": "attachment; filename=playlist.m3u"}
        )
    except requests.exceptions.RequestException as e:
        flash(f"Error fetching the playlist: {e}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
