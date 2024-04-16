import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏡",
)

st.write("# Welcome to Team Vamos' DSA3101 project! 🚡")
st.image('cablecar.jpeg')
st.markdown("""[NexGen Cable Car](https://images.app.goo.gl/HEbEEjTgk47cL8LNA)""")


st.markdown("""To mark the 50th anniversary of the Singapore Cable Car, Mount Faber Leisure Group have launched the new designs in February 2024. 
            The idea creation and first sketches started more than 2 years ago but the discussion of the new cable car with 
            the relevant companies was 5 years ago. The new design and features will create a whole new experience for both
            the users inside and outside of the cable car.""")

st.sidebar.success("Select what you would like to do above.")

st.markdown(
    """
    ### More about our project
    This website/app we created allows users to easily interact with data insights, competitor analysis, and pricing recommendations.
    We implemented interactive elements such as sliders dropdown menus. This will enable real-time adjustments and what-if analyses
    to support strategic decision-making.

    **👈 Select a tab** to try it!
    ### Want to learn more about Mount Faber Leisure Group (MFLG)?
    - Check out their [website](https://www.mountfaberleisure.com)
    """
)