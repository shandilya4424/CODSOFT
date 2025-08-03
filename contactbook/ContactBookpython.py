import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

contacts = []

class ContactBook:
    def __init__(self, root):
        self.root = root
        root.title("Contacts Book")
        root.geometry("900x550")
        self.setup_ui()
        self.display_contacts()

    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)

        left = tk.Frame(self.root, bg="#e6ffe6")
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left.columnconfigure(1, weight=1)


        tk.Label(left, text="Search (Name or Mobile):", bg="#e6ffe6").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        se = tk.Entry(left, textvariable=self.search_var, width=30)
        se.grid(row=0, column=1, sticky="ew", pady=5)
        btn_search = tk.Button(left, text="Search", width=10, command=self.search_contact)
        btn_search.grid(row=0, column=2, padx=5)
        se.bind("<KeyRelease>", lambda e: self.search_contact())

       
        self.name_var = tk.StringVar()
        self.mobile_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.tel_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.dob_day = tk.StringVar(value="Day")
        self.dob_month = tk.StringVar(value="Mon")
        self.dob_year = tk.StringVar(value=str(datetime.now().year))
        self.address_var = tk.StringVar()

        labels = [
            ("Name *", self.name_var),
            ("Mobile No *", self.mobile_var),
            ("Email", self.email_var),
            ("Tel No", self.tel_var)
        ]
        for idx, (lbl, var) in enumerate(labels, start=1):
            tk.Label(left, text=lbl, bg="#e6ffe6").grid(row=idx, column=0, sticky="w", pady=5)
            tk.Entry(left, textvariable=var, width=30).grid(row=idx, column=1, columnspan=2, sticky="ew", pady=5)

       
        tk.Label(left, text="Gender *", bg="#e6ffe6").grid(row=5, column=0, sticky="w", pady=5)
        gf = tk.Frame(left, bg="#e6ffe6")
        gf.grid(row=5, column=1, sticky="w", pady=5)
        tk.Radiobutton(gf, text="Male", variable=self.gender_var, value="Male", bg="#e6ffe6").pack(side="left")
        tk.Radiobutton(gf, text="Female", variable=self.gender_var, value="Female", bg="#e6ffe6").pack(side="left")

     
        tk.Label(left, text="DOB *", bg="#e6ffe6").grid(row=6, column=0, sticky="w", pady=5)
        df = tk.Frame(left, bg="#e6ffe6")
        df.grid(row=6, column=1, columnspan=2, sticky="w", pady=5)
        ttk.Combobox(df, values=[str(i) for i in range(1,32)], width=4,
                     state="readonly", textvariable=self.dob_day).pack(side="left", padx=2)
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        ttk.Combobox(df, values=months, width=6,
                     state="readonly", textvariable=self.dob_month).pack(side="left", padx=2)
        years = [str(i) for i in range(1900, datetime.now().year+1)]
        ttk.Combobox(df, values=years, width=6,
                     state="readonly", textvariable=self.dob_year).pack(side="left", padx=2)

        
        tk.Label(left, text="Address *", bg="#e6ffe6").grid(row=7, column=0, sticky="w", pady=5)
        tk.Entry(left, textvariable=self.address_var, width=30).grid(row=7, column=1, columnspan=2,
                                                                     sticky="ew", pady=5)

       
        actions = [("Add", self.add_contact), ("Update", self.update_contact),
                   ("Delete", self.delete_contact), ("Clear", self.clear_fields)]
        for idx, (text, cmd) in enumerate(actions):
            r = 8 + idx // 2
            c = idx % 2
            tk.Button(left, text=text, width=12, command=cmd).grid(row=r, column=c, pady=10, padx=5)

       
        right = tk.Frame(self.root, bg="#eef")
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        cols = ("Name","Mobile","Email","Tel","Gender","DOB","Address")
        self.tree = ttk.Treeview(right, columns=cols, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, stretch=True)
        vs = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        vs.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vs.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def get_dob(self):
        return f"{self.dob_day.get()} {self.dob_month.get()} {self.dob_year.get()}"

    def validate_contact(self, data):
        return all(data[:2]) and data[4] and data[6]

    def display_contacts(self, filtered=None):
        self.tree.delete(*self.tree.get_children())
        for rec in (filtered if filtered is not None else contacts):
            self.tree.insert("", "end", values=rec)

    def add_contact(self):
        dob = self.get_dob()
        data = (self.name_var.get().strip(), self.mobile_var.get().strip(),
                self.email_var.get().strip(), self.tel_var.get().strip(),
                self.gender_var.get(), dob, self.address_var.get().strip())
        if not self.validate_contact(data):
            messagebox.showwarning("Error", "Fill all required fields (*)")
            return
        contacts.append(data)
        self.display_contacts()
        messagebox.showinfo("Success", f"{data[0]} added.")
        self.clear_fields()

    def update_contact(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a contact to update.")
            return
        idx = self.tree.index(sel[0])
        dob = self.get_dob()
        data = (self.name_var.get().strip(), self.mobile_var.get().strip(),
                self.email_var.get().strip(), self.tel_var.get().strip(),
                self.gender_var.get(), dob, self.address_var.get().strip())
        if not self.validate_contact(data):
            messagebox.showwarning("Error", "Fill all required fields (*)")
            return
        contacts[idx] = data
        self.display_contacts()
        messagebox.showinfo("Success", f"{data[0]} updated.")
        self.clear_fields()

    def delete_contact(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Select a contact to delete.")
            return
        idx = self.tree.index(sel[0])
        name = contacts[idx][0]
        if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
            contacts.pop(idx)
            self.display_contacts()
            messagebox.showinfo("Deleted", f"{name} deleted.")
            self.clear_fields()

    def clear_fields(self):
        for v in [self.name_var, self.mobile_var, self.email_var,
                  self.tel_var, self.gender_var, self.address_var]:
            v.set("")
        self.dob_day.set("Day")
        self.dob_month.set("Mon")
        self.dob_year.set(str(datetime.now().year))

    def on_select(self, event):
        sel = self.tree.selection()
        if sel:
            vals = self.tree.item(sel[0], "values")
            self.name_var.set(vals[0])
            self.mobile_var.set(vals[1])
            self.email_var.set(vals[2])
            self.tel_var.set(vals[3])
            self.gender_var.set(vals[4])
            day,mon,year = vals[5].split()
            self.dob_day.set(day)
            self.dob_month.set(mon)
            self.dob_year.set(year)
            self.address_var.set(vals[6])

    def search_contact(self):
        term = self.search_var.get().strip().lower()
        if not term:
            self.display_contacts()
            return
        filtered = [c for c in contacts
                    if term in c[0].lower() or term in c[1].lower()]
        self.display_contacts(filtered)
        if filtered:
           
            item = self.tree.get_children()[0]
            self.tree.selection_set(item)
            self.tree.focus(item)
            self.tree.see(item)
        else:
            messagebox.showinfo("Search", f"No results for '{self.search_var.get()}'")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
