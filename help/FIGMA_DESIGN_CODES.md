# WorkSphere ERMA - Figma Design Specifications

## Complete Design System Documentation

---

## 🎨 Color Palette

### Primary Colors
```
Brand Blue: #64b5f6
RGB: (100, 181, 246)
HSL: (207, 88%, 68%)
Usage: Logo, headings, primary accents, links

Deep Purple: #667eea
RGB: (102, 126, 234)
HSL: (228, 76%, 66%)
Usage: Button gradients, active states

Royal Purple: #764ba2
RGB: (118, 75, 162)
HSL: (270, 37%, 46%)
Usage: Button gradients, highlights
```

### Background Colors
```
Dark Navy (Primary BG): #1a1a2e
RGB: (26, 26, 46)
HSL: (240, 28%, 14%)
Usage: Main body background

Deep Blue (Secondary BG): #16213e
RGB: (22, 33, 62)
HSL: (223, 48%, 16%)
Usage: Background gradients

Card Background: rgba(30, 30, 50, 0.6)
Usage: Cards, sections, containers

Sidebar Background: rgba(20, 20, 35, 0.95)
Usage: Navigation sidebar

Input Background: rgba(50, 50, 70, 0.5)
Usage: Form inputs, textareas, selects
```

### Text Colors
```
Primary Text: #e0e0e0
RGB: (224, 224, 224)
Usage: Main content text

Secondary Text: #b0b0b0
RGB: (176, 176, 176)
Usage: Labels, descriptions

Muted Text: #9e9e9e
RGB: (158, 158, 158)
Usage: Placeholders, timestamps, meta info
```

### Border Colors
```
Primary Border: rgba(100, 100, 150, 0.3)
Usage: Input borders, card borders

Light Border: rgba(100, 100, 150, 0.2)
Usage: Subtle dividers, table borders

Active Border: #64b5f6
Usage: Focused inputs, active elements
```

### Status Colors
```
Success Green: #4caf50
RGB: (76, 175, 80)
Usage: Success messages, approved status

Warning Orange: #ff9800
RGB: (255, 152, 0)
Usage: Pending status, medium priority

Error Red: #f44336
RGB: (244, 67, 54)
Usage: Error messages, rejected status

Info Blue: #2196f3
RGB: (33, 150, 243)
Usage: Info messages, completed status

Urgent Red: #d50000
RGB: (213, 0, 0)
Usage: Urgent priority

Low Blue: #03a9f4
RGB: (3, 169, 244)
Usage: Low priority

High Orange Red: #ff5722
RGB: (255, 87, 34)
Usage: High priority

Warning Yellow: #ffc107
RGB: (255, 193, 7)
Usage: Pending, warnings
```

---

## 📐 Typography

### Font Family
```
Primary Font: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
Fallback: System UI fonts
```

### Font Sizes
```
H1 (Page Titles): 32px
Weight: 400
Color: #64b5f6
Usage: Main page headings

H2 (Section Titles): 22px
Weight: 400
Color: #64b5f6
Usage: Section headings

H3 (Card Titles): 18px
Weight: 600
Color: #64b5f6
Usage: Card headings, subsections

Body Text: 14px
Weight: 400
Color: #e0e0e0
Usage: Main content

Small Text: 13px
Weight: 400
Color: #9e9e9e
Usage: Meta information, labels

Tiny Text: 12px
Weight: 400
Color: #9e9e9e
Usage: Timestamps, badges

Large Stats: 36px
Weight: 700
Color: #64b5f6
Usage: Dashboard statistics

Button Text: 14px
Weight: 600
Color: white
Usage: Button labels
```

### Line Heights
```
Headers: 1.2
Body: 1.5
Small Text: 1.4
```

---

## 📦 Component Specifications

### 1. Buttons

#### Primary Button
```
Background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Padding: 12px 24px
Border-Radius: 8px
Font-Size: 14px
Font-Weight: 600
Color: white
Text-Transform: none
Border: none
Cursor: pointer

Hover State:
  Transform: translateY(-2px)
  Box-Shadow: 0 5px 15px rgba(102, 126, 234, 0.4)

Active State:
  Transform: translateY(0)
```

#### Secondary Button
```
Background: rgba(100, 100, 150, 0.3)
Padding: 12px 24px
Border-Radius: 8px
Font-Size: 14px
Font-Weight: 600
Color: #e0e0e0

Hover State:
  Background: rgba(100, 100, 150, 0.5)
```

#### Small Button
```
Padding: 8px 16px
Font-Size: 13px
All other properties same as base button
```

#### Success Button
```
Background: #4caf50
Padding: 12px 24px
Border-Radius: 8px
Color: white
```

#### Danger Button
```
Background: #f44336
Padding: 12px 24px
Border-Radius: 8px
Color: white
```

---

### 2. Form Inputs

#### Text Input / Select / Textarea
```
Width: 100%
Padding: 12px 15px
Background: rgba(50, 50, 70, 0.5)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border-Radius: 8px
Color: #e0e0e0
Font-Size: 14px

Focus State:
  Border-Color: #64b5f6
  Background: rgba(50, 50, 70, 0.7)
  Outline: none

Placeholder:
  Color: #9e9e9e
  Opacity: 0.7
```

#### Label
```
Display: block
Margin-Bottom: 8px
Color: #b0b0b0
Font-Size: 14px
Font-Weight: 400
```

---

### 3. Cards

#### Standard Card
```
Background: rgba(30, 30, 50, 0.6)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border-Radius: 12px
Padding: 25px

Hover State:
  Transform: translateY(-5px)
  Box-Shadow: 0 8px 20px rgba(100, 126, 234, 0.2)
  Transition: all 0.3s ease
```

#### Stat Card
```
Background: rgba(30, 30, 50, 0.6)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border-Radius: 12px
Padding: 25px

Structure:
  - H3 Title: #9e9e9e, 14px, weight 400
  - Stat Value: #64b5f6, 36px, weight 700
  - Stat Label: #b0b0b0, 13px

Hover State:
  Transform: translateY(-5px)
  Box-Shadow: 0 8px 20px rgba(100, 126, 234, 0.2)
```

---

### 4. Navigation

#### Sidebar
```
Width: 260px
Background: rgba(20, 20, 35, 0.95)
Border-Right: 1px solid rgba(100, 100, 150, 0.2)
Padding: 20px 0
Position: fixed
Height: 100vh
Display: flex
Flex-Direction: column
Overflow-Y: auto
```

#### Logo Container
```
Padding: 0 20px 20px 20px
Border-Bottom: 1px solid rgba(100, 100, 150, 0.2)

Logo Image:
  Width: 50px
  Height: 50px
  Margin-Bottom: 10px

Title:
  Color: #64b5f6
  Font-Size: 22px
```

#### Nav Menu Item
```
Padding: 12px 20px
Color: #b0b0b0
Text-Decoration: none
Transition: all 0.3s ease

Hover State:
  Background: rgba(100, 126, 234, 0.1)
  Color: #64b5f6
  Border-Left: 3px solid #64b5f6

Active State:
  Background: rgba(100, 126, 234, 0.2)
  Color: #64b5f6
  Border-Left: 3px solid #64b5f6
```

#### User Info Section
```
Padding: 20px
Border-Top: 1px solid rgba(100, 100, 150, 0.2)
Background: rgba(20, 20, 35, 0.95)
Margin-Top: auto

Text:
  Color: #9e9e9e
  Font-Size: 14px
  Margin-Bottom: 10px
```

---

### 5. Tables

#### Data Table
```
Width: 100%
Border-Collapse: collapse
```

#### Table Header
```
Background: rgba(100, 126, 234, 0.1)
Padding: 15px
Text-Align: left
Color: #64b5f6
Font-Weight: 600
Font-Size: 14px
```

#### Table Cell
```
Padding: 15px
Border-Bottom: 1px solid rgba(100, 100, 150, 0.2)
Color: #e0e0e0
Font-Size: 14px
```

#### Table Row Hover
```
Background: rgba(100, 126, 234, 0.05)
```

---

### 6. Badges

#### Base Badge
```
Display: inline-block
Padding: 5px 12px
Border-Radius: 20px
Font-Size: 12px
Font-Weight: 600
```

#### Badge Variants
```
Pending:
  Background: rgba(255, 193, 7, 0.2)
  Color: #ffc107

Approved/Active/Success:
  Background: rgba(76, 175, 80, 0.2)
  Color: #4caf50

Rejected/Inactive:
  Background: rgba(244, 67, 54, 0.2)
  Color: #f44336

Completed:
  Background: rgba(33, 150, 243, 0.2)
  Color: #2196f3

Open/Medium:
  Background: rgba(255, 152, 0, 0.2)
  Color: #ff9800

Closed:
  Background: rgba(158, 158, 158, 0.2)
  Color: #9e9e9e

Low Priority:
  Background: rgba(3, 169, 244, 0.2)
  Color: #03a9f4

High Priority:
  Background: rgba(255, 87, 34, 0.2)
  Color: #ff5722

Urgent:
  Background: rgba(213, 0, 0, 0.2)
  Color: #d50000
```

---

### 7. Modals

#### Modal Overlay
```
Display: none (show with display: block)
Position: fixed
Z-Index: 1000
Left: 0
Top: 0
Width: 100%
Height: 100%
Background: rgba(0, 0, 0, 0.8)
```

#### Modal Content
```
Background: rgba(30, 30, 50, 0.95)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border-Radius: 15px
Margin: 5% auto
Padding: 30px
Width: 90%
Max-Width: 600px
Max-Height: 80vh
Overflow-Y: auto
```

#### Modal Close Button
```
Color: #9e9e9e
Float: right
Font-Size: 28px
Font-Weight: bold
Cursor: pointer

Hover:
  Color: #64b5f6
```

---

### 8. Alerts

#### Success Alert
```
Background: rgba(76, 175, 80, 0.2)
Border: 1px solid #4caf50
Color: #4caf50
Padding: 15px 20px
Border-Radius: 8px
Margin-Bottom: 20px
Font-Size: 14px
```

#### Error Alert
```
Background: rgba(244, 67, 54, 0.2)
Border: 1px solid #f44336
Color: #f44336
Padding: 15px 20px
Border-Radius: 8px
Margin-Bottom: 20px
Font-Size: 14px
```

#### Info Alert
```
Background: rgba(33, 150, 243, 0.2)
Border: 1px solid #2196f3
Color: #2196f3
Padding: 15px 20px
Border-Radius: 8px
Margin-Bottom: 20px
Font-Size: 14px
```

---

### 9. Logo

#### Logo Specifications
```
Format: PNG
Size: 200x200px
Background: Circular gradient
  Outer Circle: #64b5f6 (Brand Blue)
  Inner Circle: #677eea (Deep Purple)
Text: "WS"
Font: DejaVu Sans Bold, 80px
Color: White (#ffffff)
Position: Centered

Usage Sizes:
  Large (Login): 100x100px
  Small (Sidebar): 50x50px
```

---

## 📱 Layout Specifications

### Page Layout
```
Body:
  Background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)
  Min-Height: 100vh
  Font-Family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
  Color: #e0e0e0
```

### Dashboard Container
```
Display: flex
Min-Height: 100vh
```

### Main Content Area
```
Margin-Left: 260px (sidebar width)
Flex: 1
Padding: 30px
```

### Login Container
```
Display: flex
Justify-Content: center
Align-Items: center
Min-Height: 100vh
Padding: 20px
```

### Login Box
```
Background: rgba(30, 30, 50, 0.9)
Border: 1px solid rgba(100, 100, 150, 0.3)
Border-Radius: 15px
Padding: 40px
Width: 100%
Max-Width: 450px
Box-Shadow: 0 8px 32px rgba(0, 0, 0, 0.5)
```

---

## 📊 Grid Systems

### Stats Grid
```
Display: grid
Grid-Template-Columns: repeat(auto-fit, minmax(250px, 1fr))
Gap: 20px
Margin-Bottom: 30px
```

### Dashboard Grid
```
Display: grid
Grid-Template-Columns: repeat(auto-fit, minmax(400px, 1fr))
Gap: 20px
```

### Training Grid
```
Display: grid
Grid-Template-Columns: repeat(auto-fit, minmax(350px, 1fr))
Gap: 20px
```

### Payslip Grid
```
Display: grid
Grid-Template-Columns: repeat(auto-fit, minmax(300px, 1fr))
Gap: 20px
```

### Button Grid
```
Display: grid
Grid-Template-Columns: repeat(auto-fit, minmax(200px, 1fr))
Gap: 15px
```

---

## 🎭 Effects & Transitions

### Standard Transition
```
Transition: all 0.3s ease
```

### Button Hover Effect
```
Transform: translateY(-2px)
Box-Shadow: 0 5px 15px rgba(102, 126, 234, 0.4)
Transition: all 0.3s ease
```

### Card Hover Effect
```
Transform: translateY(-5px)
Box-Shadow: 0 8px 20px rgba(100, 126, 234, 0.2)
Transition: all 0.3s ease
```

### Box Shadows
```
Light Shadow: 0 2px 8px rgba(0, 0, 0, 0.2)
Medium Shadow: 0 4px 12px rgba(0, 0, 0, 0.3)
Heavy Shadow: 0 8px 32px rgba(0, 0, 0, 0.5)
Colored Shadow: 0 5px 15px rgba(102, 126, 234, 0.4)
Card Shadow: 0 8px 20px rgba(100, 126, 234, 0.2)
```

---

## 📏 Spacing System

### Padding Scale
```
XS: 5px
SM: 10px
MD: 15px
LG: 20px
XL: 25px
XXL: 30px
XXXL: 40px
```

### Margin Scale
```
XS: 5px
SM: 10px
MD: 15px
LG: 20px
XL: 30px
```

### Border Radius
```
Small: 6px
Medium: 8px
Large: 10px
XLarge: 12px
XXLarge: 15px
Pill: 20px
```

---

## 🖼️ Specific Page Layouts

### Login Page
```
Container: Centered flexbox
Background: Full viewport gradient
Card: 450px max-width, centered
Logo: 100x100px, centered
Form Elements: Full width within card
Button: Full width, gradient background
```

### Dashboard (Employee/Admin)
```
Layout: Sidebar (260px fixed) + Main Content
Stats Grid: 3-4 columns on desktop, 1 column mobile
Section Cards: Full width with 25px padding
Tables: Full width, responsive scroll on mobile
```

### Chat Interface
```
Layout: Split view
Sidebar: 300px user list
Main Area: Flex column (header, messages, input)
Messages: Scroll container with auto-refresh
```

---

## 📱 Responsive Breakpoints

```
Mobile: max-width 768px
  - Sidebar: width 100%, relative position
  - Main Content: margin-left 0
  - Grids: single column
  - Stats: single column
  - Tables: horizontal scroll

Tablet: 769px - 1024px
  - Sidebar: 260px fixed
  - Grids: 2 columns
  - Stats: 2-3 columns

Desktop: 1025px+
  - Full layout as designed
  - Multi-column grids
  - Optimal spacing
```

---

## 🎨 Accessibility

### Contrast Ratios
```
Primary Text on Background: 12.6:1 (AAA)
Secondary Text on Background: 8.4:1 (AAA)
Blue Links on Background: 4.8:1 (AA)
Button Text on Gradient: 4.5:1 (AA)
```

### Focus States
```
All Interactive Elements:
  Outline: 2px solid #64b5f6
  Outline-Offset: 2px
  
Inputs:
  Border-Color: #64b5f6
  Box-Shadow: 0 0 0 3px rgba(100, 181, 246, 0.2)
```

---

## 🔤 Icon System

```
Note: This system uses text-based UI elements
No icon font used, but can integrate:
  - Font Awesome
  - Material Icons
  - Lucide Icons
  
Recommended Size: 18-24px
Color: Inherit from parent or #64b5f6
```

---

## 📐 Component Measurements

### Header Heights
```
Page Header: 60px
Section Header: 40px
Card Header: 50px
```

### Content Widths
```
Max Container Width: 1400px
Form Max Width: 600px
Login Box Max Width: 450px
Modal Max Width: 600px
```

### Element Heights
```
Button Height: 44px (12px padding × 2 + 20px text)
Input Height: 44px (12px padding × 2 + 20px text)
Nav Item Height: 44px (12px padding × 2 + 20px text)
Table Row Height: ~50px (15px padding × 2 + 20px text)
```

---

## 🎯 Design Principles

1. **Dark Theme**: All backgrounds use dark colors for reduced eye strain
2. **Consistency**: Same spacing, colors, and patterns throughout
3. **Clarity**: High contrast text for readability
4. **Feedback**: Hover and focus states on all interactive elements
5. **Hierarchy**: Size and color create clear visual hierarchy
6. **Accessibility**: WCAG AA compliant contrast ratios
7. **Responsiveness**: Mobile-first approach with breakpoints
8. **Performance**: Minimal shadows and gradients for smooth rendering

---

## 🛠️ Implementation Notes

- CSS uses modern flexbox and grid layouts
- Transitions set to 0.3s for smooth interactions
- All colors use rgba for transparency control
- Border radius consistent at 8px for inputs/buttons, 12px for cards
- Hover effects transform elements slightly for tactile feedback
- Gradients use 135deg angle for consistent directionality

---

**Design System Version**: 2.0  
**Last Updated**: November 2025  
**Application**: WorkSphere ERMA - Employee and Roster Management Application
