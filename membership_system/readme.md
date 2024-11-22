## **API Endpoints**

### **Members**
- **URL:** `/api/members/`
- **Methods:**
  - `GET`: List all members.
  - `POST`: Create a new member.
  - `PUT`/`PATCH`: Update a member.
  - `DELETE`: Delete a member.
- **Authentication:** Required

---

### **Expenses**
- **URL:** `/api/expenses/`
- **Methods:**
  - `GET`: List all expenses.
  - `POST`: Create a new expense.
  - `PUT`/`PATCH`: Update an expense.
  - `DELETE`: Delete an expense.
- **Authentication:** Required

---

### **Memberships**
- **URL:** `/api/memberships/`
- **Methods:**
  - `GET`: List all memberships.
  - `POST`: Create a new membership.
  - `PUT`/`PATCH`: Update a membership.
  - `DELETE`: Delete a membership.
- **Authentication:** Required

---

### **Payments**
- **URL:** `/api/payments/`
- **Methods:**
  - `GET`: List all payments.
  - `POST`: Record a new payment.
  - `PUT`/`PATCH`: Update a payment record.
  - `DELETE`: Delete a payment record.
- **Authentication:** Required

---

### **Token Obtain**
- **URL:** `/api/token/`
- **Methods:**
  - `POST`: Obtain an access and refresh token.
- **Authentication:** Not Required

---

### **Token Refresh**
- **URL:** `/api/token/refresh/`
- **Methods:**
  - `POST`: Refresh the access token using the refresh token.
- **Authentication:** Required
