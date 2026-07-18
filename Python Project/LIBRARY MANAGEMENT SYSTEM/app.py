import streamlit as st
from main import Library
from datetime import datetime

# Initialize Library class to load database
lib = Library()

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# Header styling
st.title("📚 Library Management System")
st.markdown("---")

menu = st.sidebar.selectbox(
    "Menu Navigation",
    [
        "Home / Dashboard",
        "Add Book",
        "List Books",
        "Search Book",
        "Add Member",
        "List Members",
        "Borrow Book",
        "Return Book"
    ]
)

# ---------------- HOME / DASHBOARD ----------------
if menu == "Home / Dashboard":
    st.header("Dashboard Metrics")
    
    total_books = len(Library.data.get("books", []))
    total_members = len(Library.data.get("members", []))

    available = 0
    for b in Library.data.get("books", []):
        try:
            available += int(b.get("available_copies", 0))
        except (ValueError, TypeError):
            pass

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Unique Books", total_books)
    with c2:
        st.metric("Total Registered Members", total_members)
    with c3:
        st.metric("Total Available Copies", available)

    st.markdown("### Quick Tips")
    st.info("Use the sidebar selection menu to add books, manage members, and process borrows/returns.")

# ---------------- ADD BOOK ----------------
elif menu == "Add Book":
    st.header("Add a New Book to Library")

    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("Book Title").strip()
        author = st.text_input("Author Name").strip()
        copies = st.number_input("Number of Copies", min_value=1, step=1, value=1)
        
        submitted = st.form_submit_button("Add Book")
        if submitted:
            if not title or not author:
                st.error("Please fill in both Book Title and Author Name.")
            else:
                book = {
                    "id": Library.gen_id("B"),
                    "title": title,
                    "author": author,
                    "total_copies": int(copies),
                    "available_copies": int(copies),
                    "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                Library.data["books"].append(book)
                Library.save_data()
                st.success(f"Book '{title}' added successfully! (ID: {book['id']})")

# ---------------- LIST BOOKS ----------------
elif menu == "List Books":
    st.header("All Books in Library")

    books = Library.data.get("books", [])
    if not books:
        st.warning("No books in library database yet.")
    else:
        st.dataframe(books, use_container_width=True)

# ---------------- SEARCH BOOK ----------------
elif menu == "Search Book":
    st.header("Search Books")

    query = st.text_input("Enter Title, Author, or Book ID").strip()

    if query:
        result = []
        for b in Library.data.get("books", []):
            if (
                query.lower() in b.get("id", "").lower() or
                query.lower() in b.get("title", "").lower() or
                query.lower() in b.get("author", "").lower()
            ):
                result.append(b)
        
        if result:
            st.success(f"Found {len(result)} matching book(s):")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("No books found matching your search query.")
    else:
        st.info("Start typing a book name, author, or ID above to search.")

# ---------------- ADD MEMBER ----------------
elif menu == "Add Member":
    st.header("Register a New Member")

    with st.form("add_member_form", clear_on_submit=True):
        name = st.text_input("Member Name").strip()
        email = st.text_input("Email ID").strip()
        
        submitted = st.form_submit_button("Add Member")
        if submitted:
            if not name or not email:
                st.error("Please provide both Name and Email ID.")
            else:
                member = {
                    "id": Library.gen_id("M"),
                    "name": name,
                    "email": email,
                    "borrowed_books": []
                }
                Library.data["members"].append(member)
                Library.save_data()
                st.success(f"Member '{name}' registered successfully! (ID: {member['id']})")

# ---------------- LIST MEMBERS ----------------
elif menu == "List Members":
    st.header("Registered Members")

    members = Library.data.get("members", [])
    if not members:
        st.warning("No members registered yet.")
    else:
        st.dataframe(members, use_container_width=True)

# ---------------- BORROW BOOK ----------------
elif menu == "Borrow Book":
    st.header("Process Book Borrowing")

    members_list = Library.data.get("members", [])
    books_list = [b for b in Library.data.get("books", []) if int(b.get("available_copies", 0)) > 0]

    if not members_list:
        st.warning("No members registered in the database. Add a member first.")
    elif not books_list:
        st.warning("No books are currently available for borrowing.")
    else:
        member_options = {f"{m.get('name', 'N/A')} ({m.get('id', 'N/A')})": m for m in members_list}
        book_options = {f"{b.get('title', 'N/A')} ({b.get('id', 'N/A')})": b for b in books_list}

        with st.form("borrow_form"):
            selected_member_str = st.selectbox("Select Member", list(member_options.keys()))
            selected_book_str = st.selectbox("Select Book", list(book_options.keys()))
            
            submitted = st.form_submit_button("Borrow Book")
            if submitted:
                m = member_options[selected_member_str]
                b = book_options[selected_book_str]
                
                # Initialize borrowed_books list if missing
                if "borrowed_books" not in m:
                    m["borrowed_books"] = []

                borrow_entry = {
                    "book_id": b["id"],
                    "title": b["title"],
                    "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                m["borrowed_books"].append(borrow_entry)
                b["available_copies"] -= 1

                Library.save_data()
                st.success(f"Successfully checked out '{b['title']}' to {m['name']}!")
                st.rerun()

# ---------------- RETURN BOOK ----------------
elif menu == "Return Book":
    st.header("Process Book Return")

    members_list = Library.data.get("members", [])
    if not members_list:
        st.warning("No members registered in the database.")
    else:
        member_options = {f"{m.get('name', 'N/A')} ({m.get('id', 'N/A')})": m for m in members_list}
        selected_member_str = st.selectbox("Select Member", list(member_options.keys()))
        m = member_options[selected_member_str]
        
        borrowed = m.get("borrowed_books", [])
        if not borrowed:
            st.info(f"No borrowed books currently listed for {m.get('name')}.")
        else:
            borrowed_options = {f"{x.get('title')} (ID: {x.get('book_id')})": x for x in borrowed}
            selected_borrow_str = st.selectbox("Select Book to Return", list(borrowed_options.keys()))
            
            if st.button("Confirm Return"):
                borrow_entry = borrowed_options[selected_borrow_str]
                
                # Remove from borrowed list
                m["borrowed_books"].remove(borrow_entry)
                
                # Restore available copies count
                for b in Library.data.get("books", []):
                    if b.get("id") == borrow_entry.get("book_id"):
                        try:
                            b["available_copies"] = int(b.get("available_copies", 0)) + 1
                        except (ValueError, TypeError):
                            b["available_copies"] = 1
                            
                Library.save_data()
                st.success(f"Book '{borrow_entry.get('title')}' returned successfully!")
                st.rerun()
