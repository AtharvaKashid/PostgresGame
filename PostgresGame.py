import tkinter as tk
from tkinter import messagebox, simpledialog
import psycopg2
import hashlib
import random

# --- Database Configuration (Centralized) ---
DB_CONFIG = {
    "database": "postgreGame",
    "user": "postgres",
    "password": "AtharvPost@123",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        messagebox.showerror("Database Connection Error", f"Could not connect to database: {e}")
        return None

class RegistrationPage:
    def __init__(self, master):
        self.master = master
        master.title("Registration Page")
        master.geometry("800x600") # Set a fixed window size for better control
        master.resizable(False, False) # Prevent resizing

        # Center the frame
        self.frame = tk.Frame(master, bg="light gray", bd=5, relief="groove")
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=300)

        self.title_label = tk.Label(self.frame, text="Register", bg="green", fg="white", font=('Helvetica', 20, 'bold'), pady=10)
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="ew")

        self.email_label = tk.Label(self.frame, text="Email:", bg="lightblue", font=('Helvetica', 14))
        self.email_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.email_entry = tk.Entry(self.frame, width=35, font=('Helvetica', 12), bd=2, relief="sunken")
        self.email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = tk.Label(self.frame, text="Password:", bg="lightblue", font=('Helvetica', 14))
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.password_entry = tk.Entry(self.frame, show="*", width=35, font=('Helvetica', 12), bd=2, relief="sunken")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.register_button = tk.Button(self.frame, text="Register", command=self.register, bg="green", fg="white",
                                         width=18, font=('Helvetica', 13, 'bold'), relief="raised", bd=3)
        self.register_button.grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="ew")

        self.already_registered_button = tk.Button(self.frame, text="Already Registered? Login", command=self.goto_login,
                                                   bg="blue", fg="white", width=25, font=('Helvetica', 11), relief="raised", bd=2)
        self.already_registered_button.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        # Configure column weights for resizing
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)


    def register(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Input Error", "Email and Password cannot be empty.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = None
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful! You can now log in.")
                self.master.destroy()
                LoginPage()
        except psycopg2.errors.UniqueViolation:
            messagebox.showerror("Registration Failed", "This email is already registered. Please use a different email or log in.")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
        finally:
            if conn:
                conn.close()

    def goto_login(self):
        self.master.destroy()
        LoginPage()

class LoginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Page")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, bg="light gray", bd=5, relief="groove")
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=300)

        self.title_label = tk.Label(self.frame, text="Login", bg="green", fg="white", font=('Helvetica', 20, 'bold'), pady=10)
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="ew")

        self.email_label = tk.Label(self.frame, text="Email:", bg="lightblue", font=('Helvetica', 14))
        self.email_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.email_entry = tk.Entry(self.frame, width=35, font=('Helvetica', 12), bd=2, relief="sunken")
        self.email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = tk.Label(self.frame, text="Password:", bg="lightblue", font=('Helvetica', 14))
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.password_entry = tk.Entry(self.frame, show="*", width=35, font=('Helvetica', 12), bd=2, relief="sunken")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.login_button = tk.Button(self.frame, text="Login", command=self.login, bg="green", fg="white",
                                       width=18, font=('Helvetica', 13, 'bold'), relief="raised", bd=3)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="ew")

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)


        self.root.mainloop()

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Input Error", "Email and Password cannot be empty.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = None
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, email FROM users WHERE email=%s AND password=%s", (email, hashed_password))
                user = cursor.fetchone()
                if user:
                    messagebox.showinfo("Success", "Login successful!")
                    self.root.destroy()
                    GameStartPage(user[0], user[1]) # Pass user_id and email
                else:
                    messagebox.showerror("Error", "Invalid email or password!")
        except Exception as e:
            messagebox.showerror("Login Error", f"An error occurred during login: {e}")
        finally:
            if conn:
                conn.close()


class GameStartPage:
    def __init__(self, user_id, email):
        self.root = tk.Tk()
        self.root.title("Postgre Game")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.user_id = user_id
        self.email = email
        self.current_question_index = 0
        self.total_marks = 0
        self.questions = self.fetch_questions()
        random.shuffle(self.questions) # Shuffle questions for variety

        if not self.questions:
            messagebox.showerror("No Questions", "No questions found in the database. Please add some questions to play.")
            self.root.destroy()
            return

        self.frame = tk.Frame(self.root, bg="light yellow", bd=5, relief="raised")
        self.frame.pack(padx=30, pady=30, fill="both", expand=True)

        self.header_frame = tk.Frame(self.frame, bg="light yellow")
        self.header_frame.pack(fill="x", pady=10)

        self.marks_label = tk.Label(self.header_frame, text=f"Marks: {self.total_marks}", font=("Helvetica", 16, 'bold'), bg="light yellow", fg="dark green")
        self.marks_label.pack(side="left", padx=15)

        self.timer_label = tk.Label(self.header_frame, text="Time Left: 60 seconds", font=("Helvetica", 16, 'bold'), bg="light yellow", fg="dark red")
        self.timer_label.pack(side="right", padx=15)

        self.question_label = tk.Label(self.frame, text="", font=("Helvetica", 18, 'bold'), wraplength=700, justify="center", bg="light yellow", fg="dark blue")
        self.question_label.pack(pady=20, padx=20)

        self.query_entry = tk.Entry(self.frame, font=("Courier New", 14), width=70, bd=3, relief="sunken")
        self.query_entry.pack(pady=15, ipady=5)

        self.button_frame = tk.Frame(self.frame, bg="light yellow")
        self.button_frame.pack(pady=10)

        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.submit_query, bg="green", fg="white",
                                       width=15, font=("Helvetica", 14, 'bold'), relief="raised", bd=3)
        self.submit_button.pack(side="left", padx=10)

        self.next_button = tk.Button(self.button_frame, text="Next Question", command=self.load_next_question, bg="blue", fg="white",
                                     width=15, font=("Helvetica", 14, 'bold'), relief="raised", bd=3)
        self.next_button.pack(side="left", padx=10)
        self.next_button.config(state=tk.DISABLED)

        self.load_question()
        self.root.mainloop()

    def fetch_questions(self):
        conn = None
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT questions, correct_answer FROM questions")
                questions = cursor.fetchall()
                return questions
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch questions: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def load_question(self):
        if self.current_question_index >= len(self.questions):
            self.finish_game()
            return

        question, _ = self.questions[self.current_question_index]
        self.question_label.config(text=f"Question {self.current_question_index + 1}: {question}")

        self.query_entry.delete(0, tk.END)
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

        self.time_left = 60
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time Left: {self.time_left} seconds")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's Up!")
            messagebox.showinfo("Time's Up", "Sorry, time's up for this question!")
            self.submit_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.NORMAL)

    def submit_query(self):
        user_query = self.query_entry.get().strip()
        correct_answer = self.questions[self.current_question_index][1].strip()

        # Stop the timer immediately upon submission
        if hasattr(self, 'timer_id'):
            self.root.after_cancel(self.timer_id)

        if user_query.lower() == correct_answer.lower():
            self.total_marks += 1
            self.marks_label.config(text=f"Marks: {self.total_marks}")
            messagebox.showinfo("Correct!", "Your answer is correct!")
        else:
            messagebox.showerror("Incorrect!", f"Your answer is incorrect.\nCorrect answer: {correct_answer}")

        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def load_next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.load_question()
        else:
            self.finish_game()

    def finish_game(self):
        messagebox.showinfo("Game Over", f"Congratulations! You scored {self.total_marks} out of {len(self.questions)}.")
        self.save_game_completion()
        self.root.destroy()

    def save_game_completion(self):
        conn = None
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                average_score = (self.total_marks / len(self.questions)) * 100 if len(self.questions) > 0 else 0
                cursor.execute(
                    "INSERT INTO game_completion (user_id, answers_submitted, average, status) VALUES (%s, %s, %s, %s)",
                    (self.user_id, len(self.questions), average_score, "complete")
                )
                conn.commit()
                messagebox.showinfo("Game Saved", "Your game completion status has been saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save game completion status: {e}")
        finally:
            if conn:
                conn.close()

def main():
    root = tk.Tk()
    app = RegistrationPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()