import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.error
import json


API_URL = "http://localhost:8003"


def api_get(endpoint):
    url = f"{API_URL}{endpoint}"

    with urllib.request.urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def api_post(endpoint, data):
    url = f"{API_URL}{endpoint}"
    request_data = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=request_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as exc:
        error_data = json.loads(exc.read().decode("utf-8"))
        raise Exception(error_data.get("detail", "Request failed"))


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def show_connection_view():
    clear_window()

    ttk.Label(
        root,
        text="Hotel Booking Manager",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    connection_frame = ttk.Frame(root, padding=20)
    connection_frame.pack(fill="x")

    ttk.Label(
        connection_frame,
        text="API URL:"
    ).grid(row=0, column=0, padx=10, pady=10)

    api_url_entry = ttk.Entry(connection_frame, width=40)
    api_url_entry.grid(row=0, column=1, padx=10, pady=10)
    api_url_entry.insert(0, API_URL)

    status_label = ttk.Label(
        connection_frame,
        text="Not connected"
    )
    status_label.grid(row=2, column=0, columnspan=2, pady=5)

    def test_connection():
        global API_URL

        API_URL = api_url_entry.get().strip().rstrip("/")

        try:
            rooms = api_get("/rooms")

            status_label.config(
                text=f"Connected successfully - {len(rooms)} rooms found"
            )

            root.after(800, show_main_menu)

        except Exception as exc:
            status_label.config(text="Connection failed")
            messagebox.showerror("Connection error", str(exc))

    ttk.Button(
        connection_frame,
        text="Test Connection",
        command=test_connection
    ).grid(row=1, column=0, columnspan=2, pady=15)


def show_rooms():
    clear_window()

    ttk.Label(
        root,
        text="Rooms",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    try:
        rooms = api_get("/rooms")

        table = ttk.Treeview(
            root,
            columns=("room", "floor", "category", "capacity", "price"),
            show="headings",
            height=12
        )

        table.heading("room", text="Room")
        table.heading("floor", text="Floor")
        table.heading("category", text="Category")
        table.heading("capacity", text="Capacity")
        table.heading("price", text="Price/Night")

        table.column("room", width=100, anchor="center")
        table.column("floor", width=80, anchor="center")
        table.column("category", width=140, anchor="center")
        table.column("capacity", width=100, anchor="center")
        table.column("price", width=120, anchor="center")

        for room in rooms:
            table.insert(
                "",
                "end",
                values=(
                    room["room_number"],
                    room["floor"],
                    room["category"],
                    room["capacity"],
                    room["price_per_night"]
                )
            )

        table.pack(padx=20, pady=10)

    except Exception as exc:
        messagebox.showerror("Error", str(exc))

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=show_main_menu
    ).pack(pady=20)


def show_bookings():
    clear_window()

    ttk.Label(
        root,
        text="Bookings",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    try:
        bookings = api_get("/bookings")

        table = ttk.Treeview(
            root,
            columns=(
                "booking_id",
                "guest",
                "room",
                "check_in",
                "check_out",
                "status"
            ),
            show="headings",
            height=10
        )

        table.heading("booking_id", text="ID")
        table.heading("guest", text="Guest")
        table.heading("room", text="Room")
        table.heading("check_in", text="Check-In")
        table.heading("check_out", text="Check-Out")
        table.heading("status", text="Status")

        table.column("booking_id", width=60, anchor="center")
        table.column("guest", width=160, anchor="center")
        table.column("room", width=80, anchor="center")
        table.column("check_in", width=110, anchor="center")
        table.column("check_out", width=110, anchor="center")
        table.column("status", width=110, anchor="center")

        for booking in bookings:
            guest_name = (
                f"{booking['first_name']} {booking['last_name']}"
            )

            table.insert(
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

        table.pack(padx=20, pady=10)

    except Exception as exc:
        messagebox.showerror("Error", str(exc))

    ttk.Button(
        root,
        text="Create Booking",
        command=show_create_booking
    ).pack(pady=5)

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=show_main_menu
    ).pack(pady=10)


def show_create_booking():
    clear_window()

    ttk.Label(
        root,
        text="Create Booking",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    form = ttk.Frame(root, padding=20)
    form.pack()

    ttk.Label(form, text="Guest ID:").grid(
        row=0, column=0, padx=10, pady=8, sticky="w"
    )
    guest_entry = ttk.Entry(form, width=25)
    guest_entry.grid(row=0, column=1, padx=10, pady=8)

    ttk.Label(form, text="Room ID:").grid(
        row=1, column=0, padx=10, pady=8, sticky="w"
    )
    room_entry = ttk.Entry(form, width=25)
    room_entry.grid(row=1, column=1, padx=10, pady=8)

    ttk.Label(form, text="Check-In (YYYY-MM-DD):").grid(
        row=2, column=0, padx=10, pady=8, sticky="w"
    )
    check_in_entry = ttk.Entry(form, width=25)
    check_in_entry.grid(row=2, column=1, padx=10, pady=8)

    ttk.Label(form, text="Check-Out (YYYY-MM-DD):").grid(
        row=3, column=0, padx=10, pady=8, sticky="w"
    )
    check_out_entry = ttk.Entry(form, width=25)
    check_out_entry.grid(row=3, column=1, padx=10, pady=8)

    def create_booking():
        try:
            guest_id = int(guest_entry.get().strip())
            room_id = int(room_entry.get().strip())
            check_in = check_in_entry.get().strip()
            check_out = check_out_entry.get().strip()

            if not check_in or not check_out:
                messagebox.showerror(
                    "Error",
                    "Please enter check-in and check-out dates."
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
                f"Booking created successfully.\n"
                f"Booking ID: {result['booking_id']}"
            )

            show_bookings()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Guest ID and Room ID must be numbers."
            )

        except Exception as exc:
            messagebox.showerror(
                "Error",
                str(exc)
            )

    ttk.Button(
        form,
        text="Create Booking",
        command=create_booking
    ).grid(
        row=4,
        column=0,
        columnspan=2,
        pady=20
    )

    ttk.Button(
        root,
        text="Back to Bookings",
        command=show_bookings
    ).pack(pady=10)


def show_statistics():
    clear_window()

    ttk.Label(
        root,
        text="Booking Statistics",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    try:
        statistics = api_get("/statistics/bookings")

        statistics_frame = ttk.Frame(root, padding=20)
        statistics_frame.pack(pady=20)

        rows = [
            ("Total Bookings", statistics["total_bookings"]),
            ("Confirmed", statistics["confirmed_bookings"]),
            ("Checked In", statistics["checked_in_bookings"]),
            ("Checked Out", statistics["checked_out_bookings"]),
            ("Cancelled", statistics["cancelled_bookings"])
        ]

        for row, (label, value) in enumerate(rows):
            ttk.Label(
                statistics_frame,
                text=label + ":",
                font=("Arial", 12, "bold")
            ).grid(
                row=row,
                column=0,
                padx=20,
                pady=10,
                sticky="w"
            )

            ttk.Label(
                statistics_frame,
                text=str(value),
                font=("Arial", 12)
            ).grid(
                row=row,
                column=1,
                padx=20,
                pady=10
            )

    except Exception as exc:
        messagebox.showerror("Error", str(exc))

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=show_main_menu
    ).pack(pady=20)


def show_services():
    clear_window()

    ttk.Label(
        root,
        text="Add Service",
        font=("Arial", 20, "bold")
    ).pack(pady=30)

    form_frame = ttk.Frame(root, padding=20)
    form_frame.pack(pady=10)

    ttk.Label(
        form_frame,
        text="Service Name:"
    ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

    name_entry = ttk.Entry(form_frame, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(
        form_frame,
        text="Price:"
    ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

    price_entry = ttk.Entry(form_frame, width=30)
    price_entry.grid(row=1, column=1, padx=10, pady=10)

    def create_service():
        name = name_entry.get().strip()
        price_text = price_entry.get().strip()

        if not name or not price_text:
            messagebox.showerror(
                "Error",
                "Please enter name and price."
            )
            return

        try:
            price = float(price_text)

            result = api_post(
                "/services",
                {
                    "name": name,
                    "price": price
                }
            )

            messagebox.showinfo(
                "Success",
                f"Service created successfully.\n"
                f"ID: {result['service_id']}"
            )

            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Price must be a number."
            )

        except Exception as exc:
            messagebox.showerror(
                "Error",
                str(exc)
            )

    ttk.Button(
        form_frame,
        text="Create Service",
        command=create_service
    ).grid(
        row=2,
        column=0,
        columnspan=2,
        pady=20
    )

    ttk.Button(
        root,
        text="Back to Main Menu",
        command=show_main_menu
    ).pack(pady=20)


def show_main_menu():
    clear_window()

    ttk.Label(
        root,
        text="Main Menu",
        font=("Arial", 20, "bold")
    ).pack(pady=30)

    ttk.Label(
        root,
        text="Hotel Booking Manager"
    ).pack(pady=5)

    button_frame = ttk.Frame(root, padding=20)
    button_frame.pack(pady=30)

    ttk.Button(
        button_frame,
        text="Rooms",
        width=25,
        command=show_rooms
    ).grid(row=0, column=0, padx=10, pady=10)

    ttk.Button(
        button_frame,
        text="Bookings",
        width=25,
        command=show_bookings
    ).grid(row=1, column=0, padx=10, pady=10)

    ttk.Button(
        button_frame,
        text="Statistics",
        width=25,
        command=show_statistics
    ).grid(row=2, column=0, padx=10, pady=10)

    ttk.Button(
        button_frame,
        text="Services",
        width=25,
        command=show_services
    ).grid(row=3, column=0, padx=10, pady=10)

    ttk.Button(
        button_frame,
        text="Disconnect",
        width=25,
        command=show_connection_view
    ).grid(row=4, column=0, padx=10, pady=20)


root = tk.Tk()
root.title("Hotel Booking Manager")
root.geometry("760x520")
root.resizable(False, False)

show_connection_view()

root.mainloop()