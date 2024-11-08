import streamlit as st
import pandas as pd
import yfinance as yf
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import defaultdict

# Add these definitions after your imports but before any functions

# Define store items
store_items = {
    "Clothing": {
        "Basic T-shirt": {"cost": 100, "level": 1, "description": "A comfortable, everyday t-shirt."},
        "Designer Jeans": {"cost": 500, "level": 3, "description": "High-quality jeans for a stylish look."},
        "Running Shoes": {"cost": 300, "level": 2, "description": "Comfortable shoes for your daily jog."},
        "Business Suit": {"cost": 1000, "level": 5, "description": "Look sharp for important meetings."},
        "Winter Coat": {"cost": 800, "level": 4, "description": "Stay warm in cold weather."},
    },
    "Accessories": {
        "Smartwatch": {"cost": 700, "level": 4, "description": "Track your fitness and stay connected."},
        "Designer Sunglasses": {"cost": 400, "level": 3, "description": "Protect your eyes in style."},
        "Leather Wallet": {"cost": 200, "level": 2, "description": "Keep your cards and cash organized."},
        "Laptop Bag": {"cost": 150, "level": 1, "description": "Carry your tech gear safely."},
        "Wireless Earbuds": {"cost": 250, "level": 2, "description": "Enjoy your music on the go."},
    },
    "Virtual Backgrounds": {
        "Luxury Office": {"cost": 2000, "level": 7, "description": "Look professional in your video calls."},
        "Tropical Beach": {"cost": 1500, "level": 6, "description": "Bring vacation vibes to your meetings."},
        "Futuristic City": {"cost": 2500, "level": 8, "description": "Impress with a sci-fi backdrop."},
        "Cozy Library": {"cost": 1200, "level": 5, "description": "Create a scholarly atmosphere."},
        "Mountain Retreat": {"cost": 1800, "level": 6, "description": "Inspire with natural beauty."},
    },
    "Cribs": {
        "Wooden Hut": {"cost": 500, "level": 3, "description": "A humble beginning."},
        "Beach House": {"cost": 1500, "level": 6, "description": "Relax by the ocean."},
        "City Apartment": {"cost": 2500, "level": 9, "description": "Urban living with a skyline view."},
        "Mansion": {"cost": 4000, "level": 12, "description": "Luxurious living at its finest."},
        "Mountain Chalet": {"cost": 10000, "level": 15, "description": "Your private retreat in the mountains."},
    }
}

# Financial education content
financial_lessons = {
    "Budgeting Basics": {
        "content": "Budgeting is the foundation of personal finance. It involves tracking income and expenses to ensure you're living within your means and saving for future goals.",
        "quiz": [
            {
                "question": "What is the primary purpose of a budget?",
                "options": ["To restrict spending", "To track income and expenses", "To increase debt", "To impress others"],
                "correct_answer": 1
            },
            {
                "question": "Which of the following is NOT typically included in a budget?",
                "options": ["Rent/Mortgage", "Groceries", "Neighbor's income", "Utilities"],
                "correct_answer": 2
            }
        ]
    },
    "Investment Fundamentals": {
        "content": "Investing is putting money into financial schemes, shares, property, or commercial ventures with the expectation of achieving a profit. Common investment types include stocks, bonds, real estate, and mutual funds.",
        "quiz": [
            {
                "question": "What is diversification in investing?",
                "options": ["Putting all money in one stock", "Spreading investments across various assets", "Only investing in bonds", "Avoiding the stock market"],
                "correct_answer": 1
            },
            {
                "question": "Which of these is generally considered the riskiest investment?",
                "options": ["Government bonds", "High-yield savings account", "Individual stocks", "Certificate of Deposit (CD)"],
                "correct_answer": 2
            }
        ]
    },
    "Credit Management": {
        "content": "Credit management involves borrowing money or accessing goods/services with the agreement to pay later. It's crucial to understand interest rates, credit scores, and responsible borrowing practices.",
        "quiz": [
            {
                "question": "What factor has the biggest impact on your credit score?",
                "options": ["Age", "Payment history", "Number of credit cards", "Annual income"],
                "correct_answer": 1
            },
            {
                "question": "What is a good practice for managing credit card debt?",
                "options": ["Only paying the minimum balance", "Maxing out credit limits", "Paying the full balance each month", "Having multiple cards with high balances"],
                "correct_answer": 2
            }
        ]
    }
}

# All achievements
all_achievements = {
    "First Investment": "Make your first stock purchase",
    "Diversified Investor": "Own stocks in 5 different companies",
    "First Lesson Completed": "Complete your first financial lesson",
    "Financial Expert": "Complete all financial lessons",
    "First Purchase": "Buy your first item from the store",
    "Shopping Spree": "Own 10 items from the store",
    "Millionaire": "Reach a net worth of $1,000,000",
    "Day Trader": "Make 10 trades in a single day",
    "Long-term Investor": "Hold a stock for 30 days",
    "Risk Taker": "Invest 50% of your balance in a single stock",
    "Penny Pincher": "Save 20% of your initial balance",
    "Market Guru": "Achieve a 20% return on investment",
    "Excellent Credit": "Achieve a credit score of 800 or higher"
}

def create_custom_nav():
    st.markdown("""
        <style>
        .nav-button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            width: 100%;
            transition: background-color 0.3s;
        }
        .nav-button:hover {
            background-color: #45a049;
        }
        .nav-button.active {
            background-color: #357abd;
        }
        </style>
    """, unsafe_allow_html=True)

def display_character(wardrobe):
    character = "🧑"  # Default character emoji
    outfit = []
    if "Basic T-shirt" in wardrobe:
        outfit.append("👕")
    if "Designer Jeans" in wardrobe:
        outfit.append("👖")
    if "Running Shoes" in wardrobe:
        outfit.append("👟")
    if "Business Suit" in wardrobe:
        character = "🕴️"
    if "Winter Coat" in wardrobe:
        outfit.append("🧥")
    if "Smartwatch" in wardrobe:
        outfit.append("⌚")
    if "Designer Sunglasses" in wardrobe:
        outfit.append("🕶️")
    
    return f"{character} {''.join(outfit)}"

def evaluate_credit_score():
    st.header("Credit Score Evaluator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Credit Factors")
        
        # Payment History (35% impact)
        st.write("##### Payment History (35% impact)")
        late_payments = st.slider("Number of late payments in the past year", 0, 12, 0)
        payment_score = 100 - (late_payments * 8)  # Each late payment reduces score
        
        # Credit Utilization (30% impact)
        st.write("##### Credit Utilization (30% impact)")
        total_credit = st.number_input("Total credit limit ($)", min_value=0, value=10000)
        used_credit = st.number_input("Current credit usage ($)", min_value=0, value=2000)
        utilization = (used_credit / total_credit * 100) if total_credit > 0 else 100
        utilization_score = 100 - (utilization * 0.8)  # Lower utilization is better
        
        # Credit History Length (15% impact)
        st.write("##### Credit History Length (15% impact)")
        credit_years = st.slider("Years of credit history", 0, 30, 5)
        history_score = min(100, credit_years * 5)  # Max score at 20 years
        
        # Credit Mix (10% impact)
        st.write("##### Credit Mix (10% impact)")
        credit_types = st.multiselect(
            "Types of credit accounts",
            ["Credit Card", "Auto Loan", "Mortgage", "Student Loan", "Personal Loan"],
            ["Credit Card"]
        )
        mix_score = min(100, len(credit_types) * 20)  # Max score with 5 types
        
        # New Credit (10% impact)
        st.write("##### New Credit (10% impact)")
        new_accounts = st.slider("Number of new credit accounts in past year", 0, 10, 0)
        new_credit_score = 100 - (new_accounts * 10)  # Each new account reduces score
        
        if st.button("Calculate Credit Score"):
            # Calculate weighted score
            final_score = (
                payment_score * 0.35 +
                utilization_score * 0.30 +
                history_score * 0.15 +
                mix_score * 0.10 +
                new_credit_score * 0.10
            )
            
            # Convert to credit score range (300-850)
            credit_score = int(300 + (final_score / 100 * 550))
            st.session_state.credit_score = credit_score
            
            # Store history
            st.session_state.credit_history.append({
                'date': datetime.now(),
                'score': credit_score
            })
            
            # Achievement check
            if credit_score >= 800 and "Excellent Credit" not in st.session_state.achievements:
                st.session_state.achievements.add("Excellent Credit")
                st.balloons()
                st.success("Achievement Unlocked: Excellent Credit!")
    
    with col2:
        st.subheader("Your Credit Score")
        
        # Create a gauge chart for credit score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = st.session_state.credit_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [300, 850]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [300, 580], 'color': "red"},
                    {'range': [580, 670], 'color': "orange"},
                    {'range': [670, 740], 'color': "yellow"},
                    {'range': [740, 800], 'color': "lightgreen"},
                    {'range': [800, 850], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': st.session_state.credit_score
                }
            }
        ))
        
        fig.update_layout(
            title = {'text': "Credit Score Range"},
            height = 300
        )
        
        st.plotly_chart(fig)

def update_level():
    while st.session_state.experience >= st.session_state.level * 1000:
        st.session_state.level += 1
        st.balloons()
        st.success(f"Congratulations! You've reached level {st.session_state.level}!")


def main():
    # Set page config
    st.set_page_config(page_title="Money Management Mastery", layout="wide")

    # Initialize all session state variables
    if 'balance' not in st.session_state:
        st.session_state.balance = 10000
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {}
    if 'experience' not in st.session_state:
        st.session_state.experience = 0
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'wardrobe' not in st.session_state:
        st.session_state.wardrobe = {}
    if 'completed_lessons' not in st.session_state:
        st.session_state.completed_lessons = set()
    if 'achievements' not in st.session_state:
        st.session_state.achievements = set()
    if 'daily_login_streak' not in st.session_state:
        st.session_state.daily_login_streak = 0
    if 'last_login' not in st.session_state:
        st.session_state.last_login = None
    if 'trades_today' not in st.session_state:
        st.session_state.trades_today = 0
    if 'last_trade_date' not in st.session_state:
        st.session_state.last_trade_date = None
    if 'credit_score' not in st.session_state:
        st.session_state.credit_score = 650
    if 'credit_history' not in st.session_state:
        st.session_state.credit_history = []

    create_custom_nav()
    
    # Enhanced navigation
    nav_options = {
        "Dashboard": "📊",
        "Invest": "💰",
        "Learn": "📚",
        "Store": "🛍️",
        "My Character": "👤",
        "Credit Score": "📈",
        "Achievements": "🏆"
    }
    
    page = st.sidebar.radio("Navigate", list(nav_options.keys()), format_func=lambda x: f"{nav_options[x]} {x}")

    st.title("Money Management Mastery")

    # Handle daily login streak
    current_date = datetime.now().date()
    if st.session_state.last_login is None or current_date > st.session_state.last_login:
        if st.session_state.last_login is None or (current_date - st.session_state.last_login).days == 1:
            st.session_state.daily_login_streak += 1
            st.sidebar.success(f"Daily login streak: {st.session_state.daily_login_streak} days!")
            st.session_state.experience += 50 * st.session_state.daily_login_streak
            st.sidebar.info(f"You earned {50 * st.session_state.daily_login_streak} XP for logging in!")
        else:
            st.session_state.daily_login_streak = 1
            st.sidebar.warning("Daily login streak reset. Start a new streak!")
        st.session_state.last_login = current_date

    # Page content based on navigation
    # Replace the Dashboard and Invest sections in your main() function with:

    if page == "Dashboard":
        st.header("Your Financial Dashboard")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Account Balance")
            st.write(f"${st.session_state.balance:.2f}")
        with col2:
            st.subheader("Experience Points")
            st.write(f"{st.session_state.experience} XP")
        with col3:
            st.subheader("Current Level")
            st.write(f"Level {st.session_state.level}")
        
        st.subheader("Investment Portfolio")
        if st.session_state.portfolio:
            portfolio_df = pd.DataFrame(list(st.session_state.portfolio.items()), columns=['Stock', 'Shares'])
            portfolio_df['Current Price'] = portfolio_df['Stock'].apply(lambda x: yf.Ticker(x).history(period="1d")['Close'].iloc[-1])
            portfolio_df['Value'] = portfolio_df['Shares'] * portfolio_df['Current Price']
            st.dataframe(portfolio_df)
            
            total_value = portfolio_df['Value'].sum()
            st.write(f"Total Portfolio Value: ${total_value:.2f}")
            
            fig = go.Figure(data=[go.Pie(labels=portfolio_df['Stock'], values=portfolio_df['Value'])])
            st.plotly_chart(fig)
        else:
            st.write("You don't have any investments yet. Head to the Invest page to start!")
        
        st.subheader("Learning Progress")
        progress_df = pd.DataFrame({
            'Lesson': financial_lessons.keys(),
            'Completed': [lesson in st.session_state.completed_lessons for lesson in financial_lessons.keys()]
        })
        st.dataframe(progress_df)
        
        st.subheader("Recent Achievements")
        if st.session_state.achievements:
            for achievement in list(st.session_state.achievements)[-5:]:
                st.write(f"🏆 **{achievement}**: {all_achievements[achievement]}")
        else:
            st.write("No achievements yet. Keep learning and investing!")

    elif page == "Invest":
        st.header("Investment Simulator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Stock Market")
            selected_stocks = st.multiselect("Select stocks to track", 
                ["AAPL", "GOOGL", "MSFT", "AMZN", "FB", "TSLA", "NFLX", "NVDA", "JPM", "V"])

            if selected_stocks:
                @st.cache_data(ttl=60)
                def get_stock_data(tickers):
                    try:
                        data = yf.download(tickers, period="1mo")
                        if isinstance(data, pd.Series):
                            return pd.DataFrame(data, columns=[tickers])
                        elif 'Close' in data.columns:
                            return data['Close']
                        else:
                            return pd.DataFrame()
                    except Exception as e:
                        st.error(f"Error fetching stock data: {e}")
                        return pd.DataFrame()

                stock_data = get_stock_data(selected_stocks)

                if not stock_data.empty:
                    st.line_chart(stock_data)

                    for stock in selected_stocks:
                        if len(selected_stocks) == 1:
                            current_price = stock_data.iloc[-1]
                            price_change = stock_data.iloc[-1] - stock_data.iloc[-2]
                            percent_change = (price_change / stock_data.iloc[-2]) * 100
                        else:
                            current_price = stock_data[stock].iloc[-1]
                            price_change = stock_data[stock].iloc[-1] - stock_data[stock].iloc[-2]
                            percent_change = (price_change / stock_data[stock].iloc[-2]) * 100
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"{stock}")
                        with col2:
                            st.write(f"${current_price:.2f}")
                        with col3:
                            st.write(f"{percent_change:.2f}%")
                    
                    stock_to_trade = st.selectbox("Select a stock to trade", selected_stocks)
                    quantity = st.number_input("Quantity", min_value=1, value=1)
                    
                    if len(selected_stocks) == 1:
                        current_price = stock_data.iloc[-1]
                    else:
                        current_price = stock_data[stock_to_trade].iloc[-1]
                    
                    total_cost = current_price * quantity
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Buy"):
                            if total_cost <= st.session_state.balance:
                                st.session_state.balance -= total_cost
                                if stock_to_trade in st.session_state.portfolio:
                                    st.session_state.portfolio[stock_to_trade] += quantity
                                else:
                                    st.session_state.portfolio[stock_to_trade] = quantity
                                st.success(f"Bought {quantity} shares of {stock_to_trade} for ${total_cost:.2f}")
                                st.session_state.experience += 50
                                update_level()
                                
                                # Update trade count
                                current_date = datetime.now().date()
                                if st.session_state.last_trade_date != current_date:
                                    st.session_state.trades_today = 1
                                    st.session_state.last_trade_date = current_date
                                else:
                                    st.session_state.trades_today += 1
                                
                                # Check for achievements
                                if len(st.session_state.portfolio) == 1:
                                    st.session_state.achievements.add("First Investment")
                                elif len(st.session_state.portfolio) == 5:
                                    st.session_state.achievements.add("Diversified Investor")
                                if st.session_state.trades_today == 10:
                                    st.session_state.achievements.add("Day Trader")
                            else:
                                st.error("Insufficient funds!")
                    with col2:
                        if st.button("Sell"):
                            if stock_to_trade in st.session_state.portfolio and st.session_state.portfolio[stock_to_trade] >= quantity:
                                sell_value = current_price * quantity
                                st.session_state.balance += sell_value
                                st.session_state.portfolio[stock_to_trade] -= quantity
                                if st.session_state.portfolio[stock_to_trade] == 0:
                                    del st.session_state.portfolio[stock_to_trade]
                                st.success(f"Sold {quantity} shares of {stock_to_trade} for ${sell_value:.2f}")
                                st.session_state.experience += 50
                                update_level()
                            else:
                                st.error("Insufficient shares to sell!")
                else:
                    st.error("Unable to fetch stock data. Please try again later.")
            else:
                st.write("Please select stocks to track.")

        with col2:
            st.subheader("Your Portfolio")
            if st.session_state.portfolio:
                portfolio_df = pd.DataFrame(list(st.session_state.portfolio.items()), columns=['Stock', 'Shares'])
                portfolio_df['Current Price'] = portfolio_df['Stock'].apply(lambda x: yf.Ticker(x).history(period="1d")['Close'].iloc[-1] if not yf.Ticker(x).history(period="1d").empty else 0)
                portfolio_df['Value'] = portfolio_df['Shares'] * portfolio_df['Current Price']
                st.dataframe(portfolio_df)
                
                total_value = portfolio_df['Value'].sum()
                st.write(f"Total Portfolio Value: ${total_value:.2f}")
                
                if st.button("Sell All"):
                    sell_value = total_value
                    st.session_state.balance += sell_value
                    st.session_state.portfolio.clear()
                    st.success(f"Sold entire portfolio for ${sell_value:.2f}")
                    st.session_state.experience += 100
                    update_level()
            else:
                st.write("Your portfolio is empty. Start investing!")

    

    elif page == "Learn":
        st.header("Financial Education Center")
        
        lesson = st.selectbox("Choose a lesson", list(financial_lessons.keys()))
        
        st.subheader(lesson)
        st.write(financial_lessons[lesson]["content"])
        
        st.subheader("Quiz")
        with st.form(key=f'quiz_form_{lesson}'):
            user_answers = []
            for i, question in enumerate(financial_lessons[lesson]["quiz"]):
                st.write(f"**{i+1}. {question['question']}**")
                user_answer = st.radio(f"Select an answer for question {i+1}:", 
                                    options=question['options'],
                                    key=f"q{i}")
                user_answers.append(question['options'].index(user_answer))
            
            submitted = st.form_submit_button("Submit Quiz")
            
            if submitted:
                score = sum([ua == q['correct_answer'] for ua, q in zip(user_answers, financial_lessons[lesson]["quiz"])])
                st.write(f"You scored {score} out of {len(financial_lessons[lesson]['quiz'])}!")
                
                if score == len(financial_lessons[lesson]['quiz']):
                    if lesson not in st.session_state.completed_lessons:
                        st.session_state.completed_lessons.add(lesson)
                        xp_gained = 200
                        st.session_state.experience += xp_gained
                        st.success(f"Congratulations! You've completed the {lesson} lesson and earned {xp_gained} XP!")
                        update_level()
                        
                        # Check for achievements
                        if len(st.session_state.completed_lessons) == 1:
                            st.session_state.achievements.add("First Lesson Completed")
                        elif len(st.session_state.completed_lessons) == len(financial_lessons):
                            st.session_state.achievements.add("Financial Expert")
                    else:
                        st.info("You've already completed this lesson, but great job on the refresh!")
                else:
                    st.warning("Keep studying and try again to complete the lesson!")
        
        st.subheader("Financial Calculator")
        calc_type = st.selectbox("Select calculator type", ["Compound Interest", "Loan Repayment"])
        
        if calc_type == "Compound Interest":
            principal = st.number_input("Initial investment", min_value=0.0, value=1000.0)
            rate = st.number_input("Annual interest rate (%)", min_value=0.0, max_value=100.0, value=5.0)
            time = st.number_input("Investment period (years)", min_value=0, value=10)
            compound_freq = st.selectbox("Compounding frequency", ["Annually", "Semi-annually", "Quarterly", "Monthly"])
            
            freq_dict = {"Annually": 1, "Semi-annually": 2, "Quarterly": 4, "Monthly": 12}
            n = freq_dict[compound_freq]
            
            final_amount = principal * (1 + (rate/100)/n) ** (n*time)
            
            st.write(f"Final amount after {time} years: ${final_amount:.2f}")
            st.write(f"Total interest earned: ${(final_amount - principal):.2f}")
        
        elif calc_type == "Loan Repayment":
            loan_amount = st.number_input("Loan amount", min_value=0.0, value=10000.0)
            annual_rate = st.number_input("Annual interest rate (%)", min_value=0.0, max_value=100.0, value=5.0)
            loan_term = st.number_input("Loan term (years)", min_value=0, value=5)
            
            monthly_rate = annual_rate / 100 / 12
            num_payments = loan_term * 12
            
            monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
            
            st.write(f"Monthly payment: ${monthly_payment:.2f}")
            st.write(f"Total amount paid: ${(monthly_payment * num_payments):.2f}")
            st.write(f"Total interest paid: ${(monthly_payment * num_payments - loan_amount):.2f}")

    elif page == "Store":
        st.header("Reward Store")
        
        def display_items(category):
            for item, details in store_items[category].items():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 2, 2])
                with col1:
                    st.write(f"**{item}**")
                    st.write(details['description'])
                with col2:
                    st.write(f"Cost: {details['cost']} XP")
                with col3:
                    st.write(f"Level: {details['level']}")
                with col4:
                    if st.session_state.level >= details['level'] and st.session_state.experience >= details['cost']:
                        if st.button(f"Buy {item}"):
                            st.session_state.experience -= details['cost']
                            if item in st.session_state.wardrobe:
                                st.session_state.wardrobe[item] += 1
                            else:
                                st.session_state.wardrobe[item] = 1
                            st.success(f"You bought {item}!")
                            
                            # Check for achievements
                            if sum(st.session_state.wardrobe.values()) == 1:
                                st.session_state.achievements.add("First Purchase")
                            elif sum(st.session_state.wardrobe.values()) == 10:
                                st.session_state.achievements.add("Shopping Spree")
                    else:
                        st.button(f"Buy {item}", disabled=True)
                with col5:
                    if item in st.session_state.wardrobe:
                        st.write(f"Owned: {st.session_state.wardrobe[item]}")
                    else:
                        st.write("Not owned")
                st.write("---")

        tab1, tab2, tab3, tab4 = st.tabs(["Clothing", "Accessories", "Virtual Backgrounds", "Cribs"])
        
        with tab1:
            display_items("Clothing")
        
        with tab2:
            display_items("Accessories")
        
        with tab3:
            display_items("Virtual Backgrounds")

        with tab4:
            display_items("Cribs")
        
    elif page == "My Character":
        st.header("My Character")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Your Character")
            character = display_character(st.session_state.wardrobe)
            st.write(f"## {character}")
            st.write("Your current outfit and accessories")
        
        with col2:
            st.subheader("Your Possessions")
            
            def display_owned_items(category):
                items_owned = {item: quantity for item, quantity in st.session_state.wardrobe.items() 
                             if item in store_items[category]}
                if items_owned:
                    for item, quantity in items_owned.items():
                        col1, col2, col3 = st.columns([3, 1, 2])
                        with col1:
                            st.write(f"**{item}**")
                            st.write(store_items[category][item]['description'])
                        with col2:
                            st.write(f"Owned: {quantity}")
                        with col3:
                            st.write(f"Level: {store_items[category][item]['level']}")
                        st.write("---")
                else:
                    st.write(f"You don't own any {category.lower()} yet. Visit the store to buy some!")

            tab1, tab2, tab3, tab4 = st.tabs(["Clothing", "Accessories", "Virtual Backgrounds", "Cribs"])
            
            with tab1:
                display_owned_items("Clothing")
            with tab2:
                display_owned_items("Accessories")
            with tab3:
                display_owned_items("Virtual Backgrounds")
            with tab4:
                display_owned_items("Cribs")
        
        st.subheader("Investment Portfolio")
        if st.session_state.portfolio:
            portfolio_df = pd.DataFrame(list(st.session_state.portfolio.items()), 
                                      columns=['Stock', 'Shares'])
            portfolio_df['Current Price'] = portfolio_df['Stock'].apply(
                lambda x: yf.Ticker(x).history(period="1d")['Close'].iloc[-1] 
                if not yf.Ticker(x).history(period="1d").empty else 0)
            portfolio_df['Value'] = portfolio_df['Shares'] * portfolio_df['Current Price']
            st.dataframe(portfolio_df)
            
            total_value = portfolio_df['Value'].sum()
            st.write(f"Total Portfolio Value: ${total_value:.2f}")
            
            fig = go.Figure(data=[go.Pie(labels=portfolio_df['Stock'], 
                                       values=portfolio_df['Value'])])
            fig.update_layout(title="Portfolio Composition")
            st.plotly_chart(fig)
        else:
            st.write("You don't have any investments yet. Head to the Invest page to start!")
        
        st.subheader("Net Worth")
        net_worth = st.session_state.balance
        if 'total_value' in locals():
            net_worth += total_value
        st.write(f"Your current net worth: ${net_worth:.2f}")
        
        # Check for Millionaire achievement
        if net_worth >= 1000000 and "Millionaire" not in st.session_state.achievements:
            st.session_state.achievements.add("Millionaire")
            st.balloons()
            st.success("Congratulations! You've achieved Millionaire status!")

    elif page == "Achievements":
        st.header("Your Achievements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Earned Achievements")
            if st.session_state.achievements:
                for achievement in st.session_state.achievements:
                    st.write(f"🏆 **{achievement}**: {all_achievements[achievement]}")
            else:
                st.write("You haven't earned any achievements yet. Keep learning and investing!")
        
        with col2:
            st.subheader("Locked Achievements")
            locked_achievements = set(all_achievements.keys()) - st.session_state.achievements
            for achievement in locked_achievements:
                st.write(f"🔒 **{achievement}**: {all_achievements[achievement]}")
    elif page == "Credit Score":
        evaluate_credit_score()

    # Sidebar stats
    st.sidebar.write(f"Balance: ${st.session_state.balance:.2f}")
    st.sidebar.write(f"Experience: {st.session_state.experience} XP")
    st.sidebar.write(f"Level: {st.session_state.level}")
    
    # Progress bar for next level
    next_level_xp = st.session_state.level * 1000
    progress = (st.session_state.experience % 1000) / 1000
    st.sidebar.progress(progress)
    st.sidebar.write(f"Progress to Level {st.session_state.level + 1}")

if __name__ == "__main__":
    main()