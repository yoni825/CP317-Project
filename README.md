# 🚗 Car Rental System (CP317)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
![Flask](https://img.shields.io/badge/Flask-web_framework-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)

A **Python-based** web application that lets **customers** search and reserve vehicles and gives the **rental company** tools to monitor daily rentals, track fleet utilization, and analyze customer preferences.

---

## 📌 Table of Contents
- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [How to Run](#how-to-run)
  - [Seed & Admin Account](#seed--admin-account)

- [Team](#-team)

---

## 🧠 About
The **Car Rental System** is built for **CP317** to demonstrate an end-to-end software product using **Python**  
It focuses on **clear user journeys** (search → reserve → manage bookings) and **operational insights** (daily rentals, utilization, and customer preferences).

**Objectives**
- Customers can **search** available cars by category/type & date range, **reserve**, and **view rental history**.
- Company staff can **monitor daily rentals**, **track utilization by vehicle type**, and **analyze customer preferences**.

---

## 🔑 Features
**Customer**
- 🔎 Search cars by **type/category**, location, and dates  
- 📝 Reserve & cancel bookings (with conflict checks)  
- 🧾 View rental history (upcoming, active, completed, canceled)

**Company / Admin**
- 📅 Daily rentals dashboard (pickups/returns)  
- 📈 Utilization reporting by vehicle category  
- 📊 Customer preference analytics (search → reservation funnel)  
- 🚗 Vehicle inventory management (CRUD, maintenance flag)

**Quality of Life**
- 🔐 JWT auth (roles: `customer`, `staff`, `manager`)  
- 🧪 Unit & integration tests (Pytest)  
- 🧰 Seed script for demo data

---

## 🧱 Tech Stack
- **Language:** Python 3.10+
- **Framework:** Flask (Blueprints, Jinja2)
- **Database:** SQLite (dev) / MySQL or PostgreSQL (prod)
- **ORM:** SQLAlchemy + Alembic (migrations)
- **Auth:** Flask-JWT-Extended
- **Styling (optional):** Bootstrap
- **Analytics:** SQL aggregation + optional Pandas
- **Testing:** Pytest

---

## 🗂 Project Structure
