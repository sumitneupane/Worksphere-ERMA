# WorkSphere ERMA - Figma Frame Specifications

## Complete UI Component Frames for Figma Design

---

## 🖼️ Frame 1: Login Page

### Frame Dimensions
```
Width: 1920px
Height: 1080px
Name: "Login Page"
```

### Background
```
Fill: Linear Gradient
Angle: 135°
Stop 1: #1a1a2e (0%)
Stop 2: #16213e (100%)
```

### Login Card
```
Position: Center (Auto Layout)
Width: 450px
Height: Auto
Padding: 40px
Background: rgba(30, 30, 50, 0.9)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border Radius: 15px
Shadow: 0 8px 32px rgba(0, 0, 0, 0.5)

Contains:
  1. Logo (100×100px, centered)
  2. Title "WorkSphere ERMA" (28px, #64b5f6, centered)
  3. Subtitle "Employee and Roster Management" (14px, #9e9e9e, centered)
  4. Username input field
  5. Password input field
  6. Login button (full width)
  7. Demo credentials section
```

---

## 🖼️ Frame 2: Employee Dashboard

### Frame Dimensions
```
Width: 1920px
Height: 1080px
Name: "Employee Dashboard"
```

### Sidebar
```
Position: Fixed Left
Width: 260px
Height: 100vh
Background: rgba(20, 20, 35, 0.95)
Border-Right: 1px solid rgba(100, 100, 150, 0.2)

Components:
  1. Logo Container (20px padding, logo 50×50px)
  2. Navigation Menu (9 items)
  3. User Info (bottom, 20px padding)
```

### Main Content
```
Position: Relative
Margin-Left: 260px
Padding: 30px
Width: calc(100% - 260px)

Components:
  1. Page Header ("Employee Dashboard", 32px)
  2. Stats Grid (5 cards, 3-4 columns)
  3. Quick Actions Button Grid
```

### Stats Card (Component)
```
Width: Auto (grid item)
Min-Width: 250px
Height: Auto
Padding: 25px
Background: rgba(30, 30, 50, 0.6)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border Radius: 12px

Structure:
  - Title (14px, #9e9e9e, "Today's Schedule")
  - Value (36px, #64b5f6, "09:00 - 17:00")
  - Label (13px, #b0b0b0, "Staff")
```

---

## 🖼️ Frame 3: Admin Dashboard

### Frame Dimensions
```
Width: 1920px
Height: 1080px
Name: "Admin Dashboard"
```

### Sidebar
```
Same as Employee but with 11 menu items
Menu includes additional admin options
```

### Main Content Layout
```
Stats Grid: 6 stat cards in 3 columns
Dashboard Grid: 2 columns
  - Recent Leave Requests (left)
  - Recent Support Tickets (right)
```

---

## 🖼️ Frame 4: Data Table View

### Table Container
```
Width: 100%
Background: rgba(30, 30, 50, 0.6)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border Radius: 12px
Padding: 25px
```

### Table Structure
```
Header Row:
  Background: rgba(100, 126, 234, 0.1)
  Height: 50px
  Padding: 15px
  Font: 14px, weight 600, #64b5f6

Data Row:
  Height: 50px
  Padding: 15px
  Border-Bottom: 1px solid rgba(100, 100, 150, 0.2)
  Font: 14px, #e0e0e0
  
  Hover State:
    Background: rgba(100, 126, 234, 0.05)
```

---

## 🖼️ Frame 5: Form Modal

### Modal Overlay
```
Width: 1920px
Height: 1080px
Background: rgba(0, 0, 0, 0.8)
Z-Index: 1000
```

### Modal Content
```
Position: Center
Width: 600px
Max-Width: 90%
Height: Auto
Max-Height: 80vh
Padding: 30px
Background: rgba(30, 30, 50, 0.95)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border Radius: 15px

Components:
  1. Close Button (×, 28px, top-right)
  2. Modal Title (20px, #64b5f6)
  3. Form Fields (full width)
  4. Submit Button (bottom)
```

### Form Field (Component)
```
Width: 100%
Margin-Bottom: 20px

Label:
  Display: block
  Font: 14px, #b0b0b0
  Margin-Bottom: 8px

Input:
  Width: 100%
  Height: 44px
  Padding: 12px 15px
  Background: rgba(50, 50, 70, 0.5)
  Border: 1px solid rgba(100, 100, 150, 0.3)
  Border Radius: 8px
  Font: 14px, #e0e0e0
```

---

## 🖼️ Frame 6: ChatHub Interface

### Frame Dimensions
```
Width: 1920px
Height: 1080px
Name: "Employee ChatHub"
```

### Layout Structure
```
Sidebar + Chat Area (in Main Content)
```

### Chat Container
```
Display: Flex
Gap: 20px
Height: calc(100vh - 150px)
```

### Chat Sidebar (Conversations List)
```
Width: 300px
Background: rgba(30, 30, 50, 0.6)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border Radius: 12px
Padding: 20px
Overflow-Y: auto
```

### Conversation Item
```
Width: 100%
Padding: 12px
Background: rgba(50, 50, 70, 0.5)
Border: 1px solid rgba(100, 100, 150, 0.2)
Border Radius: 8px
Margin-Bottom: 10px
Cursor: pointer

Hover:
  Background: rgba(100, 126, 234, 0.1)
  Border-Color: #64b5f6
```

### Chat Main Area
```
Flex: 1
Display: Flex (column)
Background: rgba(30, 30, 50, 0.6)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border Radius: 12px

Structure:
  1. Chat Header (60px height, padding 20px)
  2. Messages Container (flex: 1, overflow-y: auto)
  3. Input Area (height auto, padding 20px)
```

### Chat Message
```
Max-Width: 70%
Margin-Bottom: 15px
Padding: 12px 15px
Background: rgba(50, 50, 70, 0.5)
Border Radius: 10px
Font: 14px, #e0e0e0
Line-Height: 1.4

Own Message:
  Margin-Left: auto
  Background: rgba(100, 126, 234, 0.3)

Other Message:
  Margin-Right: auto
  Background: rgba(50, 50, 70, 0.5)
```

---

## 🖼️ Frame 7: Training Card

### Training Card Component
```
Width: Auto (grid item)
Min-Width: 350px
Height: Auto
Padding: 20px
Background: rgba(30, 30, 50, 0.4)
Border: 1px solid rgba(100, 100, 150, 0.2)
Border Radius: 10px

Hover Effect:
  Transform: translateY(-3px)
  Box-Shadow: 0 5px 15px rgba(100, 126, 234, 0.2)

Structure:
  1. Header (flex, space-between)
     - Title (18px, #64b5f6)
     - Badge (status)
  2. Description (14px, #b0b0b0)
  3. Meta Grid (2 columns, 10px gap)
     - Category, Duration, Dates, etc.
  4. Action Button (if applicable)
```

---

## 🖼️ Frame 8: Support Ticket View

### Ticket Details Section
```
Width: 100%
Padding: 20px
Background: rgba(30, 30, 50, 0.4)
Border: 1px solid rgba(100, 100, 150, 0.2)
Border Radius: 10px
Margin-Bottom: 20px
```

### Detail Grid
```
Display: Grid
Grid-Template-Columns: repeat(auto-fit, minmax(200px, 1fr))
Gap: 15px

Detail Item:
  Display: Flex (column)
  
  Label:
    Font: 13px, #9e9e9e
    Margin-Bottom: 5px
  
  Value:
    Font: 14px, #e0e0e0
```

### Conversation Thread
```
Max-Height: 400px
Overflow-Y: auto
Margin-Bottom: 20px
```

### Conversation Message
```
Background: rgba(50, 50, 70, 0.3)
Border-Radius: 8px
Padding: 15px
Margin-Bottom: 15px

Admin Message:
  Background: rgba(100, 126, 234, 0.1)
  Border-Left: 3px solid #64b5f6

Message Header:
  Display: Flex
  Justify: space-between
  Margin-Bottom: 10px
  
  Name: 14px, weight 700, #64b5f6
  Time: 12px, #9e9e9e

Message Body:
  Font: 14px, #e0e0e0
  Line-Height: 1.5
```

---

## 🖼️ Frame 9: Payslip Card

### Payslip Card
```
Width: Auto (grid item)
Min-Width: 300px
Height: Auto
Padding: 20px
Background: rgba(30, 30, 50, 0.4)
Border: 1px solid rgba(100, 100, 150, 0.2)
Border Radius: 10px
```

### Payslip Header
```
Display: Flex
Justify: space-between
Align-Items: center
Margin-Bottom: 15px
Padding-Bottom: 15px
Border-Bottom: 1px solid rgba(100, 100, 150, 0.2)

Period: 18px, #64b5f6
Badge: Status badge
```

### Payslip Details
```
Detail Row:
  Display: Flex
  Justify: space-between
  Padding: 10px 0
  Border-Bottom: 1px solid rgba(100, 100, 150, 0.2)
  
  Label: 14px, #9e9e9e
  Amount: 14px, weight 600
    Positive: #4caf50
    Negative: #f44336

Total Row:
  Font-Weight: 700
  Font-Size: 16px
  Padding-Top: 15px
  Margin-Top: 10px
  Border-Top: 2px solid rgba(100, 126, 234, 0.3)
```

---

## 🖼️ Frame 10: Badge Variants

### Badge Component Set
```
Create Component Set with Variants:

Base:
  Padding: 5px 12px
  Border-Radius: 20px
  Font: 12px, weight 600

Variants (Property: "Status"):
  1. Pending
  2. Approved
  3. Rejected
  4. Completed
  5. Open
  6. Closed
  7. Low
  8. Medium
  9. High
  10. Urgent
  11. Active
  12. Inactive

Each variant has specific:
  - Background color
  - Text color
  (See Color Palette section)
```

---

## 🖼️ Frame 11: Button Variants

### Button Component Set
```
Create Component Set with Properties:

Size:
  - Default (12px 24px padding, 14px font)
  - Small (8px 16px padding, 13px font)
  - Block (full width)

Type:
  - Primary (gradient background)
  - Secondary (gray background)
  - Success (green)
  - Danger (red)

State:
  - Default
  - Hover (with transform)
  - Active
  - Disabled
```

---

## 🖼️ Frame 12: Navigation States

### Nav Menu Item States
```
Create Component with States:

Default:
  Padding: 12px 20px
  Color: #b0b0b0
  Background: transparent

Hover:
  Background: rgba(100, 126, 234, 0.1)
  Color: #64b5f6
  Border-Left: 3px solid #64b5f6

Active:
  Background: rgba(100, 126, 234, 0.2)
  Color: #64b5f6
  Border-Left: 3px solid #64b5f6
```

---

## 📐 Auto Layout Specifications

### Sidebar Auto Layout
```
Direction: Vertical
Spacing: 0
Padding: 20px 0
Fill: Container

Children:
  1. Logo Container (hug, 20px padding)
  2. Nav Menu (fill, spacing 0)
  3. User Info (hug, auto margin-top)
```

### Stats Grid Auto Layout
```
Direction: Horizontal (wrap)
Spacing: 20px
Padding: 0
Columns: Fill container

Responsive: Min 250px per item
```

### Form Auto Layout
```
Direction: Vertical
Spacing: 20px
Padding: 0
Fill: Container

Form Fields: Full width (fill)
```

---

## 🎨 Component Structure Guide

### Create These Master Components:

1. **Button** (with variants)
2. **Input Field** (with states)
3. **Badge** (with variants)
4. **Card** (base container)
5. **Stat Card** (dashboard stat)
6. **Table Row** (with hover)
7. **Nav Item** (with states)
8. **Modal** (base structure)
9. **Alert** (with variants)
10. **Chat Message** (own/other variants)

---

## 🔄 Interaction & Prototyping

### Button Interactions
```
On Click:
  - Navigate to page (for nav buttons)
  - Show modal (for action buttons)
  - Submit form (for submit buttons)

On Hover:
  - Change to hover state
  - Show tooltip (if applicable)
```

### Modal Interactions
```
On Click Outside:
  - Close modal

On Close Button:
  - Close modal

On Submit:
  - Close modal
  - Navigate/refresh
```

### Form Interactions
```
On Input Focus:
  - Change border color
  - Show focus state

On Submit:
  - Validate
  - Show loading state
  - Show success/error alert
```

---

## 📊 Example Frame Layout

### Desktop (1920×1080)
```
+----------------------------------+
|  [Sidebar 260px] | [Main Content]|
|                  |               |
|  Logo            | Header        |
|  Nav Menu        | Stats Grid    |
|  (9-11 items)    | Content       |
|                  | Footer        |
|  User Info       |               |
+----------------------------------+
```

### Mobile (375×812)
```
+------------------+
| Logo + Menu      |
+------------------+
| Main Content     |
| (Full Width)     |
| Stats (1 col)    |
| Tables (scroll)  |
+------------------+
```

---

## 🎯 Figma Organization

### Recommended Page Structure
```
📄 Cover
📄 Design System
   - Colors
   - Typography
   - Components
   - Spacing
📄 Pages
   - Login
   - Employee Dashboard
   - Employee Pages (Schedule, Leave, etc.)
   - Admin Dashboard
   - Admin Pages (Users, Departments, etc.)
📄 Components Library
📄 Mobile Screens
📄 Prototypes
```

---

## ✅ Checklist for Figma Recreation

- [ ] Set up color styles (all colors)
- [ ] Set up text styles (all typography)
- [ ] Create button components (all variants)
- [ ] Create input components
- [ ] Create badge components (all variants)
- [ ] Create card components
- [ ] Create nav item component
- [ ] Create modal component
- [ ] Build login page
- [ ] Build employee dashboard
- [ ] Build admin dashboard
- [ ] Build all employee pages
- [ ] Build all admin pages
- [ ] Add interactions
- [ ] Create prototype flow
- [ ] Test responsive layouts
- [ ] Export design specs

---

**Use this document to recreate the exact WorkSphere ERMA design in Figma!**
