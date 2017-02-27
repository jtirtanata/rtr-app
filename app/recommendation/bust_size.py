import pickle
import re
under_bust_dict = pickle.load( open( "../../data/under_bust.pkl", "rb" ) )
upper_bust_dict = pickle.load( open( "../../data/upper_bust.pkl", "rb" ) )

def get_cup_letter(s):
    m = re.match('\d+(.*)', s)
    if m :
        return m.group(1)

def get_band_size(s):
    m= re.match('(\d+).*', s)
    if m :
        return int(m.group(1))

def get_upper_bust(cup, band_size):
    return upper_bust_dict[cup][band_size]


def get_under_bust(band_size):
    return under_bust_dict[band_size]
