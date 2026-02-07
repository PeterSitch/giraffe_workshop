# app.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np




def read_gfile(file_path):
    with open(file_path,"r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if 'Curve depth: [mm]' in line:
                xs = [float(x) for x in lines[i+1].strip().split(";")]
            if 'Curve gains: [counts]' in line:
                ys = [float(x) for x in lines[i+1].strip().split(";")]
    return xs,ys





st.set_page_config(page_title='Giraffe Workshop', page_icon='🦒', layout='wide')#, initial_sidebar_state=None, menu_items=None)



st.title("Giraffe Workshop")


#out_files = ['5','8','9','12']
#out_files = 


meas_sets = { 'Civco pos 1': (5,6),
        'Civco pos 2': (8,7),
        'Civco pos 3': (9,10),
        'No Civco': (12,11),
}


with st.sidebar:
    #st.write('')

    mode = st.pills('Choose mode',['single','multi'])

    #if mode =='single':
    selected_set = st.selectbox('Choose measurement:',options = meas_sets, index=None,)

    #if mode == 'multi':
    #    sb1,sb2 = st.columns(2)
    #    out_meas_num = sb1.selectbox('Choose measurement:',options = out_files, index=None,)
    #    in_meas_num = sb2.selectbox('Choose measurement:',options = in_files, index=None,)

if selected_set is not None:

    if mode == 'single':
        meas_num = meas_sets[selected_set][0]
        xs,ys = read_gfile(f'measurements/120624_{meas_num}.csv')

    


        if st.toggle('Normalise'):
            ys = ys/np.max(ys)
            extrap_poss = True
            signal_type = "Proportion of max"
        else:
            extrap_poss = False
            signal_type = "Counts"


        extrap =  st.toggle('Extrapolate', disabled = not extrap_poss)

        if extrap:

            id_max = np.argmax(ys)


            x1, x2 = xs[:id_max], xs[id_max:]
            y1, y2 = ys[:id_max], ys[id_max:]


            #wanted_ys = [0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
            wanted_ys = np.round(np.arange(0.99, 0.01, -0.01), 2)

            x_interp = np.interp(wanted_ys, y2[::-1], x2[::-1])


            #vol_ans = np.interp(vol_stats,xs,ys)

            #xs = np.concatenate([xs,x_interp])
            #ys = np.concatenate([ys,wanted_ys])
            
            #sort_idx = np.argsort(ys)

            #xs = xs[sort_idx]
            #ys = ys[sort_idx]


            



        #fig = px.scatter(x=xs, y=ys)



        fig = go.Figure()
        fig.add_trace(go.Scatter( x=xs, y=ys, mode="markers", name="Measurements", marker=dict(size=5, color="blue") ))

        if extrap:

            fig.add_trace(go.Scatter( x=x_interp, y=wanted_ys, mode="markers", name="Interpolations", marker=dict(size=1, color="red") ))

        fig.update_layout( title=f"Measurement {selected_set} plot", xaxis_title="WET (mm)", yaxis_title=f"Signal ({signal_type})", showlegend=True, template="plotly_white" )




        st.plotly_chart(fig)





    if mode == 'multi':
        meas_num = meas_sets[selected_set][0]
        out_xs,out_ys = read_gfile(f'measurements/120624_{meas_num}.csv')

        meas_num = meas_sets[selected_set][1]
        in_xs,in_ys = read_gfile(f'measurements/120624_{meas_num}.csv')


        combine = st.toggle('Combine measurements')

        if combine:
            in_xs = np.array(in_xs) + 1.16 # or should it be 1?

            xs = np.concatenate([out_xs, in_xs])
            ys = np.concatenate([out_ys, in_ys])
            
            sort_idx = np.argsort(xs)

            xs = xs[sort_idx]
            ys = ys[sort_idx]


        else:


            in_shift = st.number_input('Amount to shift in set by (mm)',value=0.0)

            range = st.select_slider('select data to plot',out_xs, value=(out_xs[0],out_xs[-1]))

            
            out_xs_arr = np.array(out_xs, dtype=float)
            out_ys_arr = np.array(out_ys, dtype=float)

            
            in_xs_arr = np.array(in_xs, dtype=float)
            in_ys_arr = np.array(in_ys, dtype=float)



            in_xs_arr = in_xs_arr + in_shift

            signal_type = "Counts"


            out_mask = (out_xs_arr >= range[0]) & (out_xs_arr <= range[1])
            in_mask = (in_xs_arr >= range[0]) & (in_xs_arr <= range[1])

            fig = go.Figure()
            fig.add_trace(go.Scatter( x=out_xs_arr[out_mask], y=out_ys_arr[out_mask], mode="markers", name="Measurements", marker=dict(size=5, color="blue"), uid='trace_out'))
            fig.add_trace(go.Scatter( x=in_xs_arr[in_mask], y=in_ys_arr[in_mask], mode="markers", name="Measurements", marker=dict(size=5, color="green"), uid='trace_in') )

        

            fig.update_layout( title=f"Measurement {selected_set} plot", xaxis_title="WET (mm)", yaxis_title=f"Signal ({signal_type})", showlegend=True, template="plotly_white",
                       )

            st.plotly_chart(fig, key='plot')
            st.stop()
            

        
        if st.toggle('Normalise'):
            ys = ys/np.max(ys)
            extrap_poss = True
            signal_type = "Proportion of max"
        else:
            extrap_poss = False
            signal_type = "Counts"

        extrap =  st.toggle('Extrapolate', disabled = not extrap_poss)

        if extrap:

            id_max = np.argmax(ys)


            x1, x2 = xs[:id_max], xs[id_max:]
            y1, y2 = ys[:id_max], ys[id_max:]


            #wanted_ys = [0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
            wanted_ys = np.round(np.arange(0.99, 0.01, -0.01), 2)

            x_interp = np.interp(wanted_ys, y2[::-1], x2[::-1])



        fig = go.Figure()
        fig.add_trace(go.Scatter( x=xs, y=ys, mode="markers", name="Measurements", marker=dict(size=5, color="blue") ))

        if extrap:

            fig.add_trace(go.Scatter( x=x_interp, y=wanted_ys, mode="markers", name="Interpolations", marker=dict(size=1, color="red") ))

        fig.update_layout( title=f"Measurement {selected_set} plot", xaxis_title="WET (mm)", yaxis_title=f"Signal ({signal_type})", showlegend=True, template="plotly_white" )




        st.plotly_chart(fig)