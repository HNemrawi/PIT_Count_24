import streamlit as st


HTML_HEADER_LOGO = """
            <div style="font-style: italic; color: #808080; text-align: left;">
            <a href="https://icalliances.org/" target="_blank"><img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/eb7da336-e61c-4e0b-bbb5-1a7b9d45bff6/Dash+Logo+2.png?format=750w" width="250"></a>
            </div>
            """
HTML_HEADER_TITLE = f'<h2 style="color:#00629b; text-align:center;">Point in Time Count</h2>'

HTML_FOOTER = """
                <div style="font-style: italic; color: #808080; text-align: center;">
                    <a href="https://icalliances.org/" target="_blank">
                        <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/eb7da336-e61c-4e0b-bbb5-1a7b9d45bff6/Dash+Logo+2.png?format=750w" width="99">
                    </a>
                    DASH™ is a trademark of Institute for Community Alliances.
                </div>
                <div style="font-style: italic; color: #808080; text-align: center;">
                    <a href="https://icalliances.org/" target="_blank">
                        <img src="https://images.squarespace-cdn.com/content/v1/54ca7491e4b000c4d5583d9c/1475614371395-KFTYP42QLJN0VD5V9VB1/ICA+Official+Logo+PNG+%28transparent%29.png?format=1500w" width="99">
                    </a>
                    © 2024 Institute for Community Alliances (ICA). All rights reserved.
                </div>
                    """

def setup_header():
    """Set up the header of the Streamlit page."""
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(HTML_HEADER_LOGO, unsafe_allow_html=True)
    with col2:
        st.markdown(HTML_HEADER_TITLE, unsafe_allow_html=True)

def setup_footer():
    """Set up the footer of the Streamlit page."""
    st.markdown(HTML_FOOTER, unsafe_allow_html=True)




