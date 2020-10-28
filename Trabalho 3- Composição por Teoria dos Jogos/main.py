import numpy as np
import nashpy as nash
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
import math
from music21 import *
from sklearn.preprocessing import MinMaxScaler
from random import randint

def plot_freq(x,y,z,xs):
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(x, y)
    axs[0, 0].set_title('xy')
    axs[0, 1].plot(x, z, 'tab:orange')
    axs[0, 1].set_title('xz')
    axs[1, 0].plot(y, z, 'tab:green')
    axs[1, 0].set_title('yz')
    axs[1, 1].plot(xs)
    axs[1, 1].set_title('Frequências')
    plt.subplots_adjust(wspace=0.5,hspace=0.5)

    plt.show()

def create_df(plot):
    
    m = 10
    a1 = 1
    a2 = 1
    a3 = 2
    b1 = 3
    b2 = 2
    b3 = 4
    xa = 0.3
    xb = 0.5
    xc = 1.0-xa-xb

    def dx(x,t,A):
        f=np.dot(A,x)
        phi=np.dot(f,x)
        return x*(f-phi)

    t=np.linspace(0,10,100)
    A=np.array([[0,-a2,b3],[b1,0,-a3],[-a1,b2,0]])
    xs=odeint(func=dx,y0=[xa,xb,xc],t=t,args=(A,))

    N=len(xs)
    x=np.zeros(N)
    y=np.zeros(N)
    z=np.zeros(N)

    for i in range(N):
        x[i],y[i],z[i]=xs[i]

    data={'Bass':x,'Flute':y,'Piano':z}
    df=pd.DataFrame(data,columns=['Bass','Flute','Piano'],index=None)
    
    if plot:
        plot_freq(x,y,z,xs)
        print(x,y,z,xs)


    return df

def freq2pitch(freqs,possible_notes):
    pitches = []
    for freq in freqs:
        idx = int(round(freq[0]*(len(possible_notes)-1))) + randint(0,2)*((-1)**randint(0,1))
        if idx >= len(possible_notes):
            idx = len(possible_notes)-1

        elif idx < 0:
            idx = 0
        
        print(idx)
        pitch = possible_notes[idx]
        pitches.append(pitch)

    return pitches
def get_possible_notes(scale, octave_start,num):
    notes = []
    start = (octave_start+1)*12 + scale
    intervals = [2,2,1,2,2,2,1]
    note = start
    i = 0
    while len(notes) < num:
        notes.append(note)
        note += intervals[i]
        i += 1 
        if i == 7:
            i = 0
    return notes



def create_melody(df,instruments):
    melody = stream.Stream()
    scale = 3 #0 - C, 1 - C#, 2- D, ...
    for i in range(len(instruments)):
        freqs = df.iloc[:,i]
        freqs = np.array(freqs).reshape(-1, 1)
        scaler = MinMaxScaler()
        scaler.fit(freqs)
        freqs = scaler.transform(freqs)
        freqs.reshape(len(freqs),)
        octave_start = i+1
        possible_notes = get_possible_notes(scale,octave_start,11)
        pitches = freq2pitch(freqs,possible_notes)
        instrument = instruments[i]
        #print(f'intrument={instrument}, possible_notes={possible_notes}, pitches={pitches}')
        part = stream.Part()
        part.insert(0,instrument)
        for i in range(len(pitches)):
            pitch = note.Note(pitches[i])
            pitch.quarterLength = 1
            part.append(pitch)

        melody.append(part)
    melody.write('midi', 'Trabalho 3.mid')

    
if __name__ == '__main__':
    df = create_df(False)
    
    instruments = [instrument.Bass(),instrument.Flute(),instrument.Piano()]
    create_melody(df,instruments)