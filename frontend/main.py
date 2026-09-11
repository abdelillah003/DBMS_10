import json
import tkinter as tk
from tkinter import ttk, messagebox
from urllib import request, error


API_URL = "http://localhost:8003"
API_KEY = ""


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def api_get(path):
    req = request.Request(
        f"{API_URL}{path}",
        method="GET"
    )

    with request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def api_post(path, data):
    payload = json.dumps(data).encode("utf-8")

    req = request.Request(
        f"{API_URL}{path}",
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        }
    )

    with request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def get_error_message(exc):
    if isinstance(exc, error.HTTPError):
        try:
            body = exc.read().decode("utf-8")
            data = json.loads(body)
            return f"HTTP {exc.code}: {data.get('detail', body)}"
        except Exception:
            return f"HTTP {exc.code}: {exc.reason}"

    return str(exc)


def show_connection_view():
    clear_window()

    ttk.Label(
        root,
        text="Hotel Booking Manager",
        font=("Arial", 24, "bold")
    ).pack(pady=(35, 5))

    ttk.Label(
        root,
        text="Connect to the Hotel Booking API"
    ).pack(pady=(0, 20))

    connection_frame = ttk.Frame(
        root,
        padding=20
    )
    connection_frame.pack()

    ttk.Label(
        connection_frame,
        text="API URL:"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="W"
    )

    api_url_entry = ttk.Entry(
        connection_frame,
        width=40
    )
    api_url_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    api_url_entry.insert(
        0,
        API_URL
    )

    ttk.Label(
        connection_frame,
        text="X-API-Key:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10,
        sticky="W"
    )

    api_key_entry = ttk.Entry(
        connection_frame,
        width=40,
        show="*"
    )
    api_key_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    status_label = ttk.Label(
        connection_frame,
        text="Not connected"
    )
    status_label.grid(
        row=2,
        column=0,
        columnspan=2,
        pady=10
    )

    def test_connection():
        global API_URL, API_KEY

        API_URL = (
            api_url_entry
            .get()
            .strip()
            .rstrip("/")
        )

        API_KEY = (
            api_key_entry
            .get()
            .strip()
        )

        if not API_URL:
            messagebox.showerror(
                "Error",
                "Please enter the API URL."
            )
            return

        if not API_KEY:
            messagebox.showerror(
                "Error",
                "Please enter the X-API-Key."
            )
            return

        try:
            rooms = api_get("/rooms")

            status_label.config(
                text=(
                    "Connected successfully - "
                    f"{len(rooms)} rooms found"
                )
            )

            root.after(
                700,
                show_main_menu
            )

        except Exception as exc:
            status_label.config(
                text="Connection failed"
            )

            messagebox.showerror(
                "Connection Error",
                get_error_message(exc)
            )

    ttk.Button(
        connection_frame,
        text="Test Connection",
        command=test_connection,
        width=20
    ).grid(
        row=3,
        column=0,
        columnspan=2,
        pady=15
    )


def show_main_menu():
    clear_window()

    ttk.Label(
        root,
        text="Main Menu",
        font=("Arial", 22, "bold")
    ).pack(
        pady=(35, 25)
    )

    button_frame = ttk.Frame(root)
    button_frame.pack()

    ttk.Button(
        button_frame,
        text="Rooms",
        command=show_rooms_view,
        width=28
    ).pack(pady=8)

    ttk.Button(
        button_frame,
        text="Bookings",
        command=show_bookings_view,
        width=28
    ).pack(pady=8)

    ttk.Button(
        button_frame,
        text="Booking Statistics",
        command=show_statistics_view,
        width=28
    ).pack(pady=8)

    ttk.Button(
        button_frame,
        text="Add Service",
        command=show_add_service_view,
        width=28
    ).pack(pady=8)

    ttk.Button(
        button_frame,
        text="Disconnect",
        command=show_connection_view,
        width=28
    ).pack(pady=8)


def show_rooms_view():
    clear_window()

    ttk.Label(
        root,
        text="Rooms",
        font=("Arial", 22, "bold")
    ).pack(
        pady=(20, 10)
    )

    columns = (
        "room_id",
        "room_number",
        "floor",
        "category",
        "capacity",
        "price"
    )

    tree = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=14
    )

    tree.heading(
        "room_id",
        text="ID"
    )
    tree.heading(
        "room_number",
        text="Room"
    )
    tree.heading(
        "floor",
        text="Floor"
    )
    tree.heading(
        "category",
        text="Category"
    )
    tree.heading(
        "capacity",
        text="Capacity"
    )
    tree.heading(
        "price",
        text="Price/Night"
    )

    tree.column(
        "room_id",
        width=60,
        anchor="center"
    )
    tree.column(
        "room_number",
        width=90,
        anchor="center"
    )
    tree.column(
        "floor",
        width=70,
        anchor="center"
    )
    tree.column(
        "category",
        width=130,
        anchor="center"
    )
    tree.column(
        "capacity",
        width=90,
        anchor="center"
    )
    tree.column(
        "price",
        width=110,
        anchor="center"
    )

    tree.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    def load_rooms():
        for item in tree.get_children():
            tree.delete(item)

        try:
            rooms = api_get("/rooms")

            for room in rooms:
                tree.insert(
                    "",
                    "end",
                    values=(
                        room["room_id"],
                        room["room_number"],
                        room["floor"],
                        room["category"],
                        room["capacity"],
                        room["price_per_night"]
                    )
                )

        except Exception as exc:
            messagebox.showerror(
                "Error",
                get_error_message(exc)
            )

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    ttk.Button(
        button_frame,
        text="Refresh",
        command=load_rooms,
        width=18
    ).grid(
        row=0,
        column=0,
        padx=8
    )

    ttk.Button(
        button_frame,
        text="Back",
        command=show_main_menu,
        width=18
    ).grid(
        row=0,
        column=1,
        padx=8
    )

    load_rooms()


def show_bookings_view():
    clear_window()

    ttk.Label(
        root,
        text="Bookings",
        font=("Arial", 22, "bold")
    ).pack(
        pady=(20, 10)
    )

    columns = (
        "booking_id",
        "guest",
        "room",
        "check_in",
        "check_out",
        "status"
    )

    tree = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=13
    )

    tree.heading(
        "booking_id",
        text="ID"
    )
    tree.heading(
        "guest",
        text="Guest"
    )
    tree.heading(
        "room",
        text="Room"
    )
    tree.heading(
        "check_in",
        text="Check-In"
    )
    tree.heading(
        "check_out",
        text="Check-Out"
    )
    tree.heading(
        "status",
        text="Status"
    )

    tree.column(
        "booking_id",
        width=55,
        anchor="center"
    )
    tree.column(
        "guest",
        width=160,
        anchor="center"
    )
    tree.column(
        "room",
        width=80,
        anchor="center"
    )
    tree.column(
        "check_in",
        width=110,
        anchor="center"
    )
    tree.column(
        "check_out",
        width=110,
        anchor="center"
    )
    tree.column(
        "status",
        width=110,
        anchor="center"
    )

    tree.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    count_label = ttk.Label(
        root,
        text=""
    )
    count_label.pack()

    def load_bookings():
        for item in tree.get_children():
            tree.delete(item)

        try:
            bookings = api_get(
                "/bookings"
            )

            for booking in bookings:
                guest_name = (
                    f'{booking["first_name"]} '
                    f'{booking["last_name"]}'
                )

                tree.insert(
                    "",
                    "end",
                    values=(
                        booking["booking_id"],
                        guest_name,
                        booking["room_number"],
                        booking["check_in"],
                        booking["check_out"],
                        booking["status"]
                    )
                )

            count_label.config(
                text=(
                    "Total bookings: "
                    f"{len(bookings)}"
                )
            )

        except Exception as exc:
            messagebox.showerror(
                "Error",
                get_error_message(exc)
            )

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    ttk.Button(
        button_frame,
        text="Create Booking",
        command=show_create_booking_view,
        width=18
    ).grid(
        row=0,
        column=0,
        padx=6
    )

    ttk.Button(
        button_frame,
        text="Refresh",
        command=load_bookings,
        width=18
    ).grid(
        row=0,
        column=1,
        padx=6
    )

    ttk.Button(
        button_frame,
        text="Back",
        command=show_main_menu,
        width=18
    ).grid(
        row=0,
        column=2,
        padx=6
    )

    load_bookings()


def show_create_booking_view():
    clear_window()

    ttk.Label(
        root,
        text="Create Booking",
        font=("Arial", 22, "bold")
    ).pack(
        pady=(25, 15)
    )

    form_frame = ttk.Frame(
        root,
        padding=20
    )
    form_frame.pack()

    ttk.Label(
        form_frame,
        text="Guest ID:"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="W"
    )

    guest_entry = ttk.Entry(
        form_frame,
        width=30
    )
    guest_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    ttk.Label(
        form_frame,
        text="Room ID:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10,
        sticky="W"
    )

    room_entry = ttk.Entry(
        form_frame,
        width=30
    )
    room_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    ttk.Label(
        form_frame,
        text="Check-In (YYYY-MM-DD):"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=10,
        sticky="W"
    )

    check_in_entry = ttk.Entry(
        form_frame,
        width=30
    )
    check_in_entry.grid(
        row=2,
        column=1,
        padx=10,
        pady=10
    )

    ttk.Label(
        form_frame,
        text="Check-Out (YYYY-MM-DD):"
    ).grid(
        row=3,
        column=0,
        padx=10,
        pady=10,
        sticky="W"
    )

    check_out_entry = ttk.Entry(
        form_frame,
        width=30
    )
    check_out_entry.grid(
        row=3,
        column=1,
        padx=10,
        pady=10
    )

    def create_booking():
        try:
            guest_id = int(
                guest_entry
                .get()
                .strip()
            )

            room_id = int(
                room_entry
                .get()
                .strip()
            )

            check_in = (
                check_in_entry
                .get()
                .strip()
            )

            check_out = (
                check_out_entry
                .get()
                .strip()
            )

            if not check_in or not check_out:
                messagebox.showerror(
                    "Invalid Input",
                    "Please enter both dates."
                )
                return

            result = api_post(
                "/bookings",
                {
                    "guest_id": guest_id,
                    "room_id": room_id,
                    "check_in": check_in,
                    "check_out": check_out
                }
            )

            messagebox.showinfo(
                "Success",
                (
                    "Booking created successfully.\n"
                    f'Booking ID: {result["booking_id"]}'
                )
            )

            show_bookings_view()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Guest ID and Room ID must be numbers."
            )

        except Exception as exc:
            messagebox.showerror(
                "Booking Error",
                get_error_message(exc)
            )

    ttk.Button(
        form_frame,
        text="Create Booking",
        command=create_booking,
        width=20
    ).grid(
        row=4,
        column=0,
        columnspan=2,
        pady=20
    )

    ttk.Button(
        root,
        text="Back to Bookings",
        command=show_bookings_view,
        width=20
    ).pack(
        pady=10
    )


def show_statistics_view():
    clear_window()

    ttk.Label(
        root,
        text="Booking Statistics",
        font=("Arial", 22, "bold")
    ).pack(
        pady=(30, 20)
    )

    stats_frame = ttk.Frame(
        root,
        padding=20
    )
    stats_frame.pack()

    total_value = ttk.Label(
        stats_frame,
        text="-",
        font=("Arial", 12)
    )

    confirmed_value = ttk.Label(
        stats_frame,
        text="-",
        font=("Arial", 12)
    )

    checked_in_value = ttk.Label(
        stats_frame,
        text="-",
        font=("Arial", 12)
    )

    checked_out_value = ttk.Label(
        stats_frame,
        text="-",
        font=("Arial", 12)
    )

    cancelled_value = ttk.Label(
        stats_frame,
        text="-",
        font=("Arial", 12)
    )

    titles = [
        ("Total Bookings:", total_value),
        ("Confirmed:", confirmed_value),
        ("Checked-In:", checked_in_value),
        ("Checked-Out:", checked_out_value),
        ("Cancelled:", cancelled_value)
    ]

    for row, item in enumerate(titles):
        title = item[0]
        value_label = item[1]

        ttk.Label(
            stats_frame,
            text=title,
            font=("Arial", 12, "bold")
        ).grid(
            row=row,
            column=0,
            padx=15,
            pady=8,
            sticky="W"
        )

        value_label.grid(
            row=row,
            column=1,
            padx=15,
            pady=8
        )

    def load_statistics():
        try:
            data = api_get(
                "/statistics/bookings"
            )

            total_value.config(
                text=str(
                    data.get(
                        "total",
                        0
                    )
                )
            )

            confirmed_value.config(
                text=str(
                    data.get(
                        "confirmed",
                        0
                    )
                )
            )

            checked_in_value.config(
                text=str(
                    data.get(
                        "checked_in",
                        0
                    )
                )
            )

            checked_out_value.config(
                text=str(
                    data.get(
                        "checked_out",
                        0
                    )
                )
            )

            cancelled_value.config(
                text=str(
                    data.get(
                        "cancelled",
                        0
                    )
                )
            )

        except Exception as exc:
            messagebox.showerror(
                "Error",
                get_error_message(exc)
            )

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=15)

    ttk.Button(
        button_frame,
        text="Refresh",
        command=load_statistics,
        width=18
    ).grid(
        row=0,
        column=0,
        padx=8
    )

    ttk.Button(
        button_frame,
        text="Back",
        command=show_main_menu,
        width=18
    ).grid(
        row=0,
        column=1,
        padx=8
    )

    load_statistics()


def show_add_service_view():
    clear_window()

    ttk.Label(
        root,
        text="Add Service",
        font=("Arial", 22, "bold")
    ).pack(
        pady=(30, 20)
    )

    form_frame = ttk.Frame(
        root,
        padding=20
    )
    form_frame.pack()

    ttk.Label(
        form_frame,
        text="Service Name:"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="W"
    )

    name_entry = ttk.Entry(
        form_frame,
        width=35
    )
    name_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    ttk.Label(
        form_frame,
        text="Price:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10,
        sticky="W"
    )

    price_entry = ttk.Entry(
        form_frame,
        width=35
    )
    price_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    def create_service():
        name = (
            name_entry
            .get()
            .strip()
        )

        price_text = (
            price_entry
            .get()
            .strip()
        )

        if not name:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a service name."
            )
            return

        try:
            price = float(
                price_text
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Price must be a number."
            )
            return

        try:
            result = api_post(
                "/services",
                {
                    "name": name,
                    "price": price
                }
            )

            messagebox.showinfo(
                "Success",
                (
                    "Service created successfully.\n"
                    f'Service ID: {result["service_id"]}'
                )
            )

            name_entry.delete(
                0,
                tk.END
            )

            price_entry.delete(
                0,
                tk.END
            )

        except Exception as exc:
            messagebox.showerror(
                "Service Error",
                get_error_message(exc)
            )

    ttk.Button(
        form_frame,
        text="Create Service",
        command=create_service,
        width=20
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        pady=20
    )

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=show_main_menu,
        width=20
    ).pack(
        pady=10
    )


root = tk.Tk()

root.title(
    "Hotel Booking Manager"
)

root.geometry(
    "800x560"
)

root.resizable(
    False,
    False
)

show_connection_view()

root.mainloop()
