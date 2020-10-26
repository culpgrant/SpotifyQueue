import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '79f9626d80782cf145dd05db66bf2f83'

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
spotify_client_id = "21f3aaf01dc24ca09b45d6208b75c158"
spotify_client_secret = "722d50d399b54b4993a7cfe3245f71a1"
spotify_redirect_uri = "http://localhost"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_client_secret,
                                               redirect_uri=spotify_redirect_uri,
                                               scope="user-modify-playback-state"))
#Device ID's - I will use my Mac Computer device because it can easily alwasy be on vs. a phone.
device_id_iphone = "203e9cafe73d84fc8c5f14ea3ab601b0303ae1df"
device_id_mac = "6ecfe037163c6c49ca4b49f5c4c4dec17fdb9e97"

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