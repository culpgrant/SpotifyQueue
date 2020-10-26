import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

@app.route('/', methods = ["GET","POST"])
@app.route('/home')
def home_page():
    spotify_form = SpotifyForm()
    if spotify_form.validate_on_submit():
        message = add_to_queue(spotify_form.song_field.data)
        if message == "Please check the link to the song":
            flash(message,"danger")
            return redirect(url_for('home_page'))
        else:
            flash(message,"success")
            return redirect(url_for('home_page'))
    return render_template('layout.html', spotify_form = spotify_form)


#Creating the Simple Form to Display on the webpage
class SpotifyForm(FlaskForm):
    song_field = StringField('Spotify URL', validators=[DataRequired()])
    submit_song = SubmitField("Submit Song")


#Spotify Information
spotify_client_id = ""
spotify_client_secret = ""
spotify_redirect_uri = "http://localhost"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri=spotify_redirect_uri,
                                               scope="user-modify-playback-state"))
#Device ID's - I will use my Mac Computer device because it can easily alwasy be on vs. a phone.
device_id_iphone = ""
device_id_mac = ""

# Function which is passed in a song url and adds it to the url
def add_to_queue(url):
    try:
        track = sp.track(url)
        #Getting the song title name
        name_sub_song = track['name']
        #Getting the artists name
        for line in track['artists']:
            artist_sub_song = line['name']
        #Getting the album name
        album_name_sub_song = track['album']['name']
        sp.add_to_queue(url, device_id_mac)
        finish_sentence = f"Thank you for submitting '{name_sub_song}' by '{artist_sub_song}' from the '{album_name_sub_song}' Album! It has been added to the queue."
    except:
        finish_sentence = "Please check the link to the song"
    return finish_sentence


if __name__ == '__main__':
    app.run(debug=True)
