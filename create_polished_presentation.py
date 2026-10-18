import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Initialize presentation with widescreen layout
prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

BASE_DIR = r"d:\Machinelearning icfoss\FINAL PROJECT FOR GRADING"
PLOT_DIR = os.path.join(BASE_DIR, "plots")
SC1 = os.path.join(BASE_DIR, "Screenshot of  the website", "Screenshot 1 .jpeg")

# Brand Colors
DARK_BG = RGBColor(11, 37, 69)      # #0B2545
LIGHT_BG = RGBColor(244, 247, 246)  # #F4F7F6
DARK_TEXT = RGBColor(33, 37, 41)    # #212529
LIGHT_TEXT = RGBColor(248, 249, 250)# #F8F9FA
ACCENT_BLUE = RGBColor(33, 150, 243) # #2196F3
ACCENT_GREEN = RGBColor(39, 174, 96) # #27AE60

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text, dark_mode=False):
    # Category tracker at top-left
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.4))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_right = tf_cat.margin_top = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = 'Arial'
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_BLUE if dark_mode else ACCENT_BLUE
    
    # Title text
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.8))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Georgia'
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = LIGHT_TEXT if dark_mode else DARK_TEXT

def create_card(slide, left, top, width, height, title, points, bg_color=RGBColor(255, 255, 255), border_color=None):
    # Draw background box
    shape = slide.shapes.add_shape(
        1,  # Rectangular shape type
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
        
    # Put text inside
    tx_box = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.3), width - Inches(0.6), height - Inches(0.6))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    if title:
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(18)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_TEXT if bg_color != DARK_BG else LIGHT_TEXT
        
    for i, pt in enumerate(points):
        p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
        p.text = "• " + pt
        p.font.name = 'Arial'
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_TEXT if bg_color != DARK_BG else LIGHT_TEXT
        p.space_after = Pt(10)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 1: Title Slide (Dark Theme)
# ════════════════════════════════════════════════════════════════════════════
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide1, DARK_BG)

# Title & Subtitle in single TextFrame to prevent overlap
title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.0))
tf = title_box.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

p_tracker = tf.paragraphs[0]
p_tracker.text = "ICFOSS INTERNSHIP PROGRAMME · JUNE 2026"
p_tracker.font.name = 'Arial'
p_tracker.font.size = Pt(12)
p_tracker.font.bold = True
p_tracker.font.color.rgb = ACCENT_BLUE
p_tracker.space_after = Pt(20)

p_title = tf.add_paragraph()
p_title.text = "Flight Fare Prediction"
p_title.font.name = 'Georgia'
p_title.font.size = Pt(54)
p_title.font.bold = True
p_title.font.color.rgb = LIGHT_TEXT
p_title.space_after = Pt(10)

p_sub = tf.add_paragraph()
p_sub.text = "ML-Powered Domestic Airline Fare Estimator"
p_sub.font.name = 'Arial'
p_sub.font.size = Pt(20)
p_sub.font.color.rgb = RGBColor(173, 181, 189)

# Author Card
create_card(
    slide1, 
    left=Inches(1.0), top=Inches(5.0), width=Inches(6.0), height=Inches(1.5),
    title="Karthik KS",
    points=["Hybrid Internship Program on Machine Learning through Python"],
    bg_color=RGBColor(26, 54, 93)
)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 2: What We'll Cover (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide2, LIGHT_BG)
add_header(slide2, "What We'll Cover", "Overview")

grid_items = [
    ("01", "Problem Statement", "Why predict flight fares?"),
    ("02", "Dataset", "300,030 records · 11 features"),
    ("03", "Methodology", "EDA → Preprocessing → Modelling"),
    ("04", "Model Results", "5 algorithms compared"),
    ("05", "Flight Fare App", "Flask web deployment"),
    ("06", "Key Findings", "Insights & conclusions")
]

x_offset = Inches(1.0)
y_offset = Inches(2.0)
card_w = Inches(5.3)
card_h = Inches(1.3)

for idx, (num, title, desc) in enumerate(grid_items):
    row = idx // 2
    col = idx % 2
    l = x_offset + (col * Inches(6.0))
    t = y_offset + (row * Inches(1.6))
    
    # Background card
    shape = slide2.shapes.add_shape(1, l, t, card_w, card_h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    shape.line.fill.background()
    
    # Num Text Box
    num_box = slide2.shapes.add_textbox(l + Inches(0.3), t + Inches(0.2), Inches(0.8), Inches(0.9))
    tf_num = num_box.text_frame
    tf_num.word_wrap = True
    p_num = tf_num.paragraphs[0]
    p_num.text = num
    p_num.font.name = 'Arial'
    p_num.font.size = Pt(28)
    p_num.font.bold = True
    p_num.font.color.rgb = ACCENT_BLUE
    
    # Text Box info
    info_box = slide2.shapes.add_textbox(l + Inches(1.2), t + Inches(0.2), card_w - Inches(1.4), Inches(0.9))
    tf_info = info_box.text_frame
    tf_info.word_wrap = True
    tf_info.margin_left = tf_info.margin_right = tf_info.margin_top = tf_info.margin_bottom = 0
    p_t = tf_info.paragraphs[0]
    p_t.text = title
    p_t.font.name = 'Arial'
    p_t.font.size = Pt(16)
    p_t.font.bold = True
    p_t.font.color.rgb = DARK_TEXT
    
    p_d = tf_info.add_paragraph()
    p_d.text = desc
    p_d.font.name = 'Arial'
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = RGBColor(108, 117, 125)
    p_d.space_before = Pt(4)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 3: Problem Statement (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide3, LIGHT_BG)
add_header(slide3, "Why Is Fare Prediction Hard?", "Problem Statement")

create_card(
    slide3,
    left=Inches(1.0), top=Inches(2.0), width=Inches(5.4), height=Inches(4.5),
    title="The Challenge",
    points=[
        "Airline ticket prices change continuously — sometimes hourly.",
        "Fares spike near departure dates, holidays, and on popular routes.",
        "Pricing depends on complex, non-linear combinations of many factors.",
        "Travelers have no reliable way to know when to book for the best price."
    ]
)

create_card(
    slide3,
    left=Inches(6.8), top=Inches(2.0), width=Inches(5.4), height=Inches(4.5),
    title="Our Approach",
    points=[
        "Build a machine learning regression pipeline using historical booking data.",
        "Preprocess and clean the raw inputs to ensure high prediction quality.",
        "Compare 5 ML algorithms to find the best performing model.",
        "Deploy the model using Flask to help users estimate flight fares instantly."
    ],
    bg_color=DARK_BG
)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 4: Dataset at a Glance (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide4, LIGHT_BG)
add_header(slide4, "Dataset at a Glance", "Data")

stats = [
    ("300,030", "Flight records"),
    ("11", "Original features"),
    ("6", "Airlines covered"),
    ("6", "Indian cities")
]

for idx, (val, label) in enumerate(stats):
    l = Inches(1.0) + (idx * Inches(2.9))
    t = Inches(2.0)
    
    shape = slide4.shapes.add_shape(1, l, t, Inches(2.6), Inches(1.4))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    shape.line.fill.background()
    
    tx = slide4.shapes.add_textbox(l, t + Inches(0.2), Inches(2.6), Inches(1.0))
    tf = tx.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = val
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = 'Arial'
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_GREEN if idx == 0 else ACCENT_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = label
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = 'Arial'
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(108, 117, 125)

# Add Feature table
table_shape = slide4.shapes.add_table(6, 3, Inches(1.0), Inches(3.8), Inches(11.3), Inches(2.8))
table = table_shape.table
table.columns[0].width = Inches(2.5)
table.columns[1].width = Inches(2.0)
table.columns[2].width = Inches(6.8)

headers = ["Feature", "Type", "Description"]
for i, h in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = h
    set_cell_background(cell, "DAE6F3")
    cell.text_frame.paragraphs[0].font.bold = True

rows = [
    ("airline", "Categorical", "Carrier name (Vistara, Air India, Indigo, SpiceJet, etc.)"),
    ("source_city / dest_city", "Categorical", "Departure and arrival metro cities in India"),
    ("stops", "Categorical", "Number of stops: zero, one, or two_or_more"),
    ("class", "Categorical", "Economy or Business (the primary driver of price)"),
    ("days_left", "Numerical", "Number of days before departure booking is made"),
]

for row_idx, row_data in enumerate(rows, 1):
    for col_idx, text in enumerate(row_data):
        table.cell(row_idx, col_idx).text = text

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 5: Airline Distribution & Average Pricing (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide5, LIGHT_BG)
add_header(slide5, "Airline Distribution & Average Pricing", "Exploratory Data Analysis")

# Embed visual 08_airline_count_and_price.png
img_path = os.path.join(PLOT_DIR, "08_airline_count_and_price.png")
if os.path.exists(img_path):
    slide5.shapes.add_picture(img_path, Inches(0.8), Inches(1.8), width=Inches(6.8), height=Inches(4.8))

create_card(
    slide5,
    left=Inches(7.8), top=Inches(1.8), width=Inches(4.6), height=Inches(4.8),
    title="Key Observations",
    points=[
        "Vistara and Air India cover the majority of flights in this dataset.",
        "Vistara has the highest average ticket price (~28,500 INR) because it offers many premium class options.",
        "SpiceJet shows the lowest average fare (~5,900 INR).",
        "Budget airlines like Indigo, AirAsia, and GoFirst offer high-volume flights with very competitive prices."
    ]
)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 6: Two Critical Pricing Drivers (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide6, LIGHT_BG)
add_header(slide6, "Two Critical Pricing Drivers", "Exploratory Data Analysis")

img_days = os.path.join(PLOT_DIR, "05_days_left_vs_price.png")
if os.path.exists(img_days):
    slide6.shapes.add_picture(img_days, Inches(0.8), Inches(1.8), width=Inches(5.6), height=Inches(4.2))

img_class = os.path.join(PLOT_DIR, "09_class_comparison.png")
if os.path.exists(img_class):
    slide6.shapes.add_picture(img_class, Inches(6.8), Inches(1.8), width=Inches(5.6), height=Inches(4.2))

# Bottom insight bar
bar = slide6.shapes.add_shape(1, Inches(0.8), Inches(6.2), Inches(11.6), Inches(0.8))
bar.fill.solid()
bar.fill.fore_color.rgb = DARK_BG
bar.line.fill.background()

tx = slide6.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.2), Inches(0.6))
p = tx.text_frame.paragraphs[0]
p.text = "💡 Prices rise sharply in the last 7 days before departure. Business class costs ~5x more than Economy on average."
p.font.name = 'Arial'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = LIGHT_TEXT

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 7: ML Pipeline (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide7, LIGHT_BG)
add_header(slide7, "ML Pipeline", "Methodology")

pipeline_steps = [
    ("Load Data", "300K records\nPandas CSV"),
    ("EDA", "Matplotlib\nSeaborn plots"),
    ("Preprocessing", "IQR outlier rm\nOne-Hot + Ordinal"),
    ("Train Models", "5 algorithms\n80/20 split"),
    ("Evaluate", "MAE · RMSE\nR² score"),
    ("Deploy", "Flask web app\nPrediction page")
]

for idx, (step_title, step_desc) in enumerate(pipeline_steps):
    l = Inches(0.8) + (idx * Inches(1.95))
    t = Inches(1.8)
    w = Inches(1.8)
    h = Inches(2.2)
    
    bg = DARK_BG if idx == 5 else RGBColor(255, 255, 255)
    shape = slide7.shapes.add_shape(1, l, t, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg
    shape.line.fill.background()
    
    tx = slide7.shapes.add_textbox(l, t + Inches(0.3), w, h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = step_title
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = 'Arial'
    p1.font.size = Pt(15)
    p1.font.bold = True
    p1.font.color.rgb = LIGHT_TEXT if idx == 5 else DARK_TEXT
    
    p2 = tf.add_paragraph()
    p2.text = step_desc
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = 'Arial'
    p2.font.size = Pt(12)
    p2.font.color.rgb = RGBColor(200, 200, 200) if idx == 5 else RGBColor(108, 117, 125)
    p2.space_before = Pt(10)

# Preprocessing details
create_card(
    slide7,
    left=Inches(0.8), top=Inches(4.3), width=Inches(11.6), height=Inches(2.5),
    title="Preprocessing Details & Feature Engineering",
    points=[
        "Stops (zero=0, one=1, two_or_more=2) and Class (Economy=0, Business=1) mapped ordinally.",
        "Departure/Arrival times mapped as sequential daily slots (Early Morning, Morning, etc.).",
        "Nominal columns (airline, source_city, destination_city) encoded using One-Hot Encoding.",
        "Outliers removed using the IQR method on ticket price, excluding 123 extreme prices.",
        "StandardScaler applied to scale numeric attributes (duration, days_left) to standard format."
    ]
)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 8: Model Performance Comparison (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide8, LIGHT_BG)
add_header(slide8, "Model Performance Comparison", "Results")

img_comparison = os.path.join(PLOT_DIR, "12_model_comparison_r2.png")
if os.path.exists(img_comparison):
    slide8.shapes.add_picture(img_comparison, Inches(0.8), Inches(1.8), width=Inches(6.2), height=Inches(4.2))

# Comparison Table
table_shape = slide8.shapes.add_table(6, 4, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.2))
table = table_shape.table
table.columns[0].width = Inches(2.2)
table.columns[1].width = Inches(1.0)
table.columns[2].width = Inches(1.1)
table.columns[3].width = Inches(1.0)

cols = ["Algorithm", "MAE (₹)", "RMSE (₹)", "R²"]
for i, col_name in enumerate(cols):
    cell = table.cell(0, i)
    cell.text = col_name
    set_cell_background(cell, "DAE6F3")
    cell.text_frame.paragraphs[0].font.bold = True

rows_data = [
    ("Random Forest ✓", "1,250", "2,707", "0.9856"),
    ("XGBoost", "1,599", "2,880", "0.9837"),
    ("Decision Tree", "1,372", "3,159", "0.9804"),
    ("Linear Regression", "4,476", "6,731", "0.9112"),
    ("SVR (RBF)", "7,419", "12,514", "0.6931")
]

for row_idx, r_data in enumerate(rows_data, 1):
    for col_idx, text in enumerate(r_data):
        cell = table.cell(row_idx, col_idx)
        cell.text = text
        if row_idx == 1:
            set_cell_background(cell, "C8E6C9") # light green highlight for best model
            cell.text_frame.paragraphs[0].font.bold = True

# Bottom insight bar
bar = slide8.shapes.add_shape(1, Inches(0.8), Inches(6.2), Inches(11.6), Inches(0.8))
bar.fill.solid()
bar.fill.fore_color.rgb = DARK_BG
bar.line.fill.background()

tx = slide8.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.2), Inches(0.6))
p = tx.text_frame.paragraphs[0]
p.text = "🏆 Random Forest wins with R² = 98.56% and MAE ≈ ₹1,250 — predicting flight fares within INR 1,250 on average."
p.font.name = 'Arial'
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = LIGHT_TEXT

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 9: What Drives Flight Prices? (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide9 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide9, LIGHT_BG)
add_header(slide9, "What Drives Flight Prices?", "Results")

img_importance = os.path.join(PLOT_DIR, "15_feature_importance_rf.png")
if os.path.exists(img_importance):
    slide9.shapes.add_picture(img_importance, Inches(0.8), Inches(1.8), width=Inches(6.2), height=Inches(4.8))

create_card(
    slide9,
    left=Inches(7.3), top=Inches(1.8), width=Inches(5.2), height=Inches(1.4),
    title="Travel Class",
    points=["Importance: 0.8887 (88.9% of predictive power)", "Economy vs Business represents the largest price jump."],
    bg_color=RGBColor(255, 255, 255)
)

create_card(
    slide9,
    left=Inches(7.3), top=Inches(3.5), width=Inches(5.2), height=Inches(1.4),
    title="Flight Duration",
    points=["Importance: 0.0564 (5.6% impact)", "Longer flight distance/time corresponds with standard fare rises."],
    bg_color=RGBColor(255, 255, 255)
)

create_card(
    slide9,
    left=Inches(7.3), top=Inches(5.2), width=Inches(5.2), height=Inches(1.4),
    title="Days Left & Airline",
    points=["Combined impact: ~2.5% of predictive price details.", "Determines the last-minute price surge curves."],
    bg_color=RGBColor(255, 255, 255)
)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 10: The Flight Fare Web App (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide10 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide10, LIGHT_BG)
add_header(slide10, "The Flight Fare Web App", "Deployment")

# Embed website mockup screenshot
if os.path.exists(SC1):
    slide10.shapes.add_picture(SC1, Inches(0.8), Inches(1.8), width=Inches(4.8), height=Inches(4.8))

app_details = [
    ("ROUTE", "Route & airline dropdowns auto-populated from training classes"),
    ("DAYS", "Days left slider (1-49 days) predicting booking curves in real-time"),
    ("UI", "Clean, user-friendly interface displaying flight statistics"),
    ("PRICE", "Predicts current fare and last-minute (2-day) fare side-by-side"),
    ("INSIGHTS", "Includes model comparison and feature importance charts dynamically"),
]

for idx, (label, desc) in enumerate(app_details):
    l = Inches(6.0)
    t = Inches(1.8) + (idx * Inches(1.0))
    w = Inches(6.5)
    h = Inches(0.8)
    
    shape = slide10.shapes.add_shape(1, l, t, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    shape.line.color.rgb = DARK_BG
    shape.line.width = Pt(1)
    
    tx = slide10.shapes.add_textbox(l + Inches(0.2), t + Inches(0.1), w - Inches(0.4), h - Inches(0.2))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"🔹 {label}: {desc}"
    p.font.name = 'Arial'
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DARK_TEXT

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 11: Critical Thinking (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide11 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide11, LIGHT_BG)
add_header(slide11, "Same Flight, Different Booking Time — Same Price?", "Critical Thinking")

# Central Question Box
q_box = slide11.shapes.add_shape(1, Inches(0.8), Inches(1.8), Inches(11.6), Inches(1.2))
q_box.fill.solid()
q_box.fill.fore_color.rgb = RGBColor(220, 230, 242)
q_box.line.fill.background()

tx_q = slide11.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.2), Inches(1.0))
p_q = tx_q.text_frame.paragraphs[0]
p_q.text = "\"If two flights have identical airline, source, destination, duration, and departure time — but one was booked 45 days in advance and the other 2 days before departure — should the model predict the same fare?\""
p_q.font.name = 'Georgia'
p_q.font.size = Pt(16)
p_q.font.italic = True
p_q.font.color.rgb = DARK_TEXT

# Large NO block
no_box = slide11.shapes.add_shape(1, Inches(0.8), Inches(3.2), Inches(2.2), Inches(3.5))
no_box.fill.solid()
no_box.fill.fore_color.rgb = DARK_BG
no_box.line.fill.background()

tx_no = slide11.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(2.2), Inches(1.5))
p_no = tx_no.text_frame.paragraphs[0]
p_no.text = "NO"
p_no.alignment = PP_ALIGN.CENTER
p_no.font.name = 'Arial'
p_no.font.size = Pt(64)
p_no.font.bold = True
p_no.font.color.rgb = LIGHT_TEXT

# Explanation card
create_card(
    slide11,
    left=Inches(3.2), top=Inches(3.2), width=Inches(9.2), height=Inches(3.5),
    title="Why not?",
    points=[
        "days_left is a critical predictive feature (1.5% overall importance score).",
        "Airlines apply dynamic pricing: as booking capacity drops near departure, ticket price rises.",
        "Model predicts low early-bird fare for a booking 45 days ahead (avg ~₹19,105).",
        "Model predicts a significantly higher last-minute fare for booking 2 days ahead (avg ~₹25,630).",
        "The Flask app shows both prices side-by-side, proving the model captures this dynamic correctly."
    ]
)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 12: Challenges & Future Scope (Light Theme)
# ════════════════════════════════════════════════════════════════════════════
slide12 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide12, LIGHT_BG)
add_header(slide12, "Challenges & Future Scope", "Reflection")

create_card(
    slide12,
    left=Inches(0.8), top=Inches(2.0), width=Inches(5.6), height=Inches(4.5),
    title="Challenges Faced",
    points=[
        "Training Random Forest on 300,000 records was slow — resolved using parallel jobs (n_jobs=-1).",
        "Avoiding data leakage during encoding — resolved by fitting the encoder solely on training classes.",
        "Developing a lightweight UI distinct from generic templates.",
        "Handling edge cases when user selects identical source and destination cities."
    ]
)

create_card(
    slide12,
    left=Inches(6.8), top=Inches(2.0), width=Inches(5.6), height=Inches(4.5),
    title="Future Scope",
    points=[
        "Integrate live flight APIs (Amadeus, Skyscanner) to feed real-time pricing data.",
        "Deploy the web application on AWS / Google Cloud for public availability.",
        "Incorporate Deep Learning models (LSTM or GRU) to model sequential pricing trends.",
        "Build a price-drop alert system to email users when prices drop below a threshold.",
        "Extend the data to include international routes and multi-leg journeys."
    ],
    bg_color=RGBColor(255, 255, 255),
    border_color=DARK_BG
)

# ════════════════════════════════════════════════════════════════════════════
# SLIDE 13: Key Takeaways (Dark Theme)
# ════════════════════════════════════════════════════════════════════════════
slide13 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide13, DARK_BG)

add_header(slide13, "Key Takeaways", "Summary", dark_mode=True)

takeaways = [
    ("98.56%", "R² Model Accuracy", "Random Forest Regressor trained on 300K records"),
    ("#1 Feature", "class of travel", "Economy vs Business represents the largest price jump"),
    ("days_left", "Top-3 Predictor", "Booking early saves up to 34.2% on average ticket fares"),
    ("Flask App", "Live Web Deployment", "Interactive dashboard for real-time model inference")
]

for idx, (metric, label, desc) in enumerate(takeaways):
    l = Inches(0.8) + (idx * Inches(2.95))
    t = Inches(2.2)
    w = Inches(2.8)
    h = Inches(3.2)
    
    shape = slide13.shapes.add_shape(1, l, t, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(26, 54, 93)
    shape.line.fill.background()
    
    tx = slide13.shapes.add_textbox(l, t + Inches(0.4), w, h - Inches(0.8))
    tf = tx.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = metric
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = 'Arial'
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_GREEN if idx == 0 else ACCENT_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = label
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = 'Arial'
    p2.font.size = Pt(16)
    p2.font.bold = True
    p2.font.color.rgb = LIGHT_TEXT
    p2.space_before = Pt(12)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.alignment = PP_ALIGN.CENTER
    p3.font.name = 'Arial'
    p3.font.size = Pt(12)
    p3.font.color.rgb = RGBColor(173, 181, 189)
    p3.space_before = Pt(8)

# Footer info
footer_box = slide13.shapes.add_textbox(Inches(0.8), Inches(6.0), Inches(11.6), Inches(0.6))
p_foot = footer_box.text_frame.paragraphs[0]
p_foot.text = "Thank you · Karthik KS · ICFOSS ML Internship Project"
p_foot.alignment = PP_ALIGN.CENTER
p_foot.font.name = 'Arial'
p_foot.font.size = Pt(14)
p_foot.font.color.rgb = RGBColor(173, 181, 189)

# Save
output_path = os.path.join(BASE_DIR, "ICFOSS_Project_Presentation_Polished.pptx")
prs.save(output_path)
print(f"Presentation saved successfully to: {output_path}")
