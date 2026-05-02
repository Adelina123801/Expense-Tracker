import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # --- Поля ввода ---
        tk.Label(self.root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # --- Кнопки ---
        tk.Button(self.root, text="Добавить расход", command=self.add_expense).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # --- Таблица ---
        self.tree = ttk.Treeview(self.root, columns=("Amount", "Category", "Date"), show='headings')
        self.tree.heading("Amount", text="Сумма")
        self.tree.heading("Category", text="Категория")
        self.tree.heading("Date", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # --- Фильтры ---
        tk.Label(self.root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_category = tk.Entry(self.root)
        self.filter_category.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по дате (YYYY-MM-DD):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтры", command=self.filter_expenses).grid(
            row=7, column=0, columnspan=2, pady=10
        )

        # --- Общая сумма ---
        self.total_label = tk.Label(self.root, text="Сумма расходов: 0")
        self.total_label.grid(row=8, column=0, columnspan=2, pady=5)

    # --- Функции ---
    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date_str = self.date_entry.get()

        # Проверка суммы
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
            return

        # Проверка даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD")
            return

        expense = {"amount": amount, "category": category, "date": date_str}
        self.expenses.append(expense)
        self.save_data()
        self.update_table()
        self.clear_entries()

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def update_table(self, filtered=None):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = filtered if filtered is not None else self.expenses
        total = 0
        for exp in data:
            self.tree.insert("", tk.END, values=(exp["amount"], exp["category"], exp["date"]))
            total += exp["amount"]

        self.total_label.config(text=f"Сумма расходов: {total}")

    def filter_expenses(self):
        category = self.filter_category.get().strip()
        date = self.filter_date.get().strip()

        filtered = self.expenses
        if category:
            filtered = [e for e in filtered if e["category"].lower() == category.lower()]
        if date:
            filtered = [e for e in filtered if e["date"] == date]

        self.update_table(filtered)

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                self.expenses = json.load(f)
                self.update_table()
        except FileNotFoundError:
            self.expenses = []


# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()