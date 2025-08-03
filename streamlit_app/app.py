import streamlit as st

from components import user_view, room_view, booking_view

page = st.sidebar.selectbox(
    'menu',
    ('user', 'rooms', 'bookings', 'user_info_update', 'room_info_update', 'booking_info_update')
)

if page == 'user':
    user_view.user_registration_render()

elif page == 'rooms':
    room_view.room_registration_render()

elif page == 'bookings':
    booking_view.booking_render()

elif page == 'user_info_update':
    user_view.user_info_update_render()

elif page == 'room_info_update':
    room_view.room_info_update_render()

elif page == 'booking_info_update':
    booking_view.booking_info_update_render()