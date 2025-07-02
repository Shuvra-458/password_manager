import streamlit as st
from vault_utils import *

st.set_page_config(page_title="Multi-User Password Manager", layout="wide")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🔐 Multi-User Password Manager")

# Registration
if st.session_state.user is None:
    option = st.radio("Login or Register?", ["Login", "Register"])

    if option == "Register":
        username = st.text_input("Username")
        password = st.text_input("Master Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        if st.button("Register"):
            if password != confirm:
                st.error("Passwords do not match.")
            elif register_user(username, password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists.")

    elif option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Master Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success("Login successful!")
                st.session_state.user = username
            else:
                st.error("Invalid username or password.")

# Main Menu
if st.session_state.user:
    st.sidebar.title(f"Welcome, {st.session_state.user} 👋")
    menu = st.sidebar.selectbox("Menu", ["View Vault", "Add New Password", "Generate Password", "Search", "Delete Password", "Security Audit", "Logout"])

    if menu == "View Vault":
        vault = load_vault(st.session_state.user)
        if not vault:
            st.info("Vault is empty.")
        else:
            st.subheader("🔒 Your Saved Passwords")
            for i, entry in enumerate(vault):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                with col1:
                    st.write(f"**Website:** {entry['website']}")
                with col2:
                    st.write(f"**Username:** {entry['username']}")

                with col3:
                    key = f"show_pass_{i}"
                    if key not in st.session_state:
                       st.session_state[key] = False

                    if st.session_state[key]:
                       st.write(f"**Password:** {entry['password']}")
                    else:
                       st.write(f"**Password:** {'•' * len(entry['password'])}")

               with col4:
                    if st.button("Show" if not st.session_state[key] else "Hide", key=f"toggle_{i}"):
                       st.session_state[key] = not st.session_state[key]

    
    elif menu == "Add New Password":
        website = st.text_input("Website/App")
        username = st.text_input("Username/Email")
        password = st.text_input("Password")
        if st.button("Save Password"):
            vault = load_vault(st.session_state.user)
            entry = {
                "website": website,
                "username": username,
                "password": password,
                "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            vault.append(entry)
            save_vault(st.session_state.user, vault)
            st.success("Password saved.")

    elif menu == "Generate Password":
        length = st.slider("Password Length", 8, 32, 12)
        new_password = generate_password(length)
        st.text_area("Generated Password", new_password)

    elif menu == "Search":
        query = st.text_input("Search website or username")
        vault = load_vault(st.session_state.user)
        results = [e for e in vault if query.lower() in e['website'].lower() or query.lower() in e['username'].lower()]
        st.write(results if results else "No results found.")

    elif menu == "Security Audit":
         vault = load_vault(st.session_state.user)
         weak = [e for e in vault if len(e['password']) < 8]

         if weak:
            st.warning(f"⚠️ Weak passwords found: {len(weak)}")
            for entry in weak:
                st.write(f"🔑 Website: {entry['website']}, Username: {entry['username']}, Password: {entry['password']}")
         else:
             st.success("✅ No weak passwords found!")
    elif menu == "Delete Password":
        vault = load_vault(st.session_state.user)
        if not vault:
            st.info("Your vault is empty. Nothing to delete.")
        else:
            websites = [f"{entry['website']} - {entry['username']}" for entry in vault]
            selected = st.selectbox("Select an entry to delete:", websites)
            if selected:
                index_to_delete = websites.index(selected)
                if st.button("Confirm Delete"):
                    deleted_entry = vault.pop(index_to_delete)
                    save_vault(st.session_state.user, vault)
                    st.success(f"Deleted entry for: {deleted_entry['website']} / {deleted_entry['username']}")


    elif menu == "Logout":
        st.session_state.user = None
        st.experimental_rerun()
